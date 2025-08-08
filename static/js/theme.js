document.addEventListener('DOMContentLoaded', () => {
    const themeToggles = [
        document.getElementById('theme-toggle'),
        document.getElementById('theme-toggle-fixed')
    ];
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // 检查本地存储或系统偏好
    let currentTheme = localStorage.getItem('theme') || 
                      (prefersDarkScheme.matches ? 'dark' : 'light');
    
    // 应用初始主题
    applyTheme(currentTheme);
    
    // 为主题切换按钮添加事件
    themeToggles.forEach(toggle => {
        if (toggle) {
            toggle.addEventListener('click', () => {
                currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
                applyTheme(currentTheme);
                localStorage.setItem('theme', currentTheme);
            });
        }
    });
    
    // 监听系统主题变化
    prefersDarkScheme.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            currentTheme = e.matches ? 'dark' : 'light';
            applyTheme(currentTheme);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav');
    const hamburgerSpans = document.querySelectorAll('.menu-toggle span');
    
    menuToggle.addEventListener('click', function() {
        // 切换导航菜单显示状态
        navMenu.classList.toggle('nav-active');
        
        // 切换汉堡图标动画
        this.classList.toggle('active');
        
        // 更新ARIA可访问性属性
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', String(!isExpanded));
    });
    
    // 点击菜单外部关闭菜单
    document.addEventListener('click', function(e) {
        if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('nav-active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    });
    
    // ESC键关闭菜单
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('nav-active')) {
            navMenu.classList.remove('nav-active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    });
});

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    
    // 更新所有主题切换按钮
    const themeToggles = [
        document.getElementById('theme-toggle'),
        document.getElementById('theme-toggle-fixed')
    ];
    
    themeToggles.forEach(toggle => {
        if (toggle) {
            if (toggle.id === 'theme-toggle') {
                toggle.textContent = theme === 'dark' ? '明亮模式' : '暗黑模式';
            } else {
                const icon = toggle.querySelector('i');
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
                toggle.setAttribute('aria-label', theme === 'dark' ? '切换到明亮模式' : '切换到暗黑模式');
            }
        }
    });
}

// 控制"查看所有"按钮显示
function checkProjectCount() {
    const projectCards = document.querySelectorAll('.project-card');
    const viewAllBtn = document.querySelector('.view-all-btn');
    
    if (projectCards.length > 6) {
        viewAllBtn.style.display = 'inline-block';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    
    // 检查本地存储或系统偏好
    let currentTheme = localStorage.getItem('theme') || 
                      (prefersDarkScheme.matches ? 'dark' : 'light');
    
    // 应用初始主题
    applyTheme(currentTheme);
    
    // 主题切换按钮事件
    themeToggle.addEventListener('click', () => {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(currentTheme);
        localStorage.setItem('theme', currentTheme);
    });
    
    // 监听系统主题变化
    prefersDarkScheme.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            currentTheme = e.matches ? 'dark' : 'light';
            applyTheme(currentTheme);
        }
    });

    // 检查项目数量
    checkProjectCount();
});