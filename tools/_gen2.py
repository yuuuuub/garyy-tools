#!/usr/bin/env python3
"""批量生成工具27-52"""
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
input[type=text],input[type=number],input[type=date],input[type=time],input[type=color],textarea,select{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);outline:none;transition:border .2s}
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
    print(f"  ✓ {slug} - {title}")

tools = []

tools.append(("project-planner","项目规划器","📐","项目规划与分解",
'''<div class="cd"><h2>项目规划</h2>
<label>项目名称</label><input type="text" id="ppN" placeholder="项目名称">
<label>项目目标</label><textarea id="ppG" placeholder="项目目标描述"></textarea>
<label>开始日期</label><input type="date" id="ppS">
<label>预计结束</label><input type="date" id="ppE">
<label>任务分解（每行一个）</label>
<textarea id="ppT" rows="6" placeholder="需求分析\n设计阶段\n开发\n测试\n上线"></textarea>
<div class="bg"><button onclick="addPP()">添加项目</button></div></div>
<div class="cd"><h2>项目列表</h2><div id="ppL" class="es">暂无项目</div></div>''',
'''let PP=[];function rPP(){$('ppL').innerHTML=PP.length?PP.map((p,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+p.name+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="PP.splice('+i+',1);rPP()">删除</button></div><p style="color:var(--text2);font-size:.85rem;margin:4px 0">'+p.goal+'</p><span style="font-size:.8rem;color:var(--text2)">'+p.start+' → '+p.end+'</span><div style="margin-top:8px">'+p.tasks.map((t,j)=>'<div class="li" style="padding:6px 0"><span class="tag">'+(j+1)+'</span>'+t+'</div>').join('')+'</div></div>').join(''):'<div class="es">暂无项目</div>'}
function addPP(){const n=$('ppN').value.trim(),g=$('ppG').value.trim(),s=$('ppS').value,e=$('ppE').value,ts=$('ppT').value.split("\\n").filter(l=>l.trim());if(!n){alert('请填写项目名称');return}PP.push({name:n,goal:g,start:s||'未定',end:e||'未定',tasks:ts});rPP();['ppN','ppG','ppT'].forEach(id=>$(id).value='')}
function $(id){return document.getElementById(id)}rPP()'''))

tools.append(("task-manager","任务管理器","✅","任务列表管理",
'''<div class="cd"><h2>添加任务</h2>
<label>任务名称</label><input type="text" id="tkN" placeholder="任务名称">
<label>优先级</label><select id="tkP"><option value="high">高</option><option value="mid" selected>中</option><option value="low">低</option></select>
<label>截止日期</label><input type="date" id="tkD">
<div class="bg"><button onclick="addTK()">添加任务</button></div></div>
<div class="cd"><h2>任务列表</h2><div id="tkL" class="es">暂无任务</div></div>''',
'''let TK=JSON.parse(localStorage.getItem('tkList')||'[]');function rTK(){$('tkL').innerHTML=TK.length?TK.map((t,i)=>'<div class="li"><div style="flex:1;'+(t.done?'opacity:.5;text-decoration:line-through':'')+'"><div style="display:flex;align-items:center;gap:8px"><input type="checkbox" '+(t.done?'checked':'')+' onchange="TK['+i+'].done=this.checked;saveTK();rTK()"><span style="font-weight:600">'+t.name+'</span></div><div style="display:flex;gap:8px;margin-top:4px"><span class="tag '+(t.priority==='high'?'d':t.priority==='mid'?'w':'s')+'">'+{high:'高',mid:'中',low:'低'}[t.priority]+'</span>'+(t.deadline?'<span style="font-size:.8rem;color:var(--text2)">'+t.deadline+'</span>':'')+'</div></div><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="TK.splice('+i+',1);saveTK();rTK()">删除</button></div>').join(''):'<div class="es">暂无任务</div>'}
function addTK(){const n=$('tkN').value.trim(),p=$('tkP').value,d=$('tkD').value;if(!n){alert('请填写任务名称');return}TK.unshift({name:n,priority:p,deadline:d,done:false});saveTK();rTK();$('tkN').value=''}
function saveTK(){localStorage.setItem('tkList',JSON.stringify(TK))}
function $(id){return document.getElementById(id)}rTK()'''))

