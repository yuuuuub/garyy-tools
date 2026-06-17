#!/usr/bin/env python3
"""批量生成工具43-100"""
import os

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--accent:#3b82f6;--accent2:#2563eb;--success:#22c55e;--warn:#f59e0b;--danger:#ef4444;--radius:12px;--shadow:0 2px 12px rgba(0,0,0,.4)}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:20px;line-height:1.6}
.ctn{max-width:720px;margin:0 auto}
.hdr{text-align:center;margin-bottom:24px}
.hdr h1{font-size:1.8rem;font-weight:700}
.hdr p{color:var(--text2);margin-top:4px;font-size:.9rem}
.cd{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:16px;box-shadow:var(--shadow)}
.cd h2{font-size:1.1rem;margin-bottom:12px;color:var(--accent)}
input,textarea,select,button{font-family:inherit;font-size:.95rem}
input[type=text],input[type=number],input[type=date],input[type=time],textarea,select{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);outline:none;transition:border .2s}
input:focus,textarea:focus,select:focus{border-color:var(--accent)}
textarea{resize:vertical;min-height:80px}
select{cursor:pointer}
button{padding:10px 20px;background:var(--accent);color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:600;transition:all .2s}
button:hover{background:var(--accent2)}
button:active{transform:scale(.97)}
button.sec{background:var(--bg);border:1px solid var(--border);color:var(--text)}
button.dng{background:var(--danger)}
.bg{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
label{display:block;font-size:.85rem;color:var(--text2);margin-bottom:4px;margin-top:10px}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:480px){.fr{grid-template-columns:1fr}.ctn{padding:0}}
.li{display:flex;justify-content:space-between;align-items:center;padding:12px;border-bottom:1px solid var(--border)}
.li:last-child{border-bottom:none}
.tag{display:inline-block;padding:2px 8px;border-radius:12px;font-size:.75rem;background:var(--accent);color:#fff;margin-right:4px}
.tag.s{background:var(--success)}.tag.w{background:var(--warn)}.tag.d{background:var(--danger)}
.es{text-align:center;padding:40px;color:var(--text2)}
.pb{width:100%;height:8px;background:var(--bg);border-radius:4px;overflow:hidden;margin-top:8px}
.pb .fl{height:100%;background:var(--accent);border-radius:4px;transition:width .3s}
.gr{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}
.gr .st{text-align:center;padding:16px;background:var(--bg);border-radius:8px}
.gr .st .nm{font-size:1.5rem;font-weight:700;color:var(--accent)}
.gr .st .lb{font-size:.8rem;color:var(--text2);margin-top:4px}
table{width:100%;border-collapse:collapse;margin-top:8px}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--border);font-size:.9rem}
th{color:var(--text2);font-weight:600}
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

# 定义所有剩余工具的通用模式: tracker, planner, calculator, log, journal等
# 用模板快速生成

def simple_tracker(slug, title, icon, desc, fields, field_labels, extra=""):
    """通用追踪器模板"""
    field_inputs = "\n".join([f'<label>{fl}</label><input type="{"number" if "num" in f else "text"}" id="{f}" {"step=0.01" if "price" in f or "amount" in f or "weight" in f or "cal" in f or "mg" in f or "ml" in f or "count" in f or "hours" in f or "min" in f else ""} placeholder="{fl}">' for f, fl in zip(fields, field_labels)])
    body = f'''<div class="cd"><h2>添加记录</h2>
{field_inputs}
<div class="bg"><button onclick="addRec()">添加记录</button></div></div>
<div class="cd"><h2>记录列表</h2><div id="recL" class="es">暂无记录</div></div>{extra}'''
    key = slug.replace("-", "_")
    add_fields = "".join([f",$('{f}').value=''" for f in fields[1:]])
    rec_entries = "".join([f'<span>{{{{r.{fields[1]}}}}}</span>' if i == 1 else '' for i, _ in enumerate(fields)])
    field_display = " | ".join([f"{{{{r.{f}}}}}" for f in fields[1:]])
    js = f'''let REC=JSON.parse(localStorage.getItem('{key}List')||'[]');
function rRec(){{$('recL').innerHTML=REC.length?REC.map((r,i)=>'<div class="li"><div style="flex:1"><span class="tag">{{{{r.date}}}}</span> {field_display}</div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="REC.splice('+i+',1);localStorage.setItem('{key}List',JSON.stringify(REC));rRec()">删除</button></div>').reverse().join(''):'<div class="es">暂无记录</div>'}}
function addRec(){{{fields[0]}=document.getElementById('{fields[0]}').value.trim()||'未命名';{",".join([f"{f}=document.getElementById('{f}').value" for f in fields[1:]])};REC.push({{{",".join([f"{f}:{f}" for f in fields])},date:new Date().toLocaleDateString()}});localStorage.setItem('{key}List',JSON.stringify(REC));rRec();{add_fields}}}
function $(id){{return document.getElementById(id)}}rRec()'''
    return body, js

def simple_log(slug, title, icon, desc, field_names, field_labels):
    """通用日志模板"""
    field_inputs = "\n".join([f'<label>{fl}</label><input type="text" id="{fn}" placeholder="{fl}">' for fn, fl in zip(field_names, field_labels)])
    body = f'''<div class="cd"><h2>添加日志</h2>
{field_inputs}
<label>备注</label><textarea id="logNote" placeholder="详细描述"></textarea>
<div class="bg"><button onclick="addLog()">添加日志</button></div></div>
<div class="cd"><h2>日志列表</h2><div id="logL" class="es">暂无日志</div></div>'''
    key = slug.replace("-", "_")
    add_fields = "".join([f"document.getElementById('{fn}').value=''" for fn in field_names])
    display_fields = " ".join([f'<span class="tag">{{{{r.{fn}}}}}</span>' for fn in field_names])
    js = f'''let LOGS=JSON.parse(localStorage.getItem('{key}Logs')||'[]');
function rLog(){{$('logL').innerHTML=LOGS.length?LOGS.map((r,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span class="tag">{{{{r.date}}}}</span> {display_fields}</div><p style="color:var(--text2);font-size:.9rem;margin-top:4px">{{{{r.note}}}}</p><button class="dng" style="padding:4px 12px;font-size:.8rem;align-self:flex-start" onclick="LOGS.splice('+i+',1);localStorage.setItem('{key}Logs',JSON.stringify(LOGS));rLog()">删除</button></div>').reverse().join(''):'<div class="es">暂无日志</div>'}}
function addLog(){{{",".join([f"var {fn}=document.getElementById('{fn}').value.trim()" for fn in field_names])},note=document.getElementById('logNote').value.trim();LOGS.push({{{",".join([f"{fn}" for fn in field_names])},note,date:new Date().toLocaleDateString()}});localStorage.setItem('{key}Logs',JSON.stringify(LOGS));rLog();{add_fields}document.getElementById('logNote').value=''}}
function $(id){{return document.getElementById(id)}}rLog()'''
    return body, js

