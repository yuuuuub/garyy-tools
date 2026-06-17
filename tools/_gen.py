#!/usr/bin/env python3
"""批量生成154个工具"""
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

# ===== 工具定义 =====
# 每个工具: (slug, title, icon, desc, body_html, js_code)
# body用 {i} 占位, js用 {i} 占位

tools = []

# --- 教育类 ---
tools.append(("quiz-builder","问答构建器","📝","创建自定义问答题库，支持多选题",
'''<div class="cd" id="cC"><h2>创建问题</h2>
<label>问题</label><textarea id="qT" placeholder="输入问题"></textarea>
<label>选项A</label><input type="text" id="oA">
<label>选项B</label><input type="text" id="oB">
<label>选项C</label><input type="text" id="oC">
<label>选项D</label><input type="text" id="oD">
<label>正确答案</label><select id="cA"><option>A</option><option>B</option><option>C</option><option>D</option></select>
<div class="bg"><button onclick="addQ()">添加问题</button><button class="sec" onclick="startQ()" id="sB" style="display:none">开始测验</button></div></div>
<div class="cd" id="qA" style="display:none"><h2 id="qTi">问题 1/1</h2><p id="qQ" style="font-size:1.1rem;margin:16px 0"></p><div id="qO"></div>
<div id="qR" class="hidden" style="margin-top:16px;text-align:center"></div>
<div class="bg"><button id="nB" class="hidden" onclick="nextQ()">下一题</button><button id="fB" class="hidden" onclick="showR()">查看结果</button></div></div>
<div class="cd" id="rC" style="display:none"><h2>测验结果</h2><div id="rA"></div><div class="bg"><button onclick="resetQ()">重新开始</button></div></div>
<div class="cd"><h2>题库 (<span id="qCt">0</span>题)</h2><div id="qL" class="es">暂无问题</div></div>''',
'''let Q=[],cQ=0,sc=0,an=[];
function addQ(){const t=$('qT').value.trim(),a=$('oA').value.trim(),b=$('oB').value.trim(),c=$('oC').value.trim()||'(空)',d=$('oD').value.trim()||'(空)',co=$('cA').value;if(!t||!a||!b){alert('请填写问题和选项');return}Q.push({t,o:{A:a,B:b,C:c,D:d},c:co});$('qCt').textContent=Q.length;$('sB').style.display='';rL();['qT','oA','oB','oC','oD'].forEach(id=>$(id).value='')}
function rL(){const e=$('qL');if(!Q.length){e.innerHTML='<div class="es">暂无问题</div>';return}e.innerHTML=Q.map((q,i)=>'<div class="li"><span>'+(i+1)+'. '+q.t.substring(0,40)+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="Q.splice('+i+',1);$(\\'qCt\\').textContent=Q.length;rL()">删除</button></div>').join('')}
function startQ(){if(!Q.length)return;cQ=0;sc=0;an=[];$('cC').style.display='none';$('qA').style.display='';shQ()}
function shQ(){const q=Q[cQ];$('qTi').textContent='问题 '+(cQ+1)+'/'+Q.length;$('qQ').textContent=q.t;$('qR').classList.add('hidden');$('nB').classList.add('hidden');$('fB').classList.add('hidden');const os=Object.entries(q.o).filter(([,v])=>v!=='(空)');$('qO').innerHTML=os.map(([k,v])=>'<div class="li" style="cursor:pointer;border:1px solid var(--border);border-radius:8px;margin-bottom:8px;padding:12px" onclick="selA(\\''+k+'\\')">'+k+'. '+v+'</div>').join('')}
function selA(a){const q=Q[cQ];an.push(a);if(a===q.c)sc++;const os=$('qO').children;for(let o of os){o.style.pointerEvents='none';if(o.textContent.startsWith(q.c+'.'))o.style.borderColor='var(--success)'}const r=$('qR');r.textContent=a===q.c?'✓ 正确！':'✗ 错误，正确答案是 '+q.c;r.style.color=a===q.c?'var(--success)':'var(--danger)';r.classList.remove('hidden');if(cQ<Q.length-1)$('nB').classList.remove('hidden');else $('fB').classList.remove('hidden')}
function nextQ(){cQ++;shQ()}
function showR(){$('qA').style.display='none';$('rC').style.display='';const p=Math.round(sc/Q.length*100);$('rA').innerHTML='<div class="gr" style="margin:16px 0"><div class="st"><div class="nm">'+sc+'/'+Q.length+'</div><div class="lb">正确数</div></div><div class="st"><div class="nm">'+p+'%</div><div class="lb">正确率</div></div></div><p style="text-align:center;color:var(--text2)">'+(p>=80?'🎉 优秀！':p>=60?'👍 不错！':'📚 继续努力！')+'</p>'}
function resetQ(){$('rC').style.display='none';$('cC').style.display=''}
function $(id){return document.getElementById(id)}'''))

tools.append(("flashcard-builder","闪卡构建器","🃏","学习闪卡，点击翻转查看答案",
'''<div class="cd"><h2>创建闪卡</h2>
<label>正面（问题/术语）</label><textarea id="fT" placeholder="输入正面内容"></textarea>
<label>背面（答案/释义）</label><textarea id="bT" placeholder="输入背面内容"></textarea>
<div class="bg"><button onclick="addFC()">添加闪卡</button><button class="sec" onclick="startFC()" id="sBF" style="display:none">开始学习</button></div></div>
<div class="cd"><h2>闪卡列表 (<span id="fcC">0</span>张)</h2><div id="fcL" class="es">暂无闪卡</div></div>
<div id="sA" style="display:none">
<div class="cd" style="text-align:center;cursor:pointer;min-height:200px;display:flex;align-items:center;justify-content:center" id="fC" onclick="flipFC()"><p id="fCt" style="font-size:1.3rem;line-height:1.8"></p></div>
<p style="text-align:center;color:var(--text2);margin:8px 0" id="fH">点击卡片翻转</p>
<div style="text-align:center;color:var(--text2);margin-bottom:12px" id="fP">1/1</div>
<div class="bg" style="justify-content:center"><button class="sec" onclick="prevFC()">← 上一张</button><button onclick="nextFC()">下一张 →</button><button class="dng" style="padding:6px 12px" onclick="delFC()">删除</button></div></div>''',
'''let FC=[],cFC=0,fl=false;
function addFC(){const f=$('fT').value.trim(),b=$('bT').value.trim();if(!f||!b){alert('请填写正面和背面');return}FC.push({f,b});$('fcC').textContent=FC.length;$('sBF').style.display='';rFC();$('fT').value='';$('bT').value=''}
function rFC(){const e=$('fcL');if(!FC.length){e.innerHTML='<div class="es">暂无闪卡</div>';return}e.innerHTML=FC.map((c,i)=>'<div class="li"><span>'+(i+1)+'. '+c.f.substring(0,30)+' → '+c.b.substring(0,20)+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="FC.splice('+i+',1);$(\\'fcC\\').textContent=FC.length;rFC()">删除</button></div>').join('')}
function startFC(){if(!FC.length)return;cFC=0;fl=false;$('sA').style.display='';shFC()}
function shFC(){const c=FC[cFC];$('fCt').textContent=c.f;$('fP').textContent=(cFC+1)+'/'+FC.length;$('fH').textContent='点击卡片翻转';$('fC').style.background='var(--bg)';fl=false}
function flipFC(){fl=!fl;const c=FC[cFC];$('fCt').textContent=fl?c.b:c.f;$('fH').textContent=fl?'显示正面':'点击查看答案';$('fC').style.background=fl?'#1a2332':'var(--bg)'}
function nextFC(){if(cFC<FC.length-1){cFC++;shFC()}}
function prevFC(){if(cFC>0){cFC--;shFC()}}
function delFC(){FC.splice(cFC,1);if(!FC.length){$('sA').style.display='none';$('fcC').textContent=0;rFC();$('sBF').style.display='none';return}if(cFC>=FC.length)cFC=FC.length-1;shFC();$('fcC').textContent=FC.length;rFC()}
function $(id){return document.getElementById(id)}'''))