tools.append(("time-tracker","时间追踪器","⏱️","追踪时间花费",
'''<div class="cd"><h2>时间追踪</h2>
<label>活动名称</label><input type="text" id="ttN" placeholder="编码工作">
<label>类别</label><input type="text" id="ttC" placeholder="工作">
<div class="bg"><button id="ttB" onclick="togTT()">▶ 开始计时</button></div>
<p id="ttT" style="text-align:center;font-size:2rem;font-weight:700;margin:16px 0;font-variant-numeric:tabular-nums">00:00:00</p></div>
<div class="cd"><h2>今日记录</h2><div id="ttL" class="es">暂无记录</div></div>''',
'''let TT=[],running=false,ttInt=null,ttSec=0;function togTT(){if(running){running=false;clearInterval(ttInt);$('ttB').textContent='▶ 开始计时';$('ttB').classList.remove('dng');$('ttB').classList.add('');const n=$('ttN').value.trim()||'未命名活动',c=$('ttC').value.trim()||'未分类';TT.push({name:n,category:c,duration:ttSec});ttSec=0;upTT();rTT()}else{const n=$('ttN').value.trim();if(!n){alert('请输入活动名称');return}running=true;$('ttB').textContent='■ 停止';$('ttB').classList.add('dng');ttInt=setInterval(()=>{ttSec++;upTT()},1000)}}
function upTT(){const h=Math.floor(ttSec/3600),m=Math.floor(ttSec%3600/60),s=ttSec%60;$('ttT').textContent=(h<10?'0':'')+h+':'+(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function rTT(){$('ttL').innerHTML=TT.length?TT.map((t,i)=>'<div class="li"><span>'+t.name+' <span class="tag">'+t.category+'</span></span><span>'+formatSec(t.duration)+'</span></div>').join(''):'<div class="es">暂无记录</div>'}
function formatSec(s){const h=Math.floor(s/3600),m=Math.floor(s%3600/60);return h?h+'h'+m+'m':m+'m'+(s%60)+'s'}
function $(id){return document.getElementById(id)}rTT()'''))

tools.append(("pomodoro-pro","番茄钟Pro","🍅","专注番茄工作法",
'''<div class="cd" style="text-align:center">
<h2>番茄钟</h2>
<div style="margin:24px 0"><p id="ppT" style="font-size:3rem;font-weight:700;font-variant-numeric:tabular-nums">25:00</p><p id="ppS" style="color:var(--text2)">专注时间</p></div>
<div class="bg" style="justify-content:center"><button id="ppB" onclick="togPP()">▶ 开始</button><button class="sec" onclick="rstPP()">重置</button></div>
<div style="display:flex;justify-content:center;gap:12px;margin-top:16px">
<div style="text-align:center"><span style="font-size:1.5rem;font-weight:700;color:var(--accent)" id="ppSC">0</span><p style="font-size:.8rem;color:var(--text2)">番茄数</p></div>
<div style="text-align:center"><span style="font-size:1.5rem;font-weight:700;color:var(--success)" id="ppTT">0</span><p style="font-size:.8rem;color:var(--text2)">总分钟</p></div>
</div></div>
<div class="cd"><h2>今日完成</h2><div id="ppL" class="es">暂无番茄记录</div></div>''',
'''let ppRun=false,ppInt=null,ppSec=25*60,ppCnt=0,ppTotal=0,ppMode='work',ppLogs=[];
function togPP(){if(ppRun){ppRun=false;clearInterval(ppInt);$('ppB').textContent='▶ 继续'}else{ppRun=true;$('ppB').textContent='⏸ 暂停';ppInt=setInterval(()=>{ppSec--;if(ppSec<=0){ppRun=false;clearInterval(ppInt);if(ppMode==='work'){ppCnt++;ppTotal+=25;ppLogs.push({time:new Date().toLocaleTimeString('zh-CN'),dur:25});$('ppSC').textContent=ppCnt;$('ppTT').textContent=ppTotal;rPP();ppMode='break';ppSec=5*60;$('ppS').textContent='休息时间';alert('🍅 番茄完成！休息5分钟')}else{ppMode='work';ppSec=25*60;$('ppS').textContent='专注时间';$('ppB').textContent='▶ 开始'}}upPP()},1000)}}
function rstPP(){ppRun=false;clearInterval(ppInt);ppSec=25*60;ppMode='work';$('ppS').textContent='专注时间';$('ppB').textContent='▶ 开始';upPP()}
function upPP(){const m=Math.floor(ppSec/60),s=ppSec%60;$('ppT').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function rPP(){$('ppL').innerHTML=ppLogs.length?ppLogs.map(l=>'<div class="li"><span>'+l.time+'</span><span>🍅 '+l.dur+'分钟</span></div>').reverse().join(''):'<div class="es">暂无番茄记录</div>'}
function $(id){return document.getElementById(id)}rPP()'''))

tools.append(("focus-timer","专注计时器","🎯","自定义专注时间",
'''<div class="cd" style="text-align:center">
<h2>专注计时器</h2>
<label>专注时长(分钟)</label><input type="number" id="ftM" value="30" min="1" max="180">
<div style="margin:24px 0"><p id="ftT" style="font-size:3rem;font-weight:700;font-variant-numeric:tabular-nums">30:00</p></div>
<div class="bg" style="justify-content:center"><button id="ftB" onclick="togFT()">▶ 开始</button><button class="sec" onclick="rstFT()">重置</button></div></div>''',
'''let ftRun=false,ftInt=null,ftSec=30*60;
function togFT(){if(ftRun){ftRun=false;clearInterval(ftInt);$('ftB').textContent='▶ 继续'}else{ftSec=parseInt($('ftM').value)*60;if(!ftSec)return;ftRun=true;$('ftB').textContent='⏸ 暂停';ftInt=setInterval(()=>{ftSec--;if(ftSec<=0){ftRun=false;clearInterval(ftInt);$('ftB').textContent='▶ 开始';alert('🎯 专注完成！')}upFT()},1000)}}
function rstFT(){ftRun=false;clearInterval(ftInt);ftSec=parseInt($('ftM').value)*60;upFT();$('ftB').textContent='▶ 开始'}
function upFT(){const m=Math.floor(ftSec/60),s=ftSec%60;$('ftT').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s}
function $(id){return document.getElementById(id)}upFT()'''))