def simple_planner(slug, title, icon, desc, fields, field_labels):
    """通用计划器模板"""
    field_inputs = "\n".join([f'<label>{fl}</label><input type="text" id="{fn}" placeholder="{fl}">' for fn, fl in zip(fields, field_labels)])
    body = f'''<div class="cd"><h2>创建计划</h2>
{field_inputs}
<label>日期</label><input type="date" id="planDate">
<div class="bg"><button onclick="addPlan()">添加计划</button></div></div>
<div class="cd"><h2>计划列表</h2><div id="planL" class="es">暂无计划</div></div>'''
    key = slug.replace("-", "_")
    add_fields = "".join([f"document.getElementById('{fn}').value=''" for fn in fields])
    display_fields = " ".join([f'<span class="tag">{{{{r.{fn}}}}}</span>' for fn in fields])
    js = f'''let PLANS=JSON.parse(localStorage.getItem('{key}Plans')||'[]');
function rPlan(){{$('planL').innerHTML=PLANS.length?PLANS.map((r,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span class="tag">{{{{r.date}}}}</span> {display_fields}</div><div class="bg"><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="PLANS.splice('+i+',1);localStorage.setItem('{key}Plans',JSON.stringify(PLANS));rPlan()">删除</button></div></div>').reverse().join(''):'<div class="es">暂无计划</div>'}}
function addPlan(){{{",".join([f"var {fn}=document.getElementById('{fn}').value.trim()" for fn in fields])},date=document.getElementById('planDate').value||new Date().toLocaleDateString();PLANS.push({{{",".join([f"{fn}" for fn in fields])},date}});localStorage.setItem('{key}Plans',JSON.stringify(PLANS));rPlan();{add_fields}document.getElementById('planDate').value=''}}
function $(id){{return document.getElementById(id)}}rPlan()'''
    return body, js

def simple_calculator(slug, title, icon, desc, inputs, input_labels, calc_formula, result_display):
    """通用计算器模板"""
    field_inputs = "\n".join([f'<label>{il}</label><input type="number" id="{i}" placeholder="{il}" {"step=0.01" if "rate" in i or "pct" in i or "price" in i else ""}>' for i, il in zip(inputs, input_labels)])
    body = f'''<div class="cd"><h2>计算</h2>
{field_inputs}
<div class="bg"><button onclick="calc()">计算</button></div></div>
<div class="cd" id="calcRC" style="display:none"><h2>计算结果</h2><div id="calcRA"></div></div>'''
    js = f'''function calc(){{{calc_formula}$('calcRC').style.display='';$('calcRA').innerHTML='{result_display}'}}
function $(id){{return document.getElementById(id)}}'''
    return body, js

# ===== 批量定义工具 =====
tool_defs = []

# 44-47: 更多追踪器
tool_defs.extend([
    ("platinum-tracker","铂金追踪器","💎","铂金价格追踪",
     *simple_tracker("platinum-tracker","铂金追踪器","💎","铂金价格追踪",["ptBuy","ptCur","ptQty"],["买入价(元/克)","当前价(元/克)","持有克数"])),
    ("oil-tracker","石油追踪器","🛢️","原油价格追踪",
     *simple_tracker("oil-tracker","石油追踪器","🛢️","原油价格追踪",["olBuy","olCur","olQty"],["买入价","当前价","持有量(桶)"])),
    ("commodity-tracker","大宗商品追踪器","📦","大宗商品价格追踪",
     *simple_tracker("commodity-tracker","大宗商品追踪器","📦","大宗商品追踪",["cmName","cmBuy","cmCur","cmQty"],["商品名称","买入价","当前价","数量"])),
    ("index-tracker","指数追踪器","📊","股市指数追踪",
     *simple_tracker("index-tracker","指数追踪器","📊","股票指数追踪",["idxName","idxVal","idxChange"],["指数名称","当前点位","涨跌幅%"])),
])

# 49-52: ETF/债券/股息/财报
tool_defs.extend([
    ("etf-tracker","ETF追踪器","📈","ETF基金追踪",
     *simple_tracker("etf-tracker","ETF追踪器","📈","ETF基金追踪",["etfName","etfBuy","etfCur","etfQty"],["ETF名称","买入价","当前价","持有份额"])),
    ("bond-tracker","债券追踪器","📃","债券投资追踪",
     *simple_tracker("bond-tracker","债券追踪器","📃","债券投资追踪",["bdName","bdRate","bdAmount","bdDate"],["债券名称","票面利率%","投资金额","到期日"])),
    ("dividend-tracker","股息追踪器","💰","股票分红追踪",
     *simple_tracker("dividend-tracker","股息追踪器","💰","股票分红追踪",["dvStock","dvAmount","dvDate"],["股票名称","分红金额(元)","分红日期"])),
    ("earnings-tracker","财报追踪器","📋","上市公司财报",
     *simple_tracker("earnings-tracker","财报追踪器","📋","上市公司财报",["erCompany","erRevenue","erProfit","erDate"],["公司名称","营收(亿)","净利润(亿)","财报日期"])),
])

