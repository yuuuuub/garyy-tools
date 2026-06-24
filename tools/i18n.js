(function(){
'use strict';

var STORAGE_KEY = 'garyy_lang';
var THEME_KEY = 'garyy_theme';
var SUPPORTED = ['zh-CN', 'en'];
var DEFAULT = 'zh-CN';

function detectLang(){
  var saved = localStorage.getItem(STORAGE_KEY);
  if (saved && SUPPORTED.indexOf(saved) >= 0) return saved;
  var nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
  if (nav.indexOf('en') === 0) return 'en';
  return DEFAULT;
}

function detectTheme(){
  var saved = localStorage.getItem(THEME_KEY);
  if (saved) return saved;
  return window.matchMedia('(prefers-color-scheme:light)').matches ? 'light' : 'dark';
}

var currentLang = detectLang();

function applyTheme(theme){
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
}

applyTheme(detectTheme());

var COMMON = {
  '搜索': 'Search',
  '搜索工具...': 'Search tools...',
  '查看': 'View',
  '查看详情': 'View Details',
  '返回': 'Back',
  '返回首页': 'Back to Home',
  '首页': 'Home',
  '加载中': 'Loading',
  '正在加载': 'Loading...',
  '正在加载数据': 'Loading data',
  '正在加载实时数据': 'Loading live data',
  '正在加载...': 'Loading...',
  '加载失败': 'Load Failed',
  '重新加载': 'Retry',
  '重试': 'Retry',
  '刷新': 'Refresh',
  '关闭': 'Close',
  '确定': 'Confirm',
  '取消': 'Cancel',
  '保存': 'Save',
  '删除': 'Delete',
  '编辑': 'Edit',
  '重置': 'Reset',
  '提交': 'Submit',
  '复制': 'Copy',
  '复制成功': 'Copied',
  '已复制': 'Copied',
  '分享': 'Share',
  '下载': 'Download',
  '上传': 'Upload',
  '开始': 'Start',
  '停止': 'Stop',
  '暂停': 'Pause',
  '继续': 'Continue',
  '完成': 'Done',
  '成功': 'Success',
  '失败': 'Failed',
  '错误': 'Error',
  '提示': 'Hint',
  '暂无数据': 'No Data',
  '没有结果': 'No Results',
  '全部': 'All',
  '全选': 'Select All',
  '清空': 'Clear',
  '随机': 'Random',
  '推荐': 'Recommend',
  '今日': 'Today',
  '昨天': 'Yesterday',
  '明天': 'Tomorrow',
  '星期一': 'Monday',
  '星期二': 'Tuesday',
  '星期三': 'Wednesday',
  '星期四': 'Thursday',
  '星期五': 'Friday',
  '星期六': 'Saturday',
  '星期日': 'Sunday',
  '周日': 'Sun',
  '周六': 'Sat',
  '周一': 'Mon',
  '周二': 'Tue',
  '周三': 'Wed',
  '周四': 'Thu',
  '周五': 'Fri',
  '一月': 'January', '二月': 'February', '三月': 'March',
  '四月': 'April', '五月': 'May', '六月': 'June',
  '七月': 'July', '八月': 'August', '九月': 'September',
  '十月': 'October', '十一月': 'November', '十二月': 'December',
  '输入': 'Input',
  '请输入': 'Please enter',
  '选择': 'Select',
  '请选择': 'Please select',
  '结果': 'Result',
  '暂无': 'None',
  '数量': 'Qty',
  '价格': 'Price',
  '金额': 'Amount',
  '单位': 'Unit',
  '总计': 'Total',
  '小计': 'Subtotal',
  '说明': 'Info',
  '设置': 'Settings',
  '主题': 'Theme',
  '深色': 'Dark',
  '浅色': 'Light',
  '语言': 'Language',
  '中文': 'Chinese',
  '英文': 'English',
  '数据来源': 'Source',
  '实时数据': 'Live Data',
  '工具总数': 'Total Tools',
  '分类数量': 'Categories',
  '随机探索': 'Random',
  '搜索颜色名称（中文或英文）...': 'Search color name (Chinese or English)...',
  '搜索菜名或食材...': 'Search dish or ingredient...',
  '输入城市名，如 Beijing': 'Enter city name, e.g. Beijing',
  '输入城市名': 'Enter city name',
  '输入域名': 'Enter domain name',
  '输入IP地址': 'Enter IP address',
  '输入网址': 'Enter URL',
  '输入文本...': 'Enter text...',
  '输入要翻译的文本...': 'Enter text to translate...',
  '请输入中文姓名': 'Enter Chinese name',
  '请输入搜索关键词': 'Enter search keyword',
  '请输入要分析的文本': 'Enter text to analyze',
  '在此输入文本或网址链接...': 'Enter text or URL here...',
  '免费在线小工具，即开即用': 'free online tools, ready to use',
  '全部工具浏览器本地运行，数据不上传服务器': 'All tools run locally, no data uploaded',
  '个结果': 'results',
  '暂无该日期的历史记录': 'No records for this date',
  '数据加载失败': 'Data load failed',
  '检查网络连接': 'Check network',
  '上一页': 'Prev',
  '下一页': 'Next',
  '确认删除': 'Confirm Delete',
  '确认重置': 'Confirm Reset',
  '请输入内容': 'Enter content',
  '匹配结果': 'Matches',
  '共搜索到': 'Found',
  '日期': 'Date',
  '时间': 'Time',
  '选择日期': 'Pick date',
  '选择时间': 'Pick time',
  '历史记录': 'History',
  '收藏': 'Favorite',
  '随机推荐': 'Random Pick',
  '生成': 'Generate',
  '计算': 'Calculate',
  '天': 'days',
  '小时': 'hours',
  '分钟': 'mins',
  '秒': 'secs',
  '约': '~',
  '不限': 'Any',
  '其他': 'Other',
  '自定义': 'Custom',
  '默认': 'Default',
  '高级': 'Advanced',
  '帮助': 'Help',
  '关于': 'About',
  '真实数据': 'Live Data',
  '模拟数据': 'Demo Data',
  '再次搜索': 'Search Again',
  '暂无内容': 'No Content',
  '暂无结果': 'No Results',
  '查看更多': 'View More',
  '收起': 'Collapse',
  '展开': 'Expand',
  '复制链接': 'Copy Link',
  '在新窗口打开': 'Open in New Tab',
  '打印': 'Print',
  '全屏': 'Fullscreen',
  '退出全屏': 'Exit Fullscreen',
  '添加': 'Add',
  '修改': 'Modify',
  '更新': 'Update',
  '确认': 'Confirm',
  '取消收藏': 'Unfavorite',
  '已收藏': 'Favorited',
  '已添加': 'Added',
  '添加成功': 'Added',
  '修改成功': 'Updated',
  '删除成功': 'Deleted',
  '操作成功': 'Success',
  '操作失败': 'Failed',
  '网络错误': 'Network Error',
  '请求超时': 'Timeout',
  '服务器错误': 'Server Error',
  '未知错误': 'Unknown Error',
  '正在提交': 'Submitting...',
  '提交成功': 'Submitted',
  '提交失败': 'Submit Failed',
  '请输入搜索关键词': 'Enter search keyword',
  '无匹配结果': 'No matches',
  '共找到': 'Found',
  '点击复制': 'Click to copy',
  '手机号': 'Phone',
  '邮箱': 'Email',
  '密码': 'Password',
  '验证码': 'Verification Code',
  '登录': 'Login',
  '注册': 'Register',
  '退出': 'Logout',
  '我的': 'My',
  '个人信息': 'Profile',
  '消息': 'Messages',
  '通知': 'Notifications',
  '允许': 'Allow',
  '拒绝': 'Deny',
  '知道了': 'Got it',
  '了解更多': 'Learn More',
  '猜你喜欢': 'Recommended',
  '热门推荐': 'Popular',
  '最新': 'Latest',
  '最热': 'Hottest',
  '排行榜': 'Ranking',
  '评分': 'Rating',
  '评价': 'Review',
  '评论': 'Comment',
  '点赞': 'Like',
  '转发': 'Share',
  '举报': 'Report',
  '反馈': 'Feedback',
  '意见反馈': 'Feedback',
  '客服': 'Support',
  '常见问题': 'FAQ',
  '使用指南': 'Guide',
  '版本': 'Version',
  '更新日志': 'Changelog',
  '隐私政策': 'Privacy Policy',
  '用户协议': 'Terms of Service',
  '证书': 'Certificate',
  '凭证': 'Credential',
  '待定': 'TBD',
  '正在加载数据...': 'Loading data...',
  '小组赛': 'Group Stage',
  '淘汰赛': 'Knockout',
  '赛事信息': 'Info',
  '小组赛进行中': 'Group Stage',
  '淘汰赛进行中': 'Knockout Stage',
  '距开幕': 'Countdown',
  '倒计时': 'Countdown',
  '已结束': 'Ended',
  '参赛球队': 'Teams',
  '小组': 'Groups',
  '主办城市': 'Host Cities',
  '总场次': 'Matches',
  '赛事进度': 'Progress',
  '进球最多': 'Top Scorers',
  '防守最强': 'Best Defense',
  '1/16决赛': 'Round of 32',
  '1/8决赛': 'Round of 16',
  '1/4决赛': 'Quarterfinal',
  '半决赛': 'Semifinal',
  '季军赛': '3rd Place',
  '决赛': 'Final',
  '净胜球': 'GD',
  '积分': 'Pts',
  '赛': 'P',
  '胜': 'W',
  '平': 'D',
  '负': 'L',
  '进': 'GF',
  '失': 'GA',
  '净': 'GD',
  '分': 'Pts',
  '已晋级': 'Advanced',
  '刷新数据': 'Refresh',
  '数据每60秒自动刷新': 'Auto-refresh every 60s',
  '上次更新': 'Last updated',
  '淘汰赛数据暂未发布': 'Knockout data not available yet',
  '淘汰赛对阵数据暂不可用': 'Knockout matchups not available',
  '重新开始': 'Restart',
  '游乐场': 'Playground',
  '得分': 'Score',
  '显示答案': 'Show Answer',
  '将事件按时间顺序排列': 'Arrange events in chronological order',
  '点击正确的下一个事件': 'Click the correct next event',
  '已排对': 'Sorted',
  '分数': 'Points',
  '代码': 'Code',
  '新游戏': 'New Game',
  '例如': 'e.g.',
  '点击': 'Click',
  '再来一局': 'Play Again',
  '语法参考': 'Syntax Reference',
  '编辑器': 'Editor',
  '复制代码': 'Copy Code',
  '返回工具列表': 'Back to Tools',
  '下一题': 'Next Question',
  '暂无记录': 'No Records',
  '计划列表': 'Plan List',
  '暂无计划': 'No Plans',
  '添加计划': 'Add Plan',
  '创建计划': 'Create Plan',
  '开始游戏': 'Start Game',
  '备注': 'Notes',
  '已复制到剪贴板': 'Copied to clipboard',
  '输出': 'Output',
  '添加记录': 'Add Record',
  '困难': 'Hard',
  '速度': 'Speed',
  '运行': 'Run',
  '返回工具箱': 'Back to Toolbox',
  '用时': 'Time Used',
  '记录列表': 'Record List',
  '就绪': 'Ready',
  '中等': 'Medium',
  '模板': 'Template',
  '查询': 'Query',
  '切换暗色模式': 'Toggle Dark Mode',
  '排序': 'Sort',
  '按评分排序': 'Sort by Rating',
  '步数': 'Steps',
  '示例': 'Example',
  '行数': 'Lines',
  '导出': 'Export',
  '简单': 'Easy',
  '游戏结束': 'Game Over',
  '切换主题': 'Toggle Theme',
  '数据仅供参考': 'Data for reference only',
  '支持': 'Support',
};

function translateText(text){
  return COMMON[text] || text;
}

function translateNode(node){
  if (!node) return;
  if (node.nodeType === 3){
    var text = node.textContent;
    var translated = translateText(text);
    if (translated !== text){
      node.textContent = translated;
    }
  } else if (node.nodeType === 1 && node.querySelectorAll){
    if (/^(SCRIPT|STYLE)$/i.test(node.tagName)) return;
    if (/^(INPUT|TEXTAREA)$/i.test(node.tagName)){
      var ph = node.getAttribute('placeholder');
      if (ph && COMMON[ph]) node.setAttribute('placeholder', COMMON[ph]);
      return;
    }
    if (node.getAttribute && node.getAttribute('data-i18n')){
      var key = node.getAttribute('data-i18n');
      if (COMMON[key]) node.textContent = COMMON[key];
      return;
    }
    var walker = document.createTreeWalker(node, 4, null, false);
    var n;
    while (n = walker.nextNode()){
      if (n.nodeType === 3){
        var t = n.textContent;
        var tr = translateText(t);
        if (tr !== t) n.textContent = tr;
      }
    }
  }
}

function scanAndTranslate(){
  if (currentLang === 'zh-CN') return;
  translateNode(document.body);
}

window.garyyTranslate = function(el){
  if (currentLang === 'zh-CN') return;
  translateNode(el || document.body);
};

var observer = null;
function startObserver(){
  if (observer) observer.disconnect();
  if (currentLang === 'zh-CN') return;
  observer = new MutationObserver(function(mutations){
    for (var i = 0; i < mutations.length; i++){
      var m = mutations[i];
      for (var j = 0; j < (m.addedNodes || []).length; j++){
        var node = m.addedNodes[j];
        if (node.nodeType === 1 && !/^(SCRIPT|STYLE)$/i.test(node.tagName)){
          translateNode(node);
        } else if (node.nodeType === 3){
          var text = node.textContent;
          var translated = translateText(text);
          if (translated !== text) node.textContent = translated;
        }
      }
    }
  });
  observer.observe(document.body, {childList: true, subtree: true});
}

function applyLang(lang){
  if (lang === currentLang) return;
  currentLang = lang;
  localStorage.setItem(STORAGE_KEY, lang);
  document.documentElement.lang = lang;
  location.reload();
}

window.garyyApplyLang = applyLang;

function createToggle(){
  var langBtn = document.getElementById('lang-toggle');
  if (langBtn){
    langBtn.innerHTML = currentLang === 'zh-CN' ? '🌐 EN' : '🌐 中';
    langBtn.addEventListener('click', function(){
      applyLang(currentLang === 'zh-CN' ? 'en' : 'zh-CN');
    });
    return;
  }
  var btn = document.createElement('div');
  btn.id = 'garyy-lang-toggle';
  btn.style.cssText = 'position:fixed;bottom:20px;left:20px;z-index:99999;background:var(--bg-card,#1f2937);color:var(--text,#e5e7eb);border:1px solid var(--border,#374151);border-radius:20px;padding:6px 14px;font-size:.8rem;cursor:pointer;box-shadow:0 2px 12px rgba(0,0,0,.3);display:flex;align-items:center;gap:6px;font-family:-apple-system,BlinkMacSystemFont,sans-serif;transition:all .2s';
  btn.innerHTML = '<span style="font-size:1rem">🌐</span> <span id="garyy-lang-label">' + (currentLang === 'zh-CN' ? '中文' : 'EN') + '</span>';
  btn.addEventListener('click', function(){
    var newLang = currentLang === 'zh-CN' ? 'en' : 'zh-CN';
    applyLang(newLang);
  });
  document.body.appendChild(btn);
}

document.documentElement.lang = currentLang;
if (currentLang === 'en') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){
      scanAndTranslate();
      startObserver();
    });
  } else {
    scanAndTranslate();
    startObserver();
  }
}
createToggle();

