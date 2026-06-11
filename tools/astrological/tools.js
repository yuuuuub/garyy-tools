/**
 * 占星学工具 - JavaScript
 */

// 星座日期范围
const zodiacDates = {
    '白羊座': { start: [3, 21], end: [4, 19], symbol: '♈' },
    '金牛座': { start: [4, 20], end: [5, 20], symbol: '♉' },
    '双子座': { start: [5, 21], end: [6, 21], symbol: '♊' },
    '巨蟹座': { start: [6, 22], end: [7, 22], symbol: '♋' },
    '狮子座': { start: [7, 23], end: [8, 22], symbol: '♌' },
    '处女座': { start: [8, 23], end: [9, 22], symbol: '♍' },
    '天秤座': { start: [9, 23], end: [10, 23], symbol: '♎' },
    '天蝎座': { start: [10, 24], end: [11, 22], symbol: '♏' },
    '射手座': { start: [11, 23], end: [12, 21], symbol: '♐' },
    '摩羯座': { start: [12, 22], end: [1, 19], symbol: '♑' },
    '水瓶座': { start: [1, 20], end: [2, 18], symbol: '♒' },
    '双鱼座': { start: [2, 19], end: [3, 20], symbol: '♓' }
};

// 查询星座
function checkZodiac() {
    const month = parseInt(document.getElementById('birth-month')?.value?.split('-')[1]) || 0;
    const day = parseInt(document.getElementById('birth-day')?.value) || 0;
    const result = document.getElementById('zodiac-result');
    const symbol = document.getElementById('zodiac-symbol');
    const name = document.getElementById('zodiac-name');

    if (!month || !day || day < 1 || day > 31) {
        alert('请输入有效的日期');
        return;
    }

    let zodiac = '';
    for (const [name, dates] of Object.entries(zodiacDates)) {
        const [startMonth, startDay] = dates.start;
        const [endMonth, endDay] = dates.end;

        if (startMonth === endMonth) {
            if (month === startMonth && day >= startDay && day <= endDay) {
                zodiac = name;
                break;
            }
        } else if (startMonth < endMonth) {
            if ((month === startMonth && day >= startDay) || (month === endMonth && day <= endDay)) {
                zodiac = name;
                break;
            }
        } else {
            if ((month === startMonth && day >= startDay) || (month === endMonth && day <= endDay) || month === 12 || month === 1) {
                zodiac = name;
                break;
            }
        }
    }

    if (zodiac && result && symbol && name) {
        symbol.textContent = zodiacDates[zodiac].symbol;
        name.textContent = zodiac;
        result.classList.remove('hidden');
    } else {
        alert('无法确定星座，请检查日期');
    }
}

// 行星符号记忆游戏
const planets = [
    { symbol: '☉', name: '太阳' },
    { symbol: '☽', name: '月亮' },
    { symbol: '☿', name: '水星' },
    { symbol: '♀', name: '金星' },
    { symbol: '♂', name: '火星' },
    { symbol: '♃', name: '木星' },
    { symbol: '♄', name: '土星' },
    { symbol: '♅', name: '天王星' },
    { symbol: '♆', name: '海王星' },
    { symbol: '♇', name: '冥王星' }
];

let memoryGameCards = [];
let flippedCards = [];
let matches = 0;

function startMemoryGame() {
    const game = document.getElementById('memory-game');
    const score = document.getElementById('game-score');
    
    if (game && score) {
        game.classList.remove('hidden');
        score.classList.remove('hidden');
        game.innerHTML = '';
        matches = 0;
        flippedCards = [];
        
        // 选择5个行星
        const selected = planets.slice(0, 5).sort(() => Math.random() - 0.5);
        memoryGameCards = [...selected, ...selected].sort(() => Math.random() - 0.5);
        
        memoryGameCards.forEach((planet, index) => {
            const card = document.createElement('div');
            card.className = 'memory-card cursor-pointer';
            card.dataset.index = index;
            card.innerHTML = `
                <div class="memory-card-inner">
                    <div class="memory-card-front bg-indigo-600 rounded-lg p-4 h-24 flex items-center justify-center">
                        <span class="text-3xl">?</span>
                    </div>
                    <div class="memory-card-back bg-gray-800 rounded-lg p-4 h-24 flex flex-col items-center justify-center">
                        <span class="text-3xl mb-1">${planet.symbol}</span>
                        <span class="text-xs text-gray-400">${planet.name}</span>
                    </div>
                </div>
            `;
            card.addEventListener('click', () => flipCard(index));
            game.appendChild(card);
        });
        
        document.getElementById('matches').textContent = '0';
    }
}