# 53-56: 新闻/RSS/书签/笔记
tool_defs.extend([
    ("news-aggregator","新闻聚合器","📰","自定义新闻聚合",
     '''<div class="cd"><h2>添加新闻</h2>
<label>标题</label><input type="text" id="nsT" placeholder="新闻标题">
<label>来源</label><input type="text" id="nsS" placeholder="新闻来源">
<label>链接</label><input type="text" id="nsL" placeholder="https://...">
<label>分类</label><select id="nsC"><option>科技</option><option>财经</option><option>体育</option><option>娱乐</option><option>其他</option></select>
<div class="bg"><button onclick="addNS()">添加</button></div></div>
<div class="cd"><h2>新闻列表</h2><div id="nsL2" class="es">暂无新闻</div></div>''',
     '''let NS=JSON.parse(localStorage.getItem('nsList')||'[]');function rNS(){$('nsL2').innerHTML=NS.length?NS.map((n,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+n.title+'</span><span class="tag">'+n.category+'</span></div><div style="display:flex;justify-content:space-between;margin-top:4px"><span style="font-size:.8rem;color:var(--text2)">'+n.source+'</span>'+(n.link?'<a href="'+n.link+'" target="_blank" style="color:var(--accent);font-size:.85rem">阅读 →</a>':'')+'</div><button class="dng" style="padding:4px 12px;font-size:.8rem;align-self:flex-start;margin-top:4px" onclick="NS.splice('+i+',1);localStorage.setItem(\\'nsList\\',JSON.stringify(NS));rNS()">删除</button></div>').reverse().join(''):'<div class="es">暂无新闻</div>'}
function addNS(){const t=$('nsT').value.trim(),s=$('nsS').value.trim(),l=$('nsL').value.trim(),c=$('nsC').value;if(!t){alert('请填写标题');return}NS.push({title:t,source:s||'未知',link:l,category:c});localStorage.setItem('nsList',JSON.stringify(NS));rNS();$('nsT').value='';$('nsS').value='';$('nsL').value=''}
function $(id){return document.getElementById(id)}rNS()'''),

    ("rss-reader","RSS阅读器","📡","RSS订阅阅读",
     '''<div class="cd"><h2>添加订阅</h2>
<label>订阅名称</label><input type="text" id="rsN" placeholder="订阅名称">
<label>RSS地址</label><input type="text" id="rsU" placeholder="https://example.com/rss">
<div class="bg"><button onclick="addRS()">添加订阅</button></div></div>
<div class="cd"><h2>已订阅</h2><div id="rsL" class="es">暂无订阅</div></div>''',
     '''let RS=JSON.parse(localStorage.getItem('rsList')||'[]');function rRS(){$('rsL').innerHTML=RS.length?RS.map((r,i)=>'<div class="li"><div style="flex:1"><span style="font-weight:600">'+r.name+'</span><br><span style="font-size:.8rem;color:var(--text2)">'+r.url+'</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="RS.splice('+i+',1);localStorage.setItem(\\'rsList\\',JSON.stringify(RS));rRS()">删除</button></div>').join(''):'<div class="es">暂无订阅</div>'}
function addRS(){const n=$('rsN').value.trim(),u=$('rsU').value.trim();if(!n||!u){alert('请填写名称和地址');return}RS.push({name:n,url:u});localStorage.setItem('rsList',JSON.stringify(RS));rRS();$('rsN').value='';$('rsU').value=''}
function $(id){return document.getElementById(id)}rRS()'''),

    ("bookmark-manager","书签管理器","🔖","网页书签管理",
     '''<div class="cd"><h2>添加书签</h2>
<label>标题</label><input type="text" id="bmT" placeholder="书签标题">
<label>链接</label><input type="text" id="bmL" placeholder="https://...">
<label>分类</label><input type="text" id="bmC" placeholder="分类">
<div class="bg"><button onclick="addBM()">添加书签</button></div></div>
<div class="cd"><h2>书签列表</h2><div id="bmL2" class="es">暂无书签</div></div>''',
     '''let BM=JSON.parse(localStorage.getItem('bmList')||'[]');function rBM(){$('bmL2').innerHTML=BM.length?BM.map((b,i)=>'<div class="li"><div style="flex:1"><span style="font-weight:600">'+b.title+'</span><br><a href="'+b.link+'" target="_blank" style="color:var(--accent);font-size:.85rem">'+b.link.substring(0,40)+'...</a>'+(b.category?'<br><span class="tag" style="margin-top:4px">'+b.category+'</span>':'')+'</div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="BM.splice('+i+',1);localStorage.setItem(\\'bmList\\',JSON.stringify(BM));rBM()">删除</button></div>').join(''):'<div class="es">暂无书签</div>'}
function addBM(){const t=$('bmT').value.trim(),l=$('bmL').value.trim(),c=$('bmC').value.trim();if(!t||!l){alert('请填写标题和链接');return}BM.push({title:t,link:l,category:c});localStorage.setItem('bmList',JSON.stringify(BM));rBM();$('bmT').value='';$('bmL').value='';$('bmC').value=''}
function $(id){return document.getElementById(id)}rBM()'''),

    ("note-taking","笔记工具","📝","快速笔记",
     '''<div class="cd"><h2>新建笔记</h2>
<label>标题</label><input type="text" id="ntT" placeholder="笔记标题">
<label>标签</label><input type="text" id="ntG" placeholder="标签（逗号分隔）">
<label>内容</label><textarea id="ntC" rows="6" placeholder="笔记内容"></textarea>
<div class="bg"><button onclick="addNT()">保存笔记</button></div></div>
<div class="cd"><h2>笔记列表</h2><div id="ntL" class="es">暂无笔记</div></div>''',
     '''let NT=JSON.parse(localStorage.getItem('ntList')||'[]');function rNT(){$('ntL').innerHTML=NT.length?NT.map((n,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+n.title+'</span><span style="font-size:.8rem;color:var(--text2)">'+n.date+'</span></div>'+(n.tags.length?'<div style="margin:4px 0">'+n.tags.map(t=>'<span class="tag">'+t+'</span>').join('')+'</div>':'')+'<p style="color:var(--text2);font-size:.9rem;white-space:pre-wrap">'+n.content.substring(0,200)+(n.content.length>200?'...':'')+'</p><div class="bg"><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="NT.splice('+i+',1);localStorage.setItem(\\'ntList\\',JSON.stringify(NT));rNT()">删除</button></div></div>').reverse().join(''):'<div class="es">暂无笔记</div>'}
function addNT(){const t=$('ntT').value.trim(),g=$('ntG').value.trim(),c=$('ntC').value.trim();if(!c){alert('请填写笔记内容');return}NT.push({title:t||'无标题',tags:g?g.split(/[,，]/).map(s=>s.trim()):[],content:c,date:new Date().toLocaleDateString()});localStorage.setItem('ntList',JSON.stringify(NT));rNT();$('ntT').value='';$('ntG').value='';$('ntC').value=''}
function $(id){return document.getElementById(id)}rNT()'''),
])

