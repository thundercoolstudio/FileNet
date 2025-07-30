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

    // 移动端菜单控制
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        nav.classList.toggle('active');
    });

    // 检查项目数量
    checkProjectCount();
});