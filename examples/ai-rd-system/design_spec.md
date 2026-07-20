# AI双引擎产品智能研发体系 - Design Spec

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | AI双引擎产品智能研发体系 |
| **Canvas Format** | PPT 16:9 (1920×1080) |
| **Page Count** | 39 |
| **Design Style** | 字节产品感：明亮、克制、高信息密度的产品战略叙事 |
| **Target Audience** | 产品负责人、研发管理层、业务决策者 |
| **Use Case** | 跨境服饰 AI 研发战略升级汇报 |
| **Created Date** | 2026-07-20 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1920×1080 |
| **viewBox** | `0 0 1920 1080` |
| **Margins** | 左右 80px；顶部 64px；底部 48px |
| **Content Area** | 1760×840px，标题与内容清晰分区 |

---

## III. Visual Theme

### Theme Style

- **Style**: 字节产品感的产品战略汇报，不采用泛科技霓虹或厚重融资路演风格。
- **Theme**: Light theme。
- **Tone**: 清醒、效率导向、模块化、可追溯。
- **Visual language**: 冷白画布、深墨文字、极细分隔线、蓝紫系统主线；创新通道使用青色，爆款通道使用橙色。

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#F7F8FA` | 页面底色 |
| **Secondary bg** | `#FFFFFF` | 内容面板与卡片 |
| **Primary** | `#1664FF` | 标题、系统主线、关键状态 |
| **Accent** | `#6A4CFF` | 结构强调、渐变过渡 |
| **Explore accent** | `#00B8D9` | 创新/探索通道 |
| **Utilize accent** | `#FF8A34` | 爆款/利用通道 |
| **Body text** | `#161823` | 标题与主信息 |
| **Secondary text** | `#4E5969` | 正文与说明 |
| **Tertiary text** | `#86909C` | 注释、页脚 |
| **Border/divider** | `#E5E6EB` | 分隔与低强调边界 |
| **Success** | `#00B42A` | 正向状态 |
| **Warning** | `#F53F3F` | 风险、问题与终止状态 |

### Gradient Scheme

系统强调可使用 `#1664FF → #6A4CFF` 的轻量线性渐变；大面积背景仅用于封面、章节和结尾，正文页不得用渐变替代信息层级。

---

## IV. Typography System

### Font Plan

**Typography direction**: modern CJK sans，中文优先，数字紧凑清晰。

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `Microsoft YaHei` | `Arial` | `sans-serif` |
| **Body** | `Microsoft YaHei` | `Arial` | `sans-serif` |
| **Emphasis** | `Microsoft YaHei` | `Arial` | `sans-serif` |
| **Code** | — | `Consolas, Courier New` | `monospace` |