tools.append(("habit-tracker-pro","习惯追踪Pro","🔄","每日习惯追踪",
'''<div class="cd"><h2>添加习惯</h2>
<label>习惯名称</label><input type="text" id="hpN" placeholder="每日运动">
<label>频率</label><select id="hpF"><option value="daily">每天</option><option value="weekly">每周</option></select>
<div class="bg"><button onclick="addHP()">添加习惯</button></div></div>
<div class="cd"><h2>今日习惯</h2><div id="hpL" class="es">暂无习惯</div></div>''',
'''let HP=JSON.parse(localStorage.getItem('hpList')||'[]'),hpDate=new Date().toLocaleDateString();
function rHP(){if(HP.length&&HP[0].date!==hpDate){HP.forEach(h=>h.done=false);HP.forEach(h=>h.date=hpDate)}
$('hpL').innerHTML=HP.length?HP.map((h,i)=>'<div class="li"><div style="display:flex;align-items:center;gap:12px;flex:1;cursor:pointer" onclick="HP['+i+'].done=!HP['+i+'].done;saveHP();rHP()"><div style="width:32px;height:32px;border-radius:50%;border:2px solid '+(h.done?'var(--success)':'var(--border)')+';display:flex;align-items:center;justify-content:center;background:'+(h.done?'var(--success)':'transparent')+'">'+(h.done?'✓':'')+'</div><span style="'+(h.done?'text-decoration:line-through;opacity:.6':'')+'">'+h.name+'</span></div><span class="tag">'+(h.frequency==='daily'?'每天':'每周')+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="HP.splice('+i+',1);saveHP();rHP()">删除</button></div>').join(''):'<div class="es">暂无习惯</div>'}
function addHP(){const n=$('hpN').value.trim(),f=$('hpF').value;if(!n){alert('请填写习惯名称');return}HP.push({name:n,frequency:f,done:false,date:hpDate});saveHP();rHP();$('hpN').value=''}
function saveHP(){localStorage.setItem('hpList',JSON.stringify(HP))}
function $(id){return document.getElementById(id)}rHP()'''))

tools.append(("goal-tracker","目标追踪器","🎯","设定和追踪目标",
'''<div class="cd"><h2>设定目标</h2>
<label>目标名称</label><input type="text" id="gtN" placeholder="阅读20本书">
<label>目标类别</label><select id="gtC"><option>学习</option><option>工作</option><option>健康</option><option>财务</option><option>其他</option></select>
<label>截止日期</label><input type="date" id="gtD">
<label>当前进度 (0-100)</label><input type="number" id="gtP" value="0" min="0" max="100">
<div class="bg"><button onclick="addGT()">添加目标</button></div></div>
<div class="cd"><h2>目标列表</h2><div id="gtL" class="es">暂无目标</div></div>''',
'''let GT=[];function rGT(){$('gtL').innerHTML=GT.length?GT.map((g,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+g.name+'</span><div><span class="tag">'+g.category+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem;margin-left:4px" onclick="GT.splice('+i+',1);rGT()">删除</button></div></div><div class="pb" style="margin-top:8px"><div class="fl" style="width:'+g.progress+'%;background:'+(g.progress>=100?'var(--success)':'var(--accent)')+'"></div></div><div style="display:flex;justify-content:space-between;margin-top:4px"><span style="font-size:.8rem;color:var(--text2)">'+g.progress+'%</span><span style="font-size:.8rem;color:var(--text2)">'+g.deadline+'</span></div><div class="bg"><button class="sec" style="padding:4px 12px;font-size:.8rem" onclick="GT['+i+'].progress=Math.min(100,GT['+i+'].progress+10);rGT()">+10%</button><button class="sec" style="padding:4px 12px;font-size:.8rem" onclick="GT['+i+'].progress=Math.max(0,GT['+i+'].progress-10);rGT()">-10%</button></div></div>').join(''):'<div class="es">暂无目标</div>'}
function addGT(){const n=$('gtN').value.trim(),c=$('gtC').value,d=$('gtD').value,p=parseInt($('gtP').value)||0;if(!n){alert('请填写目标名称');return}GT.push({name:n,category:c,deadline:d||'未定',progress:p});rGT();$('gtN').value=''}
function $(id){return document.getElementById(id)}rGT()'''))

