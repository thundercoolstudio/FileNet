
**[[ 中 文 (简 体) ]](#简介) | [[ E n g l i s h ]](#简介)**

# 简介
**`FileNet`（中文名`文件网络`）是一个基于`Python Flask`&`HTML/CSS/JS`实现的个人网盘部署程序，如果您想快速部署一个网盘，或者有部署小型网盘的需求，可以尝试使用此程序；不建议您使用本程序构建较大的网盘，如果您追求极致的性能，您可以移步其他项目，也可以等待我们的`C/C++`版本实现[等待个90年就差不多了吧(BUSHI)]**

# 部署要求
***对于需要部署本程序的机器，要求:***
- [x] **`Windows10+`(支持py就行)/`Linux`(支持py就行)**
- [x] **至少`1GB`可用磁盘空间(不包含您存储的文件)**
- [x] **至少`1GB`可用内存(实际上用不着这么多,为了方便直接写的AwA，上同)**
- [x] **`Python3.12+` & `Flask >= 3.0.3` & `Flask_login >= 0.6.0`**

# 部署
### Windows
```shell
~$ cd I:/Test #你需要部署程序的文件夹
~$ I: #你需要部署程序的文件夹的盘符
~$ git clone https://github.com/BuelieR/FileNet.git #克隆项目
~$ pip install -r requirements.txt #安装依赖
~$ python main.py
~$ cpolar http 5000 #配置开放端口(内网穿透，可选，注意不要泄露您的token)
```

### Linux
***emm，快了快了***

# 声明
- **本程序仅供学习交流使用，请勿用于任何商业用途，如产生法律纠纷与团队人无关，本团队对此不承担任何责任**
- **README文件中的功能，程序可能未完全实现**
- **使用时需要登录才能访问所有资源**

# 配置说明
**配置文件位于`Settings/`目录下,由程序第一次运行时生成,目前规划的配置文件有`settings.json`(使用标准JSON格式存储),各选项说明如下：**
- **`LANGUAGE` : 配置网站多语言支持，存储格式为一个列表，`List[0]`是默认语言，存储的信息类型为`str`,`List[1]`配置是否启用多语言支持，存储类型为`bool`,下面是一个存储例子:**
```json
{
    "LANGUAGE":["zh_CN",true],
    
}
```
- **`SITE_NAME` : 配置站点名，默认为 `雷酷工作室`,下面是一个存储例子:**
```json
{
    
    "SITE_NAME":"<string_value>",
    
}
```
- **`LICENSE` : 配置网站的使用协议，默认为`Settings/LICENSE.txt`,下面是一个存储例子:**
```json
{
    
    "LICENSE":"<file_path>",
    
}
```
- **`FILE_TYPE` : 文件类型分类，存储格式为一个字典，对不同后缀的文件进行归类，下面是一个存储例子：**
```json
{
    
    "FILE_TYPE":{
        "模型": [".obj", ".fbx", ".blend"],
        "图片": [".jpg", ".png", ".gif"],
        "音乐": [".mp3", ".wav", ".flac"],
        "软件": [".exe", ".deb", ".dmg"],
        "视频": [".mp4", ".avi", ".mov"],
        "文档": [".txt", ".docx", ".xlsx"],
        "PDF": [".pdf"],
        "镜像": [".iso", ".img", ".vhd"],
        "源代码文件": [".py",".java",".c","cpp",
                    ".cs","wd",".css",".rs"
                    ".js", ".html",],
        "Godot": [".tscn", ".wd"],
        "压缩包": [".zip",".7z",".tar",".gz",".rar",".jar",".tgz"]
    }
    
}
```
- **`DOWNLOAD` : 配置下载相关，存储格式为一个列表，`List[0]`存储扫描的文件夹，默认为`Download/`,`List[1]`存储类型为`bool`,存储是否展示子文件夹(True为启用),下面是一个存储例子:**
```json
{
    
    "DOWNLOAD":["<folder_path>",true],
    
}
```
- **`UPLOAD` : 配置上传相关，存储格式为一个列表，`List[0]`存储是否启用上传审核(True为启用，启用后需要经过管理员或审核用户审核方可放到扫描的下载文件夹,当为`Fasle`时,`List[1]`为None)，`List[1]`存储上传默认暂存的文件夹，默认是`Upload/`,List[2]配置最大上传限制，默认单位为MB(由`List[3]`存储),当`List[2]`值为0时，则表示无限制，下面是一个存储例子:**
```json
{
    
    "UPLOAD":[true,"<folder_path>",<max>,"512MB"],
    
}
```
- **`FILE_PAGE` : 配置每多少个文件为一页进行分页，默认为`10`,若`FILE_PAGE <= 0`则不进行分页，若填写小数则直接取整数部分进行分页,下面是一个存储例子:**
```json
{
    
    "FILE_PAGE":"<page_value>",
    
}
```
- **`SYS_CONF` : 部署应用的权限最高的可登录账户,存储方式为一个列表(表名`SYS_CONF`,存储内容`[true,<name>,<password>,<uuid>]`,当第一次运行项目时会在网页提升是否配置,其中true表示是否允许该账户在网页端登录,`<name>`是该账户的名称、`<uuid>`是该账户辨识uuid、`<password>`是该账户的密码哈希值,当`true`为`Fasle`时,后几项为None),下面是一个存储例子:**
```json
{
    
    "SYS_CONF":[true,"<name>","<password_hash>","<uuid>"],
    
}
```
- **`USER` ：存储各用户的用户名(用于登录)、注册时验证码MD5值(蜜罐用)及密码哈希值(用于登录,若注册时填写为空，则记录`None`，则登录时不验证其密码)、`<uuid>`是账户辨识uuid,存储方式为字典、`<int_number>`是账户类型(`0`为管理员用户,`1`为审核用户，`2`为普通用户,`3`为封禁账户),下面是一个存储例子:**
```json
{
    
    "USER":{
        "<username>":{
            "<uuid>":"<uuid_value>",
            "<password>":"<hash_value>",
            "<signin_value>":"<md5_value>",
            "<type>":<int_number>"
        },
    },
    
}
```
- **`UUID_JNE` : 是否允许账户重名(`True`为运行,`False`为禁止),若允许则通过UUID区分身份(每次登录也需要填写,若禁用则不需要),下面是一个存储例子:**
```json
{
    
    "UUID_JNE":true,
    
}
```

# 法律声明
**最终解释权归`雷酷工作室`所有，暂时不支持应用于商业用途**