- Title: `"Microsoft YaHei", Arial, sans-serif`
- Body: `"Microsoft YaHei", Arial, sans-serif`
- Emphasis: `"Microsoft YaHei", Arial, sans-serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 20px。

| Purpose | Size | Weight |
| ------- | ---- | ------ |
| Cover title | 104px | Heavy |
| Chapter opener | 84px | Bold |
| Page title | 44px | Bold |
| Hero number | 56px | Heavy |
| Subtitle | 26px | SemiBold |
| Body content | 20px | Regular |
| Annotation | 15px | Regular |
| Page number | 13px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 页眉标签、英文模块名与 44px 结论式标题。
- **Content area**: 以流程、对比、产品看板、分层架构为主；内容宽度随信息权重变化。
- **Footer area**: 细分隔线、章节名与页码；保持低对比。

### Layout Principles

1. 每页先给出结论，再给出结构与支撑信息；标题不复述图形。
2. 同章统一组件语言，跨章切换内容布局，避免 39 页全部是卡片栅格。
3. 创新与爆款通道始终以青/橙标识，但正文主色只使用蓝紫系统色。
4. 卡片仅承载并列信息；关键结论、章节过渡、循环与终局页使用裸文本、留白或全幅视觉。
5. 圆角 12px，边框 1px，阴影仅在浮层使用；信息优先于装饰。

### Spacing Specification

| Element | Current Project |
| ------- | --------------- |
| Safe margin from canvas edge | 80px |
| Content block gap | 24–36px |
| Icon-text gap | 10px |
| Card gap | 16–24px |
| Card padding | 24–32px |
| Card border radius | 12px |

---

## VI. Icon Usage Specification

- **Source**: 本项目现有 Lucide 图标，统一为 1.8px 线性描边。
- **Approach**: 每个功能模块最多一个图标；图标仅作定位标记，不作为装饰性重复元素。
- **Core semantics**: target、telescope、wrench、workflow、database、shield、archive、chart、rocket。

---

## VII. Visualization Reference List

| Visualization Type | Reference Template | Used In |
| ------------------ | ------------------ | ------- |
| `process_flow` | `templates/charts/process_flow.svg` | 05, 10, 16, 27, 28 |
| `comparison_columns` | `templates/charts/comparison_columns.svg` | 09, 30, 34, 35, 37 |
| `radar_chart` | `templates/charts/radar_chart.svg` | 24 |
| `kpi_cards` | `templates/charts/kpi_cards.svg` | 13, 17, 25, 38 |
| `layered_architecture` | `templates/charts/layered_architecture.svg` | 22, 32 |
| `cycle_diagram` | `templates/charts/cycle_diagram.svg` | 05, 27, 32 |
| `matrix_2x2` | `templates/charts/matrix_2x2.svg` | 06, 37 |

---

## VIII. Image Resource List

| Filename | Purpose | Type | Status |
| -------- | ------- | ---- | ------ |
| `assets/cover_bg.jpg` | 首页全幅背景 | Background | Existing |
| `assets/chapter_problem.jpg` | 第一章视觉背景 | Background | Existing |
| `assets/chapter_engine.jpg` | 第二章视觉背景 | Background | Existing |
| `assets/chapter_score.jpg` | 第三章视觉背景 | Background | Existing |
| `assets/ai_trend_intelligence_4x3.jpg` | 趋势洞察情境图 | Illustration | Existing |
| `assets/technical_architecture_4x3.jpg` | 技术架构情境图 | Illustration | Existing |
| `assets/agent_workflow_4x3.jpg` | Agent 协同情境图 | Illustration | Existing |
| `assets/decision_pool_dashboard_4x3.jpg` | 决策池情境图 | Illustration | Existing |
| `assets/closing_bg.jpg` | 结束页背景 | Background | Existing |

---

## IX. Content Outline

### Part 1: 认知破局

| Slide | Layout / Focus |
| ----- | -------------- |
| 01 | 全幅封面；产品 OS 定位与一句价值承诺。 |
| 02 | 章节目录；7 个章节以轻量导航列表呈现。 |
| 03 | 第一章全幅章节页；问题诊断引入。 |
| 04 | 垂直问题清单；五个底层问题按严重度排布。 |
| 05 | 闭环流程；从单一逻辑到战略停滞的因果链。 |
| 06 | 2×2 问题—机制—价值矩阵。 |
| 07 | 三项核心价值；战略、效率、资产沉淀。 |

### Part 2: 核心体系

| Slide | Layout / Focus |
| ----- | -------------- |
| 08 | 第二章章节页；双路径洞察体系。 |
| 09 | 创新/爆款两栏对比；保留青橙通道。 |
| 10 | 创新五层横向阶段流。 |
| 11 | 趋势洞察；场景图 + 三段产品化洞察。 |
| 12 | 需求洞察；采集维度到需求字段库。 |
| 13 | 缺口洞察；溯源流程 + 供需空白指标。 |
| 14 | 竞品趋势；可用、规避、错位三类结论。 |
| 15 | 创新定型；产品参数模型。 |
| 16 | 爆款五层横向阶段流。 |
| 17 | 爆款识别；数据维度到资质矩阵。 |
| 18 | DNA 拆解；产品基因组模块。 |
| 19 | 因果需求；优势、缺陷、付费痛点。 |
| 20 | 竞品超车；复用、整改、微创新策略。 |
| 21 | 爆款定型；优化参数模型。 |
| 22 | 双引擎数据融合；分层架构。 |

### Part 3: 工程化打分

| Slide | Layout / Focus |
| ----- | -------------- |
| 23 | 第三章章节页；分层量化评审。 |
| 24 | 双模型权重雷达图；突出权重差异。 |
| 25 | 四级决策；从重仓到终止的投资动作。 |

### Part 4: 流程对比

| Slide | Layout / Focus |
| ----- | -------------- |
| 26 | 第四章章节页；单链路与双引擎对照。 |
| 27 | 传统缺陷闭环；风险导向视觉。 |
| 28 | 双引擎标准流程；Agent 协同和回流。 |

### Part 5: 企业研发闭环

| Slide | Layout / Focus |
| ----- | -------------- |
| 29 | 第五章章节页；从机会到研发资产。 |
| 30 | 双机会池；两类字段体系对照。 |
| 31 | 统一决策池；汇聚、评分、优先级。 |
| 32 | 研发飞轮；探索、利用、防御三层闭环。 |

### Part 6: 终审与归档

| Slide | Layout / Focus |
| ----- | -------------- |
| 33 | 第六章章节页；终审与资产化。 |
| 34 | 分层风控；创新款与爆款款分别审查。 |
| 35 | 标准归档；两条证据链沉淀。 |

### Part 7: 体系复盘

| Slide | Layout / Focus |
| ----- | -------------- |
| 36 | 第七章章节页；体系终复盘。 |
| 37 | 终局对比；五个关键能力升级。 |
| 38 | 六大目标；价值闭环。 |
| 39 | 全幅结尾；收束产品 OS 价值。 |

---

## X. Speaker Notes Requirements

- 保留每页对应的讲稿编号与现有页序。
- 风格：专业但口语化，先给结论，再补充页面证据。
- 关键页面需给出自然转场：问题 → 体系 → 打分 → 流程 → 闭环 → 风控 → 价值。

---

## XI. Technical Constraints Reminder

1. 前端预览以 SVG 为准，须同步 39 页 `svg_final/`。
2. SVG 使用 `viewBox="0 0 1920 1080"`，不使用 `foreignObject`。
3. 透明效果使用 opacity，不使用 `rgba()`；页面中避免外部 CSS 依赖。
4. 字体使用 PPT 安全字体栈；核心文本保持可编辑 SVG text。
5. 页面信息与 HTML 源稿保持一致，优化布局不改变业务结论。
