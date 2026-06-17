#!/usr/bin/env python3
import os, json, random
random.seed(42)

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# Import generators
import sys
sys.path.insert(0, TOOLS_DIR)
from _gen_part1 import (DARK_CSS, js_str, js_list, quiz_html, timeline_html,
                         write_tool, write_index)

# ===== Word Search =====
WORD_SEARCH_WORDS = [
    '春天','夏天','秋天','冬天','中国','北京','上海','深圳',
    '大学','小学','中学','老师','学生','同学','朋友','家人',
    '快乐','幸福','健康','美丽','聪明','勇敢','善良','温柔',
    '苹果','香蕉','葡萄','西瓜','草莓','橙子','柠檬','芒果',
    '电脑','手机','电视','空调','冰箱','洗衣机','自行车','汽车'
]

def gen_word_search():
    size = 12
    grid = [['']*size for _ in range(size)]
    dirs = [(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(1,-1),(-1,1)]
    placed = []
    for word in WORD_SEARCH_WORDS[:20]:
        for _ in range(100):
            d = random.choice(dirs)
            r = random.randint(0, size-1)
            c = random.randint(0, size-1)
            ok = True
            for i, ch in enumerate(word):
                nr, nc = r+d[0]*i, c+d[1]*i
                if nr<0 or nr>=size or nc<0 or nc>=size: ok=False; break
                if grid[nr][nc] not in ('', ch): ok=False; break
            if ok:
                for i, ch in enumerate(word):
                    grid[r+d[0]*i][c+d[1]*i] = ch
                placed.append(word)
                break
    chars = '的一是了不在有个人这中大为上以到说时要就出会也你对生能子那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己法命老世位同特之类后整合通竞件期工号处总'
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(chars)
    
    grid_json = json.dumps(grid, ensure_ascii=False)
    words_json = json.dumps(placed, ensure_ascii=False)
    
    gs = size
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>中文找单词</title><style>{DARK_CSS}.grid-cn{{display:grid;grid-template-columns:repeat({gs},1fr);gap:2px;margin:16px 0}}.cell-cn{{aspect-ratio:1;display:flex;align-items:center;justify-content:center;background:var(--bg);border:1px solid var(--border);border-radius:4px;font-size:clamp(10px,2.5vw,16px);cursor:pointer;transition:all .2s;user-select:none}}.cell-cn:hover{{border-color:var(--accent)}}.cell-cn.sel{{background:rgba(59,130,246,.2);border-color:var(--accent)}}.cell-cn.found{{background:rgba(34,197,94,.2);border-color:var(--success);color:var(--success)}}.word-tag{{display:inline-block;padding:6px 12px;background:var(--bg);border:1px solid var(--border);border-radius:20px;font-size:.9em;margin:4px}}.word-tag.found{{background:rgba(34,197,94,.15);border-color:var(--success);color:var(--success);text-decoration:line-through}}</style></head><body><div class="container"><h1>中文找单词</h1><p class="subtitle">在汉字网格中找出隐藏的词语</p><div class="card"><div class="score" id="score">已找到: 0 / {len(placed)}</div><div class="grid-cn" id="grid"></div><div id="words" style="text-align:center"></div><div style="text-align:center"><button class="btn btn-primary" onclick="init()">重新生成</button></div></div></div><script>const G={grid_json};const W={words_json};let found=new Set(),sel=[];function init(){{document.getElementById('grid').innerHTML='';for(let i=0;i<G.length;i++)for(let j=0;j<G[i].length;j++){{const c=document.createElement('div');c.className='cell-cn';c.textContent=G[i][j];c.onclick=()=>pick(c);document.getElementById('grid').appendChild(c)}}document.getElementById('words').innerHTML=W.map(w=>'<span class="word-tag" id="w-'+w+'">'+w+'</span>').join('');found=new Set();sel=[];upd()}}function pick(c){{if(c.classList.contains('found'))return;if(sel.includes(c)){{c.classList.remove('sel');sel=sel.filter(s=>s!==c)}}else{{c.classList.add('sel');sel.push(c)}}if(sel.length>=2)check()}}function check(){{const t=sel.map(c=>c.textContent).join('');for(const w of W){{if(!found.has(w)&&(t===w||t===w.split('').reverse().join(''))){{found.add(w);sel.forEach(c=>{{c.classList.remove('sel');c.classList.add('found')}});const e=document.getElementById('w-'+w);if(e)e.classList.add('found');upd();if(found.size===W.length)setTimeout(()=>alert('恭喜！全部找到！'),300);break}}}}sel=[];document.querySelectorAll('.cell-cn.sel').forEach(c=>c.classList.remove('sel'))}}function upd(){{document.getElementById('score').textContent='已找到: '+found.size+' / '+W.length}}init();</script></body></html>'''
    write_tool('word-search-cn', html)

# ===== Anagram =====
def gen_anagram():
    words = ['学习','音乐','飞机','电话','花朵','星星','月亮','太阳','地球',
             '海洋','森林','河流','城市','国家','世界','历史','科学','技术',
             '文化','艺术','体育','电影','电视','网络']
    pairs = []
    for w in words:
        chars = list(w)
        random.shuffle(chars)
        s = ''.join(chars)
        while s == w and len(w) > 1:
            random.shuffle(chars)
            s = ''.join(chars)
        pairs.append({'o': w, 's': s})
    pairs_json = json.dumps(pairs, ensure_ascii=False)
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>中文变位词</title><style>{DARK_CSS}.scrambled{{font-size:2em;text-align:center;letter-spacing:8px;margin:20px 0;color:var(--accent);font-weight:700}}.input-row{{display:flex;gap:8px;justify-content:center;margin:16px 0}}</style></head><body><div class="container"><h1>中文变位词</h1><p class="subtitle">将打乱的汉字重新排列成正确的词语</p><div class="card" id="game"><div class="score" id="score">得分: 0 / 0</div><div class="progress-bar"><div class="progress-fill" id="progress"></div></div><div class="scrambled" id="scrambled"></div><div class="input-row"><input class="input" id="answer" placeholder="输入正确的词语" style="max-width:300px" onkeypress="if(event.key==='Enter')check()"><button class="btn btn-primary" onclick="check()">确认</button></div><button class="btn btn-outline" onclick="skip()" style="margin-top:8px">跳过</button><div id="fb" style="text-align:center;margin-top:12px"></div></div><div class="card hidden" id="result"><div class="result"><h2 id="rt"></h2><p id="rx" style="margin:12px 0;color:#8b949e"></p><button class="btn btn-primary" onclick="restart()">重新开始</button></div></div></div><script>const P={pairs_json};let cur=0,sc=0,done=false;function show(){{const p=P[cur];document.getElementById('scrambled').textContent=p.s;document.getElementById('answer').value='';document.getElementById('answer').focus();document.getElementById('fb').innerHTML='';document.getElementById('progress').style.width=(cur/P.length*100)+'%';document.getElementById('score').textContent='得分: '+sc+' / '+cur;done=false}}function check(){{if(done)return;const v=document.getElementById('answer').value.trim(),p=P[cur];done=true;if(v===p.o){{sc++;document.getElementById('fb').innerHTML='<span style="color:var(--success)">正确！</span>'}}else{{document.getElementById('fb').innerHTML='<span style="color:var(--danger)">正确答案: '+p.o+'</span>'}}document.getElementById('score').textContent='得分: '+sc+' / '+(cur+1);setTimeout(next,1200)}}function skip(){{if(done)return;done=true;document.getElementById('fb').innerHTML='<span style="color:#8b949e">答案: '+P[cur].o+'</span>';setTimeout(next,1200)}}function next(){{cur++;if(cur>=P.length){{document.getElementById('game').classList.add('hidden');document.getElementById('result').classList.remove('hidden');const p=Math.round(sc/P.length*100);document.getElementById('rt').textContent=p>=80?'太棒了！':'继续加油！';document.getElementById('rx').textContent='最终得分: '+sc+'/'+P.length+' ('+p+'%)'}}else show()}}function restart(){{cur=0;sc=0;document.getElementById('game').classList.remove('hidden');document.getElementById('result').classList.add('hidden');show()}}show();</script></body></html>'''
    write_tool('anagram-cn', html)

# ===== Word Scramble =====
def gen_word_scramble():
    words = ['春天','夏天','秋天','冬天','北京','上海','大学','老师',
             '学生','快乐','幸福','健康','美丽','聪明','勇敢','音乐',
             '飞机','电话','花朵','星星','月亮','太阳','地球','海洋',
             '电脑','手机','汽车','森林','河流','城市','国家','世界']
    game_words = random.sample(words, 15)
    words_json = json.dumps(game_words, ensure_ascii=False)
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>中文文字拼图</title><style>{DARK_CSS}</style></head><body><div class="container"><h1>中文文字拼图</h1><p class="subtitle">猜猜被打乱的文字是什么</p><div class="card" id="game"><div class="score" id="score">得分: 0 / 0</div><div class="progress-bar"><div class="progress-fill" id="progress"></div></div><p style="text-align:center;color:#8b949e" id="hint"></p><div class="answer-slots" id="slots"></div><div class="puzzle-chars" id="chars"></div><div style="text-align:center"><button class="btn btn-primary" onclick="submit()">确认</button> <button class="btn btn-outline" onclick="clearSlots()">清除</button> <button class="btn btn-outline" onclick="skip()">跳过</button></div></div><div class="card hidden" id="result"><div class="result"><h2 id="rt"></h2><p id="rx" style="margin:12px 0;color:#8b949e"></p><button class="btn btn-primary" onclick="restart()">重新开始</button></div></div></div><script>const W={words_json};let cur=0,sc=0,slots=[],used=[];function show(){{const w=W[cur],cs=w.split('');for(let i=cs.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[cs[i],cs[j]]=[cs[j],cs[i]]}}document.getElementById('hint').textContent=w.length+'个字的词语';document.getElementById('slots').innerHTML=Array(w.length).fill(0).map((_,i)=>'<div class="answer-slot" onclick="rmSlot('+i+')"></div>').join('');document.getElementById('chars').innerHTML=cs.map((c,i)=>'<div class="puzzle-char" data-c="'+c+'" data-i="'+i+'" onclick="pickChar(this)">'+c+'</div>').join('');document.getElementById('progress').style.width=(cur/W.length*100)+'%';slots=[];used=[]}}function pickChar(el){{if(el.classList.contains('placed'))return;if(slots.length>=W[cur].length)return;slots.push({{c:el.dataset.c,i:el.dataset.i}});el.classList.add('placed');updSlots()}}function rmSlot(i){{if(i>=slots.length)return;const r=slots.splice(i,1)[0];document.querySelectorAll('.puzzle-char').forEach(c=>{{if(c.dataset.i===r.i&&c.dataset.c===r.c)c.classList.remove('placed')}});updSlots()}}function updSlots(){{document.querySelectorAll('.answer-slot').forEach((s,i)=>{{if(i<slots.length){{s.textContent=slots[i].c;s.classList.add('filled')}}else{{s.textContent='';s.classList.remove('filled')}}}})}}function submit(){{const ans=slots.map(s=>s.c).join('');if(ans===W[cur]){{sc++;fb(true,'正确！')}}else{{fb(false,'正确答案: '+W[cur])}}setTimeout(next,1200)}}function fb(ok,msg){{const d=document.createElement('div');d.style.cssText='text-align:center;margin-top:12px;font-size:1.1em;color:'+(ok?'var(--success)':'var(--danger)');d.textContent=(ok?' ':' ')+msg;document.getElementById('game').appendChild(d)}}function skip(){{fb(false,'答案: '+W[cur]);setTimeout(next,1200)}}function next(){{cur++;if(cur>=W.length){{document.getElementById('game').classList.add('hidden');document.getElementById('result').classList.remove('hidden');const p=Math.round(sc/W.length*100);document.getElementById('rt').textContent=p>=80?'太棒了！':'继续加油！';document.getElementById('rx').textContent='最终得分: '+sc+'/'+W.length+' ('+p+'%)'}}else show()}}function restart(){{cur=0;sc=0;document.getElementById('game').classList.remove('hidden');document.getElementById('result').classList.add('hidden');show()}}show();</script></body></html>'''
    write_tool('word-scramble-cn', html)

# ===== Quiz Data =====
def load_quiz_data():
    with open(os.path.join(TOOLS_DIR, '_quiz_data.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def gen_all_quizzes():
    data = load_quiz_data()
    for name, qdata in data.items():
        html = quiz_html(qdata['title'], qdata['subtitle'], qdata['questions'])
        write_tool(name, html)

# ===== Timeline Data =====
def load_timeline_data():
    with open(os.path.join(TOOLS_DIR, '_timeline_data.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def gen_all_timelines():
    data = load_timeline_data()
    for name, tdata in data.items():
        html = timeline_html(tdata['title'], tdata['subtitle'], tdata['events'])
        write_tool(name, html)

if __name__ == '__main__':
    gen_word_search()
    print('1/100 word-search-cn')
    gen_anagram()
    print('2/100 anagram-cn')
    gen_word_scramble()
    print('3/100 word-scramble-cn')
    gen_all_quizzes()
    print('25/100 quizzes done')
    gen_all_timelines()
    print('75/100 timelines done')
    write_index()
    print('100/100 + index done')
    print('All 100 tools created!')
