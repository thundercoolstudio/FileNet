import os
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import hashlib
import uuid

def check_file():
    """检查并初始化配置文件"""
    settings_path = Path("Settings/settings.json")
    settings_path.parent.mkdir(exist_ok=True)
    
    if not settings_path.exists():
        default_config = {
            "LANGUAGE": ["zh_CN", True],
            "SITE_NAME": "雷酷工作室",
            "LICENSE": "Settings/LICENSE.txt",
            "FILE_TYPE": {
                "模型": [".obj", ".fbx", ".blend"],
                "图片": [".jpg", ".png", ".gif"],
                "音乐": [".mp3", ".wav", ".flac"],
                "软件": [".exe", ".deb", ".dmg"],
                "视频": [".mp4", ".avi", ".mov"],
                "文档": [".txt", ".docx", ".xlsx"],
                "PDF": [".pdf"],
                "镜像": [".iso", ".img", ".vhd"],
                "源代码文件": [".py",".java",".c","cpp",
                            ".cs","wd",".css",".rs",
                            ".js", ".html"],
                "Godot": [".tscn", ".wd"],
                "压缩包": [".zip",".7z",".tar",".gz",".rar",".jar",".tgz"]
            },
            "DOWNLOAD": ["Download/", True],
            "UPLOAD": [False, "Upload/", 100, "MB"],
            "FILE_PAGE": 10,
            "SYS_CONF": [False, None, None, None],
            "USER": {},
            "UUID_JNE": False
        }
        
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
    
    # 检查LICENSE文件
    license_path = Path("Settings/LICENSE.txt")
    if not license_path.exists():
        license_path.parent.mkdir(exist_ok=True)
        with open(license_path, 'w', encoding='utf-8') as f:
            f.write("请在此处添加您的使用协议")

def load_config():
    """加载配置文件"""
    with open("Settings/settings.json", 'r', encoding='utf-8') as f:
        return json.load(f)