# 57-58: 待办/看板
tool_defs.extend([
    ("todo-app","待办应用","☑️","简单待办列表",
     '''<div class="cd"><h2>添加待办</h2>
<label>待办内容</label><input type="text" id="tdT" placeholder="输入待办事项" onkeypress="if(event.key==='Enter')addTD()">
<div class="bg"><button onclick="addTD()">添加</button></div></div>
<div class="cd"><h2>待办列表 (<span id="tdC">0</span>项)</h2><div id="tdL" class="es">暂无待办</div></div>''',
     '''let TD=JSON.parse(localStorage.getItem('tdList')||'[]');function rTD(){$('tdC').textContent=TD.length;const pending=TD.filter(t=>!t.done),done=TD.filter(t=>t.done);let html=pending.map((t,i)=>'<div class="li"><div style="display:flex;align-items:center;gap:10px;flex:1;cursor:pointer" onclick="TD['+TD.indexOf(t)+'].done=true;saveTD();rTD()"><div style="width:22px;height:22px;border:2px solid var(--border);border-radius:50%;flex-shrink:0"></div><span>'+t.text+'</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="TD.splice('+TD.indexOf(t)+',1);saveTD();rTD()">删除</button></div>').join('');if(done.length){html+='<div style="padding:8px 0;color:var(--text2);font-size:.85rem">已完成 ('+done.length+')</div>';html+=done.map((t,i)=>'<div class="li" style="opacity:.6"><div style="display:flex;align-items:center;gap:10px;flex:1"><div style="width:22px;height:22px;border:2px solid var(--success);border-radius:50%;background:var(--success);display:flex;align-items:center;justify-content:center;color:#fff;font-size:.7rem">✓</div><span style="text-decoration:line-through">'+t.text+'</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="TD.splice('+TD.indexOf(t)+',1);saveTD();rTD()">删除</button></div>').join('')}$('tdL').innerHTML=html||'<div class="es">暂无待办</div>'}
function addTD(){const t=$('tdT').value.trim();if(!t)return;TD.push({text:t,done:false});saveTD();rTD();$('tdT').value=''}
function saveTD(){localStorage.setItem('tdList',JSON.stringify(TD))}
function $(id){return document.getElementById(id)}rTD()'''),

    ("kanban-board","看板工具","📋","Kanban看板",
     '''<div class="cd"><h2>添加卡片</h2>
<label>标题</label><input type="text" id="kbT" placeholder="卡片标题">
<label>列</label><select id="kbC"><option>待办</option><option>进行中</option><option>已完成</option></select>
<div class="bg"><button onclick="addKB()">添加卡片</button></div></div>
<div id="kbB" style="display:flex;gap:12px;overflow-x:auto"></div>''',
     '''let KB=JSON.parse(localStorage.getItem('kbList')||'[]');const cols=['待办','进行中','已完成'];const colColors=['var(--warn)','var(--accent)','var(--success)'];
function rKB(){$('kbB').innerHTML=cols.map((col,i)=>'<div style="min-width:200px;flex:1;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px"><div style="display:flex;justify-content:space-between;margin-bottom:12px"><h3 style="font-size:.95rem;color:'+colColors[i]+'">'+col+'</h3><span class="tag">'+KB.filter(k=>k.col===i).length+'</span></div>'+KB.filter(k=>k.col===i).map((k,j)=>'<div style="padding:10px;background:var(--bg);border-radius:8px;margin-bottom:8px;cursor:move"><span style="font-size:.9rem">'+k.title+'</span><div style="display:flex;gap:4px;margin-top:6px">'+(i>0?'<button class="sec" style="padding:2px 8px;font-size:.7rem" onclick="KB['+KB.indexOf(k)+'].col--;rKB()">←</button>':'')+(i<2?'<button class="sec" style="padding:2px 8px;font-size:.7rem" onclick="KB['+KB.indexOf(k)+'].col++;rKB()">→</button>':'')+'<button class="dng" style="padding:2px 8px;font-size:.7rem" onclick="KB.splice('+KB.indexOf(k)+',1);localStorage.setItem(\\'kbList\\',JSON.stringify(KB));rKB()">×</button></div></div>').join('')+'</div>').join('')}
function addKB(){const t=$('kbT').value.trim(),c=parseInt($('kbC').value);if(!t){alert('请填写标题');return}KB.push({title:t,col:c});localStorage.setItem('kbList',JSON.stringify(KB));rKB();$('kbT').value=''}
function $(id){return document.getElementById(id)}rKB()'''),
])

# 59-60: 甘特图/时间线
tool_defs.extend([
    ("gantt-chart","甘特图","📊","项目甘特图",
     '''<div class="cd"><h2>添加任务</h2>
<label>任务名称</label><input type="text" id="gtN" placeholder="任务名称">
<label>开始日期</label><input type="date" id="gtS">
<label>结束日期</label><input type="date" id="gtE">
<label>进度 (0-100%)</label><input type="number" id="gtP" value="0" min="0" max="100">
<div class="bg"><button onclick="addGT()">添加任务</button></div></div>
<div class="cd"><h2>甘特图</h2><div id="gtL" class="es">暂无任务</div></div>''',
     '''let GT=JSON.parse(localStorage.getItem('gtList')||'[]');function rGT(){if(!GT.length){$('gtL').innerHTML='<div class="es">暂无任务</div>';return}const allDates=GT.flatMap(t=>[new Date(t.start),new Date(t.end)]);const minD=new Date(Math.min(...allDates)),maxD=new Date(Math.max(...allDays=GT.map(t=>new Date(t.end))));const totalDays=Math.max(1,(maxD-minD)/(86400000))+1;let html='<div style="overflow-x:auto">'+GT.map((t,i)=>{const s=new Date(t.start),e=new Date(t.end);const startOff=Math.max(0,(s-minD)/86400000);const dur=Math.max(1,(e-s)/86400000);const leftPct=startOff/totalDays*100;const widthPct=Math.max(2,dur/totalDays*100);return'<div style="display:flex;align-items:center;margin-bottom:8px"><div style="width:120px;font-size:.85rem;flex-shrink:0">'+t.name+'</div><div style="flex:1;height:24px;background:var(--bg);border-radius:4px;position:relative"><div style="position:absolute;left:'+leftPct+'%;width:'+widthPct+'%;height:100%;background:var(--accent);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:.7rem;color:#fff">'+t.progress+'%</div></div></div>'}).join('')+'</div>';$('gtL').innerHTML=html}
function addGT(){const n=$('gtN').value.trim(),s=$('gtS').value,e=$('gtE').value,p=parseInt($('gtP').value)||0;if(!n||!s||!e){alert('请填写完整信息');return}GT.push({name:n,start:s,end:e,progress:p});localStorage.setItem('gtList',JSON.stringify(GT));rGT();$('gtN').value=''}
function $(id){return document.getElementById(id)}rGT()'''),

    ("timeline-builder","时间线构建器","📅","事件时间线",
     '''<div class="cd"><h2>添加事件</h2>
<label>事件名称</label><input type="text" id="tlN" placeholder="事件名称">
<label>日期</label><input type="date" id="tlD">
<label>描述</label><textarea id="tlDesc" rows="2" placeholder="事件描述"></textarea>
<div class="bg"><button onclick="addTL()">添加事件</button></div></div>
<div class="cd"><h2>时间线</h2><div id="tlL" class="es">暂无事件</div></div>''',
     '''let TL=JSON.parse(localStorage.getItem('tlList')||'[]');function rTL(){$('tlL').innerHTML=TL.length?'<div style="border-left:3px solid var(--accent);padding-left:20px">'+TL.sort((a,b)=>a.date.localeCompare(b.date)).map((e,i)=>'<div style="position:relative;margin-bottom:16px"><div style="position:absolute;left:-26px;width:12px;height:12px;border-radius:50%;background:var(--accent)"></div><span class="tag">'+e.date+'</span><h3 style="margin:4px 0">'+e.name+'</h3><p style="color:var(--text2);font-size:.9rem">'+e.desc+'</p><button class="dng" style="padding:2px 10px;font-size:.75rem" onclick="TL.splice('+i+',1);localStorage.setItem(\\'tlList\\',JSON.stringify(TL));rTL()">删除</button></div>').join('')+'</div>':'<div class="es">暂无事件</div>'}
function addTL(){const n=$('tlN').value.trim(),d=$('tlD').value,desc=$('tlDesc').value.trim();if(!n){alert('请填写事件名称');return}TL.push({name:n,date:d||new Date().toLocaleDateString(),desc});localStorage.setItem('tlList',JSON.stringify(TL));rTL();$('tlN').value='';$('tlDesc').value=''}
function $(id){return document.getElementById(id)}rTL()'''),
])