tools.append(("progress-tracker","进度追踪器","📊","项目进度可视化",
'''<div class="cd"><h2>添加进度项</h2>
<label>项目名称</label><input type="text" id="pgN" placeholder="项目名称">
<label>总任务数</label><input type="number" id="pgT" value="10" min="1">
<label>已完成</label><input type="number" id="pgD" value="0" min="0">
<div class="bg"><button onclick="addPG()">添加</button></div></div>
<div class="cd"><h2>进度看板</h2><div id="pgL" class="es">暂无项目</div></div>''',
'''let PG=[];function rPG(){$('pgL').innerHTML=PG.length?PG.map((p,i)=>{const pct=p.total?Math.round(p.done/p.total*100):0;return'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+p.name+'</span><span style="color:var(--text2)">'+p.done+'/'+p.total+'</span></div><div class="pb" style="margin-top:8px"><div class="fl" style="width:'+pct+'%;background:'+(pct>=100?'var(--success)':pct>=50?'var(--warn)':'var(--accent)')+'"></div></div><div style="display:flex;justify-content:space-between;margin-top:4px"><span style="font-size:.8rem">'+pct+'%</span><div><button class="sec" style="padding:2px 10px;font-size:.75rem" onclick="PG['+i+'].done=Math.min(PG['+i+'].total,PG['+i+'].done+1);rPG()">+1</button><button class="dng" style="padding:2px 10px;font-size:.75rem;margin-left:4px" onclick="PG.splice('+i+',1);rPG()">删除</button></div></div></div>'}).join(''):'<div class="es">暂无项目</div>'}
function addPG(){const n=$('pgN').value.trim(),t=parseInt($('pgT').value)||10,d=parseInt($('pgD').value)||0;if(!n){alert('请填写名称');return}PG.push({name:n,total:t,done:Math.min(d,t)});rPG();$('pgN').value=''}
function $(id){return document.getElementById(id)}rPG()'''))

tools.append(("budget-tracker","预算追踪器","💰","月度预算管理",
'''<div class="cd"><h2>设置预算</h2>
<label>月收入</label><input type="number" id="btI" placeholder="10000">
<button onclick="saveBT()">保存收入</button></div>
<div class="cd"><h2>添加支出</h2>
<label>类别</label><input type="text" id="btC" placeholder="餐饮">
<label>金额</label><input type="number" id="btA" placeholder="0">
<div class="bg"><button onclick="addBT()">添加支出</button></div></div>
<div class="cd"><h2>预算概览</h2><div id="btS"></div></div>
<div class="cd"><h2>支出明细</h2><div id="btL" class="es">暂无支出</div></div>''',
'''let btInc=0,btExp=JSON.parse(localStorage.getItem('btExp')||'[]');function saveBT(){btInc=parseInt($('btI').value)||0;localStorage.setItem('btInc',btInc);rBT()}
function rBT(){const total=btExp.reduce((s,e)=>s+e.amount,0);const remain=btInc-total;$('btS').innerHTML='<div class="gr"><div class="st"><div class="nm">'+btInc.toLocaleString()+'</div><div class="lb">月收入</div></div><div class="st"><div class="nm" style="color:var(--danger)">'+total.toLocaleString()+'</div><div class="lb">总支出</div></div><div class="st"><div class="nm" style="color:'+(remain>=0?'var(--success)':'var(--danger)')+'">'+remain.toLocaleString()+'</div><div class="lb">结余</div></div></div>';$('btL').innerHTML=btExp.length?btExp.map((e,i)=>'<div class="li"><span>'+e.category+'</span><span style="color:var(--danger)">-'+e.amount.toLocaleString()+'元</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="btExp.splice('+i+',1);localStorage.setItem(\\'btExp\\',JSON.stringify(btExp));rBT()">删除</button></div>').reverse().join(''):'<div class="es">暂无支出</div>'}
function addBT(){const c=$('btC').value.trim(),a=parseInt($('btA').value)||0;if(!c||a<=0){alert('请填写类别和金额');return}btExp.push({category:c,amount:a});localStorage.setItem('btExp',JSON.stringify(btExp));rBT();$('btC').value='';$('btA').value=''}
function $(id){return document.getElementById(id)}btInc=parseInt(localStorage.getItem('btInc'))||0;$('btI').value=btInc;rBT()'''))

tools.append(("expense-tracker-pro","支出追踪Pro","💸","详细支出记录",
'''<div class="cd"><h2>记录支出</h2>
<label>金额</label><input type="number" id="epA" placeholder="金额">
<label>类别</label><select id="epC"><option>餐饮</option><option>交通</option><option>购物</option><option>娱乐</option><option>居住</option><option>医疗</option><option>教育</option><option>其他</option></select>
<label>备注</label><input type="text" id="epN" placeholder="备注">
<div class="bg"><button onclick="addEP()">记录支出</button></div></div>
<div class="cd"><h2>本月统计</h2><div id="epS"></div></div>
<div class="cd"><h2>支出明细</h2><div id="epL" class="es">暂无记录</div></div>''',
'''let EP=JSON.parse(localStorage.getItem('epList')||'[]');function rEP(){const total=EP.reduce((s,e)=>s+e.amount,0);const cats={};EP.forEach(e=>{cats[e.category]=(cats[e.category]||0)+e.amount});$('epS').innerHTML='<div class="gr" style="margin-bottom:12px"><div class="st"><div class="nm" style="color:var(--danger)">'+total.toLocaleString()+'</div><div class="lb">总支出</div></div><div class="st"><div class="nm">'+EP.length+'</div><div class="lb">笔数</div></div></div><div style="display:flex;flex-wrap:wrap;gap:8px">'+Object.entries(cats).map(([k,v])=>'<span class="tag">'+k+': '+v+'</span>').join('')+'</div>';$('epL').innerHTML=EP.length?EP.map((e,i)=>'<div class="li"><div><span class="tag">'+e.category+'</span> '+(e.note||'无备注')+'</div><span style="color:var(--danger)">-'+e.amount+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="EP.splice('+i+',1);localStorage.setItem(\\'epList\\',JSON.stringify(EP));rEP()">×</button></div>').reverse().join(''):'<div class="es">暂无记录</div>'}
function addEP(){const a=parseInt($('epA').value)||0,c=$('epC').value,n=$('epN').value.trim();if(a<=0){alert('请输入金额');return}EP.push({amount:a,category:c,note:n,date:new Date().toLocaleDateString()});localStorage.setItem('epList',JSON.stringify(EP));rEP();$('epA').value='';$('epN').value=''}
function $(id){return document.getElementById(id)}rEP()'''))

