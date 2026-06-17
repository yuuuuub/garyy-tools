#!/usr/bin/env python3
import os, json, random
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
random.seed(42)

DARK_CSS = ''':root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--accent:#3b82f6;--accent2:#10b981;--accent3:#f59e0b;--danger:#ef4444;--success:#22c55e;--radius:12px}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.container{max-width:800px;margin:0 auto}
h1{text-align:center;font-size:1.8em;margin-bottom:8px;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.subtitle{text-align:center;color:#8b949e;margin-bottom:24px;font-size:.95em}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:16px}
.btn{display:inline-block;padding:10px 24px;border:none;border-radius:8px;font-size:1em;cursor:pointer;transition:all .2s;font-weight:600}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{opacity:.9;transform:translateY(-1px)}
.btn-success{background:var(--accent2);color:#fff}.btn-success:hover{opacity:.9}
.btn-danger{background:var(--danger);color:#fff}.btn-danger:hover{opacity:.9}
.btn-outline{background:transparent;color:var(--accent);border:2px solid var(--accent)}.btn-outline:hover{background:var(--accent);color:#fff}
.score{text-align:center;font-size:1.3em;margin:16px 0;color:var(--accent3);font-weight:700}
.progress-bar{width:100%;height:8px;background:var(--border);border-radius:4px;overflow:hidden;margin:12px 0}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .3s;border-radius:4px}
.options{display:grid;gap:10px;margin:16px 0}
.option{background:var(--bg);border:2px solid var(--border);border-radius:8px;padding:14px 18px;cursor:pointer;transition:all .2s;text-align:left;font-size:1em;color:var(--text)}
.option:hover{border-color:var(--accent);background:#1a2332}
.option.correct{border-color:var(--success);background:rgba(34,197,94,.1);color:var(--success)}
.option.wrong{border-color:var(--danger);background:rgba(239,68,68,.1);color:var(--danger)}
.option.disabled{pointer-events:none;opacity:.7}
.result{text-align:center;padding:32px}.result h2{font-size:1.5em;margin-bottom:12px}
.hidden{display:none}
.timeline{position:relative;padding-left:40px;margin:20px 0}
.timeline::before{content:'';position:absolute;left:15px;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--accent),var(--accent2))}
.timeline-item{position:relative;margin-bottom:24px;padding:16px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius)}
.timeline-item::before{content:'';position:absolute;left:-33px;top:20px;width:12px;height:12px;background:var(--accent);border-radius:50%;border:3px solid var(--bg)}
.timeline-year{font-weight:700;color:var(--accent);font-size:1.1em}
.timeline-text{color:#8b949e;margin-top:4px;font-size:.95em}
.input{width:100%;padding:12px 16px;background:var(--bg);border:2px solid var(--border);border-radius:8px;color:var(--text);font-size:1em;margin:8px 0}
.input:focus{outline:none;border-color:var(--accent)}
.quiz-card{margin-bottom:12px;padding:16px;background:var(--bg);border:1px solid var(--border);border-radius:8px;cursor:pointer;transition:all .2s}
.quiz-card:hover{border-color:var(--accent)}
.quiz-card.correct{border-color:var(--success);background:rgba(34,197,94,.1)}
.quiz-card.wrong{border-color:var(--danger);background:rgba(239,68,68,.1)}
.year-label{font-weight:700;color:var(--accent);margin-bottom:4px}
.event-text{color:#8b949e;font-size:.95em}
.order-num{display:inline-block;width:28px;height:28px;background:var(--accent);color:#fff;border-radius:50%;text-align:center;line-height:28px;font-size:.85em;margin-right:8px}
.grid-cn{display:grid;gap:2px;margin:16px 0}
.cell-cn{aspect-ratio:1;display:flex;align-items:center;justify-content:center;background:var(--bg);border:1px solid var(--border);border-radius:4px;font-size:clamp(10px,2.5vw,16px);cursor:pointer;transition:all .2s;user-select:none}
.cell-cn:hover{border-color:var(--accent)}
.cell-cn.sel{background:rgba(59,130,246,.2);border-color:var(--accent)}
.cell-cn.found{background:rgba(34,197,94,.2);border-color:var(--success);color:var(--success)}
.word-tag{display:inline-block;padding:6px 12px;background:var(--bg);border:1px solid var(--border);border-radius:20px;font-size:.9em;margin:4px}
.word-tag.found{background:rgba(34,197,94,.15);border-color:var(--success);color:var(--success);text-decoration:line-through}
.scrambled{font-size:2em;text-align:center;letter-spacing:8px;margin:20px 0;color:var(--accent);font-weight:700}
.input-row{display:flex;gap:8px;justify-content:center;margin:16px 0}
.puzzle-chars{display:flex;gap:8px;justify-content:center;margin:20px 0;flex-wrap:wrap}
.puzzle-char{width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:var(--bg);border:2px solid var(--border);border-radius:8px;font-size:1.3em;cursor:pointer;transition:all .2s;user-select:none}
.puzzle-char:hover{border-color:var(--accent)}
.puzzle-char.placed{background:rgba(59,130,246,.15);border-color:var(--accent)}
.answer-slots{display:flex;gap:8px;justify-content:center;margin:16px 0}
.answer-slot{width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:var(--bg);border:2px dashed var(--border);border-radius:8px;font-size:1.3em;cursor:pointer}
.answer-slot.filled{border-style:solid;border-color:var(--accent)}
@media(max-width:600px){h1{font-size:1.4em}.card{padding:16px}.option{padding:12px}.scrambled{font-size:1.4em;letter-spacing:4px}.puzzle-char{width:40px;height:40px;font-size:1.1em}.answer-slot{width:40px;height:40px}.timeline{padding-left:30px}}
'''

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def js_list(arr):
    return '[' + ','.join(js_str(a) for a in arr) + ']'