# 61-66: 日历/提醒/闹钟/秒表/计时器/倒计时
tool_defs.extend([
    ("calendar-pro","日历Pro","📅","个人日历管理",
     '''<div class="cd"><h2>添加事件</h2>
<label>标题</label><input type="text" id="cpT" placeholder="事件标题">
<label>日期</label><input type="date" id="cpD">
<label>时间</label><input type="time" id="cpTm" value="09:00">
<label>类型</label><select id="cpTy"><option>工作</option><option>个人</option><option>纪念日</option></select>
<div class="bg"><button onclick="addCP()">添加事件</button></div></div>
<div class="cd"><h2>事件列表</h2><div id="cpL" class="es">暂无事件</div></div>''',
     '''let CP=JSON.parse(localStorage.getItem('cpList')||'[]');function rCP(){$('cpL').innerHTML=CP.length?CP.sort((a,b)=>a.date.localeCompare(b.date)).map((e,i)=>'<div class="li"><div style="flex:1"><div style="display:flex;align-items:center;gap:8px"><span class="tag">'+e.type+'</span><span style="font-weight:600">'+e.title+'</span></div><span style="font-size:.8rem;color:var(--text2)">'+e.date+' '+e.time+'</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="CP.splice('+i+',1);localStorage.setItem(\\'cpList\\',JSON.stringify(CP));rCP()">删除</button></div>').join(''):'<div class="es">暂无事件</div>'}
function addCP(){const t=$('cpT').value.trim(),d=$('cpD').value,tm=$('cpTm').value,ty=$('cpTy').value;if(!t){alert('请填写标题');return}CP.push({title:t,date:d,time:tm,type:ty});localStorage.setItem('cpList',JSON.stringify(CP));rCP();$('cpT').value=''}
function $(id){return document.getElementById(id)}rCP()'''),

    ("reminder-app","提醒应用","⏰","定时提醒",
     '''<div class="cd"><h2>设置提醒</h2>
<label>提醒内容</label><input type="text" id="rmC" placeholder="提醒内容">
<label>提醒时间</label><input type="time" id="rmT">
<div class="bg"><button onclick="addRM()">添加提醒</button></div></div>
<div class="cd"><h2>提醒列表</h2><div id="rmL" class="es">暂无提醒</div></div>''',
     '''let RM=JSON.parse(localStorage.getItem('rmList')||'[]');function rRM(){$('rmL').innerHTML=RM.length?RM.map((r,i)=>'<div class="li"><div style="flex:1"><span style="font-weight:600">'+r.content+'</span><br><span style="font-size:.8rem;color:var(--text2)">'+r.time+'</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="RM.splice('+i+',1);localStorage.setItem(\\'rmList\\',JSON.stringify(RM));rRM()">删除</button></div>').join(''):'<div class="es">暂无提醒</div>'}
function addRM(){const c=$('rmC').value.trim(),t=$('rmT').value;if(!c){alert('请填写提醒内容');return}RM.push({content:c,time:t||'未设定'});localStorage.setItem('rmList',JSON.stringify(RM));rRM();$('rmC').value=''}
function $(id){return document.getElementById(id)}rRM()'''),

    ("alarm-app","闹钟应用","🔔","自定义闹钟",
     '''<div class="cd" style="text-align:center">
<p style="font-size:3rem;font-weight:700;font-variant-numeric:tabular-nums" id="alTime">00:00:00</p>
<p style="color:var(--text2);margin-bottom:16px" id="alDate"></p>
<div class="bg" style="justify-content:center">
<button onclick="setAlarm()">设置闹钟</button>
<button class="sec" id="alStop" style="display:none" onclick="stopAlarm()">停止</button>
</div></div>
<div class="cd"><h2>闹钟列表</h2><div id="alL" class="es">暂无闹钟</div></div>''',
     '''let ALS=JSON.parse(localStorage.getItem('alList')||'[]'),alarmPlaying=false;
function upClock(){const now=new Date();$('alTime').textContent=now.toLocaleTimeString('zh-CN',{hour12:false});$('alDate').textContent=now.toLocaleDateString('zh-CN',{weekday:'long',year:'numeric',month:'long',day:'numeric'});ALS.forEach(a=>{if(!a.fired&&now.toTimeString().substring(0,5)===a.time){a.fired=true;alarmPlaying=true;$('alStop').style.display='';alert('⏰ '+a.content)}})}
function rAL(){$('alL').innerHTML=ALS.length?ALS.map((a,i)=>'<div class="li"><div style="flex:1"><span style="font-weight:600">'+a.time+'</span> - '+a.content+'</div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="ALS.splice('+i+',1);localStorage.setItem(\\'alList\\',JSON.stringify(ALS));rAL()">删除</button></div>').join(''):'<div class="es">暂无闹钟</div>'}
function setAlarm(){const t=prompt('设置闹钟时间(格式: 07:30):');if(!t)return;ALS.push({time:t,content:'闹钟提醒',fired:false});localStorage.setItem('alList',JSON.stringify(ALS));rAL()}
function stopAlarm(){alarmPlaying=false;$('alStop').style.display='none'}
setInterval(upClock,1000);upClock();rAL();
function $(id){return document.getElementById(id)}'''),

    ("stopwatch-pro","秒表Pro","⏱️","精确秒表",
     '''<div class="cd" style="text-align:center">
<p style="font-size:3rem;font-weight:700;font-variant-numeric:tabular-nums" id="swT">00:00.00</p>
<div class="bg" style="justify-content:center">
<button id="swB" onclick="togSW()">▶ 开始</button>
<button class="sec" onclick="lapSW()">计次</button>
<button class="sec" onclick="rstSW()">重置</button>
</div></div>
<div class="cd"><h2>计次记录</h2><div id="swL" class="es">暂无记录</div></div>''',
     '''let swRun=false,swInt=null,swMs=0,swLaps=[];
function togSW(){if(swRun){swRun=false;clearInterval(swInt);$('swB').textContent='▶ 继续'}else{swRun=true;$('swB').textContent='⏸ 暂停';swInt=setInterval(()=>{swMs++;upSW()},10)}}
function rstSW(){swRun=false;clearInterval(swInt);swMs=0;swLaps=[];$('swB').textContent='▶ 开始';upSW();$('swL').innerHTML=''}
function lapSW(){if(swRun)swLaps.push(swMs);rLap()}
function rLap(){$('swL').innerHTML=swLaps.length?swLaps.map((l,i)=>'<div class="li"><span>计次 '+(i+1)+'</span><span>'+fmtMs(l)+'</span></div>').reverse().join(''):'<div class="es">暂无记录</div>'}
function upSW(){$('swT').textContent=fmtMs(swMs)}
function fmtMs(ms){const m=Math.floor(ms/6000),s=Math.floor(ms%6000/100),c=ms%100;return(m<10?'0':'')+m+':'+(s<10?'0':'')+s+'.'+(c<10?'0':'')+c}
function $(id){return document.getElementById(id)}'''),

    ("timer-pro","计时器Pro","⏳","自定义倒计时",
     '''<div class="cd" style="text-align:center">
<label>设置时间</label>
<div class="fr" style="max-width:300px;margin:0 auto"><div><label>小时</label><input type="number" id="tmH" value="0" min="0" max="23"></div><div><label>分钟</label><input type="number" id="tmM" value="5" min="0" max="59"></div><div><label>秒</label><input type="number" id="tmS" value="0" min="0" max="59"></div></div>
<p style="font-size:3rem;font-weight:700;margin:24px 0;font-variant-numeric:tabular-nums" id="tmD">00:05:00</p>
<div class="bg" style="justify-content:center"><button id="tmB" onclick="togTM()">▶ 开始</button><button class="sec" onclick="rstTM()">重置</button></div></div>''',
     '''let tmRun=false,tmInt=null,tmRem=300;
function togTM(){if(tmRun){tmRun=false;clearInterval(tmInt);$('tmB').textContent='▶ 继续'}else{if(!tmRem){tmRem=parseInt($('tmH').value)*3600+parseInt($('tmM').value)*60+parseInt($('tmS').value)}tmRun=true;$('tmB').textContent='⏸ 暂停';tmInt=setInterval(()=>{tmRem--;if(tmRem<=0){tmRun=false;clearInterval(tmInt);$('tmB').textContent='▶ 开始';alert('⏰ 时间到！')}upTM()},1000)}}
function rstTM(){tmRun=false;clearInterval(tmInt);tmRem=parseInt($('tmH').value)*3600+parseInt($('tmM').value)*60+parseInt($('tmS').value);upTM();$('tmB').textContent='▶ 开始'}
function upTM(){const h=Math.floor(tmRem/3600),m=Math.floor(tmRem%3600/60),s=tmRem%60;$('tmD').textContent=(h<10?'0':'')+h+':'+(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function $(id){return document.getElementById(id)}upTM()'''),

    ("countdown-pro","倒计时Pro","⏳","目标日倒计时",
     '''<div class="cd"><h2>添加倒计时</h2>
<label>事件名称</label><input type="text" id="cdN" placeholder="新年/生日/考试...">
<label>目标日期</label><input type="date" id="cdD">
<div class="bg"><button onclick="addCD()">添加</button></div></div>
<div class="cd"><h2>倒计时列表</h2><div id="cdL" class="es">暂无倒计时</div></div>''',
     '''let CD=JSON.parse(localStorage.getItem('cdList')||'[]');function rCD(){$('cdL').innerHTML=CD.length?CD.map((c,i)=>{const target=new Date(c.date),now=new Date(),diff=Math.ceil((target-now)/86400000);const color=diff<=0?'var(--danger)':diff<=7?'var(--warn)':'var(--accent)';return'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+c.name+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="CD.splice('+i+',1);localStorage.setItem(\\'cdList\\',JSON.stringify(CD));rCD()">删除</button></div><div style="text-align:center;padding:12px;background:var(--bg);border-radius:8px;margin-top:8px"><p style="font-size:2rem;font-weight:700;color:'+color+'">'+(diff>0?diff+'天':'已过期')+'</p><p style="font-size:.85rem;color:var(--text2)">'+c.date+'</p></div></div>'}).join(''):'<div class="es">暂无倒计时</div>'}
function addCD(){const n=$('cdN').value.trim(),d=$('cdD').value;if(!n||!d){alert('请填写完整信息');return}CD.push({name:n,date:d});localStorage.setItem('cdList',JSON.stringify(CD));rCD();$('cdN').value=''}
function $(id){return document.getElementById(id)}rCD()'''),
])