tools.append(("income-tracker","收入追踪器","💵","收入记录管理",
'''<div class="cd"><h2>记录收入</h2>
<label>金额</label><input type="number" id="icA" placeholder="金额">
<label>来源</label><select id="icS"><option>工资</option><option>奖金</option><option>兼职</option><option>投资</option><option>其他</option></select>
<label>备注</label><input type="text" id="icN" placeholder="备注">
<div class="bg"><button onclick="addIC()">记录收入</button></div></div>
<div class="cd"><h2>统计</h2><div id="icSt"></div></div>
<div class="cd"><h2>收入明细</h2><div id="icL" class="es">暂无记录</div></div>''',
'''let IC=JSON.parse(localStorage.getItem('icList')||'[]');function rIC(){const total=IC.reduce((s,e)=>s+e.amount,0);const srcs={};IC.forEach(e=>{srcs[e.source]=(srcs[e.source]||0)+e.amount});$('icSt').innerHTML='<div class="gr"><div class="st"><div class="nm" style="color:var(--success)">'+total.toLocaleString()+'</div><div class="lb">总收入</div></div><div class="st"><div class="nm">'+IC.length+'</div><div class="lb">笔数</div></div></div>';$('icL').innerHTML=IC.length?IC.map((e,i)=>'<div class="li"><div><span class="tag s">'+e.source+'</span> '+(e.note||'')+'</div><span style="color:var(--success)">+'+e.amount+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="IC.splice('+i+',1);localStorage.setItem(\\'icList\\',JSON.stringify(IC));rIC()">×</button></div>').reverse().join(''):'<div class="es">暂无记录</div>'}
function addIC(){const a=parseInt($('icA').value)||0,s=$('icS').value,n=$('icN').value.trim();if(a<=0){alert('请输入金额');return}IC.push({amount:a,source:s,note:n,date:new Date().toLocaleDateString()});localStorage.setItem('icList',JSON.stringify(IC));rIC();$('icA').value='';$('icN').value=''}
function $(id){return document.getElementById(id)}rIC()'''))

tools.append(("investment-tracker","投资追踪器","📈","投资组合管理",
'''<div class="cd"><h2>记录投资</h2>
<label>投资名称</label><input type="text" id="ivN" placeholder="沪深300ETF">
<label>买入价格</label><input type="number" id="ivB" placeholder="买入价">
<label>当前价格</label><input type="number" id="ivP" placeholder="当前价">
<label>持有数量</label><input type="number" id="ivQ" placeholder="数量">
<div class="bg"><button onclick="addIV()">添加投资</button></div></div>
<div class="cd"><h2>投资概览</h2><div id="ivS"></div></div>
<div class="cd"><h2>持仓列表</h2><div id="ivL" class="es">暂无投资</div></div>''',
'''let IV=JSON.parse(localStorage.getItem('ivList')||'[]');function rIV(){let totalCost=0,totalVal=0;const rows=IV.map((v,i)=>{const cost=v.buy*v.qty,val=v.cur*v.qty;totalCost+=cost;totalVal+=val;const pnl=val-cost;const pct=cost?Math.round(pnl/cost*100):0;return{...v,cost,val,pnl,pct}});const totalPnl=totalVal-totalCost;const totalPct=totalCost?Math.round(totalPnl/totalCost*100):0;$('ivS').innerHTML='<div class="gr"><div class="st"><div class="nm">'+totalVal.toLocaleString()+'</div><div class="lb">当前市值</div></div><div class="st"><div class="nm" style="color:'+(totalPnl>=0?'var(--success)':'var(--danger)')+'">'+(totalPnl>=0?'+':'')+totalPnl.toLocaleString()+'</div><div class="lb">盈亏</div></div><div class="st"><div class="nm" style="color:'+(totalPct>=0?'var(--success)':'var(--danger)')+'">'+(totalPct>=0?'+':'')+totalPct+'%</div><div class="lb">收益率</div></div></div>';$('ivL').innerHTML=rows.length?rows.map((r,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+r.name+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="IV.splice('+i+',1);localStorage.setItem(\\'ivList\\',JSON.stringify(IV));rIV()">删除</button></div><div style="display:flex;justify-content:space-between;margin-top:4px;font-size:.85rem"><span>成本: '+r.cost.toLocaleString()+' | 市值: '+r.val.toLocaleString()+'</span><span style="color:'+(r.pnl>=0?'var(--success)':'var(--danger)')+'">'+(r.pnl>=0?'+':'')+r.pnl+' ('+r.pct+'%)</span></div></div>').join(''):'<div class="es">暂无投资</div>'}
function addIV(){const n=$('ivN').value.trim(),b=parseFloat($('ivB').value)||0,p=parseFloat($('ivP').value)||0,q=parseInt($('ivQ').value)||0;if(!n||!q){alert('请填写完整信息');return}IV.push({name:n,buy:b,cur:p,qty:q});localStorage.setItem('ivList',JSON.stringify(IV));rIV();['ivN','ivB','ivP','ivQ'].forEach(id=>$(id).value='')}
function $(id){return document.getElementById(id)}rIV()'''))