tools.append(("mindmap-builder","思维导图构建器","🧠","文本格式思维导图",
'''<div class="cd"><h2>创建思维导图</h2>
<label>中心主题</label><input type="text" id="mT" placeholder="输入中心主题">
<label>子主题（每行一个，缩进表示层级：两空格=二级，四空格=三级）</label>
<textarea id="mS" rows="8" placeholder="主题A&#10;  子主题A1&#10;    三级主题A1a&#10;  子主题A2&#10;主题B&#10;  子主题B1"></textarea>
<button onclick="bMM()">生成导图</button></div>
<div class="cd" id="mMC" style="display:none"><h2>思维导图</h2><div id="mM"></div></div>''',
'''function bMM(){const t=$('mT').value.trim();if(!t){alert('请输入中心主题');return}const lines=$('mS').value.split("\\n").filter(l=>l.trim());$('mMC').style.display='';function pL(lines){const r=[];let i=0;while(i<lines.length){const l=lines[i],ind=l.search(/\\S/),txt=l.trim(),lv=Math.floor(ind/2),nd={t:txt,c:[]};i++;while(i<lines.length){const nl=lines[i],ni=nl.search(/\\S/),nlv=Math.floor(ni/2);if(nlv>lv){nd.c.push(...pL([nl]));i++}else break}r.push(nd)}return r}function rN(n,d=0){let h='<div style="margin-left:'+(d*24)+'px;padding:8px 12px;margin:4px 0;border-radius:8px;background:'+(d===0?'var(--accent)':'var(--bg)')+';color:'+(d===0?'#fff':'var(--text)')+';font-weight:'+(d===0?'700':'400')+';font-size:'+Math.max(.85,1.1-d*.1)+'rem;border-left:3px solid '+['var(--accent)','var(--success)','var(--warn)','var(--danger)'][d%4]+'">'+n.t+'</div>';n.c.forEach(c=>{h+=rN(c,d+1)});return h}const tree=pL(lines);let html='<div style="padding:12px;background:var(--accent);color:#fff;border-radius:12px;text-align:center;font-size:1.2rem;font-weight:700;margin-bottom:16px">'+t+'</div>';tree.forEach(n=>{html+=rN(n,1)});$('mM').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("flowchart-builder","流程图构建器","🔀","文本流程图",
'''<div class="cd"><h2>创建流程图</h2>
<label>流程步骤（使用 → 连接）</label>
<textarea id="fSt" rows="6" placeholder="开始 → 处理数据 → 分析结果 → 输出报告 → 结束"></textarea>
<button onclick="bFL()">生成流程图</button></div>
<div class="cd" id="fLC" style="display:none"><h2>流程图</h2><div id="fL"></div></div>''',
'''function bFL(){const raw=$('fSt').value.trim();if(!raw){alert('请输入流程步骤');return}const steps=raw.split(/[→➜>]+/).map(s=>s.trim()).filter(Boolean);$('fLC').style.display='';let html='<div style="display:flex;align-items:center;gap:0;flex-wrap:wrap;justify-content:center;padding:16px 0">';steps.forEach((s,i)=>{const f=i===0,l=i===steps.length-1,bg=f?'var(--success)':l?'var(--danger)':'var(--accent)',sh=f||l?'border-radius:24px':'border-radius:8px';html+='<div style="background:'+bg+';color:#fff;padding:14px 24px;'+sh+';text-align:center;font-weight:600;min-width:100px;box-shadow:0 2px 8px rgba(0,0,0,.3)">'+s+'</div>';if(i<steps.length-1)html+='<div style="color:var(--text2);font-size:1.5rem;padding:0 8px">→</div>'});html+='</div>';const ls=steps.map((s,i)=>'<div class="li"><span class="tag">'+(i+1)+'</span>'+s+'</div>').join('');$('fL').innerHTML=html+'<div style="margin-top:16px">'+ls+'</div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("diagram-builder","图表构建器","📈","柱状图可视化",
'''<div class="cd"><h2>创建图表</h2>
<label>标题</label><input type="text" id="dT" placeholder="图表标题">
<label>数据（标签:值，每行一个）</label><textarea id="dD" rows="6" placeholder="一月:120\n二月:200\n三月:150\n四月:180"></textarea>
<button onclick="dCH()">生成图表</button></div>
<div class="cd" id="dCC" style="display:none"><h2 id="dTi"></h2><div id="dC"></div></div>''',
'''function dCH(){const t=$('dT').value||'图表';const lines=$('dD').value.split("\\n").filter(l=>l.trim());const items=lines.map(l=>{const[k,v]=l.split(":");return{l:k.trim(),v:parseFloat(v)||0}});if(!items.length){alert('请输入数据');return}$('dCC').style.display='';$('dTi').textContent=t;const mx=Math.max(...items.map(i=>i.v));let html='<div style="display:flex;align-items:flex-end;gap:8px;height:200px;padding:16px 0">';items.forEach(it=>{const h=mx?it.v/mx*180:0;html+='<div style="flex:1;display:flex;flex-direction:column;align-items:center"><span style="font-size:.75rem;color:var(--text2)">'+it.v+'</span><div style="width:100%;background:var(--accent);border-radius:4px 4px 0 0;height:'+h+'px;min-height:4px"></div><span style="font-size:.7rem;color:var(--text2);margin-top:4px">'+it.l+'</span></div>'});html+='</div>';$('dC').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("chart-builder","图表制作器","📊","柱状图/饼图/折线图",
'''<div class="cd"><h2>创建图表</h2>
<label>图表类型</label><select id="cTy"><option value="bar">柱状图</option><option value="pie">饼图</option><option value="line">折线图</option></select>
<label>数据（标签:值，每行一个）</label><textarea id="cDa" rows="6" placeholder="苹果:30\n香蕉:20\n橘子:25\n葡萄:15"></textarea>
<button onclick="mCH()">生成图表</button></div>
<div class="cd" id="cCC" style="display:none"><h2>图表</h2><div id="cCH"></div></div>''',
'''function mCH(){const type=$('cTy').value;const lines=$('cDa').value.split("\\n").filter(l=>l.trim());const items=lines.map(l=>{const[k,v]=l.split(":");return{k:k.trim(),v:parseFloat(v)||0}});if(!items.length){alert('请输入数据');return}$('cCC').style.display='';const total=items.reduce((s,i)=>s+i.v,0);const co=["#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6","#ec4899","#06b6d4","#f97316"];let html="";if(type==="bar"){const mx=Math.max(...items.map(i=>i.v));html='<div style="display:flex;align-items:flex-end;gap:6px;height:200px;padding:16px 0">'+items.map((it,i)=>'<div style="flex:1;display:flex;flex-direction:column;align-items:center"><span style="font-size:.7rem">'+it.v+'</span><div style="width:100%;background:'+co[i%8]+';height:'+(mx?it.v/mx*180:0)+'px;border-radius:4px 4px 0 0"></div><span style="font-size:.7rem;color:var(--text2);margin-top:4px">'+it.k+'</span></div>').join('')+'</div>'}else if(type==="pie"){let cum=0;const segs=items.map((it,i)=>{const pct=total?it.v/total*100:0;const st=cum;cum+=pct;return'conic-gradient(from '+(st*3.6)+'deg,'+co[i%8]+' 0 '+(pct*3.6)+'deg,transparent '+(pct*3.6)+'deg)'}).join(',');html='<div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;justify-content:center"><div style="width:180px;height:180px;border-radius:50%;background:'+segs+';box-shadow:0 4px 12px rgba(0,0,0,.3)"></div><div>'+items.map((it,i)=>'<div style="margin:4px 0;display:flex;align-items:center;gap:8px"><span style="width:12px;height:12px;border-radius:50%;background:'+co[i%8]+';display:inline-block"></span>'+it.k+': '+(total?Math.round(it.v/total*100):0)+'%</div>').join('')+'</div></div>'}else{const mx=Math.max(...items.map(i=>i.v));const pts=items.map((it,i)=>''+(i/(items.length-1||1)*100)+','+(100-(mx?it.v/mx*80:0))).join(' ');html='<svg viewBox="0 0 100 100" style="width:100%;height:200px"><polyline points="'+pts+'" fill="none" stroke="var(--accent)" stroke-width="2" vector-effect="non-scaling-stroke"/>'+items.map((it,i)=>'<circle cx="'+(i/(items.length-1||1)*100)+'" cy="'+(100-(mx?it.v/mx*80:0))+'" r="3" fill="var(--accent)"/>').join('')+'</svg><div style="display:flex;justify-content:space-between;padding:0 16px;color:var(--text2);font-size:.7rem">'+items.map(it=>'<span>'+it.k+'</span>').join('')+'</div>'}$('cCH').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("graph-builder","图形构建器","🕸️","SVG图形生成器",
'''<div class="cd"><h2>生成图形</h2>
<label>图形类型</label><select id="gSh"><option value="circle">圆形</option><option value="rect">矩形</option><option value="triangle">三角形</option><option value="star">星形</option><option value="pentagon">五边形</option><option value="hexagon">六边形</option><option value="heart">心形</option></select>
<label>大小 (50-300)</label><input type="number" id="gSi" value="150" min="50" max="300">
<label>颜色</label><input type="color" id="gCo" value="#3b82f6">
<button onclick="dSH()">生成图形</button></div>
<div class="cd" id="gSC" style="display:none"><h2>图形</h2><div id="gSV" style="text-align:center"></div></div>''',
'''function dSH(){const type=$('gSh').value,s=parseInt($('gSi').value)||150,color=$('gCo').value,h=s/2;let p="";if(type==="circle")p='<circle cx="'+h+'" cy="'+h+'" r="'+(h-5)+'" fill="'+color+'" opacity=".85"/>';else if(type==="rect")p='<rect x="5" y="5" width="'+(s-10)+'" height="'+(s-10)+'" rx="8" fill="'+color+'" opacity=".85"/>';else if(type==="triangle")p='<polygon points="'+h+',5 5,'+(s-5)+' '+(s-5)+','+(s-5)+'" fill="'+color+'" opacity=".85"/>';else if(type==="star"){const pts=[];for(let i=0;i<10;i++){const r=i%2===0?h-5:(h-5)*.4,a=Math.PI*2*i/10-Math.PI/2;pts.push((h+r*Math.cos(a))+','+(h+r*Math.sin(a)))}p='<polygon points="'+pts.join(' ')+'" fill="'+color+'" opacity=".85"/>'}else if(type==="pentagon"){const pts=[];for(let i=0;i<5;i++){const a=Math.PI*2*i/5-Math.PI/2;pts.push((h+(h-5)*Math.cos(a))+','+(h+(h-5)*Math.sin(a)))}p='<polygon points="'+pts.join(' ')+'" fill="'+color+'" opacity=".85"/>'}else if(type==="hexagon"){const pts=[];for(let i=0;i<6;i++){const a=Math.PI*2*i/6;pts.push((h+(h-5)*Math.cos(a))+','+(h+(h-5)*Math.sin(a)))}p='<polygon points="'+pts.join(' ')+'" fill="'+color+'" opacity=".85"/>'}else{p='<path d="M'+h+','+(s*.15)+' C'+(h-s*.35)+','+(s*.15)+' '+(h-s*.5)+','+(s*.55)+' '+h+','+(s*.85)+' C'+(h+s*.5)+','+(s*.55)+' '+(h+s*.35)+','+(s*.15)+' '+h+','+(s*.15)+'" fill="'+color+'" opacity=".85"/>'}$('gSC').style.display='';$('gSV').innerHTML='<svg viewBox="0 0 '+s+' '+s+'" style="width:'+s+'px;height:'+s+'px;filter:drop-shadow(0 4px 12px '+color+'44)">'+p+'</svg>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("table-builder","表格构建器","📋","在线表格编辑器",
'''<div class="cd"><h2>创建表格</h2>
<div class="fr"><div><label>行数</label><input type="number" id="tR" value="4" min="1" max="50"></div><div><label>列数</label><input type="number" id="tC" value="4" min="1" max="20"></div></div>
<button onclick="cTB()">创建表格</button></div>
<div class="cd" id="tBC" style="display:none"><h2>表格</h2><div id="tA" style="overflow-x:auto"></div></div>''',
'''let TD=[];function cTB(){const r=parseInt($('tR').value)||4,c=parseInt($('tC').value)||4;TD=Array.from({length:r},()=>Array(c).fill(""));$('tBC').style.display='';rTB()}function rTB(){let html="<table><tr>";for(let j=0;j<TD[0].length;j++)html+='<th>列'+(j+1)+'</th>';html+="</tr>";TD.forEach((row,i)=>{html+="<tr>";row.forEach((cell,j)=>{html+='<td><input type="text" value="'+cell+'" style="width:100%;padding:6px;background:transparent;border:1px solid transparent;color:var(--text);font-size:.9rem" onfocus="this.style.borderColor=\\'var(--accent)\\'" onblur="this.style.borderColor=\\'transparent\\';TD['+i+']['+j+']=this.value"></td>'});html+="</tr>"});html+="</table>";$('tA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("form-builder","表单构建器","📝","可视化表单构建器",
'''<div class="cd"><h2>创建表单</h2>
<label>表单标题</label><input type="text" id="fTi" placeholder="我的表单">
<label>字段（标签:类型，每行一个，类型:text/email/tel/textarea/date/number）</label>
<textarea id="fFi" rows="6" placeholder="姓名:text\n邮箱:email\n电话:tel\n备注:textarea"></textarea>
<button onclick="bFM()">生成表单</button></div>
<div class="cd" id="fMC" style="display:none"><h2>表单</h2><div id="fMA"></div></div>''',
'''function bFM(){const title=$('fTi').value||'表单';const lines=$('fFi').value.split("\\n").filter(l=>l.trim());const fields=lines.map(l=>{const[label,type]=l.split(":");return{label:label.trim(),type:(type||"text").trim()}});if(!fields.length){alert('请添加字段');return}let html='<h2 style="margin-bottom:16px">'+title+'</h2><form onsubmit="event.preventDefault();alert(\\'提交成功！\\')">';fields.forEach(f=>{html+='<label>'+f.label+'</label>';if(f.type==="textarea")html+='<textarea placeholder="请输入'+f.label+'"></textarea>';else html+='<input type="'+f.type+'" placeholder="请输入'+f.label+'">'});html+='<div class="bg"><button type="submit">提交</button></div></form>';$('fMC').style.display='';$('fMA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("survey-builder","调查构建器","📊","在线调查问卷",
'''<div class="cd"><h2>创建调查</h2>
<label>调查标题</label><input type="text" id="sTi" placeholder="满意度调查">
<label>问题（每行一个，格式：问题:类型）</label>
<textarea id="sQs" rows="6" placeholder="你对服务的满意度？:1-5\n你会推荐我们吗？:1-5\n你的建议:文本"></textarea>
<button onclick="bSV()">生成调查</button></div>
<div class="cd" id="sVC" style="display:none"><h2>调查</h2><div id="sVA"></div></div>''',
'''function bSV(){const title=$('sTi').value||'调查';const lines=$('sQs').value.split("\\n").filter(l=>l.trim());const qs=lines.map(l=>{const[q,type]=l.split(":");return{q:q.trim(),type:(type||"text").trim()}});if(!qs.length){alert('请添加问题');return}let html='<h2>'+title+'</h2><form onsubmit="event.preventDefault();alert(\\'感谢参与！\\')">';qs.forEach((q,i)=>{html+='<label>'+(i+1)+'. '+q.q+'</label>';if(q.type==="1-5"){html+='<div style="display:flex;gap:8px;margin:8px 0">'+[1,2,3,4,5].map(n=>'<label style="display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;padding:8px 12px;background:var(--bg);border:1px solid var(--border);border-radius:8px"><input type="radio" name="q'+i+'" value="'+n+'"><span>'+n+'</span></label>').join('')+'</div>'}else html+='<textarea placeholder="请输入..."></textarea>'});html+='<div class="bg"><button type="submit">提交</button></div></form>';$('sVC').style.display='';$('sVA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

# --- 教育/考试 ---
tools.append(("quiz-maker","问答制作器","❓","快速制作问答测验",
'''<div class="cd"><h2>创建问答</h2>
<label>问题</label><textarea id="qmQ" placeholder="输入问题"></textarea>
<label>答案</label><textarea id="qmA" placeholder="输入答案"></textarea>
<div class="bg"><button onclick="addQM()">添加</button><button class="sec" onclick="startQM()" id="qmSB" style="display:none">开始复习</button></div></div>
<div class="cd"><h2>问答列表 (<span id="qmC">0</span>)</h2><div id="qmL" class="es">暂无</div></div>
<div class="cd" id="qmSC" style="display:none"><h2 id="qmTi">1/1</h2><p id="qmQt" style="font-size:1.1rem;margin:12px 0"></p><div id="qmAt" class="hidden" style="padding:16px;background:var(--bg);border-radius:8px;margin:12px 0"></div>
<div class="bg"><button onclick="showQMAns()">显示答案</button><button id="qmNB" class="hidden" onclick="nextQM()">下一题</button></div></div>''',
'''let QM=[],cQM=0;function addQM(){const q=$('qmQ').value.trim(),a=$('qmA').value.trim();if(!q||!a){alert('请填写问题和答案');return}QM.push({q,a});$('qmC').textContent=QM.length;$('qmSB').style.display='';rQM();$('qmQ').value='';$('qmA').value=''}
function rQM(){const e=$('qmL');if(!QM.length){e.innerHTML='<div class="es">暂无</div>';return}e.innerHTML=QM.map((q,i)=>'<div class="li"><span>'+(i+1)+'. '+q.q.substring(0,40)+'</span><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="QM.splice('+i+',1);$(\\'qmC\\').textContent=QM.length;rQM()">删除</button></div>').join('')}
function startQM(){if(!QM.length)return;cQM=0;document.querySelector('.cd:nth-child(1)').style.display='none';document.querySelector('.cd:nth-child(2)').style.display='none';$('qmSC').style.display='';shQM()}
function shQM(){const q=QM[cQM];$('qmTi').textContent=(cQM+1)+'/'+QM.length;$('qmQt').textContent=q.q;$('qmAt').classList.add('hidden');$('qmNB').classList.add('hidden');$('qmAt').textContent=''}
function showQMAns(){$('qmAt').textContent=QM[cQM].a;$('qmAt').classList.remove('hidden');if(cQM<QM.length-1)$('qmNB').classList.remove('hidden');else $('qmNB').classList.remove('hidden')}
function nextQM(){cQM++;shQM()}
function $(id){return document.getElementById(id)}'''))

tools.append(("test-maker","测试制作器","✍️","创建结构化测试",
'''<div class="cd"><h2>创建测试</h2>
<label>测试名称</label><input type="text" id="tmN" placeholder="期末测试">
<label>题目（每行一个，格式：问题|选项A|选项B|正确答案编号(1-2)）</label>
<textarea id="tmQ" rows="6" placeholder="1+1=?|1|2|2\n2+3=?|4|5|2"></textarea>
<button onclick="bTM()">生成测试</button></div>
<div class="cd" id="tmC" style="display:none"><h2 id="tmTi"></h2><div id="tmA"></div><div class="bg" id="tmB"></div></div>''',
'''function bTM(){const name=$('tmN').value||'测试';const lines=$('tmQ').value.split("\\n").filter(l=>l.trim());const qs=lines.map(l=>{const p=l.split("|");return{q:p[0],opts:p.slice(1,-1),ans:parseInt(p[p.length-1])||1}});if(!qs.length){alert('请添加题目');return}$('tmC').style.display='';$('tmTi').textContent=name;let html='';qs.forEach((q,i)=>{html+='<div style="margin-bottom:16px"><p style="font-weight:600;margin-bottom:8px">'+(i+1)+'. '+q.q+'</p>';q.opts.forEach((o,j)=>{html+='<label style="display:flex;align-items:center;gap:8px;padding:8px;cursor:pointer;border:1px solid var(--border);border-radius:8px;margin-bottom:4px"><input type="radio" name="tm'+i+'" value="'+(j+1)+'"><span>'+o+'</span></label>'});html+='</div>'});$('tmA').innerHTML=html;$('tmB').innerHTML='<button onclick="ckTM()">提交答案</button>';window._tmQs=qs;window._tmAn=[]}
function ckTM(){const qs=window._tmQs;let sc=0;qs.forEach((q,i)=>{const sel=document.querySelector('input[name="tm'+i+'"]:checked');const val=sel?parseInt(sel.value):0;if(val===q.ans)sc++;const labels=document.querySelectorAll('input[name="tm'+i+'"]');labels.forEach(l=>{const p=l.parentElement;if(parseInt(l.value)===q.ans)p.style.borderColor='var(--success)';if(l.checked&&parseInt(l.value)!==q.ans)p.style.borderColor='var(--danger)'})});$('tmB').innerHTML='<div class="gr" style="margin:16px 0"><div class="st"><div class="nm">'+sc+'/'+qs.length+'</div><div class="lb">得分</div></div><div class="st"><div class="nm">'+Math.round(sc/qs.length*100)+'%</div><div class="lb">正确率</div></div></div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("exam-maker","考试制作器","🎓","模拟考试系统",
'''<div class="cd"><h2>创建考试</h2>
<label>考试名称</label><input type="text" id="exN" placeholder="期末考试">
<label>时间限制(分钟)</label><input type="number" id="exT" value="60" min="1">
<label>题目（每行一个，格式：问题|选项A|选项B|选项C|正确答案编号1-3）</label>
<textarea id="exQ" rows="6" placeholder="问题1|A选项|B选项|C选项|1\n问题2|A选项|B选项|C选项|2"></textarea>
<div class="bg"><button onclick="startEX()">开始考试</button></div></div>
<div class="cd" id="exC" style="display:none"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><h2 id="exTi"></h2><span id="exTi2" style="color:var(--warn);font-weight:700;font-size:1.2rem"></span></div><div id="exA"></div><div class="bg" id="exB"></div></div>''',
'''let exTimer=null,exRem=0;function startEX(){const name=$('exN').value||'考试';const t=parseInt($('exT').value)||60;const lines=$('exQ').value.split("\\n").filter(l=>l.trim());const qs=lines.map(l=>{const p=l.split("|");return{q:p[0],opts:p.slice(1,-1),ans:parseInt(p[p.length-1])||1}});if(!qs.length){alert('请添加题目');return}$('exC').style.display='';$('exTi').textContent=name;exRem=t*60;if(exTimer)clearInterval(exTimer);exTimer=setInterval(()=>{exRem--;const m=Math.floor(exRem/60),s=exRem%60;$('exTi2').textContent=m+':'+(s<10?'0':'')+s;if(exRem<=0){clearInterval(exTimer);alert('时间到！');ckEX()}},1000);let html='';qs.forEach((q,i)=>{html+='<div style="margin-bottom:16px;padding:12px;background:var(--bg);border-radius:8px"><p style="font-weight:600;margin-bottom:8px">'+(i+1)+'. '+q.q+'</p>';q.opts.forEach((o,j)=>{html+='<label style="display:flex;align-items:center;gap:8px;padding:8px;cursor:pointer;border:1px solid var(--border);border-radius:8px;margin-bottom:4px"><input type="radio" name="ex'+i+'" value="'+(j+1)+'"><span>'+o+'</span></label>'});html+='</div>'});$('exA').innerHTML=html;$('exB').innerHTML='<button onclick="ckEX()">交卷</button>';window._exQs=qs}
function ckEX(){if(exTimer)clearInterval(exTimer);const qs=window._exQs;let sc=0;qs.forEach((q,i)=>{const sel=document.querySelector('input[name="ex'+i+'"]:checked');const val=sel?parseInt(sel.value):0;if(val===q.ans)sc++;const labels=document.querySelectorAll('input[name="ex'+i+'"]');labels.forEach(l=>{const p=l.parentElement;if(parseInt(l.value)===q.ans)p.style.borderColor='var(--success)';if(l.checked&&parseInt(l.value)!==q.ans)p.style.borderColor='var(--danger)';l.disabled=true})});$('exB').innerHTML='<div class="gr" style="margin:16px 0"><div class="st"><div class="nm">'+sc+'/'+qs.length+'</div><div class="lb">得分</div></div><div class="st"><div class="nm">'+Math.round(sc/qs.length*100)+'%</div><div class="lb">正确率</div></div></div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("homework-maker","作业制作器","📚","布置和管理作业",
'''<div class="cd"><h2>创建作业</h2>
<label>科目</label><input type="text" id="hwS" placeholder="数学">
<label>作业内容</label><textarea id="hwC" placeholder="作业内容描述"></textarea>
<label>截止日期</label><input type="date" id="hwD">
<label>优先级</label><select id="hwP"><option value="high">高</option><option value="mid">中</option><option value="low">低</option></select>
<div class="bg"><button onclick="addHW()">添加作业</button></div></div>
<div class="cd"><h2>作业列表</h2><div id="hwL" class="es">暂无作业</div></div>''',
'''let HW=JSON.parse(localStorage.getItem('hwList')||'[]');function rHW(){$('hwL').innerHTML=HW.length?HW.map((h,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+h.subject+'</span><span class="tag '+(h.priority==='high'?'d':h.priority==='mid'?'w':'s')+'">'+{high:'高',mid:'中',low:'低'}[h.priority]+'</span></div><p style="color:var(--text2);font-size:.9rem;margin:4px 0">'+h.content+'</p><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:.8rem;color:var(--text2)">截止: '+h.deadline+'</span><div><button class="sec" style="padding:4px 12px;font-size:.8rem;margin-right:4px" onclick="HW['+i+'].done=!HW['+i+'].done;localStorage.setItem(\\'hwList\\',JSON.stringify(HW));rHW()">'+(h.done?'✓ 已完成':'标记完成')+'</button><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="HW.splice('+i+',1);localStorage.setItem(\\'hwList\\',JSON.stringify(HW));rHW()">删除</button></div></div></div>').join(''):'<div class="es">暂无作业</div>'}
function addHW(){const s=$('hwS').value.trim(),c=$('hwC').value.trim(),d=$('hwD').value,p=$('hwP').value;if(!s||!c){alert('请填写科目和内容');return}HW.unshift({subject:s,content:c,deadline:d||'无',priority:p,done:false});localStorage.setItem('hwList',JSON.stringify(HW));rHW();$('hwS').value='';$('hwC').value='';$('hwD').value=''}
function $(id){return document.getElementById(id)}rHW()'''))

tools.append(("lesson-plan","课程计划器","📋","教师课程计划",
'''<div class="cd"><h2>创建课程计划</h2>
<label>课程名称</label><input type="text" id="lpN" placeholder="数学课">
<label>日期</label><input type="date" id="lpD">
<label>时间</label><input type="time" id="lpT" value="09:00">
<label>时长(分钟)</label><input type="number" id="lpDu" value="45">
<label>教学目标</label><textarea id="lpG" placeholder="本节课教学目标"></textarea>
<label>教学内容</label><textarea id="lpC" placeholder="教学内容大纲"></textarea>
<label>作业安排</label><textarea id="lpH" placeholder="课后作业"></textarea>
<div class="bg"><button onclick="addLP()">添加课程</button></div></div>
<div class="cd"><h2>课程计划</h2><div id="lpL" class="es">暂无课程计划</div></div>''',
'''let LP=[];function rLP(){$('lpL').innerHTML=LP.length?LP.map((p,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+p.name+'</span><span style="color:var(--text2);font-size:.8rem">'+p.date+' '+p.time+' ('+p.duration+'分钟)</span></div><p style="color:var(--text2);font-size:.9rem;margin:4px 0">目标: '+p.goal+'</p><p style="color:var(--text2);font-size:.9rem">内容: '+p.content+'</p>'+(p.homework?'<p style="color:var(--text2);font-size:.9rem">作业: '+p.homework+'</p>':'')+'<div class="bg"><button class="dng" style="padding:4px 12px;font-size:.8rem" onclick="LP.splice('+i+',1);rLP()">删除</button></div></div></div>').join(''):'<div class="es">暂无课程计划</div>'}
function addLP(){const n=$('lpN').value.trim(),d=$('lpD').value,t=$('lpT').value,du=$('lpDu').value,g=$('lpG').value.trim(),c=$('lpC').value.trim(),h=$('lpH').value.trim();if(!n){alert('请填写课程名称');return}LP.push({name:n,date:d||'未定',time:t,duration:du,goal:g,content:c,homework:h});rLP();['lpN','lpG','lpC','lpH'].forEach(id=>$(id).value='')}
function $(id){return document.getElementById(id)}rLP()'''))

tools.append(("course-builder","课程构建器","🎓","在线课程结构设计",
'''<div class="cd"><h2>构建课程</h2>
<label>课程名称</label><input type="text" id="cbN" placeholder="Python编程入门">
<label>课程简介</label><textarea id="cbD" placeholder="课程简介"></textarea>
<label>模块（每行一个）</label>
<textarea id="cbM" rows="6" placeholder="第一模块：Python基础\n第二模块：数据结构\n第三模块：面向对象"></textarea>
<button onclick="bCB()">生成课程结构</button></div>
<div class="cd" id="cbC" style="display:none"><h2>课程结构</h2><div id="cbA"></div></div>''',
'''function bCB(){const n=$('cbN').value||'课程';const d=$('cbD').value;const ms=$('cbM').value.split("\\n").filter(l=>l.trim());if(!ms.length){alert('请添加模块');return}$('cbC').style.display='';let html='<div style="background:var(--accent);color:#fff;padding:16px;border-radius:12px;text-align:center;margin-bottom:16px"><h3 style="margin-bottom:4px">'+n+'</h3><p style="opacity:.8;font-size:.9rem">'+d+'</p></div>';ms.forEach((m,i)=>{html+='<div style="padding:16px;background:var(--bg);border-radius:8px;margin-bottom:8px;border-left:4px solid '+['var(--accent)','var(--success)','var(--warn)','var(--danger)'][i%4]+'"><span class="tag">'+(i+1)+'</span> '+m+'</div>'});$('cbA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("curriculum-builder","课程体系构建器","🏫","完整课程体系设计",
'''<div class="cd"><h2>课程体系</h2>
<label>体系名称</label><input type="text" id="cuN" placeholder="计算机科学课程体系">
<label>年级/阶段</label><input type="text" id="cuG" placeholder="大一">
<label>课程（每行一个）</label>
<textarea id="cuC" rows="6" placeholder="高等数学\n线性代数\nC语言程序设计\n大学英语"></textarea>
<button onclick="addCu()">添加阶段</button></div>
<div class="cd"><h2>课程体系</h2><div id="cuL" class="es">暂无阶段</div></div>''',
'''let CU=[];function rCU(){$('cuL').innerHTML=CU.length?CU.map((c,i)=>'<div style="padding:12px;background:var(--bg);border-radius:8px;margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-weight:600">'+c.grade+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="CU.splice('+i+',1);rCU()">删除</button></div><p style="color:var(--text2);font-size:.8rem;margin-bottom:4px">'+c.name+'</p><div style="display:flex;flex-wrap:wrap;gap:4px">'+c.courses.map(co=>'<span class="tag">'+co+'</span>').join('')+'</div></div>').join(''):'<div class="es">暂无阶段</div>'}
function addCu(){const n=$('cuN').value.trim(),g=$('cuG').value.trim(),cs=$('cuC').value.split("\\n").filter(l=>l.trim());if(!g||!cs.length){alert('请填写年级和课程');return}CU.push({name:n,grade:g,courses:cs});rCU();$('cuN').value='';$('cuG').value='';$('cuC').value=''}
function $(id){return document.getElementById(id)}rCU()'''))

tools.append(("learning-path","学习路径","🛤️","规划学习路径",
'''<div class="cd"><h2>学习路径</h2>
<label>目标技能</label><input type="text" id="lpG" placeholder="全栈开发">
<label>当前水平</label><select id="lpL"><option>初学者</option><option>中级</option><option>高级</option></select>
<label>阶段（每行一个）</label>
<textarea id="lpS" rows="6" placeholder="HTML/CSS基础\nJavaScript入门\nReact框架\nNode.js后端\n数据库设计\n项目实战"></textarea>
<button onclick="bLP()">生成路径</button></div>
<div class="cd" id="lpC" style="display:none"><h2>学习路径</h2><div id="lpA"></div></div>''',
'''function bLP(){const g=$('lpG').value||'学习目标';const l=$('lpL').value;const ss=$('lpS').value.split("\\n").filter(x=>x.trim());if(!ss.length){alert('请添加阶段');return}$('lpC').style.display='';let html='<div style="text-align:center;margin-bottom:16px"><h3>'+g+'</h3><span class="tag">'+l+'</span></div>';ss.forEach((s,i)=>{const colors=['var(--accent)','var(--success)','var(--warn)','#8b5cf6','#ec4899','#06b6d4'];html+='<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px"><div style="width:40px;height:40px;border-radius:50%;background:'+colors[i%6]+';display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;flex-shrink:0">'+(i+1)+'</div><div style="flex:1;padding:12px;background:var(--bg);border-radius:8px">'+s+'</div></div>'+(i<ss.length-1?'<div style="text-align:center;color:var(--text2);margin:4px 0">↓</div>':'')});$('lpA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("skill-matrix","技能矩阵","📊","技能评估矩阵",
'''<div class="cd"><h2>技能矩阵</h2>
<label>技能名称</label><input type="text" id="smN" placeholder="JavaScript">
<label>熟练度 (1-10)</label><input type="number" id="smL" min="1" max="10" value="5">
<label>分类</label><input type="text" id="smC" placeholder="编程语言">
<div class="bg"><button onclick="addSM()">添加技能</button></div></div>
<div class="cd"><h2>技能矩阵</h2><div id="smA" class="es">暂无技能</div></div>''',
'''let SM=[];function rSM(){$('smA').innerHTML=SM.length?SM.map((s,i)=>'<div class="li"><div style="flex:1"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+s.name+'</span><span style="color:var(--text2);font-size:.8rem">'+s.category+'</span></div><div class="pb"><div class="fl" style="width:'+s.level*10+'%;background:'+['var(--danger)','var(--warn)','var(--success)'][Math.floor(s.level/4)]+'"></div></div><span style="font-size:.8rem;color:var(--text2)">'+s.level+'/10</span></div><button class="dng" style="padding:4px 12px;font-size:.8rem;margin-left:12px" onclick="SM.splice('+i+',1);rSM()">删除</button></div>').join(''):'<div class="es">暂无技能</div>'}
function addSM(){const n=$('smN').value.trim(),l=parseInt($('smL').value)||5,c=$('smC').value.trim()||'未分类';if(!n){alert('请填写技能名称');return}SM.push({name:n,level:l,category:c});rSM();$('smN').value='';$('smL').value='5';$('smC').value=''}
function $(id){return document.getElementById(id)}rSM()'''))

tools.append(("competency-map","能力地图","🗺️","能力模型评估",
'''<div class="cd"><h2>能力评估</h2>
<label>能力领域</label><input type="text" id="cmN" placeholder="沟通能力">
<label>当前水平</label><select id="cmL"><option value="1">1-待发展</option><option value="2" selected>2-基础</option><option value="3">3-熟练</option><option value="4">4-精通</option><option value="5">5-专家</option></select>
<label>目标水平</label><select id="cmT"><option value="1">1-待发展</option><option value="2">2-基础</option><option value="3">3-熟练</option><option value="4">4-精通</option><option value="5" selected>5-专家</option></select>
<div class="bg"><button onclick="addCM()">添加能力</button></div></div>
<div class="cd"><h2>能力地图</h2><div id="cmA" class="es">暂无能力项</div></div>''',
'''let CM=[];function rCM(){$('cmA').innerHTML=CM.length?CM.map((c,i)=>{const gap=c.target-c.current;return'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span style="font-weight:600">'+c.name+'</span><button class="dng" style="padding:2px 10px;font-size:.8rem" onclick="CM.splice('+i+',1);rCM()">删除</button></div><div style="display:flex;gap:16px;margin-top:8px"><div style="flex:1"><div style="font-size:.75rem;color:var(--text2)">当前</div><div class="pb"><div class="fl" style="width:'+c.current*20+'%"></div></div><span style="font-size:.8rem">'+c.current+'/5</span></div><div style="flex:1"><div style="font-size:.75rem;color:var(--text2)">目标</div><div class="pb"><div class="fl" style="width:'+c.target*20+'%;background:var(--success)"></div></div><span style="font-size:.8rem">'+c.target+'/5</span></div></div>'+(gap>0?'<span style="font-size:.8rem;color:var(--warn);margin-top:4px">差距: '+gap+' 级</span>':'<span style="font-size:.8rem;color:var(--success);margin-top:4px">已达目标 ✓</span>')+'</div>'}).join(''):'<div class="es">暂无能力项</div>'}
function addCM(){const n=$('cmN').value.trim(),l=parseInt($('cmL').value),t=parseInt($('cmT').value);if(!n){alert('请填写能力名称');return}CM.push({name:n,current:l,target:t});rCM();$('cmN').value=''}
function $(id){return document.getElementById(id)}rCM()'''))

tools.append(("career-path","职业路径","🛤️","职业发展规划",
'''<div class="cd"><h2>职业路径</h2>
<label>当前职位</label><input type="text" id="cpC" placeholder="初级开发者">
<label>目标职位</label><input type="text" id="cpT" placeholder="技术总监">
<label>时间框架</label><input type="text" id="cpF" placeholder="5年">
<label>里程碑（每行一个）</label>
<textarea id="cpM" rows="6" placeholder="高级开发者\n技术组长\n架构师\n技术总监"></textarea>
<button onclick="bCP()">生成路径</button></div>
<div class="cd" id="cpC2" style="display:none"><h2>职业路径</h2><div id="cpA"></div></div>''',
'''function bCP(){const c=$('cpC').value||'当前',t=$('cpT').value||'目标',f=$('cpF').value||'未定',ms=$('cpM').value.split("\\n").filter(x=>x.trim());if(!ms.length){alert('请添加里程碑');return}$('cpC2').style.display='';let html='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><div class="tag">'+c+'</div><span style="color:var(--text2)">→ '+f+' →</span><div class="tag s">'+t+'</div></div>';ms.forEach((m,i)=>{html+='<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px"><div style="width:32px;height:32px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;color:#fff;font-size:.8rem;flex-shrink:0">'+(i+1)+'</div><div style="flex:1;padding:12px;background:var(--bg);border-radius:8px">'+m+'</div></div>'+(i<ms.length-1?'<div style="text-align:center;color:var(--text2);margin:2px 0">↓</div>':'')});$('cpA').innerHTML=html}
function $(id){return document.getElementById(id)}'''))

tools.append(("salary-negotiation-cn","薪资谈判CN","💰","中国薪资谈判助手",
'''<div class="cd"><h2>薪资评估</h2>
<label>目标月薪(元)</label><input type="number" id="snT" placeholder="15000">
<label>当前月薪(元)</label><input type="number" id="snC" placeholder="12000">
<label>工作年限</label><input type="number" id="snY" value="3" min="0">
<label>学历</label><select id="snE"><option>大专</option><option selected>本科</option><option>硕士</option><option>博士</option></select>
<button onclick="calcSN()">评估谈判空间</button></div>
<div class="cd" id="snR" style="display:none"><h2>谈判分析</h2><div id="snA"></div></div>''',
'''function calcSN(){const t=parseInt($('snT').value)||0,c=parseInt($('snC').value)||0,y=parseInt($('snY').value)||0,e=$('snE').value;if(!t){alert('请输入目标月薪');return}const diff=t-c;const pct=c?Math.round(diff/c*100):0;const yrsal=t*12;const bonus=yrsal*0.15;const tax=Math.round(yrsal*0.1);const net=Math.round((yrsal+bonus-tax)/12);$('snR').style.display='';$('snA').innerHTML='<div class="gr" style="margin:16px 0"><div class="st"><div class="nm">'+t.toLocaleString()+'</div><div class="lb">目标月薪</div></div><div class="st"><div class="nm">+'+pct+'%</div><div class="lb">涨幅</div></div><div class="st"><div class="nm">'+(yrsal/10000).toFixed(1)+'万</div><div class="lb">年薪</div></div><div class="st"><div class="nm">'+net.toLocaleString()+'</div><div class="lb">预估月薪(扣税后)</div></div></div><div style="padding:12px;background:var(--bg);border-radius:8px"><h3 style="font-size:.95rem;margin-bottom:8px">💡 谈判建议</h3><ul style="color:var(--text2);font-size:.9rem;padding-left:20px"><li>建议先了解市场行情，合理定位</li><li>突出你的核心竞争力和过往业绩</li><li>可谈判年终奖、股票、补贴等福利</li><li>准备2-3个备选offer增加筹码</li><li>保持礼貌但坚定的态度</li></ul></div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("interview-prep","面试准备","🎤","面试问题准备器",
'''<div class="cd"><h2>添加面试问题</h2>
<label>公司</label><input type="text" id="ivC" placeholder="公司名称">
<label>职位</label><input type="text" id="ivP" placeholder="应聘职位">
<label>问题</label><textarea id="ivQ" placeholder="面试问题"></textarea>
<label>你的回答</label><textarea id="ivA" placeholder="准备的回答"></textarea>
<div class="bg"><button onclick="addIV()">添加</button></div></div>
<div class="cd"><h2>面试准备</h2><div id="ivL" class="es">暂无问题</div></div>''',
'''let IV=[];function rIV(){$('ivL').innerHTML=IV.length?IV.map((q,i)=>'<div class="li" style="flex-direction:column;align-items:stretch"><div style="display:flex;justify-content:space-between"><span class="tag">'+q.company+'</span><span style="color:var(--text2);font-size:.8rem">'+q.position+'</span></div><p style="font-weight:600;margin:8px 0 4px">'+q.question+'</p><p style="color:var(--text2);font-size:.9rem">回答: '+q.answer+'</p><button class="dng" style="padding:4px 12px;font-size:.8rem;align-self:flex-start;margin-top:8px" onclick="IV.splice('+i+',1);rIV()">删除</button></div>').join(''):'<div class="es">暂无问题</div>'}
function addIV(){const c=$('ivC').value.trim(),p=$('ivP').value.trim(),q=$('ivQ').value.trim(),a=$('ivA').value.trim();if(!q||!a){alert('请填写问题和回答');return}IV.push({company:c||'未指定',position:p||'未指定',question:q,answer:a});rIV();$('ivQ').value='';$('ivA').value=''}
function $(id){return document.getElementById(id)}rIV()'''))

tools.append(("resume-builder","简历构建器","📄","在线简历生成",
'''<div class="cd"><h2>个人信息</h2>
<label>姓名</label><input type="text" id="rN" placeholder="张三">
<label>电话</label><input type="text" id="rP" placeholder="138-xxxx-xxxx">
<label>邮箱</label><input type="text" id="rE" placeholder="email@example.com">
<label>求职意向</label><input type="text" id="rJ" placeholder="前端开发工程师">
<label>自我评价</label><textarea id="rS" placeholder="简短自我介绍"></textarea></div>
<div class="cd"><h2>工作经历</h2>
<textarea id="rW" rows="4" placeholder="公司名称 | 职位 | 时间段&#10;工作内容描述"></textarea></div>
<div class="cd"><h2>教育背景</h2>
<textarea id="rEd" rows="3" placeholder="学校名称 | 专业 | 学历 | 毕业时间"></textarea></div>
<div class="cd"><h2>技能</h2>
<textarea id="rSk" rows="3" placeholder="JavaScript, React, Node.js"></textarea></div>
<button onclick="prevRV()" style="margin-top:8px">预览简历</button>
<div class="cd" id="rvC" style="display:none"><h2>简历预览</h2><div id="rvA"></div></div>''',
'''function prevRV(){$('rvC').style.display='';$('rvA').innerHTML='<div style="padding:24px;background:var(--bg);border-radius:8px;border:1px solid var(--border)"><div style="text-align:center;border-bottom:2px solid var(--accent);padding-bottom:16px;margin-bottom:16px"><h2 style="font-size:1.5rem">'+($('rN').value||'姓名')+'</h2><p style="color:var(--text2)">'+($('rP').value||'电话')+' | '+($('rE').value||'邮箱')+'</p><p style="color:var(--accent)">'+($('rJ').value||'求职意向')+'</p></div>'+(($('rS').value)?'<div style="margin-bottom:16px"><h3 style="color:var(--accent);margin-bottom:8px">自我评价</h3><p style="color:var(--text2);font-size:.9rem">'+$('rS').value+'</p></div>':'')+(($('rW').value)?'<div style="margin-bottom:16px"><h3 style="color:var(--accent);margin-bottom:8px">工作经历</h3><p style="color:var(--text2);font-size:.9rem;white-space:pre-line">'+$('rW').value+'</p></div>':'')+(($('rEd').value)?'<div style="margin-bottom:16px"><h3 style="color:var(--accent);margin-bottom:8px">教育背景</h3><p style="color:var(--text2);font-size:.9rem;white-space:pre-line">'+$('rEd').value+'</p></div>':'')+(($('rSk').value)?'<div style="margin-bottom:16px"><h3 style="color:var(--accent);margin-bottom:8px">专业技能</h3><div style="display:flex;flex-wrap:wrap;gap:6px">'+$('rSk').value.split(/[,，、]/).map(s=>'<span class="tag">'+s.trim()+'</span>').join('')+'</div></div>':'')+'</div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("cover-letter","求职信","✉️","专业求职信生成",
'''<div class="cd"><h2>求职信</h2>
<label>你的姓名</label><input type="text" id="clN" placeholder="张三">
<label>公司名称</label><input type="text" id="clC" placeholder="目标公司">
<label>应聘职位</label><input type="text" id="clP" placeholder="应聘职位">
<label>为什么选择这家公司</label><textarea id="clW" placeholder="你对公司的了解和兴趣"></textarea>
<label>你的优势</label><textarea id="clS" placeholder="你的核心竞争力"></textarea>
<button onclick="genCL()">生成求职信</button></div>
<div class="cd" id="clRC" style="display:none"><h2>求职信</h2><div id="clA"></div></div>''',
'''function genCL(){const n=$('clN').value||'应聘者',c=$('clC').value||'贵公司',p=$('clP').value||'相关职位',w=$('clW').value||'贵公司在行业内的卓越表现和发展前景深深吸引了我',s=$('clS').value||'我相信我的专业技能和工作经验能够为贵公司创造价值';$('clRC').style.display='';$('clA').innerHTML='<div style="padding:24px;background:var(--bg);border-radius:8px;border:1px solid var(--border);line-height:2"><p>尊敬的招聘负责人：</p><p>您好！我是'+n+'，写信应聘贵公司'+p+'一职。</p><p>'+w+'，因此我非常期待能加入贵公司。</p><p>'+s+'。</p><p>随信附上我的简历，期待有机会进一步交流。感谢您的时间！</p><p style="margin-top:24px">'+n+'<br>'+new Date().toLocaleDateString('zh-CN')+'</p></div>'}
function $(id){return document.getElementById(id)}'''))

tools.append(("portfolio-builder","作品集构建器","💼","个人作品集展示",
'''<div class="cd"><h2>添加作品</h2>
<label>作品名称</label><input type="text" id="pbN" placeholder="项目名称">
<label>作品描述</label><textarea id="pbD" placeholder="项目描述"></textarea>
<label>技术栈</label><input type="text" id="pbT" placeholder="React, Node.js">
<label>链接</label><input type="text" id="pbL" placeholder="https://...">
<div class="bg"><button onclick="addPB()">添加作品</button></div></div>
<div class="cd"><h2>作品集</h2><div id="pbL2" class="es">暂无作品</div></div>''',
'''let PB=[];function rPB(){$('pbL2').innerHTML=PB.length?'<div class="gr">'+PB.map((p,i)=>'<div style="padding:16px;background:var(--bg);border-radius:8px;border:1px solid var(--border)"><div style="display:flex;justify-content:space-between"><h3 style="font-size:1rem">'+p.name+'</h3><button class="dng" style="padding:2px 8px;font-size:.75rem" onclick="PB.splice('+i+',1);rPB()">×</button></div><p style="color:var(--text2);font-size:.85rem;margin:8px 0">'+p.desc+'</p><div style="display:flex;flex-wrap:wrap;gap:4px">'+p.tech.map(t=>'<span class="tag">'+t+'</span>').join('')+'</div>'+(p.link?'<a href="'+p.link+'" target="_blank" style="color:var(--accent);font-size:.85rem;display:block;margin-top:8px;text-decoration:none">🔗 查看项目</a>':'')+'</div>').join('')+'</div>':'<div class="es">暂无作品</div>'}
function addPB(){const n=$('pbN').value.trim(),d=$('pbD').value.trim(),t=$('pbT').value.trim(),l=$('pbL').value.trim();if(!n){alert('请填写作品名称');return}PB.push({name:n,desc:d,tech:t?t.split(/[,，、]/).map(s=>s.trim()):[],link:l});rPB();['pbN','pbD','pbT','pbL'].forEach(id=>$(id).value='')}
function $(id){return document.getElementById(id)}rPB()'''))

print(f"\nBatch 1: {len(tools)} tools")

# Write all tools
for slug, title, icon, desc, body, js in tools:
    w(slug, title, icon, desc, body, js)

print(f"\nTotal created: {len(tools)}")
