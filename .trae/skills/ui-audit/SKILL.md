---
name: "ui-audit"
description: "Audits web tool UI across 4 dimensions: consistency, anti-AI-flavor, usability, info architecture. Invoke when reviewing tool page aesthetics or before UI refactors."
---

# UI 审美审查 (UI Aesthetic Audit)

对单个 Web 工具页执行四维审美审查：**一致性 / 反 AI 味 / 可用性 / 信息架构**。输出标准化评分、问题清单与可执行优化建议。

## 何时调用
- 用户要求审查某工具页 UI 是否可优化
- 用户在批量重构工具页前需要先评估当前状态
- 用户对某页面"AI 味儿太重"提出抱怨后定位具体问题
- 用户问"这个工具页设计怎么样"

## 审查前置：环境与工具
- 必须先加载 `TRAE-browseruse` skill（用于截图、DOM 提取、computed style 读取）
- 浏览器尺寸：默认 1280×800（桌面）+ 375×700（移动端），各取一张截图
- 通过 `browser_evaluate` 提取关键样式（color palette、font stack、shadow count 等）
- 工具页路径模式：`/tools/<tool-name>/index.html`

## 四维准则与检查清单

### 维度 1：一致性 (Consistency) — 25 分
检查整页是否遵循统一设计系统：

- [ ] 主色板 ≤ 3 个语义色（primary / success / danger / warning 之外不滥用）
- [ ] 字体栈单一（≤ 2 个 font-family），中文字号阶梯 ≤ 4 级
- [ ] 间距使用 4/8 网格（4/8/12/16/24/32/48），不出现 13px、17px、22px 这类非网格值
- [ ] 圆角统一（按钮 / 卡片 / 输入框圆角值一致，不混用 4px 与 16px）
- [ ] 阴影层级 ≤ 3 级，不出现 5+ 种不同阴影
- [ ] 按钮主/次/三级样式清晰，不出现 6 种以上按钮变体
- [ ] hover/focus 反馈一致（同类型元素同种 hover 效果）

**扣分项**：每条不达标 -3 分，最低 0 分。

### 维度 2：反 AI 味 (Anti-AI-Flavor) — 25 分
检查是否落入"AI 生成默认审美"陷阱。**任一项命中即记为该维度不达标，整维度 ≤ 10 分**：

- [ ] **禁**：紫色（#7c3aed / #8b5cf6 / indigo→pink）渐变作为主色或标题文字
- [ ] **禁**：玻璃态卡片（`backdrop-filter: blur` + 半透明白底 + 1px 半透明边框）占页面卡片总数 > 30%
- [ ] **禁**：标题或按钮带 text-shadow 发光效果（neon glow）
- [ ] **禁**：emoji 作为主要功能图标（按钮文字、CTA、导航项里直接出现 emoji 替代 SVG icon）
- [ ] **禁**：所有区块一律居中布局 + 大留白，没有信息层级差异
- [ ] **禁**：3 列等高 feature 卡片网格（emoji + 标题 + 一行描述）作为主要信息组织方式
- [ ] **禁**：营销话术文案（"⚡ Supercharge"、"🚀 一键"、"赋能"、"闭环"、"重塑"）
- [ ] **禁**：Inter / Geist 字体 + slate 灰阶 + violet 强调色的 Tailwind UI 默认组合
- [ ] **禁**：与当前工具任务无关的"装饰性 hero"（大渐变标题 + 副标题 + 两个 CTA 按钮，但工具本体在第二屏）

**判定原则**：清单命中即记不达标，不做主观降分；命中 0 项给 25 分，命中 1-2 项给 10-15 分，命中 3+ 项给 0-5 分。

### 维度 3：可用性 (Usability / A11y) — 25 分
基础可访问性与键盘可达性（WCAG 2.1 AA 为底线）：

- [ ] 文字与背景对比度 ≥ 4.5:1（关键文字 ≥ 7:1），用 `browser_evaluate` 取 computed color + bg color 后查 WCAG 表
- [ ] 所有交互元素键盘可达（Tab 顺序合理，无键盘陷阱）
- [ ] focus 状态可见（outline 不为 0；或自定义 focus ring 对比度 ≥ 3:1）
- [ ] 表单 input 都关联 label（`<label for>` 或 `aria-label`）
- [ ] 按钮文案是动词短语（"提交"/"复制"），不是 emoji 或图标单独
- [ ] 错误提示文案明确（不出现 "Error"、"发生错误" 等无信息量文本）
- [ ] 空状态有引导（无数据时给出"如何产生数据"提示，不是空白）
- [ ] 移动端点击目标 ≥ 44×44px

**扣分项**：每条不达标 -3 分，最低 0 分。

### 维度 4：信息架构 (Information Architecture) — 25 分
布局是否服务于用户任务：

- [ ] 一屏内能识别"这是什么工具 + 主要操作在哪"
- [ ] 主要 CTA（提交/生成/复制按钮）在视觉权重上突出（颜色 / 大小 / 位置）
- [ ] 输入区与输出区分明（左右/上下分割清晰，不混乱）
- [ ] 操作流符合工具任务心智模型（输入 → 处理 → 输出顺序自然）
- [ ] 不出现与当前工具无关的装饰区块（如无关的工具站横幅、广告位）
- [ ] 长内容有滚动锚点或分段标题
- [ ] 工具结果可复制 / 可下载（提供明确的"复制"按钮）