tools.append(("portfolio-tracker","投资组合追踪器","💼","综合投资追踪",
'''<div class="cd"><h2>添加资产</h2>
<label>资产名称</label><input type="text" id="ptN" placeholder="资产名称">
<label>资产类型</label><select id="ptT"><option>股票</option><option>基金</option><option>债券</option><option>房产</option><option>现金</option><option>其他</option></select>
<label>当前价值</label><input type="number" id="ptV" placeholder="价值">
<div class="bg"><button onclick="addPT()">添加资产</button></div></div>
<div class="cd"><h2>资产配置</h2><div id="ptC"></div></div>
<div class="cd"><h2>资产列表</h2><div id="ptL" class="es">暂无资产</div></div>''',
'''let PT=JSON.parse(localStorage.getItem('ptList')||'[]');function rPT(){const total=PT.reduce((s,p)=>s+p.value,0);const types={};PT.forEach(p=>{types[p.type]=(types[p.type]||0)+p.value});const colors={股票:'var(--accent)',基金:'var(--success)',债券:'var(--warn)',房产:'#8b5cf6',现金:'#06b6d4',其他:'var(--danger)'};$('ptC').innerHTML='<div class="gr"><div class="st"><div class="nm">'+total.toLocaleString()+'</div><div class="lb">总资产</div></div><div class="st"><div class="nm">'+PT.length+'</div><div class="lb">资产数</div></div></div><div style="margin-top:12px">'+Object.entries(types).map(([k,v])=>'<div style="display:flex;align-items:center;gap:8px;margin:4px 0"><span style="width:12px;height:12px;border-radius:50%;background:'+(colors[k]||'var(--accent)')+'"></span><span style="flex:1;font-size:.9rem">'+k+'</span><span style="font-size:.85rem">'+v.toLocaleString()+' ('+Math.round(v/total*100)+'%)</span></div>').join('')+'</div>';$('ptL').innerHTML=PT.length?PT.map((p,i)=>'<div class="li"><div><span class="tag">'+p.type+'</span> '+p.name+'</div><span>'+p.value.toLocaleString()+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="PT.splice('+i+',1);localStorage.setItem(\\'ptList\\',JSON.stringify(PT));rPT()">删除</button></div>').join(''):'<div class="es">暂无资产</div>'}
function addPT(){const n=$('ptN').value.trim(),t=$('ptT').value,v=parseInt($('ptV').value)||0;if(!n||v<=0){alert('请填写完整信息');return}PT.push({name:n,type:t,value:v});localStorage.setItem('ptList',JSON.stringify(PT));rPT();$('ptN').value='';$('ptV').value=''}
function $(id){return document.getElementById(id)}rPT()'''))

tools.append(("stock-tracker","股票追踪器","📊","自选股追踪",
'''<div class="cd"><h2>添加自选</h2>
<label>股票代码</label><input type="text" id="stC" placeholder="600519">
<label>股票名称</label><input type="text" id="stN" placeholder="贵州茅台">
<label>买入价格</label><input type="number" id="stB" placeholder="买入价">
<label>当前价格</label><input type="number" id="stP" placeholder="现价">
<label>持有数量</label><input type="number" id="stQ" value="100">
<div class="bg"><button onclick="addST()">添加</button></div></div>
<div class="cd"><h2>自选股</h2><div id="stL" class="es">暂无股票</div></div>''',
'''let ST=JSON.parse(localStorage.getItem('stList')||'[]');function rST(){$('stL').innerHTML=ST.length?ST.map((s,i)=>{const pnl=(s.cur-s.buy)*s.qty;const pct=s.buy?Math.round((s.cur-s.buy)/s.buy*100):0;return'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><div><span class="tag">'+s.code+'</span> <span style="font-weight:600">'+s.name+'</span></div><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="ST.splice('+i+',1);localStorage.setItem(\\'stList\\',JSON.stringify(ST));rST()">删除</button></div><div style="display:flex;justify-content:space-between;margin-top:4px;font-size:.85rem"><span>买入: '+s.buy+' | 现价: '+s.cur+' | 数量: '+s.qty+'</span><span style="color:'+(pnl>=0?'var(--success)':'var(--danger)')+'">'+(pnl>=0?'+':'')+pnl.toFixed(0)+' ('+pct+'%)</span></div></div>'}).join(''):'<div class="es">暂无股票</div>'}
function addST(){const c=$('stC').value.trim(),n=$('stN').value.trim(),b=parseFloat($('stB').value)||0,p=parseFloat($('stP').value)||0,q=parseInt($('stQ').value)||0;if(!c||!n){alert('请填写股票信息');return}ST.push({code:c,name:n,buy:b,cur:p,qty:q});localStorage.setItem('stList',JSON.stringify(ST));rST();['stC','stN','stB','stP'].forEach(id=>$(id).value='')}
function $(id){return document.getElementById(id)}rST()'''))

