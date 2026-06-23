/**
 * Astrological Guide - Enhanced Features
 * 实现搜索、主题切换、目录导航、字体调整、分享、收藏等功能
 */

(function() {
    'use strict';

    // 配置
    const CONFIG = {
        searchDebounce: 300,
        fontSizeSteps: [14, 16, 18, 20, 22],
        defaultFontSize: 2, // 索引，对应18px
        storageKeys: {
            theme: 'astrological_theme',
            fontSize: 'astrological_font_size',
            bookmarks: 'astrological_bookmarks'
        }
    };

    // 工具函数
    const utils = {
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        getStorage(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                return defaultValue;
            }
        },

        setStorage(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) { }
        },

        scrollToElement(elementId, offset = 80) {
            const element = document.getElementById(elementId);
            if (element) {
                const elementPosition = element.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }
    };

    // 搜索功能
    const SearchFeature = {
        modal: null,
        input: null,
        results: null,
        searchData: [],

        init() {
            this.modal = document.getElementById('search-modal');
            this.input = document.getElementById('search-input');
            this.results = document.getElementById('search-results');
            
            const toggleBtn = document.getElementById('search-toggle');
            const closeBtn = document.getElementById('search-close');

            // 收集搜索数据
            this.collectSearchData();

            // 事件监听
            toggleBtn?.addEventListener('click', () => this.open());
            closeBtn?.addEventListener('click', () => this.close());
            
            this.input?.addEventListener('input', utils.debounce((e) => {
                this.search(e.target.value);
            }, CONFIG.searchDebounce));

            this.input?.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') this.close();
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const firstResult = this.results?.querySelector('a');
                    firstResult?.click();
                }
            });

            // 点击遮罩关闭
            this.modal?.addEventListener('click', (e) => {
                if (e.target === this.modal) this.close();
            });
        },

        collectSearchData() {
            this.searchData = [];

            // 收集标题和内容
            const sections = document.querySelectorAll('section[id]');
            sections.forEach(section => {
                const id = section.id;
                const heading = section.querySelector('h2');
                const title = heading?.textContent || '';
                const content = section.textContent.substring(0, 500);

                this.searchData.push({
                    id,
                    title,
                    content,
                    type: 'section'
                });
            });

            // 收集卡片（行星、星座、相位等）
            const cards = document.querySelectorAll('article[role="listitem"]');
            cards.forEach(card => {
                const heading = card.querySelector('h3');
                const title = heading?.textContent || '';
                const content = card.textContent.substring(0, 200);

                this.searchData.push({
                    id: heading?.id || card.closest('section')?.id,
                    title,
                    content,
                    type: 'card'
                });
            });
        },

        open() {
            if (this.modal) {
                this.modal.classList.remove('hidden');
                this.modal.classList.add('flex');
                this.input?.focus();
                document.body.style.overflow = 'hidden';
            }
        },

        close() {
            if (this.modal) {
                this.modal.classList.add('hidden');
                this.modal.classList.remove('flex');
                this.input.value = '';
                this.results.innerHTML = '';
                document.body.style.overflow = '';
            }
        },

        search(query) {
            if (!query.trim()) {
                this.results.innerHTML = '<p class="text-gray-400 text-center py-4">输入关键词搜索...</p>';
                return;
            }

            const lowerQuery = query.toLowerCase();
            const matches = this.searchData.filter(item => {
                return item.title.toLowerCase().includes(lowerQuery) ||
                       item.content.toLowerCase().includes(lowerQuery);
            });

            if (matches.length === 0) {
                this.results.innerHTML = '<p class="text-gray-400 text-center py-4">未找到相关结果</p>';
                return;
            }

            this.results.innerHTML = matches.map(item => `
                <a href="#${item.id}" 
                   class="block p-3 mb-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors search-result"
                   onclick="window.SearchFeature?.close()">
                    <div class="font-medium text-white mb-1">${this.highlight(item.title, query)}</div>
                    <div class="text-sm text-gray-400">${this.highlight(item.content.substring(0, 100), query)}...</div>
                    <div class="text-xs text-indigo-400 mt-1">${item.type === 'section' ? '章节' : '内容'}</div>
                </a>
            `).join('');
        },

        highlight(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<mark class="bg-yellow-500 text-black">$1</mark>');
        }
    };

    // 主题切换功能
    const ThemeFeature = {
        body: null,
        toggleBtn: null,
        iconDark: null,
        iconLight: null,
        currentTheme: 'dark',

        init() {
            this.body = document.getElementById('main-body');
            this.toggleBtn = document.getElementById('theme-toggle');
            this.iconDark = document.getElementById('theme-icon-dark');
            this.iconLight = document.getElementById('theme-icon-light');

            // 加载保存的主题
            this.currentTheme = utils.getStorage(CONFIG.storageKeys.theme, 'dark');
            this.applyTheme(this.currentTheme);

            this.toggleBtn?.addEventListener('click', () => {
                this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
                this.applyTheme(this.currentTheme);
                utils.setStorage(CONFIG.storageKeys.theme, this.currentTheme);
            });
        },

        applyTheme(theme) {
            if (!this.body) return;

            // 使用 data-theme 属性来控制主题
            this.body.setAttribute('data-theme', theme);
            
            if (theme === 'light') {
                this.body.classList.remove('bg-black', 'text-gray-100');
                this.body.classList.add('bg-gray-50', 'text-gray-900');
                if (this.iconDark) this.iconDark.classList.add('hidden');
                if (this.iconLight) this.iconLight.classList.remove('hidden');
                document.documentElement.classList.add('light-theme');
            } else {
                this.body.classList.remove('bg-gray-50', 'text-gray-900');
                this.body.classList.add('bg-black', 'text-gray-100');
                if (this.iconDark) this.iconDark.classList.remove('hidden');
                if (this.iconLight) this.iconLight.classList.add('hidden');
                document.documentElement.classList.remove('light-theme');
            }
        }
    };

    // 字体大小调整
    const FontSizeFeature = {
        currentIndex: CONFIG.defaultFontSize,
        body: null,
        display: null,

        init() {
            this.body = document.body;
            this.display = document.getElementById('font-size-display');
            
            const decreaseBtn = document.getElementById('font-decrease');
            const increaseBtn = document.getElementById('font-increase');

            // 加载保存的字体大小
            this.currentIndex = utils.getStorage(CONFIG.storageKeys.fontSize, CONFIG.defaultFontSize);
            this.applyFontSize();

            decreaseBtn?.addEventListener('click', () => {
                if (this.currentIndex > 0) {
                    this.currentIndex--;
                    this.applyFontSize();
                    utils.setStorage(CONFIG.storageKeys.fontSize, this.currentIndex);
                }
            });

            increaseBtn?.addEventListener('click', () => {
                if (this.currentIndex < CONFIG.fontSizeSteps.length - 1) {
                    this.currentIndex++;
                    this.applyFontSize();
                    utils.setStorage(CONFIG.storageKeys.fontSize, this.currentIndex);
                }
            });
        },

        applyFontSize() {
            const size = CONFIG.fontSizeSteps[this.currentIndex];
            if (this.body) {
                this.body.style.fontSize = `${size}px`;
            }
            if (this.display) {
                this.display.textContent = 'A'.repeat(Math.min(this.currentIndex + 1, 5));
            }
        }
    };

    // 目录导航
    const TOCFeature = {
        sidebar: null,
        nav: null,
        isOpen: false,
        currentSection: null,

        init() {
            this.sidebar = document.getElementById('sidebar-toc');
            this.nav = document.getElementById('toc-nav');
            
            const toggleBtn = document.getElementById('toc-toggle');
            const closeBtn = document.getElementById('toc-close');

            this.buildTOC();
            this.setupScrollTracking();

            toggleBtn?.addEventListener('click', () => this.toggle());
            closeBtn?.addEventListener('click', () => this.close());

            // 点击链接后关闭
            this.nav?.addEventListener('click', (e) => {
                if (e.target.tagName === 'A') {
                    setTimeout(() => this.close(), 300);
                }
            });
        },

        buildTOC() {
            if (!this.nav) return;

            const sections = document.querySelectorAll('section[id]');
            const tocHTML = Array.from(sections).map(section => {
                const id = section.id;
                const heading = section.querySelector('h2');
                const title = heading?.textContent || id;
                
                return `
                    <a href="#${id}" 
                       class="block py-2 px-3 mb-1 text-gray-300 hover:text-indigo-400 hover:bg-gray-800 rounded transition-colors toc-link"
                       data-section="${id}">
                        ${title}
                    </a>
                `;
            }).join('');

            this.nav.innerHTML = tocHTML || '<p class="text-gray-400">暂无目录</p>';
        },

        toggle() {
            this.isOpen = !this.isOpen;
            if (this.sidebar) {
                if (this.isOpen) {
                    this.sidebar.classList.remove('-translate-x-full');
                } else {
                    this.sidebar.classList.add('-translate-x-full');
                }
            }
        },

        close() {
            this.isOpen = false;
            if (this.sidebar) {
                this.sidebar.classList.add('-translate-x-full');
            }
        },

        setupScrollTracking() {
            const sections = document.querySelectorAll('section[id]');
            const observerOptions = {
                root: null,
                rootMargin: '-20% 0px -70% 0px',
                threshold: 0
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id;
                        this.setActiveSection(id);
                    }
                });
            }, observerOptions);

            sections.forEach(section => observer.observe(section));
        },

        setActiveSection(id) {
            if (this.currentSection === id) return;
            this.currentSection = id;

            const links = this.nav?.querySelectorAll('.toc-link');
            links?.forEach(link => {
                if (link.dataset.section === id) {
                    link.classList.add('text-indigo-400', 'bg-gray-800');
                    link.classList.remove('text-gray-300');
                } else {
                    link.classList.remove('text-indigo-400', 'bg-gray-800');
                    link.classList.add('text-gray-300');
                }
            });
        }
    };

    // 分享功能
    const ShareFeature = {
        shareBtn: null,

        init() {
            this.shareBtn = document.getElementById('share-button');
            this.shareBtn?.addEventListener('click', () => this.share());
        },

        async share() {
            const shareData = {
                title: '占星学入门指南',
                text: '完整的占星学入门学习资源，包含行星、星座、宫位和相位详解',
                url: window.location.href
            };

            // 使用 Web Share API（如果支持）
            if (navigator.share) {
                try {
                    await navigator.share(shareData);
                } catch (err) {
                    if (err.name !== 'AbortError') {
                        this.showShareDialog();
                    }
                }
            } else {
                this.showShareDialog();
            }
        },

        showShareDialog() {
            const url = window.location.href;
            const text = encodeURIComponent('占星学入门指南 - 完整的占星学入门学习资源');

            const shareHTML = `
                <div id="share-dialog" class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center">
                    <div class="bg-gray-900 rounded-lg p-6 max-w-md w-full mx-4 border border-gray-700">
                        <h3 class="text-xl font-semibold text-white mb-4">分享到</h3>
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <a href="https://twitter.com/intent/tweet?text=${text}&url=${encodeURIComponent(url)}" 
                               target="_blank" 
                               class="flex items-center justify-center p-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
                                Twitter
                            </a>
                            <a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}" 
                               target="_blank" 
                               class="flex items-center justify-center p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                                Facebook
                            </a>
                            <a href="https://t.me/share/url?url=${encodeURIComponent(url)}&text=${text}" 
                               target="_blank" 
                               class="flex items-center justify-center p-3 bg-blue-400 hover:bg-blue-500 text-white rounded-lg transition-colors">
                                Telegram
                            </a>
                            <button onclick="navigator.clipboard.writeText('${url}').then(() => alert('链接已复制！'))" 
                                    class="flex items-center justify-center p-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors">
                                复制链接
                            </button>
                        </div>
                        <button onclick="document.getElementById('share-dialog').remove()" 
                                class="w-full bg-gray-800 hover:bg-gray-700 text-white py-2 rounded-lg transition-colors">
                            关闭
                        </button>
                    </div>
                </div>
            `;

            const dialog = document.createElement('div');
            dialog.innerHTML = shareHTML;
            document.body.appendChild(dialog);

            // 点击遮罩关闭
            dialog.addEventListener('click', (e) => {
                if (e.target.id === 'share-dialog') {
                    dialog.remove();
                }
            });
        }
    };

    // 收藏功能
    const BookmarkFeature = {
        toggleBtn: null,
        icon: null,
        currentUrl: '',

        init() {
            this.toggleBtn = document.getElementById('bookmark-toggle');
            this.icon = document.getElementById('bookmark-icon');
            this.currentUrl = window.location.href;

            this.updateIcon();
            this.toggleBtn?.addEventListener('click', () => this.toggle());
        },

        isBookmarked() {
            const bookmarks = utils.getStorage(CONFIG.storageKeys.bookmarks, []);
            return bookmarks.includes(this.currentUrl);
        },

        toggle() {
            let bookmarks = utils.getStorage(CONFIG.storageKeys.bookmarks, []);
            const isBookmarked = bookmarks.includes(this.currentUrl);

            if (isBookmarked) {
                bookmarks = bookmarks.filter(url => url !== this.currentUrl);
                this.showMessage('已取消收藏');
            } else {
                bookmarks.push(this.currentUrl);
                this.showMessage('已添加收藏');
            }

            utils.setStorage(CONFIG.storageKeys.bookmarks, bookmarks);
            this.updateIcon();
        },

        updateIcon() {
            if (!this.icon) return;
            const isBookmarked = this.isBookmarked();
            this.icon.setAttribute('fill', isBookmarked ? 'currentColor' : 'none');
            this.icon.setAttribute('fill-opacity', isBookmarked ? '1' : '0');
        },

        showMessage(text) {
            const msg = document.createElement('div');
            msg.className = 'fixed bottom-20 right-4 bg-gray-900 text-white px-4 py-2 rounded-lg shadow-lg z-50';
            msg.textContent = text;
            document.body.appendChild(msg);
            setTimeout(() => msg.remove(), 2000);
        }
    };

    // 打印优化
    const PrintFeature = {
        init() {
            // 添加打印样式
            const style = document.createElement('style');
            style.textContent = `
                @media print {
                    .no-print { display: none !important; }
                    body { background: white; color: black; }
                    a { color: blue; text-decoration: underline; }
                    .bg-gray-900, .bg-black { background: white !important; }
                    .text-white, .text-gray-100 { color: black !important; }
                }
            `;
            document.head.appendChild(style);

            // 为不需要打印的元素添加类
            const noPrintElements = document.querySelectorAll('#toolbar, #sidebar-toc, #toc-toggle, #back-to-top');
            noPrintElements.forEach(el => el.classList.add('no-print'));
        }
    };

    // 初始化所有功能
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
        } else {
            initialize();
        }
    }

    function initialize() {
        try {
            SearchFeature.init();
            ThemeFeature.init();
            FontSizeFeature.init();
            TOCFeature.init();
            ShareFeature.init();
            BookmarkFeature.init();
            PrintFeature.init();

            // 导出到全局，方便调试
            window.SearchFeature = SearchFeature;
            window.ThemeFeature = ThemeFeature;
            window.TOCFeature = TOCFeature;

        } catch (error) { }
    }

    // 启动
    init();
})();