def quiz_html(title, subtitle, questions):
    qdata = []
    for q in questions:
        opts = q.get('options', q.get('opts', []))
        ans = q.get('answer', q.get('ans', 0))
        exp = q.get('explain', q.get('exp', ''))
        qdata.append({'q': q.get('q', q.get('question', '')), 'opts': opts, 'ans': ans, 'exp': exp})
    qjs = json.dumps(qdata, ensure_ascii=False)
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>{DARK_CSS}.question{{font-size:1.15em;font-weight:600;margin-bottom:16px;line-height:1.6}}</style></head><body><div class="container"><h1>{title}</h1><p class="subtitle">{subtitle}</p><div class="card" id="game"><div class="score" id="score">得分: 0 / 0</div><div class="progress-bar"><div class="progress-fill" id="progress"></div></div><div class="question" id="question"></div><div class="options" id="options"></div><div style="text-align:center;margin-top:16px"><button class="btn btn-primary" id="nextBtn" onclick="nextQ()" style="display:none">下一题 &rarr;</button></div></div><div class="card hidden" id="result"><div class="result"><h2 id="resultTitle"></h2><p id="resultText" style="margin:12px 0;color:#8b949e"></p><button class="btn btn-primary" onclick="restart()">重新开始</button></div></div></div><script>const Q={qjs};let cur=0,sc=0,ans=false;function show(){{const q=Q[cur];document.getElementById('question').textContent=(cur+1)+'. '+q.q;document.getElementById('options').innerHTML='';q.opts.forEach((o,i)=>{{const b=document.createElement('button');b.className='option';b.textContent=o;b.onclick=()=>check(i);document.getElementById('options').appendChild(b)}});document.getElementById('progress').style.width=(cur/Q.length*100)+'%';document.getElementById('score').textContent='得分: '+sc+' / '+cur;document.getElementById('nextBtn').style.display='none';ans=false}}function check(i){{if(ans)return;ans=true;const q=Q[cur],os=document.querySelectorAll('.option');os.forEach((o,j)=>{{o.classList.add('disabled');if(j===q.ans)o.classList.add('correct');if(j===i&&j!==q.ans)o.classList.add('wrong')}});if(i===q.ans)sc++;if(q.exp){{const d=document.createElement('div');d.style.cssText='margin-top:12px;padding:12px;background:var(--bg);border-radius:8px;color:#8b949e;font-size:.9em';d.textContent=q.exp;document.getElementById('options').appendChild(d)}}document.getElementById('score').textContent='得分: '+sc+' / '+(cur+1);document.getElementById('nextBtn').style.display='inline-block'}}function nextQ(){{cur++;if(cur>=Q.length){{document.getElementById('game').classList.add('hidden');document.getElementById('result').classList.remove('hidden');const p=Math.round(sc/Q.length*100);let t='太棒了！';if(p<60)t='继续加油！';else if(p<80)t='不错哦！';document.getElementById('resultTitle').textContent=t;document.getElementById('resultText').textContent='最终得分: '+sc+'/'+Q.length+' ('+p+'%)'}}else show()}}function restart(){{cur=0;sc=0;document.getElementById('game').classList.remove('hidden');document.getElementById('result').classList.add('hidden');show()}}show();</script></body></html>'''

def timeline_html(title, subtitle, events):
    edata = json.dumps(events, ensure_ascii=False)
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>{DARK_CSS}</style></head><body><div class="container"><h1>{title}</h1><p class="subtitle">{subtitle}</p><div class="card" id="game"><div class="score" id="score">已排对: 0 / 0</div><p style="text-align:center;color:#8b949e;margin:8px 0">将事件按时间顺序排列，点击正确的下一个事件</p><div id="events"></div><div style="text-align:center;margin-top:12px"><button class="btn btn-outline" onclick="showAnswer()">显示答案</button></div></div><div class="card hidden" id="result"><div class="result"><h2 id="resultTitle"></h2><p id="resultText" style="margin:12px 0;color:#8b949e"></p><div id="answerList"></div><br><button class="btn btn-primary" onclick="restart()">重新开始</button></div></div></div><script>const E={edata};let cur=0,correct=0,sh=[];function shuffle(){{sh=E.map((e,i)=>({{...e,idx:i}}));for(let i=sh.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[sh[i],sh[j]]=[sh[j],sh[i]]}}}}function show(){{const rem=sh.filter(e=>!e.done);document.getElementById('events').innerHTML=rem.map(e=>`<div class="quiz-card" onclick="pick(${{e.idx}})" id="card-${{e.idx}}"><span class="order-num">${{e.idx+1}}</span><span class="year-label">${{e.year}}</span><div class="event-text">${{e.text}}</div></div>`).join('');document.getElementById('score').textContent='已排对: '+correct+' / '+E.length}}function pick(idx){{if(idx===cur){{correct++;const c=document.getElementById('card-'+idx);if(c){{c.classList.add('correct');c.style.pointerEvents='none'}}cur++;document.getElementById('score').textContent='已排对: '+correct+' / '+E.length;if(correct===E.length)setTimeout(finish,500)}}else{{const c=document.getElementById('card-'+idx);if(c){{c.classList.add('wrong');setTimeout(()=>c.classList.remove('wrong'),800)}}}}function showAnswer(){{document.getElementById('game').classList.add('hidden');document.getElementById('result').classList.remove('hidden');document.getElementById('resultTitle').textContent='完整时间线';document.getElementById('answerList').innerHTML='<div class="timeline">'+E.map(e=>`<div class="timeline-item"><div class="timeline-year">${{e.year}}</div><div class="timeline-text">${{e.text}}</div></div>`).join('')+'</div>'}}function finish(){{document.getElementById('game').classList.add('hidden');document.getElementById('result').classList.remove('hidden');document.getElementById('resultTitle').textContent='排序完成！';document.getElementById('resultText').textContent='全部事件已按正确顺序排列';document.getElementById('answerList').innerHTML='<div class="timeline">'+E.map(e=>`<div class="timeline-item"><div class="timeline-year">${{e.year}}</div><div class="timeline-text">${{e.text}}</div></div>`).join('')+'</div>'}}function restart(){{cur=0;correct=0;shuffle();document.getElementById('game').classList.remove('hidden');document.getElementById('result').classList.add('hidden');show()}}shuffle();show();</script></body></html>'''