tools.append(("crypto-tracker-pro","加密货币追踪Pro","₿","加密货币追踪",
'''<div class="cd"><h2>添加币种</h2>
<label>币种</label><select id="ctC"><option>BTC 比特币</option><option>ETH 以太坊</option><option>SOL</option><option>DOGE</option><option>其他</option></select>
<label>买入价格(USDT)</label><input type="number" id="ctB" placeholder="买入价">
<label>当前价格(USDT)</label><input type="number" id="ctP" placeholder="现价">
<label>持有数量</label><input type="number" id="ctQ" step="0.0001" placeholder="数量">
<div class="bg"><button onclick="addCT()">添加</button></div></div>
<div class="cd"><h2>持仓概览</h2><div id="ctS"></div></div>
<div class="cd"><h2>持仓列表</h2><div id="ctL" class="es">暂无持仓</div></div>''',
'''let CT=JSON.parse(localStorage.getItem('ctList')||'[]');function rCT(){let totalCost=0,totalVal=0;CT.forEach(c=>{totalCost+=c.buy*c.qty;totalVal+=c.cur*c.qty});const pnl=totalVal-totalCost;$('ctS').innerHTML='<div class="gr"><div class="st"><div class="nm">'+totalVal.toFixed(2)+'</div><div class="lb">总价值(USDT)</div></div><div class="st"><div class="nm" style="color:'+(pnl>=0?'var(--success)':'var(--danger)')+'">'+(pnl>=0?'+':'')+pnl.toFixed(2)+'</div><div class="lb">盈亏</div></div></div>';$('ctL').innerHTML=CT.length?CT.map((c,i)=>{const pnl=(c.cur-c.buy)*c.qty;const pct=c.buy?Math.round((c.cur-c.buy)/c.buy*100):0;return'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+c.coin+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="CT.splice('+i+',1);localStorage.setItem(\\'ctList\\',JSON.stringify(CT));rCT()">删除</button></div><div style="display:flex;justify-content:space-between;margin-top:4px;font-size:.85rem"><span>买入: '+c.buy+' | 现价: '+c.cur+' | 数量: '+c.qty+'</span><span style="color:'+(pnl>=0?'var(--success)':'var(--danger)')+'">'+(pnl>=0?'+':'')+pnl.toFixed(2)+' ('+pct+'%)</span></div></div>'}).join(''):'<div class="es">暂无持仓</div>'}
function addCT(){const coin=$('ctC').value.split(' ')[0],b=parseFloat($('ctB').value)||0,p=parseFloat($('ctP').value)||0,q=parseFloat($('ctQ').value)||0;if(!q){alert('请填写数量');return}CT.push({coin,buy:b,cur:p,qty:q});localStorage.setItem('ctList',JSON.stringify(CT));rCT();$('ctB').value='';$('ctP').value='';$('ctQ').value=''}
function $(id){return document.getElementById(id)}rCT()'''))

tools.append(("forex-tracker","外汇追踪器","💱","外汇汇率追踪",
'''<div class="cd"><h2>汇率查询</h2>
<label>货币对</label><select id="fxP"><option>USD/CNY</option><option>EUR/CNY</option><option>GBP/CNY</option><option>JPY/CNY</option><option>EUR/USD</option><option>GBP/USD</option></select>
<label>金额</label><input type="number" id="fxA" value="1000" placeholder="金额">
<label>汇率</label><input type="number" id="fxR" step="0.0001" placeholder="当前汇率">
<button onclick="calcFX()">计算</button></div>
<div class="cd" id="fxRC" style="display:none"><h2>换算结果</h2><div id="fxRA"></div></div>''',
'''function calcFX(){const pair=$('fxP').value,amt=parseFloat($('fxA').value)||0,rate=parseFloat($('fxR').value)||0;if(!rate){alert('请输入汇率');return}const result=(amt*rate).toFixed(2);const [from,to]=pair.split('/');$('fxRC').style.display='';$('fxRA').innerHTML='<div class="gr"><div class="st"><div class="nm">'+amt.toLocaleString()+'</div><div class="lb">'+from+'</div></div><div class="st"><div class="nm" style="font-size:1.2rem">≈</div><div class="lb"></div></div><div class="st"><div class="nm" style="color:var(--success)">'+parseFloat(result).toLocaleString()+'</div><div class="lb">'+to+'</div></div></div><p style="text-align:center;color:var(--text2);margin-top:8px">汇率: 1 '+from+' = '+rate+' '+to+'</p>'}
function $(id){return document.getElementById(id)}'''))