# 67-73: 世界时钟/多秒表/多计时器/番茄扩展/专注/冥想/呼吸
tool_defs.extend([
    ("world-clock-pro","世界时钟Pro","🌍","多时区时钟",
     '''<div class="cd"><h2>添加城市</h2>
<label>城市名称</label><input type="text" id="wcN" placeholder="东京">
<label>UTC偏移</label><input type="number" id="wcU" value="8" min="-12" max="14">
<div class="bg"><button onclick="addWC()">添加城市</button></div></div>
<div id="wcB"></div>''',
     '''let WC=JSON.parse(localStorage.getItem('wcList')||'[{name:"北京",offset:8},{name:"纽约",offset:-4},{name:"伦敦",offset:1},{name:"东京",offset:9}]');
function rWC(){$('wcB').innerHTML=WC.map((c,i)=>'<div class="cd" style="text-align:center;padding:16px"><p style="font-size:.85rem;color:var(--text2)">'+c.name+' (UTC+'+(c.offset>=0?'+':'')+c.offset+')</p><p style="font-size:1.8rem;font-weight:700;font-variant-numeric:tabular-nums" id="wc'+i+'"></p><button class="dng" style="padding:2px 10px;font-size:.75rem" onclick="WC.splice('+i+',1);localStorage.setItem(\\'wcList\\',JSON.stringify(WC));rWC()">删除</button></div>').join('')}
function addWC(){const n=$('wcN').value.trim(),u=parseInt($('wcU').value)||0;if(!n){alert('请填写城市名称');return}WC.push({name:n,offset:u});localStorage.setItem('wcList',JSON.stringify(WC));rWC();$('wcN').value=''}
function upWC(){const now=new Date();WC.forEach((c,i)=>{const utc=now.getTime()+now.getTimezoneOffset()*60000;const local=new Date(utc+c.offset*3600000);const el=document.getElementById('wc'+i);if(el)el.textContent=local.toLocaleTimeString('zh-CN',{hour12:false})})}
setInterval(upWC,1000);rWC();upWC();
function $(id){return document.getElementById(id)}'''),

    ("stopwatch-multi","多秒表","⏱️","同时多个秒表",
     '''<div class="cd"><h2>创建秒表</h2>
<label>秒表名称</label><input type="text" id="smN" placeholder="跑步">
<div class="bg"><button onclick="addSM()">创建秒表</button></div></div>
<div id="smB"></div>''',
     '''let SMS=[];function rSM(){$('smB').innerHTML=SMS.map((s,i)=>'<div class="cd"><div style="display:flex;justify-content:space-between;align-items:center"><h2>'+s.name+'</h2><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="SMS.splice('+i+',1);rSM()">删除</button></div><p style="font-size:2rem;font-weight:700;text-align:center;margin:12px 0;font-variant-numeric:tabular-nums">'+fmtSW(s.ms)+'</p><div class="bg" style="justify-content:center"><button onclick="togSM('+i+')">'+(s.running?'暂停':'开始')+'</button><button class="sec" onclick="rstSM('+i+')">重置</button></div></div>').join('')}
function addSM(){const n=$('smN').value.trim()||'秒表'+(SMS.length+1);SMS.push({name:n,ms:0,running:false,int:null});rSM();$('smN').value=''}
function togSM(i){const s=SMS[i];if(s.running){clearInterval(s.int);s.running=false}else{s.running=true;s.int=setInterval(()=>{s.ms++;upSM(i)},10)}rSM()}
function rstSM(i){clearInterval(SMS[i].int);SMS[i].ms=0;SMS[i].running=false;rSM()}
function upSM(i){const el=document.querySelector('#smB .cd:nth-child('+(i+1)+') p');if(el)el.textContent=fmtSW(SMS[i].ms)}
function fmtSW(ms){const m=Math.floor(ms/6000),s=Math.floor(ms%6000/100),c=ms%100;return(m<10?'0':'')+m+':'+(s<10?'0':'')+s+'.'+(c<10?'0':'')+c}
function $(id){return document.getElementById(id)}'''),

    ("timer-multi","多计时器","⏳","同时多个倒计时",
     '''<div class="cd"><h2>创建倒计时</h2>
<label>名称</label><input type="text" id="tmN" placeholder="煮面">
<label>分钟</label><input type="number" id="tmM" value="10" min="1">
<div class="bg"><button onclick="addMT()">创建</button></div></div>
<div id="mtB"></div>''',
     '''let MTS=[];function rMT(){$('mtB').innerHTML=MTS.map((t,i)=>'<div class="cd" style="text-align:center"><div style="display:flex;justify-content:space-between"><h2>'+t.name+'</h2><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="clearInterval(MTS['+i+'].int);MTS.splice('+i+',1);rMT()">删除</button></div><p style="font-size:2rem;font-weight:700;margin:12px 0;color:'+(t.rem<=0?'var(--danger)':'var(--text)')+';font-variant-numeric:tabular-nums">'+fmtMT(t.rem)+'</p><div class="bg" style="justify-content:center"><button onclick="togMT('+i+')">'+(t.running?'暂停':'开始')+'</button><button class="sec" onclick="rstMT('+i+')">重置</button></div></div>').join('')}
function addMT(){const n=$('tmN').value.trim()||'计时'+(MTS.length+1),m=parseInt($('tmM').value)||10;MTS.push({name:n,rem:m*60,orig:m*60,running:false,int:null});rMT();$('tmN').value=''}
function togMT(i){const t=MTS[i];if(t.running){clearInterval(t.int);t.running=false}else{t.running=true;t.int=setInterval(()=>{t.rem--;if(t.rem<=0){clearInterval(t.int);t.running=false;alert('⏰ '+t.name+' 时间到！')}rMT()},1000)}rMT()}
function rstMT(i){clearInterval(MTS[i].int);MTS[i].rem=MTS[i].orig;MTS[i].running=false;rMT()}
function fmtMT(s){const h=Math.floor(s/3600),m=Math.floor(s%3600/60),sc=s%60;return(h?((h<10?'0':'')+h+':'):(''))+(m<10?'0':'')+m+':'+(sc<10?'0':'')+sc}
function $(id){return document.getElementById(id)}'''),

    ("pomodoro-extended","扩展番茄钟","🍅","番茄钟+统计",
     '''<div class="cd" style="text-align:center">
<h2>扩展番茄钟</h2>
<div class="fr" style="max-width:300px;margin:16px auto"><div><label>专注(分)</label><input type="number" id="peW" value="25" min="1"></div><div><label>休息(分)</label><input type="number" id="peB" value="5" min="1"></div></div>
<p style="font-size:3rem;font-weight:700;margin:16px 0;font-variant-numeric:tabular-nums" id="peT">25:00</p>
<p style="color:var(--text2)" id="peS">专注时间</p>
<div class="bg" style="justify-content:center"><button id="peBt" onclick="togPE()">▶ 开始</button><button class="sec" onclick="rstPE()">重置</button></div></div>
<div class="cd"><h2>今日统计</h2><div class="gr"><div class="st"><div class="nm" id="peCnt">0</div><div class="lb">番茄数</div></div><div class="st"><div class="nm" id="peMin">0</div><div class="lb">专注分钟</div></div></div></div>''',
     '''let peRun=false,peInt=null,peRem=25*60,peMode='work',peCount=0,peTotalMin=0;
function togPE(){if(peRun){peRun=false;clearInterval(peInt);$('peBt').textContent='▶ 继续'}else{peRem=parseInt(peMode==='work'?$('peW').value:$('peB').value)*60;peRun=true;$('peBt').textContent='⏸ 暂停';peInt=setInterval(()=>{peRem--;if(peRem<=0){clearInterval(peInt);peRun=false;if(peMode==='work'){peCount++;peTotalMin+=parseInt($('peW').value);$('peCnt').textContent=peCount;$('peMin').textContent=peTotalMin;peMode='break';alert('🍅 完成！休息一下')}else{peMode='work';alert('💪 休息结束！继续')}$('peS').textContent=peMode==='work'?'专注时间':'休息时间';$('peBt').textContent='▶ 开始'}upPE()},1000)}}
function rstPE(){peRun=false;clearInterval(peInt);peMode='work';peRem=parseInt($('peW').value)*60;$('peS').textContent='专注时间';$('peBt').textContent='▶ 开始';upPE()}
function upPE(){const m=Math.floor(peRem/60),s=peRem%60;$('peT').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function $(id){return document.getElementById(id)}upPE()'''),

    ("focus-session","专注会话","🎯","深度专注会话",
     '''<div class="cd"><h2>专注会话</h2>
<label>会话目标</label><input type="text" id="fsG" placeholder="专注目标">
<label>时长(分钟)</label><input type="number" id="fsM" value="45" min="5" max="180">
<label>屏蔽干扰</label><select id="fsD"><option value="full">完全屏蔽</option><option value="partial">部分屏蔽</option><option value="none">不屏蔽</option></select>
<div class="bg"><button onclick="startFS()">开始专注</button></div></div>
<div class="cd" id="fsC" style="display:none;text-align:center">
<h2 id="fsTi">专注中</h2>
<p style="font-size:3rem;font-weight:700;margin:16px 0;font-variant-numeric:tabular-nums" id="fsT">00:00</p>
<p style="color:var(--text2)" id="fsDesc"></p>
<div class="bg" style="justify-content:center"><button class="dng" onclick="endFS()">结束会话</button></div></div>''',
     '''let fsRun=false,fsInt=null,fsRem=0;
function startFS(){const m=parseInt($('fsM').value)||45;const g=$('fsG').value.trim()||'专注会话';fsRem=m*60;fsRun=true;$('fsC').style.display='';$('fsTi').textContent=g;$('fsDesc').textContent='屏蔽: '+{full:'完全屏蔽',partial:'部分屏蔽',none:'不屏蔽'}[$('fsD').value];fsInt=setInterval(()=>{fsRem--;if(fsRem<=0){fsRun=false;clearInterval(fsInt);alert('🎯 专注完成！');$('fsC').style.display='none'}upFS()},1000)}
function endFS(){fsRun=false;clearInterval(fsInt);$('fsC').style.display='none'}
function upFS(){const m=Math.floor(fsRem/60),s=fsRem%60;$('fsT').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function $(id){return document.getElementById(id)}'''),

    ("meditation-timer","冥想计时器","🧘","冥想引导计时",
     '''<div class="cd"><h2>冥想计时</h2>
<label>冥想类型</label><select id="mtTy"><option value="breathing">呼吸冥想</option><option value="body">身体扫描</option><option value="focus">专注冥想</option><option value="loving">慈悲冥想</option></select>
<label>时长(分钟)</label><input type="number" id="mtM" value="10" min="1" max="60">
<div class="bg"><button onclick="startMT()">开始冥想</button></div></div>
<div class="cd" id="mtC" style="display:none;text-align:center">
<div style="font-size:4rem;margin:16px 0" id="mtIcon">🧘</div>
<p style="font-size:2rem;font-weight:700;font-variant-numeric:tabular-nums" id="mtT">10:00</p>
<p style="color:var(--text2);margin:12px 0" id="mtGuide">闭上眼睛，深呼吸...</p>
<div class="bg" style="justify-content:center"><button class="dng" onclick="endMT()">结束</button></div></div>''',
     '''let mtRun=false,mtInt=null,mtRem=0,mtGI=0;
const guides={breathing:['闭上眼睛','深吸一口气','慢慢呼出','感受呼吸的节奏','让思绪随呼吸流动'],body:['从头顶开始','感受面部肌肉','放松肩膀','注意手臂的感觉','感受双腿的重量'],focus:['选择一个焦点','注意力集中','当思绪飘走时拉回','保持觉察','回到当下'],loving:['想到自己','对自己微笑','想到亲人朋友','祝福所有人','感受爱与温暖']};
function startMT(){const ty=$('mtTy').value,m=parseInt($('mtM').value)||10;mtRem=m*60;mtRun=true;$('mtC').style.display='';mtGI=0;window._mtGuides=guides[ty];$('mtGuide').textContent=window._mtGuides[0];mtInt=setInterval(()=>{mtRem--;if(mtRem%30===0&&mtGI<window._mtGuides.length-1){mtGI++;$('mtGuide').textContent=window._mtGuides[mtGI]}if(mtRem<=0){mtRun=false;clearInterval(mtInt);alert('🧘 冥想完成！Namaste');$('mtC').style.display='none'}upMT()},1000)}
function endMT(){mtRun=false;clearInterval(mtInt);$('mtC').style.display='none'}
function upMT(){const m=Math.floor(mtRem/60),s=mtRem%60;$('mtT').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function $(id){return document.getElementById(id)}'''),

    ("breathing-pro","呼吸Pro","🫁","呼吸练习引导",
     '''<div class="cd"><h2>呼吸练习</h2>
<label>练习类型</label><select id="bpTy"><option value="478">4-7-8 放松呼吸</option><option value="box">盒子呼吸</option><option value="calm">平静呼吸</option><option value="energy">能量呼吸</option></select>
<label>重复次数</label><input type="number" id="bpR" value="5" min="1" max="20">
<div class="bg"><button onclick="startBP()">开始练习</button></div></div>
<div class="cd" id="bpC" style="display:none;text-align:center">
<div style="width:150px;height:150px;border-radius:50%;border:4px solid var(--accent);margin:16px auto;display:flex;align-items:center;justify-content:center;transition:all 1s" id="bpCir">
<p style="font-size:1.5rem;font-weight:700" id="bpAct">准备</p>
</div>
<p style="font-size:2rem;font-weight:700;margin:12px 0" id="bpT">0</p>
<p style="color:var(--text2)" id="bpInfo"></p>
<div class="bg" style="justify-content:center"><button class="dng" onclick="endBP()">结束</button></div></div>''',
     '''let bpRun=false,bpInt=null,bpCycles=0,bpMaxCycles=5;
const bpPatterns={478:{name:'4-7-8',steps:[{dur:4,act:'吸气',size:1.3},{dur:7,act:'屏息',size:1.3},{dur:8,act:'呼气',size:1}]},box:{name:'盒子',steps:[{dur:4,act:'吸气',size:1.3},{dur:4,act:'屏息',size:1.3},{dur:4,act:'呼气',size:1},{dur:4,act:'屏息',size:1}]},calm:{name:'平静',steps:[{dur:4,act:'吸气',size:1.2},{dur:6,act:'呼气',size:1}]},energy:{name:'能量',steps:[{dur:2,act:'吸气',size:1.3},{dur:2,act:'呼气',size:1}]}};
function startBP(){const ty=$('bpTy').value;bpMaxCycles=parseInt($('bpR').value)||5;bpCycles=0;bpRun=true;$('bpC').style.display='';runBPStep(bpPatterns[ty],0)}
function runBPStep(pat,stepIdx){if(!bpRun)return;if(stepIdx>=pat.steps.length){bpCycles++;if(bpCycles>=bpMaxCycles){endBP();alert('🫁 练习完成！');return}runBPStep(pat,0);return}const step=pat.steps[stepIdx];$('bpAct').textContent=step.act;$('bpCir').style.transform='scale('+step.size+')';$('bpCir').style.borderColor=step.act==='吸气'?'var(--success)':'var(--accent)';let countdown=step.dur;$('bpT').textContent=countdown;$('bpInfo').textContent='第 '+(bpCycles+1)+'/'+bpMaxCycles+' 轮';bpInt=setInterval(()=>{countdown--;$('bpT').textContent=countdown;if(countdown<=0){clearInterval(bpInt);runBPStep(pat,stepIdx+1)}},1000)}
function endBP(){bpRun=false;clearInterval(bpInt);$('bpC').style.display='none'}
function $(id){return document.getElementById(id)}'''),
])

# Write all
for slug, title, icon, desc, body, js in tool_defs:
    w(slug, title, icon, desc, body, js)

print(f"\nBatch 3 done: {len(tool_defs)} tools")