**扣分项**：每条不达标 -3.5 分，最低 0 分。

## 评分汇总
每个维度 0-25 分，总分 100：

| 维度分数段 | 含义 |
|---|---|
| 0-9 | 严重问题，必须重构 |
| 10-17 | 有明显短板，可针对性优化 |
| 18-22 | 基本达标，少量改进点 |
| 23-25 | 优秀，无需改动 |

**总分门槛**：
- < 60 分：建议重构
- 60-75 分：建议针对性优化
- 76-85 分：可选择性优化
- \> 85 分：维持现状

## 执行流程

1. 加载 `TRAE-browseruse` skill
2. `browser_navigate` 到目标工具页 URL，`browser_wait_for({ time: 2 })` 等待渲染
3. `browser_take_screenshot` 取桌面 + 移动各一张截图（参考用，主观判断时辅以 snapshot）
4. `browser_evaluate` 单次调用提取以下信息（一次拿全，避免多轮）。注意：emoji 检测用 `codePointAt` 而非正则字面量（避免沙箱转义问题）；排除 `i18n.js` 注入的浮动组件（id 以 `garyy-` 开头），它们是全局 UI 不算工具本体问题：
   ```javascript
   JSON.stringify({
     title: document.title,
     body_bg: getComputedStyle(document.body).backgroundColor,
     primary_color: getComputedStyle(document.querySelector('button, .btn, [class*="primary"]') || document.body).color,
     font_stack: getComputedStyle(document.body).fontFamily,
     button_count: document.querySelectorAll('button').length,
     input_count: document.querySelectorAll('input, textarea').length,
     emoji_in_tool_buttons: Array.from(document.querySelectorAll('button')).filter(b => !b.id.startsWith('garyy-') && !b.closest('#garyy-feedback')).filter(b => Array.from(b.textContent).some(ch => { var c = ch.codePointAt(0); return c >= 0x1F300 && c <= 0x1FAFF; })).length,
     emoji_in_title: /[\u{1F300}-\u{1FAFF}]/u.test(document.querySelector('h1')?.textContent || ''),
     backdrop_blur_count: Array.from(document.querySelectorAll('*')).filter(el => getComputedStyle(el).backdropFilter.includes('blur')).length,
     text_shadow_count: Array.from(document.querySelectorAll('h1,h2,h3,button,a')).filter(el => getComputedStyle(el).textShadow !== 'none').length,
     gradient_count: Array.from(document.querySelectorAll('*')).filter(el => /gradient/i.test(getComputedStyle(el).backgroundImage)).length,
     gradient_sources: Array.from(document.querySelectorAll('*')).filter(el => /gradient/i.test(getComputedStyle(el).backgroundImage)).slice(0,3).map(el => ({tag:el.tagName, cls:String(el.className).slice(0,40), bg:getComputedStyle(el).backgroundImage.slice(0,80)})),
     outline_none_count: Array.from(document.querySelectorAll('a,button,input,textarea')).filter(el => getComputedStyle(el).outlineStyle === 'none').length
   })
   ```
5. `browser_snapshot` 获取页面结构（取 interactive 元素，用于信息架构判断）
6. 对照四维清单逐项判定，命中即记录
7. 输出报告（见下）

## 报告格式（严格遵守）

```markdown
## UI 审查报告：<工具名>

**总评**：xx/100 ｜ 一致性 xx/25 ｜ 反AI味 xx/25 ｜ 可用性 xx/25 ｜ 信息架构 xx/25

### 关键问题（按优先级排序）
1. [维度名] <问题描述> - <位置/DOM 选择器>
   建议：<具体修复方向，写到 CSS 属性或 DOM 结构层级，不要"优化样式"等空话>

2. ...

### 维度详情

#### 一致性 (xx/25)
- ✅ <达标项>
- ❌ <不达标项 + 证据：computed style 值>

#### 反 AI 味 (xx/25)
- ✅ <未命中项>
- ❌ <命中项 + 证据：颜色值/选择器>

#### 可用性 (xx/25)
- ✅ <达标项>
- ❌ <不达标项 + 证据>

#### 信息架构 (xx/25)
- ✅ <达标项>
- ❌ <不达标项 + 证据>

### 优化建议（按优先级排序）
1. **高优先级**：<具体动作> - <预期效果>
2. **中优先级**：...
3. **低优先级**：...
```

## 注意事项
- "AI 味儿"判断有主观性，**清单命中即记不达标**，不靠主观降分；这样保证多次审查结果一致
- 一致性问题以"是否影响用户认知"为判定依据，吹毛求疵的微小差异（如 16px vs 14px 行高）不算不达标
- 可用性以 WCAG 2.1 AA 为底线，AAA 级不强制
- 报告里建议**必须可执行**（具体到改哪个 CSS 属性 / 哪个 DOM 结构），不要"建议优化样式"这类空话
- 单工具页审查 ≤ 5 次 tool call（navigate + screenshot + evaluate + snapshot + report），避免冗余
- 批量审查（>5 个工具）应分批进行，每批 3-5 个，避免上下文过长导致判断质量下降