class User(UserMixin):
    """用户模型"""
    def __init__(self, user_data):
        self.id = user_data.get('uuid')
        self.username = user_data.get('username')
        self.password_hash = user_data.get('password')
        self.user_type = user_data.get('type', 2)  # 默认为普通用户

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CONFIG=load_config()
    )

    # 初始化Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        """用户加载回调"""
        config = app.config['CONFIG']
        for username, user_data in config['USER'].items():
            if user_data['uuid'] == user_id:
                user_data['username'] = username
                return User(user_data)
        return None

    @app.route('/')
    def index():
        """主页路由"""
        config = app.config['CONFIG']
        download_dir = Path(config['DOWNLOAD'][0])
        
        # 扫描文件
        files = []
        for root, dirs, filenames in os.walk(download_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                file_ext = file_path.suffix.lower()
                file_type = "其他"
                
                # 确定文件类型
                for category, exts in config['FILE_TYPE'].items():
                    if file_ext in exts:
                        file_type = category
                        break
                
                files.append({
                    'name': filename,
                    'path': str(file_path.relative_to(download_dir)),
                    'size': os.path.getsize(file_path),
                    'type': file_type,
                    'modified': os.path.getmtime(file_path)
                })
        
        # 分页处理
        page = request.args.get('page', 1, type=int)
        per_page = config['FILE_PAGE']
        if per_page <= 0:
            per_page = len(files)
        
        start = (page - 1) * per_page
        end = start + per_page
        paginated_files = files[start:end]

        return render_template('index.html',
                            files=paginated_files,
                            site_name=config['SITE_NAME'],
                            config=config,
                            page=page)

    @app.errorhandler(404)
    def show_404_page(e):
        return render_template('404.html',
                               site_name=app.config['CONFIG']['SITE_NAME']), 404

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """登录路由"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            config = app.config['CONFIG']
            
            # 验证用户
            if username in config['USER']:
                user_data = config['USER'][username]
                # 验证密码
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                if input_hash == user_data['password']:
                    user = User(user_data)
                    login_user(user)
                    return redirect(url_for('dashboard'))
            
            flash('用户名或密码错误')
        return render_template('login.html',
                               site_name=app.config['CONFIG']['SITE_NAME'])

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """用户仪表盘"""
        config = app.config['CONFIG']
        download_dir = Path(config['DOWNLOAD'][0])
        upload_dir = Path(config['UPLOAD'][1])
        
        # 统计文件数量
        total_files = sum(len(files) for _, _, files in os.walk(download_dir))
        pending_files = sum(len(files) for _, _, files in os.walk(upload_dir)) if config['UPLOAD'][0] else 0
        
        # 统计用户数量
        total_users = len(config['USER'])
        admin_users = sum(1 for user in config['USER'].values() if user['type'] == 0)
        
        return render_template('dashboard.html',
                             site_name=config['SITE_NAME'],
                             total_files=total_files,
                             pending_files=pending_files,
                             total_users=total_users,
                             admin_users=admin_users,
                             current_user=current_user._get_current_object())

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """用户注册"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            config = app.config['CONFIG']
            
            # 基本验证
            if not username or not password or not confirm_password:
                flash('所有字段不能为空')
                return redirect(url_for('register'))
            
            if username in config['USER']:
                flash('用户名已存在')
                return redirect(url_for('register'))
            
            # 密码确认验证
            if password != confirm_password:
                flash('两次输入的密码不一致')
                return redirect(url_for('register'))
            
            # 密码强度检查
            if len(password) < 8:
                flash('密码长度至少为8个字符')
                return redirect(url_for('register'))
            
            # 生成密码哈希
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # 创建新用户
            new_user = {
                'uuid': str(uuid.uuid4()),
                'password': password_hash,
                'signin_value': hashlib.md5(str(uuid.uuid4()).encode()).hexdigest(),
                'type': 2,  # 普通用户
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            
            # 更新配置文件
            config['USER'][username] = new_user
            with open("Settings/settings.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            flash('注册成功，请登录')
            return redirect(url_for('login'))
        
        return render_template('register.html',
                               site_name=app.config['CONFIG']['SITE_NAME'])

    @app.route('/logout')
    @login_required
    def logout():
        """退出登录"""
        logout_user()
        return redirect(url_for('index'),)

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        """文件上传"""
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('未选择文件')
                return redirect(url_for('upload'))
            
            file = request.files['file']
            if file.filename == '':
                flash('未选择文件')
                return redirect(url_for('upload'))
            
            # 验证文件类型
            config = app.config['CONFIG']
            file_ext = os.path.splitext(file.filename)[1].lower()
            allowed = False
            for category, exts in config['FILE_TYPE'].items():
                if file_ext in exts:
                    allowed = True
                    break
            
            if not allowed:
                flash('不支持的文件类型')
                return redirect(url_for('upload'))
            
            # 保存文件
            upload_dir = Path(config['UPLOAD'][1])
            upload_dir.mkdir(exist_ok=True)
            file.save(str(upload_dir / file.filename))
            
            flash('文件上传成功')
            return redirect(url_for('index'))
        
        return render_template('upload.html', 
                            config=app.config['CONFIG'],
                            site_name=app.config['CONFIG']['SITE_NAME'])

    @app.route('/search')
    def search():
        """文件搜索"""
        query = request.args.get('q', '').lower()
        config = app.config['CONFIG']
        download_dir = Path(config['DOWNLOAD'][0])
        
        # 扫描文件
        matched_files = []
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                if query in file.lower():
                    file_path = Path(root) / file
                    file_ext = file_path.suffix.lower()
                    file_type = "其他"
                    
                    # 确定文件类型
                    for category, exts in config['FILE_TYPE'].items():
                        if file_ext in exts:
                            file_type = category
                            break
                    
                    matched_files.append({
                        'name': file,
                        'path': str(file_path.relative_to(download_dir)),
                        'size': os.path.getsize(file_path),
                        'type': file_type,
                        'modified': os.path.getmtime(file_path)
                    })
        
        return render_template('search_results.html', 
                             query=query,
                             files=matched_files,
                             site_name=config['SITE_NAME'],)

    # 添加日期格式化过滤器
    @app.template_filter('datetimeformat')
    def datetimeformat_filter(value, format='%Y-%m-%d %H:%M'):
        if value is None:
            return ""
        return datetime.fromtimestamp(value).strftime(format)

    @app.route('/download/<path:filename>')
    @login_required
    def download_file(filename):
        """文件下载路由"""
        config = app.config['CONFIG']
        download_dir = Path(config['DOWNLOAD'][0])
        file_path = download_dir / filename
        
        # 安全检查
        try:
            file_path.resolve().relative_to(download_dir.resolve())
        except (ValueError, FileNotFoundError):
            abort(404)
        
        if not file_path.exists():
            abort(404)
            
        return send_from_directory(
            directory=download_dir,
            path=filename,
            as_attachment=True
        )

    @app.route('/review', methods=['GET', 'POST'])
    @login_required
    def review():
        """文件审核页面"""
        if current_user.user_type != 0:
            abort(403)
        
        config = app.config['CONFIG']
        upload_dir = Path(config['UPLOAD'][1])
        download_dir = Path(config['DOWNLOAD'][0])
        
        if request.method == 'POST':
            action = request.form.get('action')
            filename = request.form.get('filename')
            
            if action == 'approve':
                # 移动文件到下载目录
                src = upload_dir / filename
                dest = download_dir / filename
                dest.parent.mkdir(parents=True, exist_ok=True)
                src.replace(dest)
                flash(f'已批准文件: {filename}')
            elif action == 'reject':
                # 删除文件
                (upload_dir / filename).unlink()
                flash(f'已拒绝文件: {filename}')
            
            return redirect(url_for('review'))
        
        # 获取待审核文件
        pending_files = []
        for root, dirs, filenames in os.walk(upload_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                pending_files.append({
                    'name': filename,
                    'path': str(file_path.relative_to(upload_dir)),
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                })
        
        return render_template('review.html',
                             files=pending_files,
                             site_name=config['SITE_NAME'])

    @app.route('/manage_users', methods=['GET', 'POST'])
    @login_required
    def manage_users():
        """用户管理页面"""
        if current_user.user_type != 0:
            abort(403)
            
        config = app.config['CONFIG']
        
        if request.method == 'POST':
            action = request.form.get('action')
            username = request.form.get('username')
            
            if action == 'update_role':
                new_role = int(request.form.get('role'))
                if username in config['USER']:
                    config['USER'][username]['type'] = new_role
                    flash(f'已更新用户 {username} 的权限')
            
            elif action == 'delete_user':
                if username in config['USER']:
                    del config['USER'][username]
                    flash(f'已删除用户 {username}')
            
            # 保存配置
            with open("Settings/settings.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            return redirect(url_for('manage_users'))
        
        return render_template('manage_users.html',
                             users=config['USER'],
                             site_name=config['SITE_NAME'])

    return app

if __name__ == '__main__':
    os.makedirs('Download', exist_ok=True)
    check_file() # 检查文件完整性
    app = create_app()
    
    # 检查模板文件是否存在
    if not Path("templates/index.html").exists():
        raise FileNotFoundError("缺少模板文件 templates/index.html")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    