for slug,title,icon,desc,body,js in [
    ("gold-tracker","黄金追踪器","🥇","黄金价格追踪",
     '<div class="cd"><h2>黄金记录</h2><label>买入价格(元/克)</label><input type="number" id="gdB" placeholder="买入价"><label>当前价格(元/克)</label><input type="number" id="gdP" placeholder="现价"><label>持有克数</label><input type="number" id="gdQ" placeholder="克数"><div class="bg"><button onclick="addGD()">添加</button></div></div><div class="cd"><h2>持仓概览</h2><div id="gdS"></div></div><div class="cd"><h2>记录</h2><div id="gdL" class="es">暂无记录</div></div>',
     'let GD=JSON.parse(localStorage.getItem("gdList")||"[]");function rGD(){let tc=0,tv=0;GD.forEach(g=>{tc+=g.buy*g.qty;tv+=g.cur*g.qty});const pnl=tv-tc;document.getElementById("gdS").innerHTML=\'<div class="gr"><div class="st"><div class="nm">"+tv.toFixed(0)+"</div><div class="lb">当前价值(元)</div></div><div class="st"><div class="nm" style="color:"+(pnl>=0?"var(--success)":"var(--danger)")+">"+(pnl>=0?"+":"")+pnl.toFixed(0)+"</div><div class="lb">盈亏</div></div></div>\';document.getElementById("gdL").innerHTML=GD.length?GD.map((g,i)=>{const p=(g.cur-g.buy)*g.qty,pct=g.buy?Math.round((g.cur-g.buy)/g.buy*100):0;return\'<div class="li"><div><span style="font-weight:600">"+g.buy+"元/克 × "+g.qty+"克</span><br><span style="font-size:.8rem;color:var(--text2)">现价: "+g.cur+"元/克</span></div><span style="color:"+(p>=0?"var(--success)":"var(--danger)")+">"+(p>=0?"+":"")+p.toFixed(0)+" ("+pct+"%)</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="GD.splice("+i+",1);localStorage.setItem(\"gdList\",JSON.stringify(GD));rGD()">删除</button></div>\').join(""):\'<div class="es">暂无记录</div>\'}function addGD(){const b=parseFloat(document.getElementById("gdB").value)||0,p=parseFloat(document.getElementById("gdP").value)||0,q=parseFloat(document.getElementById("gdQ").value)||0;if(!q){alert("请填写克数");return}GD.push({buy:b,cur:p,qty:q});localStorage.setItem("gdList",JSON.stringify(GD));rGD();document.getElementById("gdB").value="";document.getElementById("gdP").value="";document.getElementById("gdQ").value=""}rGD()'),
    ("silver-tracker","白银追踪器","🥈","白银价格追踪",
     '<div class="cd"><h2>白银记录</h2><label>买入价格(元/克)</label><input type="number" id="svB"><label>当前价格(元/克)</label><input type="number" id="svP"><label>持有克数</label><input type="number" id="svQ"><div class="bg"><button onclick="addSV()">添加</button></div></div><div class="cd"><h2>持仓概览</h2><div id="svS"></div></div><div class="cd"><h2>记录</h2><div id="svL" class="es">暂无记录</div></div>',
     'let SV=JSON.parse(localStorage.getItem("svList")||"[]");function rSV(){let tc=0,tv=0;SV.forEach(s=>{tc+=s.buy*s.qty;tv+=s.cur*s.qty});const pnl=tv-tc;document.getElementById("svS").innerHTML=\'<div class="gr"><div class="st"><div class="nm">"+tv.toFixed(0)+"</div><div class="lb">当前价值(元)</div></div><div class="st"><div class="nm" style="color:"+(pnl>=0?"var(--success)":"var(--danger)")+">"+(pnl>=0?"+":"")+pnl.toFixed(0)+"</div><div class="lb">盈亏</div></div></div>\';document.getElementById("svL").innerHTML=SV.length?SV.map((s,i)=>{const p=(s.cur-s.buy)*s.qty,pct=s.buy?Math.round((s.cur-s.buy)/s.buy*100):0;return\'<div class="li"><div><span style="font-weight:600">"+s.buy+"元/克 × "+s.qty+"克</span><br><span style="font-size:.8rem;color:var(--text2)">现价: "+s.cur+"元/克</span></div><span style="color:"+(p>=0?"var(--success)":"var(--danger)")+">"+(p>=0?"+":"")+p.toFixed(0)+" ("+pct+"%)</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="SV.splice("+i+",1);localStorage.setItem(\"svList\",JSON.stringify(SV));rSV()">删除</button></div>\').join(""):\'<div class="es">暂无记录</div>\'}function addSV(){const b=parseFloat(document.getElementById("svB").value)||0,p=parseFloat(document.getElementById("svP").value)||0,q=parseFloat(document.getElementById("svQ").value)||0;if(!q){alert("请填写克数");return}SV.push({buy:b,cur:p,qty:q});localStorage.setItem("svList",JSON.stringify(SV));rSV();["svB","svP","svQ"].forEach(id=>document.getElementById(id).value="")}rSV()'),
]:
    w(slug, title, icon, desc, body, js)

print(f"\nBatch 2 done: {len(tools)} tools")
for s, t, i, d, b, j in tools:
    w(s, t, i, d, b, j)
print(f"Batch 2 total written: {len(tools)}")