if (location.pathname.indexOf('/tools/') === 0) {
  var homeBtn = document.createElement('a');
  homeBtn.href = '/index.html';
  homeBtn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:99998;background:var(--bg-card,#1f2937);color:var(--text,#e5e7eb);border:1px solid var(--border,#374151);border-radius:20px;padding:6px 14px;font-size:.8rem;cursor:pointer;box-shadow:0 2px 12px rgba(0,0,0,.3);display:flex;align-items:center;gap:6px;font-family:-apple-system,BlinkMacSystemFont,sans-serif;transition:all .2s;text-decoration:none';
  homeBtn.innerHTML = '<span style="font-size:1rem">🏠</span> ' + (currentLang === 'en' ? 'Home' : '首页');
  homeBtn.onmouseenter = function(){this.style.borderColor='#3b82f6';};
  homeBtn.onmouseleave = function(){this.style.borderColor='#374151';};
  document.body.appendChild(homeBtn);

  var themeBtn = document.createElement('button');
  var savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
  themeBtn.id = 'garyy-theme-btn';
  themeBtn.style.cssText = 'position:fixed;bottom:20px;right:' + (currentLang === 'en' ? '100px' : '90px') + ';z-index:99998;background:var(--bg-card,#1f2937);color:var(--text,#e5e7eb);border:1px solid var(--border,#374151);border-radius:50%;width:36px;height:36px;font-size:1rem;cursor:pointer;box-shadow:0 2px 12px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;transition:all .2s;line-height:1';
  themeBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
  themeBtn.onmouseenter = function(){this.style.borderColor='#3b82f6';};
  themeBtn.onmouseleave = function(){this.style.borderColor='#374151';};
  themeBtn.onclick = function(){
    var cur = localStorage.getItem(THEME_KEY) || 'dark';
    var next = cur === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';
  };
  document.body.appendChild(themeBtn);
}

})();
