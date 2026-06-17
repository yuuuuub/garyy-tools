#!/usr/bin/env python3
"""批量生成工具74-154"""
import os

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--accent:#3b82f6;--accent2:#2563eb;--success:#22c55e;--warn:#f59e0b;--danger:#ef4444;--radius:12px;--shadow:0 2px 12px rgba(0,0,0,.4)}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:20px;line-height:1.6}
.ctn{max-width:720px;margin:0 auto}.hdr{text-align:center;margin-bottom:24px}.hdr h1{font-size:1.8rem;font-weight:700}.hdr p{color:var(--text2);margin-top:4px;font-size:.9rem}
.cd{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:16px;box-shadow:var(--shadow)}.cd h2{font-size:1.1rem;margin-bottom:12px;color:var(--accent)}
input,textarea,select,button{font-family:inherit;font-size:.95rem}
input[type=text],input[type=number],input[type=date],input[type=time],textarea,select{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);outline:none;transition:border .2s}
input:focus,textarea:focus,select:focus{border-color:var(--accent)}textarea{resize:vertical;min-height:80px}select{cursor:pointer}
button{padding:10px 20px;background:var(--accent);color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all .2s}button:hover{background:var(--accent2)}button:active{transform:scale(.97)}
button.sec{background:var(--bg);border:1px solid var(--border);color:var(--text)}button.dng{background:var(--danger)}
.bg{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}label{display:block;font-size:.85rem;color:var(--text2);margin-bottom:4px;margin-top:10px}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:480px){.fr{grid-template-columns:1fr}.ctn{padding:0}}
.li{display:flex;justify-content:space-between;align-items:center;padding:12px;border-bottom:1px solid var(--border)}.li:last-child{border-bottom:none}
.tag{display:inline-block;padding:2px 8px;border-radius:12px;font-size:.75rem;background:var(--accent);color:#fff;margin-right:4px}.tag.s{background:var(--success)}.tag.w{background:var(--warn)}.tag.d{background:var(--danger)}
.es{text-align:center;padding:40px;color:var(--text2)}
.pb{width:100%;height:8px;background:var(--bg);border-radius:4px;overflow:hidden;margin-top:8px}.pb .fl{height:100%;background:var(--accent);border-radius:4px;transition:width .3s}
.gr{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}.gr .st{text-align:center;padding:16px;background:var(--bg);border-radius:8px}.gr .st .nm{font-size:1.5rem;font-weight:700;color:var(--accent)}.gr .st .lb{font-size:.8rem;color:var(--text2);margin-top:4px}
table{width:100%;border-collapse:collapse;margin-top:8px}th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--border);font-size:.9rem}th{color:var(--text2);font-weight:600}
.hidden{display:none}
"""

def w(slug, title, icon, desc, body, js=""):
    d = os.path.join(TOOLS_DIR, slug)
    os.makedirs(d, exist_ok=True)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{icon} {title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="ctn">
<div class="hdr"><h1>{icon} {title}</h1><p>{desc}</p></div>
{body}
</div>
<script>{js}</script>
</body>
</html>'''
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ {slug}")

# 通用追踪器模板
def tracker(slug, title, icon, desc, ls_key, field_names, field_labels):
    field_inputs = "\n".join([f'<label>{fl}</label><input type="text" id="{fn}" placeholder="{fl}">' for fn, fl in zip(field_names, field_labels)])
    field_vals = ",".join([f"{fn}=document.getElementById('{fn}').value.trim()" for fn in field_names])
    field_save = ",".join([f"{fn}" for fn in field_names])
    field_display = " ".join([f'<span class="tag">{{{{r.{fn}}}}}</span>' for fn in field_names])
    field_reset = "".join([f"document.getElementById('{fn}').value=''" for fn in field_names])
    body = f'''<div class="cd"><h2>添加记录</h2>
{field_inputs}
<div class="bg"><button onclick="addR()">添加记录</button></div></div>
<div class="cd"><h2>记录列表</h2><div id="rL" class="es">暂无记录</div></div>'''
    js = f'''let R=JSON.parse(localStorage.getItem('{ls_key}')||'[]');
function rR(){{$('rL').innerHTML=R.length?R.map((r,i)=>'<div class="li"><div style="flex:1"><span class="tag">{{{{r.date}}}}</span> {field_display}</div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="R.splice('+i+',1);localStorage.setItem('{ls_key}',JSON.stringify(R));rR()">删除</button></div>').reverse().join(''):'<div class="es">暂无记录</div>'}}
function addR(){{{field_vals};R.push({{{field_save},date:new Date().toLocaleDateString()}});localStorage.setItem('{ls_key}',JSON.stringify(R));rR();{field_reset}}}
function $(id){{return document.getElementById(id)}}rR()'''
    return body, js

# 通用日志模板
def log(slug, title, icon, desc, ls_key, field_names, field_labels):
    field_inputs = "\n".join([f'<label>{fl}</label><input type="text" id="{fn}" placeholder="{fl}">' for fn, fl in zip(field_names, field_labels)])
    field_vals = ",".join([f"{fn}=document.getElementById('{fn}').value.trim()" for fn in field_names])
    field_save = ",".join([f"{fn}" for fn in field_names])
    field_display = " ".join([f'<span class="tag">{{{{r.{fn}}}}}</span>' for fn in field_names])
    field_reset = "".join([f"document.getElementById('{fn}').value=''" for fn in field_names])
    body = f'''<div class="cd"><h2>添加日志</h2>
{field_inputs}
<label>备注</label><textarea id="note" placeholder="详细描述"></textarea>
<div class="bg"><button onclick="addR()">添加日志</button></div></div>
<div class="cd"><h2>日志列表</h2><div id="rL" class="es">暂无日志</div></div>'''
    js = f'''let R=JSON.parse(localStorage.getItem('{ls_key}')||'[]');
function rR(){{$('rL').innerHTML=R.length?R.map((r,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span class="tag">{{{{r.date}}}}</span> {field_display}</div><p style="color:var(--text2);font-size:.9rem;margin-top:4px">{{{{r.note}}}}</p><button class="dng" style="padding:4px 12px;font-size:.8rem;align-self:flex-start" onclick="R.splice('+i+',1);localStorage.setItem('{ls_key}',JSON.stringify(R));rR()">删除</button></div>').reverse().join(''):'<div class="es">暂无日志</div>'}}
function addR(){{{field_vals};var note=document.getElementById('note').value.trim();R.push({{{field_save},note,date:new Date().toLocaleDateString()}});localStorage.setItem('{ls_key}',JSON.stringify(R));rR();{field_reset}document.getElementById('note').value=''}}
function $(id){{return document.getElementById(id)}}rR()'''
    return body, js

# 通用计划器模板
def planner(slug, title, icon, desc, ls_key, field_names, field_labels):
    field_inputs = "\n".join([f'<label>{fl}</label><input type="text" id="{fn}" placeholder="{fl}">' for fn, fl in zip(field_names, field_labels)])
    field_vals = ",".join([f"{fn}=document.getElementById('{fn}').value.trim()" for fn in field_names])
    field_save = ",".join([f"{fn}" for fn in field_names])
    field_display = " ".join([f'<span class="tag">{{{{r.{fn}}}}}</span>' for fn in field_names])
    field_reset = "".join([f"document.getElementById('{fn}').value=''" for fn in field_names])
    body = f'''<div class="cd"><h2>创建计划</h2>
{field_inputs}
<label>日期</label><input type="date" id="date">
<div class="bg"><button onclick="addR()">添加计划</button></div></div>
<div class="cd"><h2>计划列表</h2><div id="rL" class="es">暂无计划</div></div>'''
    js = f'''let R=JSON.parse(localStorage.getItem('{ls_key}')||'[]');
function rR(){{$('rL').innerHTML=R.length?R.map((r,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span class="tag">{{{{r.date}}}}</span> {field_display}</div><div class="bg"><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="R.splice('+i+',1);localStorage.setItem('{ls_key}',JSON.stringify(R));rR()">删除</button></div></div>').reverse().join(''):'<div class="es">暂无计划</div>'}}
function addR(){{{field_vals};var date=document.getElementById('date').value||new Date().toLocaleDateString();R.push({{{field_save},date}});localStorage.setItem('{ls_key}',JSON.stringify(R));rR();{field_reset}document.getElementById('date').value=''}}
function $(id){{return document.getElementById(id)}}rR()'''
    return body, js

# 通用计算器模板
def calculator(slug, title, icon, desc, inputs_info, calc_code, result_html):
    field_inputs = "\n".join([f'<label>{il}</label><input type="number" id="{i}" placeholder="{il}" {"step=0.01" if "rate" in i or "pct" in i or "price" in i or "weight" in i else ""}>' for i, il in inputs_info])
    body = f'''<div class="cd"><h2>计算</h2>
{field_inputs}
<div class="bg"><button onclick="calc()">计算</button></div></div>
<div class="cd" id="rC" style="display:none"><h2>计算结果</h2><div id="rA"></div></div>'''
    js = f'''function calc(){{{calc_code}$('rC').style.display='';$('rA').innerHTML='{result_html}'}}
function $(id){{return document.getElementById(id)}}'''
    return body, js

# ===== 74-90: 健康追踪类 =====
health_tools = [
    ("sleep-tracker","睡眠追踪器","😴","记录睡眠质量",["sleepTime","wakeTime","quality","dreams"],["入睡时间","起床时间","质量(1-5)","梦境记录"]),
    ("water-tracker-pro","喝水追踪Pro","💧","每日饮水量",["amount","type"],["饮水量(ml)","饮品类型"]),
    ("exercise-tracker","运动追踪器","🏃","记录运动数据",["sport","duration","calories"],["运动类型","时长(分钟)","消耗热量"]),
    ("calorie-tracker-pro","卡路里追踪Pro","🔥","食物热量追踪",["food","calories","meal"],["食物名称","卡路里","餐次"]),
    ("weight-tracker","体重追踪器","⚖️","体重变化追踪",["weight","bodyFat"],["体重(kg)","体脂率(%)"]),
    ("body-measurements","身体测量","📐","身体围度记录",["chest","waist","hip","arm"],["胸围(cm)","腰围(cm)","臀围(cm)","臂围(cm)"]),
    ("fitness-log","健身日志","💪","健身训练记录",["exercise","sets","reps","weight"],["训练动作","组数","次数","重量(kg)"]),
    ("workout-log-pro","训练日志Pro","🏋️","详细训练记录",["workout","muscleGroup","duration","difficulty"],["训练名称","肌群","时长","难度"]),
    ("meal-log","饮食日志","🍽️","记录每日饮食",["mealType","food","calories"],["餐次","食物","热量"]),
    ("recipe-book","菜谱本","📖","个人菜谱收藏",["recipeName","ingredients","cookTime","difficulty"],["菜名","食材","烹饪时间","难度"]),
    ("grocery-list","购物清单Pro","🛒","智能购物清单",["item","quantity","category"],["物品名称","数量","分类"]),
    ("pantry-tracker","食品库存追踪","🗄️","食品库存管理",["item","quantity","expiry"],["物品","数量/重量","保质期"]),
    ("meal-prep","备餐计划","🍱","一周备餐规划",["day","meal","dish"],["星期","餐次","菜品"]),
    ("nutrition-tracker","营养追踪器","📊","营养素追踪",["nutrient","amount","unit"],["营养素","含量","单位"]),
    ("vitamin-tracker","维生素追踪器","💊","每日维生素摄入",["vitamin","dose","time"],["维生素","剂量","服用时间"]),
    ("supplement-tracker","补剂追踪器","💊","营养补剂记录",["supplement","dose","frequency"],["补剂名称","剂量","频率"]),
    ("medication-tracker","药物追踪器","💊","用药记录管理",["medication","dosage","frequency","time"],["药物名称","用量","频率","时间"]),
]
for slug, title, icon, desc, fns, fls in health_tools:
    b, j = tracker(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 91-93: 预约/健康日志/症状
appointment_tools = [
    ("appointment-tracker","预约追踪器","📅","管理各类预约",["appt","doctor","date","time"],["预约事项","医生/地点","日期","时间"]),
    ("health-log","健康日志","📋","健康状态记录",["symptom","severity","notes"],["症状","严重程度(1-5)","备注"]),
    ("symptom-tracker","症状追踪器","🩺","症状变化追踪",["symptom","severity","duration","notes"],["症状","严重程度","持续时间","备注"]),
]
for slug, title, icon, desc, fns, fls in appointment_tools:
    b, j = log(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 94-98: 心情/日记/感恩/梦境/旅行
journal_tools = [
    ("mood-tracker-pro","心情追踪Pro","😊","心情变化追踪",["mood","energy","notes"],["心情(1-5)","精力(1-5)","备注"]),
    ("journal-app","日记应用","📔","个人日记",["title","mood"],["标题","心情"]),
    ("gratitude-journal","感恩日记","🙏","记录感恩事项",["gratitude","reason"],["感恩事项","原因"]),
    ("dream-journal","梦境日记","🌙","梦境记录",["dream","vividness","emotion"],["梦境内容","清晰度(1-5)","情绪"]),
    ("travel-journal","旅行日记","✈️","旅行记录",["destination","activity","companion"],["目的地","活动","同行者"]),
]
for slug, title, icon, desc, fns, fls in journal_tools:
    b, j = log(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 99-106: 各类日志/追踪
log_tools = [
    ("reading-log","阅读日志","📚","阅读记录追踪",["book","author","genre"],["书名","作者","类型"]),
    ("movie-log","电影日志","🎬","观影记录",["movie","director","rating"],["电影名称","导演","评分(1-5)"]),
    ("music-log","音乐日志","🎵","听歌记录",["song","artist","genre"],["歌曲","歌手","类型"]),
    ("game-log","游戏日志","🎮","游戏记录",["game","platform","hours"],["游戏名称","平台","游戏时长"]),
    ("hobby-tracker","爱好追踪器","🎨","兴趣爱好追踪",["hobby","hours","notes"],["爱好","投入时间","备注"]),
    ("skill-tracker","技能追踪器","📈","个人技能追踪",["skill","level","hours"],["技能名称","等级(1-5)","练习小时"]),
    ("language-tracker","语言追踪器","🌍","语言学习追踪",["language","level","hours"],["语言","等级","学习小时"]),
    ("certification-tracker","证书追踪器","🏆","证书管理追踪",["cert","issuer","date","expiry"],["证书名称","颁发机构","获取日期","有效期"]),
]
for slug, title, icon, desc, fns, fls in log_tools:
    b, j = log(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 107-116: 通讯录/生日/纪念日/活动策划/婚礼/派对/旅行/搬家/装修/园艺
social_planner_tools = [
    ("contact-book","通讯录","📇","联系人管理",["name","phone","email","group"],["姓名","电话","邮箱","分组"]),
    ("birthday-tracker","生日追踪器","🎂","生日提醒追踪",["name","birthday","gift"],["姓名","生日日期","礼物计划"]),
    ("anniversary-tracker","纪念日追踪器","💕","纪念日管理",["couple","anniversary","notes"],["纪念日名称","日期","备注"]),
    ("event-planner","活动策划器","🎉","活动策划管理",["event","venue","date","budget"],["活动名称","场地","日期","预算"]),
    ("wedding-planner","婚礼策划器","💒","婚礼筹备规划",["task","category","deadline","cost"],["任务","类别","截止日期","费用"]),
    ("party-planner","派对策划器","🎊","派对策划管理",["party","theme","date","guests"],["派对名称","主题","日期","宾客数"]),
    ("trip-planner","旅行策划器","✈️","旅行行程规划",["destination","date","activity","budget"],["目的地","日期","活动","预算"]),
    ("moving-planner","搬家策划器","🏠","搬家流程规划",["task","deadline","status"],["任务","日期","状态"]),
    ("renovation-planner","装修策划器","🔨","装修流程管理",["area","task","budget","status"],["区域","任务","预算","状态"]),
    ("garden-planner","园艺策划器","🌱","花园规划管理",["plant","location","plantDate","care"],["植物名称","种植位置","种植日期","养护方式"]),
]
for slug, title, icon, desc, fns, fls in social_planner_tools:
    b, j = planner(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 117-133: 各类计划器
more_planner_tools = [
    ("meal-planner-pro","膳食策划Pro","🍽️","一周膳食规划",["day","meal","dish","calories"],["星期","餐次","菜品","热量"]),
    ("diet-planner","饮食计划器","🥗","健康饮食计划",["meal","food","calories","notes"],["餐次","食物","热量","备注"]),
    ("exercise-planner","运动计划器","🏃","运动计划安排",["day","exercise","duration","intensity"],["星期","运动项目","时长","强度"]),
    ("study-planner","学习计划器","📚","学习计划安排",["subject","topic","duration","priority"],["科目","主题","时长","优先级"]),
    ("work-planner","工作计划器","💼","工作任务规划",["task","deadline","priority","status"],["任务","截止日期","优先级","状态"]),
    ("life-planner","人生计划器","🌟","人生目标规划",["goal","category","deadline","milestone"],["目标","类别","截止日期","里程碑"]),
    ("retirement-planner","退休计划器","🏖️","退休生活规划",["goal","age","amount","notes"],["退休目标","目标年龄","所需金额","备注"]),
    ("savings-planner","储蓄计划器","💰","储蓄目标计划",["goal","monthly","target","deadline"],["储蓄目标","每月存入","目标金额","截止日期"]),
    ("debt-planner","债务计划器","💳","还债计划管理",["debt","amount","rate","minPay"],["债务名称","金额","利率%","最低还款"]),
    ("investment-planner","投资计划器","📈","投资配置计划",["asset","allocation","risk","return"],["资产类别","配置比例%","风险等级","预期回报%"]),
    ("insurance-planner","保险计划器","🛡️","保险规划管理",["type","coverage","premium","expiry"],["保险类型","保额","保费","到期日"]),
    ("tax-planner","税务计划器","📋","税务规划助手",["income","deduction","rate","notes"],["收入","扣除项","税率%","备注"]),
    ("estate-planner","遗产计划器","📜","遗产分配规划",["heir","asset","percentage","notes"],["继承人","资产","分配比例%","备注"]),
    ("college-planner","大学计划器","🎓","大学申请规划",["school","major","deadline","status"],["学校名称","专业","截止日期","状态"]),
    ("career-planner","职业计划器","💼","职业发展规划",["goal","timeline","action","status"],["职业目标","时间线","行动计划","状态"]),
    ("skill-planner","技能计划器","📈","技能提升计划",["skill","level","target","deadline"],["技能名称","当前水平","目标水平","截止日期"]),
    ("learning-planner","学习计划器","📖","学习路径规划",["topic","resource","hours","deadline"],["学习主题","学习资源","计划时长","截止日期"]),
]
for slug, title, icon, desc, fns, fls in more_planner_tools:
    b, j = planner(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 134: 旅行计划器CN
b, j = planner("travel-planner-cn","旅行计划器CN","✈️","中国旅行规划","travel-CN-plan",["destination","date","activity","budget"],["目的地","日期","活动","预算(元)"])
w("travel-planner-cn","旅行计划器CN","✈️","中国旅行规划",b,j)

# 135-136: 预算/现金流
budget_tools = [
    ("budget-planner-pro","预算计划Pro","💰","详细预算规划",["income","category","budget","actual"],["收入来源","支出类别","预算金额","实际金额"]),
    ("cash-flow-planner","现金流计划器","💹","现金流管理",["type","amount","date","notes"],["类型(收入/支出)","金额","日期","备注"]),
]
for slug, title, icon, desc, fns, fls in budget_tools:
    b, j = planner(slug, title, icon, desc, f"{slug.replace('-','_')}DB", fns, fls)
    w(slug, title, icon, desc, b, j)

# 137-154: 计算器
calc_tools = [
    ("emergency-fund","应急基金计算器","🏦","计算应急基金目标",["monthly","months"],
     "var m=parseFloat($('monthly').value)||0,mo=parseInt($('months').value)||6;var target=m*mo,monthly=Math.ceil(target/12);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+target.toLocaleString()+'"""+'</div><div class="lb">应急基金目标(元)</div></div><div class="st"><div class="nm">'+"""'+monthly+'"""+'</div><div class="lb">每月需存(元)</div></div></div>'),

    ("net-worth-calculator","净资产计算器","💎","计算个人净资产",["assets","debts"],
     "var a=parseFloat($('assets').value)||0,d=parseFloat($('debts').value)||0;var nw=a-d,pct=a?Math.round(nw/a*100):0;",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+nw.toLocaleString()+'"""+'</div><div class="lb">净资产(元)</div></div><div class="st"><div class="nm">'+"""'+pct+'"""+'%</div><div class="lb">净资产率</div></div></div>'),

    ("debt-payoff-calculator","还债计算器","💳","计算还清债务时间",["balance","rate","payment"],
     "var b=parseFloat($('balance').value)||0,r=parseFloat($('rate').value)/100/12||0,p=parseFloat($('payment').value)||0;var months=0,totalInterest=0,bal=b;if(p<=0||b<=0){alert('请输入有效数据');return}while(bal>0&&months<600){var int=bal*r;totalInterest+=int;bal+=int-p;months++;if(p<=int){months=999;break}};",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+(months>=999?'∞':months)+'"""+'</div><div class="lb">还清月数</div></div><div class="st"><div class="nm">'+"""'+Math.round(totalInterest).toLocaleString()+'"""+'</div><div class="lb">总利息(元)</div></div></div><p style="text-align:center;color:var(--text2);margin-top:8px">'+"""'+(months>=999?'⚠️ 还款额不足以覆盖利息！':'预计'+months+'个月还清，利息共'+Math.round(totalInterest).toLocaleString()+'元')+'"""+'</p>'),

    ("savings-goal-calculator","储蓄目标计算器","🎯","计算储蓄达标时间",["goal","monthly","rate"],
     "var g=parseFloat($('goal').value)||0,m=parseFloat($('monthly').value)||0,r=parseFloat($('rate').value)/100/12||0;var months=0,saved=0;if(m<=0||g<=0){alert('请输入有效数据');return}while(saved<g&&months<600){saved=saved*(1+r)+m;months++};",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+months+'"""+'</div><div class="lb">达标月数</div></div><div class="st"><div class="nm">'+"""'+Math.round(saved).toLocaleString()+'"""+'</div><div class="lb">最终金额(元)</div></div></div>'),

    ("retirement-calculator","退休计算器","🏖️","退休储蓄规划",["currentAge","retireAge","monthly","return"],
     "var ca=parseInt($('currentAge').value)||30,ra=parseInt($('retireAge').value)||60;var m=parseFloat($('monthly').value)||0,r=parseFloat($('return').value)/100/12||0;var years=ra-ca,months=years*12,saved=0;for(var i=0;i<months;i++)saved=saved*(1+r)+m;var monthlyIncome=Math.round(saved*0.04/12);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.round(saved).toLocaleString()+'"""+'</div><div class="lb">退休基金(元)</div></div><div class="st"><div class="nm">'+"""'+monthlyIncome.toLocaleString()+'"""+'</div><div class="lb">月可取(元)</div></div><div class="st"><div class="nm">'+"""'+years+'"""+'</div><div class="lb">距退休年数</div></div></div>'),

    ("college-savings-calculator","大学储蓄计算器","🎓","大学费用规划",["childAge","collegeAge","annual","return"],
     "var ca=parseInt($('childAge').value)||0,cla=parseInt($('collegeAge').value)||18;var a=parseFloat($('annual').value)||0,r=parseFloat($('return').value)/100||0;var totalCost=a*4*Math.pow(1.05,4);var yearsLeft=Math.max(1,cla-ca);var monthly=Math.ceil(totalCost/yearsLeft/12);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.round(totalCost).toLocaleString()+'"""+'</div><div class="lb">预计总费用(元)</div></div><div class="st"><div class="nm">'+"""'+monthly+'"""+'</div><div class="lb">每月需存(元)</div></div></div>'),

    ("roth-ira-calculator","Roth IRA计算器","💰","Roth IRA增长预测",["annual","years","return"],
     "var a=parseFloat($('annual').value)||0,y=parseInt($('years').value)||0,r=parseFloat($('return').value)/100||0;var saved=0;for(var i=0;i<years;i++)saved=saved*(1+r)+a;var growth=saved-a*years;",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.round(saved).toLocaleString()+'"""+'</div><div class="lb">最终余额($)</div></div><div class="st"><div class="nm">'+"""'+Math.round(growth).toLocaleString()+'"""+'</div><div class="lb">投资收益($)</div></div></div>'),

    ("401k-calculator","401k计算器","🏦","401k退休计划",["salary","contribution","match","years","return"],
     "var s=parseFloat($('salary').value)||0,c=parseFloat($('contribution').value)/100||0;var mt=parseFloat($('match').value)/100||0,y=parseInt($('years').value)||0,r=parseFloat($('return').value)/100||0;var annual=s*c;var matchAmt=s*Math.min(c,mt);var total=annual+matchAmt;var saved=0;for(var i=0;i<years;i++)saved=saved*(1+r)+total;",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.round(saved).toLocaleString()+'"""+'</div><div class="lb">最终余额($)</div></div><div class="st"><div class="nm">'+"""'+Math.round(total).toLocaleString()+'"""+'</div><div class="lb">年存入($)</div></div></div>'),

    ("social-security-calculator","社保计算器","🏛️","社保待遇估算",["salary","years","avgSalary"],
     "var s=parseFloat($('salary').value)||0,y=parseInt($('years').value)||0;var avg=parseFloat($('avgSalary').value)||0;var basicPension=Math.round(avg*(1+y*0.01)/2);var personalAcc=Math.round(s*0.08*y*12*1.03);var monthly=basicPension+Math.round(personalAcc/139);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+monthly.toLocaleString()+'"""+'</div><div class="lb">预估月养老金(元)</div></div><div class="st"><div class="nm">'+"""'+basicPension.toLocaleString()+'"""+'</div><div class="lb">基础养老金(元)</div></div><div class="st"><div class="nm">'+"""'+personalAcc.toLocaleString()+'"""+'</div><div class="lb">个人账户(元)</div></div></div><p style="text-align:center;color:var(--text2);font-size:.8rem;margin-top:8px">*仅供参考</p>'),

    ("medicare-calculator","医保计算器","🏥","医疗保险费用",["income","familySize","age"],
     "var inc=parseFloat($('income').value)||0,fam=parseInt($('familySize').value)||1;var age=parseInt($('age').value)||30;var basePremium=Math.round(inc*0.0289);var ageAdj=age>=40?Math.round(basePremium*0.3):0;var total=basePremium+ageAdj;var subsidy=inc<40000?Math.round(total*0.5):0;",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+total.toLocaleString()+'"""+'</div><div class="lb">年保费($)</div></div><div class="st"><div class="nm">'+"""'+subsidy.toLocaleString()+'"""+'</div><div class="lb">补贴($)</div></div><div class="st"><div class="nm">'+"""'+(total-subsidy).toLocaleString()+'"""+'</div><div class="lb">实际保费($)</div></div></div>'),

    ("life-insurance-calculator","人寿保险计算器","🛡️","人寿保险需求",["income","debts","dependents","years"],
     "var inc=parseFloat($('income').value)||0,debt=parseFloat($('debts').value)||0;var dep=parseInt($('dependents').value)||0,y=parseInt($('years').value)||10;var need=inc*y+debt+dep*100000-50000;var monthly=Math.round(need/y/12*0.01);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.max(0,need).toLocaleString()+'"""+'</div><div class="lb">建议保额($)</div></div><div class="st"><div class="nm">'+"""'+monthly+'"""+'</div><div class="lb">预估月保费($)</div></div></div>'),

    ("disability-insurance-calculator","残疾保险计算器","🛡️","残疾保险需求",["income","savings","expenses"],
     "var inc=parseFloat($('income').value)||0;var sav=parseFloat($('savings').value)||0,exp=parseFloat($('expenses').value)||0;var benefit=Math.round(inc*0.6);var coverage=Math.round((exp*12-sav)/0.6);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+benefit.toLocaleString()+'"""+'</div><div class="lb">月给付额($)</div></div><div class="st"><div class="nm">'+"""'+coverage.toLocaleString()+'"""+'</div><div class="lb">建议保额($)</div></div></div>'),

    ("long-term-care-calculator","长期护理计算器","🏥","护理费用规划",["age","years","dailyCost"],
     "var age=parseInt($('age').value)||65,y=parseInt($('years').value)||3;var dc=parseFloat($('dailyCost').value)||200;var total=dc*365*y;var monthly=Math.round(total/(y*12));",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+total.toLocaleString()+'"""+'</div><div class="lb">总费用($)</div></div><div class="st"><div class="nm">'+"""'+monthly.toLocaleString()+'"""+'</div><div class="lb">月费用($)</div></div></div>'),

    ("annuity-calculator","年金计算器","💰","年金收益计算",["principal","rate","years"],
     "var p=parseFloat($('principal').value)||0,r=parseFloat($('rate').value)/100||0;var y=parseInt($('years').value)||0;var monthly=p*r/12*Math.pow(1+r/12,y*12)/(Math.pow(1+r/12,y*12)-1);var total=monthly*y*12;",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+Math.round(monthly).toLocaleString()+'"""+'</div><div class="lb">月领金额($)</div></div><div class="st"><div class="nm">'+"""'+Math.round(total).toLocaleString()+'"""+'</div><div class="lb">总领取($)</div></div></div>'),

    ("pension-calculator","养老金计算器","💰","养老金预估",["salary","years","contribution"],
     "var s=parseFloat($('salary').value)||0,y=parseInt($('years').value)||0;var c=parseFloat($('contribution').value)/100||0;var totalContrib=s*c*y*12;var monthlyPension=Math.round(totalContrib/139+s*0.01*y);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+monthlyPension.toLocaleString()+'"""+'</div><div class="lb">月养老金(元)</div></div><div class="st"><div class="nm">'+"""'+totalContrib.toLocaleString()+'"""+'</div><div class="lb">累计缴纳(元)</div></div></div>'),

    ("inheritance-tax-calculator","遗产税计算器","📋","遗产税估算",["estate","exemption","rate"],
     "var e=parseFloat($('estate').value)||0;var ex=parseFloat($('exemption').value)||0,r=parseFloat($('rate').value)/100||0;var taxable=Math.max(0,e-ex);var tax=Math.round(taxable*r);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+taxable.toLocaleString()+'"""+'</div><div class="lb">应税金额($)</div></div><div class="st"><div class="nm">'+"""'+tax.toLocaleString()+'"""+'</div><div class="lb">预估税额($)</div></div><div class="st"><div class="nm">'+"""'+(e-tax).toLocaleString()+'"""+'</div><div class="lb">净遗产($)</div></div></div>'),

    ("gift-tax-calculator","赠与税计算器","🎁","赠与税计算",["amount","exemption","rate"],
     "var a=parseFloat($('amount').value)||0;var ex=parseFloat($('exemption').value)||0,r=parseFloat($('rate').value)/100||0;var taxable=Math.max(0,a-ex);var tax=Math.round(taxable*r);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+taxable.toLocaleString()+'"""+'</div><div class="lb">应税金额($)</div></div><div class="st"><div class="nm">'+"""'+tax.toLocaleString()+'"""+'</div><div class="lb">赠与税($)</div></div><div class="st"><div class="nm">'+"""'+(a-tax).toLocaleString()+'"""+'</div><div class="lb">实际到手($)</div></div></div>'),

    ("estate-tax-calculator","财产税计算器","🏠","财产税估算",["value","rate","exemption"],
     "var v=parseFloat($('value').value)||0;var r=parseFloat($('rate').value)/100||0;var ex=parseFloat($('exemption').value)||0;var taxable=Math.max(0,v-ex);var tax=Math.round(taxable*r);",
     '<div class="gr"><div class="st"><div class="nm">'+"""'+v.toLocaleString()+'"""+'</div><div class="lb">财产价值($)</div></div><div class="st"><div class="nm">'+"""'+tax.toLocaleString()+'"""+'</div><div class="lb">财产税($)</div></div><div class="st"><div class="nm">'+"""'+Math.round(r*100*100)/100+'"""+'%</div><div class="lb">实际税率</div></div></div>'),
]

for slug, title, icon, desc, inputs_info, calc_code, result_html in calc_tools:
    # Build calculator
    field_inputs = "\n".join([f'<label>{il}</label><input type="number" id="{i}" placeholder="{il}" {"step=0.01" if "rate" in i or "pct" in i or "price" in i or "contribution" in i else ""}>' for i, il in inputs_info])
    body = f'''<div class="cd"><h2>计算</h2>
{field_inputs}
<div class="bg"><button onclick="calc()">计算</button></div></div>
<div class="cd" id="rC" style="display:none"><h2>计算结果</h2><div id="rA"></div></div>'''

    # Generate the full JS
    js = f'''function calc(){{{calc_code}$('rC').style.display='';$('rA').innerHTML='{result_html}'}}
function $(id){{return document.getElementById(id)}}'''
    w(slug, title, icon, desc, body, js)

print(f"\nBatch 4 done")