def write_tool(name, html):
    path = os.path.join(TOOLS_DIR, name)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

def write_index():
    tools = [
        ('word-search-cn', '中文找单词', '在汉字网格中找出隐藏的词语'),
        ('anagram-cn', '中文变位词', '将打乱的汉字重新排列成正确的词语'),
        ('word-scramble-cn', '中文文字拼图', '猜猜被打乱的文字是什么'),
        ('hangman-cn', '中文猜词', '猜测隐藏的中文词语'),
        ('quiz-cn', '中文知识问答', '测试你的中文知识储备'),
        ('trivia-cn', '中文百科问答', '挑战你的百科知识'),
        ('history-quiz', '历史问答', '测试你的历史知识'),
        ('science-quiz', '科学问答', '探索科学的奥秘'),
        ('geography-quiz-cn', '中文地理问答', '测试你的地理知识'),
        ('music-quiz-cn', '中文音乐问答', '测试你的音乐知识'),
        ('movie-quiz-cn', '中文电影问答', '测试你的电影知识'),
        ('anime-quiz', '动漫问答', '测试你的动漫知识'),
        ('game-quiz', '游戏问答', '测试你的游戏知识'),
        ('sports-quiz', '体育问答', '测试你的体育知识'),
        ('food-quiz', '美食问答', '测试你的美食知识'),
        ('tech-quiz', '科技问答', '测试你的科技知识'),
        ('nature-quiz', '自然问答', '探索大自然的奥秘'),
        ('art-quiz', '艺术问答', '测试你的艺术知识'),
        ('literature-quiz', '文学问答', '测试你的文学知识'),
        ('philosophy-quiz', '哲学问答', '思考哲学的智慧'),
        ('math-quiz-cn', '中文数学问答', '测试你的数学知识'),
        ('logic-quiz', '逻辑问答', '挑战你的逻辑思维'),
        ('riddle-quiz', '谜语问答', '猜猜这些有趣的谜语'),
        ('idiom-quiz', '成语问答', '测试你的成语知识'),
        ('poem-quiz', '诗词问答', '测试你的古诗词知识'),
        ('history-timeline', '历史时间线', '人类历史的重要时刻'),
        ('world-history', '世界历史', '探索世界历史的重要事件'),
        ('china-history', '中国历史', '探索中国悠久的历史'),
        ('ancient-civilization', '古代文明', '探索古代文明的辉煌'),
        ('medieval-history', '中世纪历史', '探索中世纪的黑暗与辉煌'),
        ('renaissance', '文艺复兴', '探索文艺复兴的艺术与科学'),
        ('enlightenment', '启蒙运动', '探索启蒙运动的思想光芒'),
        ('industrial-revolution', '工业革命', '探索工业革命的变革力量'),
        ('modern-history', '近代历史', '探索近代历史的风云变幻'),
        ('contemporary-history', '当代历史', '探索当代世界的重要事件'),
        ('world-war-1', '第一次世界大战', '探索一战的历史'),
        ('world-war-2', '第二次世界大战', '探索二战的历史'),
        ('cold-war', '冷战', '探索冷战时期的对峙与博弈'),
        ('space-race', '太空竞赛', '探索美苏太空竞赛的历史'),
        ('internet-history', '互联网历史', '探索互联网的发展历程'),
        ('music-history', '音乐历史', '探索音乐的发展历程'),
        ('art-history', '艺术历史', '探索艺术的发展历程'),
        ('architecture-history', '建筑历史', '探索建筑的发展历程'),
        ('fashion-history', '时尚历史', '探索时尚的发展历程'),
        ('food-history', '食物历史', '探索食物的发展历程'),
        ('sport-history', '体育历史', '探索体育的发展历程'),
        ('film-history', '电影历史', '探索电影的发展历程'),
        ('game-history', '游戏历史', '探索电子游戏的发展历程'),
        ('tech-history', '科技历史', '探索科技的发展历程'),
        ('science-history', '科学历史', '探索科学的发展历程'),
        ('china-timeline', '中国时间线', '中国历史的重要时刻'),
        ('world-cup-history', '世界杯历史', '世界杯足球赛的辉煌时刻'),
        ('olympic-history', '奥运会历史', '奥运会的精彩瞬间'),
        ('nobel-history', '诺贝尔奖历史', '诺贝尔奖的重要时刻'),
        ('space-history', '太空历史', '人类探索太空的历程'),
        ('aviation-history', '航空历史', '人类征服天空的历程'),
        ('automotive-history', '汽车历史', '汽车工业的发展历程'),
        ('photography-history', '摄影历史', '摄影技术的发展历程'),
        ('printing-history', '印刷历史', '印刷技术的发展历程'),
        ('communication-history', '通信历史', '通信技术的发展历程'),
        ('energy-history', '能源历史', '能源技术的发展历程'),
        ('medicine-history', '医学历史', '医学的发展历程'),
        ('education-history', '教育历史', '教育的发展历程'),
        ('law-history', '法律历史', '法律的发展历程'),
        ('religion-history', '宗教历史', '宗教的发展历程'),
        ('philosophy-history', '哲学历史', '哲学的发展历程'),
        ('economics-history', '经济学历史', '经济学的发展历程'),
        ('politics-history', '政治历史', '政治的发展历程'),
        ('military-history', '军事历史', '军事的发展历程'),
        ('technology-timeline', '科技时间线', '科技发展的重要时刻'),
        ('invention-timeline', '发明时间线', '改变世界的发明'),
        ('discovery-timeline', '发现时间线', '科学发现的重要时刻'),
        ('exploration-timeline', '探险时间线', '人类探险的重要时刻'),
        ('art-timeline', '艺术时间线', '艺术发展的重要时刻'),
        ('music-timeline', '音乐时间线', '音乐发展的重要时刻'),
        ('film-timeline', '电影时间线', '电影发展的重要时刻'),
        ('game-timeline', '游戏时间线', '电子游戏发展的重要时刻'),
        ('sports-timeline', '体育时间线', '体育发展的重要时刻'),
        ('fashion-timeline', '时尚时间线', '时尚发展的重要时刻'),
        ('food-timeline', '食物时间线', '食物发展的重要时刻'),
        ('science-timeline', '科学时间线', '科学发展的重要时刻'),
        ('medicine-timeline', '医学时间线', '医学发展的重要时刻'),
        ('education-timeline', '教育时间线', '教育发展的重要时刻'),
        ('politics-timeline', '政治时间线', '政治发展的重要时刻'),
        ('economics-timeline', '经济学时间线', '经济学发展的重要时刻'),
        ('military-timeline', '军事时间线', '军事发展的重要时刻'),
        ('space-timeline', '太空时间线', '太空探索的重要时刻'),
        ('aviation-timeline', '航空时间线', '航空发展的重要时刻'),
        ('automotive-timeline', '汽车时间线', '汽车发展的重要时刻'),
        ('communication-timeline', '通信时间线', '通信发展的重要时刻'),
        ('energy-timeline', '能源时间线', '能源发展的重要时刻'),
        ('environment-timeline', '环境时间线', '环境发展的重要时刻'),
        ('society-timeline', '社会时间线', '社会发展的重要时刻'),
        ('culture-timeline', '文化时间线', '文化发展的重要时刻'),
        ('religion-timeline', '宗教时间线', '宗教发展的重要时刻'),
        ('philosophy-timeline', '哲学时间线', '哲学发展的重要时刻'),
        ('law-timeline', '法律时间线', '法律发展的重要时刻'),
        ('medicine-timeline', '医学时间线', '医学发展的重要时刻'),
        ('education-timeline-cn', '中国教育时间线', '中国教育发展的重要时刻'),
        ('china-tech-timeline', '中国科技时间线', '中国科技发展的重要时刻'),
    ]
    tools_json = json.dumps(tools, ensure_ascii=False)
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>游戏工具合集</title><style>
:root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--accent:#3b82f6}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}}
h1{{text-align:center;font-size:2em;margin:20px 0;background:linear-gradient(135deg,var(--accent),#10b981);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.subtitle{{text-align:center;color:#8b949e;margin-bottom:24px}}
.search{{width:100%;max-width:500px;margin:0 auto 24px;display:block;padding:12px 16px;background:var(--card);border:2px solid var(--border);border-radius:8px;color:var(--text);font-size:1em}}
.search:focus{{outline:none;border-color:var(--accent)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;max-width:1200px;margin:0 auto}}
.card-link{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px;text-decoration:none;color:var(--text);transition:all .2s}}
.card-link:hover{{border-color:var(--accent);transform:translateY(-2px)}}
.card-link h3{{font-size:1em;margin-bottom:4px}}
.card-link p{{font-size:.85em;color:#8b949e}}
</style></head><body><h1>游戏工具合集</h1><p class="subtitle">100个中文游戏工具，无需网络，即开即玩</p><input class="search" id="search" placeholder="搜索游戏..." oninput="filter()"><div id="app"></div><script>
const T={tools_json};
function filter(){{const q=document.getElementById('search').value.toLowerCase();render(T.filter(t=>t[1].toLowerCase().includes(q)||t[0].includes(q)||t[2].includes(q)))}}
function render(list){{document.getElementById('app').innerHTML='<div class="grid">'+list.map(t=>`<a class="card-link" href="${{t[0]}}/index.html"><h3>${{t[1]}}</h3><p>${{t[2]}}</p></a>`).join('')+'</div>'}}
render(T);
</script></body></html>'''
    with open(os.path.join(TOOLS_DIR, 'games-index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    print('Part 1 loaded OK')