function flipCard(index) {
    const card = document.querySelector(`[data-index="${index}"]`);
    if (!card || card.classList.contains('flipped') || flippedCards.length >= 2) return;
    
    card.classList.add('flipped');
    flippedCards.push({ index, planet: memoryGameCards[index] });
    
    if (flippedCards.length === 2) {
        setTimeout(() => {
            const [first, second] = flippedCards;
            if (first.planet.symbol === second.planet.symbol) {
                matches++;
                document.getElementById('matches').textContent = matches;
                if (matches === 5) {
                    setTimeout(() => alert('恭喜！你完成了游戏！'), 300);
                }
            } else {
                document.querySelector(`[data-index="${first.index}"]`).classList.remove('flipped');
                document.querySelector(`[data-index="${second.index}"]`).classList.remove('flipped');
            }
            flippedCards = [];
        }, 1000);
    }
}

// 占星学小测验
const quizQuestions = [
    {
        question: '太阳在占星学中代表什么？',
        options: ['情绪和感受', '核心自我和身份认同', '沟通方式', '行动力'],
        correct: 1
    },
    {
        question: '哪个星座是火象星座？',
        options: ['巨蟹座', '天秤座', '白羊座', '双鱼座'],
        correct: 2
    },
    {
        question: '第一宫（上升点）代表什么？',
        options: ['家庭', '自我形象和个性', '事业', '人际关系'],
        correct: 1
    },
    {
        question: '三分相的角度是多少？',
        options: ['60°', '90°', '120°', '180°'],
        correct: 2
    },
    {
        question: '哪个行星代表沟通和思维？',
        options: ['水星', '金星', '火星', '木星'],
        correct: 0
    }
];

let currentQuestion = 0;
let quizScore = 0;

function startQuiz() {
    const container = document.getElementById('quiz-container');
    if (container) {
        container.classList.remove('hidden');
        currentQuestion = 0;
        quizScore = 0;
        showQuestion();
    }
}

function showQuestion() {
    if (currentQuestion >= quizQuestions.length) {
        showQuizResult();
        return;
    }
    
    const question = quizQuestions[currentQuestion];
    const questionEl = document.getElementById('quiz-question');
    const optionsEl = document.getElementById('quiz-options');
    const progressEl = document.getElementById('quiz-progress');
    const resultEl = document.getElementById('quiz-result');
    
    if (questionEl) questionEl.textContent = question.question;
    if (optionsEl) {
        optionsEl.innerHTML = question.options.map((option, index) => `
            <button onclick="selectAnswer(${index})" 
                    class="w-full text-left bg-gray-800 hover:bg-gray-700 text-white p-3 rounded-lg transition-colors">
                ${String.fromCharCode(65 + index)}. ${option}
            </button>
        `).join('');
    }
    if (progressEl) progressEl.textContent = currentQuestion + 1;
    if (resultEl) resultEl.classList.add('hidden');
}

function selectAnswer(selected) {
    const question = quizQuestions[currentQuestion];
    const resultEl = document.getElementById('quiz-result');
    const optionsEl = document.getElementById('quiz-options');
    
    if (selected === question.correct) {
        quizScore++;
        if (resultEl) {
            resultEl.className = 'mt-4 p-4 bg-green-900 text-green-200 rounded-lg';
            resultEl.textContent = '✓ 回答正确！';
        }
    } else {
        if (resultEl) {
            resultEl.className = 'mt-4 p-4 bg-red-900 text-red-200 rounded-lg';
            resultEl.textContent = `✗ 回答错误。正确答案是: ${question.options[question.correct]}`;
        }
    }
    
    if (resultEl) resultEl.classList.remove('hidden');
    if (optionsEl) {
        const buttons = optionsEl.querySelectorAll('button');
        buttons.forEach((btn, index) => {
            btn.disabled = true;
            if (index === question.correct) {
                btn.classList.add('bg-green-800');
            } else if (index === selected && index !== question.correct) {
                btn.classList.add('bg-red-800');
            }
        });
    }
    
    currentQuestion++;
    setTimeout(() => showQuestion(), 2000);
}

function showQuizResult() {
    const container = document.getElementById('quiz-container');
    if (container) {
        container.innerHTML = `
            <div class="text-center">
                <h3 class="text-2xl font-semibold text-white mb-4">测验完成！</h3>
                <div class="text-4xl font-bold text-indigo-400 mb-4">${quizScore}/${quizQuestions.length}</div>
                <p class="text-gray-300 mb-4">你答对了 ${quizScore} 道题</p>
                <button onclick="location.reload()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg transition-colors">
                    重新开始
                </button>
            </div>
        `;
    }
}

