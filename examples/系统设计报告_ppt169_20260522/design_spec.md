# 系统设计报告 - Design Spec

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | 系统设计报告 |
| **Canvas Format** | PPT 16:9 (1920×1080) |
| **Page Count** | 14 |
| **Design Style** | General Consulting |
| **Target Audience** | 企划研发部内部团队 + 管理层决策者 |
| **Use Case** | 系统设计报告汇报，展示全数智化企划研发业务系统的架构、业务域、数据流、缺口分析与实施路径 |
| **Created Date** | 2026-05-22 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1920×1080 |
| **viewBox** | `0 0 1920 1080` |
| **Margins** | Left/Right 60px, Top/Bottom 50px |
| **Content Area** | 1800×980 (60,50 to 1860,1030) |

---

## III. Visual Theme

### Theme Style

- **Style**: General Consulting — "Let data speak"
- **Theme**: Dark theme (deep navy background)
- **Tone**: Tech, professional, modern, data-driven

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#0a0e1a` | Page background (deep navy) |
| **Secondary bg** | `#161d2e` | Card background, section background |
| **Primary** | `#06b6d4` | Title decorations, key sections, icons (Cyan) |
| **Accent** | `#3b82f6` | Data highlights, key information (Blue) |
| **Secondary accent** | `#8b5cf6` | Secondary emphasis, gradient transitions (Violet) |
| **Amber accent** | `#f59e0b` | AMZN system, market intelligence |
| **Emerald accent** | `#10b981` | YFB system, success indicators |
| **Rose accent** | `#f43f5e` | LASEN system, warning indicators |
| **Body text** | `#f1f5f9` | Main body text (light) |
| **Secondary text** | `#94a3b8` | Captions, annotations |
| **Tertiary text** | `#64748b` | Supplementary info, footers |
| **Border/divider** | `#1e293b` | Card borders, divider lines |

### Gradient Scheme

```xml
<linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#06b6d4"/>
  <stop offset="100%" stop-color="#3b82f6"/>
</linearGradient>

<linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#06b6d4"/>
  <stop offset="50%" stop-color="#3b82f6"/>
  <stop offset="100%" stop-color="#8b5cf6"/>
</linearGradient>

<radialGradient id="bgDecor" cx="80%" cy="20%" r="50%">
  <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.08"/>
  <stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/>
</radialGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: Modern CJK sans

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei"`, `"PingFang SC"` | `Arial` | `sans-serif` |
| **Body** | `"Microsoft YaHei"`, `"PingFang SC"` | `Arial` | `sans-serif` |
| **Emphasis** | `SimSun` | `Georgia` | `serif` |
| **Code** | — | `Consolas, "Courier New"` | `monospace` |

**Per-role font stacks**:

- Title: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `Georgia, SimSun, serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 18px (dense content report)

| Purpose | Ratio to body | Size | Weight |
| ------- | ------------- | ---- | ------ |
| Cover title | 2.5-5x | 72px | Bold |
| Chapter opener | 2-2.5x | 42px | Bold |
| Page title | 1.5-2x | 32px | Bold |
| Hero number (KPIs) | 1.5-2x | 36px | Bold |
| Subtitle | 1.2-1.5x | 24px | SemiBold |
| **Body content** | **1x** | **18px** | Regular |
| Annotation / caption | 0.7-0.85x | 14px | Regular |
| Page number / footnote | 0.5-0.65x | 11px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 60px — Page title + chapter label
- **Content area**: 920px — Main content zone
- **Footer area**: 40px — Page number + branding

### Layout Pattern Library

| Pattern | Used In |
| ------- | ------- |
| **Single column centered** | P01 Cover, P14 Conclusion |
| **Three/four column cards** | P03-P04 Subsystems, P07-P08 Domains |
| **Center-radiating** | P05 Architecture diagram |
| **Matrix grid (2×2)** | P13 Tech stack |
| **Top-bottom split** | P09 Data flow |
| **Asymmetric split** | P10 Gap analysis |
| **Z-pattern / waterfall** | P11-P12 Roadmap |

### Spacing Specification

**Universal**:

| Element | Value |
| ------- | ----- |
| Safe margin from canvas edge | 60px |
| Content block gap | 32px |
| Icon-text gap | 12px |

**Card-based layouts**:

| Element | Value |
| ------- | ----- |
| Card gap | 24px |
| Card padding | 24px |
| Card border radius | 12px |
| Single-row card height | 560px |
| Double-row card height | 270px each |
| Three-column card width | 580px each |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `templates/icons/chunk/`
- **Usage method**: Placeholder format `{{icon:chunk/icon-name}}`

### Icon Inventory

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| VOC system | `{{icon:chunk/hexagon}}` | P03 |
| AMZN system | `{{icon:chunk/magnifying-glass}}` | P03 |
| COLOR system | `{{icon:chunk/palette}}` | P03 |
| YFB system | `{{icon:chunk/calculator}}` | P04 |
| LASEN system | `{{icon:chunk/chart-bar}}` | P04 |
| Market intelligence | `{{icon:chunk/radar}}` | P07 |
| Consumer insight | `{{icon:chunk/users}}` | P07 |
| Planning management | `{{icon:chunk/clipboard}}` | P07 |
| Design standard | `{{icon:chunk/eyedropper}}` | P08 |
| Business decision | `{{icon:chunk/arrow-trend-up}}` | P08 |
| Operations feedback | `{{icon:chunk/activity}}` | P08 |
| Data entity | `{{icon:chunk/database}}` | P09 |
| Integration check | `{{icon:chunk/git-merge}}` | P10 |
| Capability check | `{{icon:chunk/shield-check}}` | P10 |
| Phase marker | `{{icon:chunk/target}}` | P11-P12 |
| Core strength | `{{icon:chunk/circle-checkmark}}` | P14 |
| Core challenge | `{{icon:chunk/circle-exclamation}}` | P14 |
| API modules | `{{icon:chunk/layers}}` | P06 |
| Tech stack | `{{icon:chunk/server}}` | P13 |

---

## VII. Visualization Reference List

| Visualization Type | Reference Template | Used In |
| ------------------ | ------------------ | ------- |
| Architecture diagram (custom SVG) | — | P05 |
| Data flow diagram (custom SVG) | — | P09 |
| Progress bar | — | P10 |
| Timeline/roadmap | — | P11-P12 |

---

## VIII. Image Resource List

No images required — pure data/architecture report with SVG diagrams.

---

## IX. Content Outline

### Part 1: 总览

#### Slide 01 - 封面

- **Layout**: Single column centered
- **Title**: 全数智化企划研发业务系统
- **Subtitle**: 系统设计报告 v2.0
- **Info**: LASEN.Digital · 2026.05 · 企划研发部
- **Visual**: Gradient title text, decorative radial glow

#### Slide 02 - 总览

- **Layout**: Center-radiating with KPI cards
- **Title**: 系统总览
- **Content**:
  - 4 KPI hero numbers: 5核心子系统 / 24 API能力模块 / 6业务域覆盖 / 2914品牌色彩体系
  - 一句话定位: 以VOC为轴心，融合亚马逊爬虫、品牌色彩库、利润测算与中台运营分析

### Part 2: 系统解构

#### Slide 03 - 五大子系统解构（上）

- **Layout**: Three-column cards
- **Title**: 五大子系统解构
- **Content**:
  - VOC · 数智化企划设计中心 (Cyan) — 核心中枢，24个API模块
  - AMZN · 亚马逊数据爬虫 (Amber) — 市场情报采集引擎
  - COLOR · 品牌色彩库 (Violet) — 2914色设计标准化体系

#### Slide 04 - 五大子系统解构（下）

- **Layout**: Two-column cards (wider)
- **Content**:
  - YFB · 利润测算与货盘工具 (Emerald) — FBA全链路成本与利润率
  - LASEN · 中台产品表现分析 (Rose) — 运营反馈仪表盘

### Part 3: 架构设计

#### Slide 05 - 一核四翼架构

- **Layout**: Center-radiating architecture diagram
- **Title**: 一核四翼架构设计
- **Content**:
  - VOC核心中枢居中
  - AMZN(左上) / COLOR(右上) / YFB(左下) / LASEN(右下) 环绕
  - 底部统一数据中台
  - 连线标注数据流向

#### Slide 06 - VOC 24 API模块清单

- **Layout**: Dense table layout
- **Title**: VOC 24 API模块完整清单
- **Content**:
  - 5 KPI numbers: 24模块 / 2榜单 / 2914色 / 10+成本项 / 3分析维度
  - 24行模块表格，按业务层级分组(市场洞察/企划管理/设计研发/成本合同/知识智能/系统支撑)

### Part 4: 业务域

#### Slide 07 - 六大业务域映射（上）

- **Layout**: Three-column domain cards
- **Title**: 六大业务域映射
- **Content**:
  - 01 市场情报域 (Amber) — AMZN爬虫→VOC竞品分析→趋势洞察
  - 02 消费者洞察域 (Cyan) — VOC评论分析→消费者画像→需求挖掘
  - 03 企划管理域 (Blue) — 需求池→产品规划→进度跟踪→月度计划

#### Slide 08 - 六大业务域映射（下）

- **Layout**: Three-column domain cards
- **Content**:
  - 04 设计标准域 (Violet) — COLOR色彩库→VOC色彩调研→灵感关联
  - 05 商业决策域 (Emerald) — VOC成本数据→YFB利润测算→货盘规划
  - 06 运营反馈域 (Rose) — LASEN评分数据→预警监控→迭代优化

### Part 5: 数据流

#### Slide 09 - 产品全生命周期数据流

- **Layout**: Top-bottom split
- **Title**: 产品全生命周期数据流
- **Content**:
  - 上半: 6阶段流程线 (市场洞察→企划立项→设计研发→成本定价→上架运营→运营反馈)
  - 下半: 核心数据实体关系图 (产品/灵感/成本/进度/竞品/表现/面料)

### Part 6: 缺口分析

#### Slide 10 - 集成度与缺口分析

- **Layout**: Asymmetric split (table left, cards right)
- **Title**: 集成度与缺口分析
- **Content**:
  - 左: 系统集成度矩阵表格 (5行4列)
  - 右: 三大断点卡片 (AMZN→VOC 15% / LASEN→VOC 0% / COLOR→VOC 20%)

### Part 7: 实施路径

#### Slide 11 - 实施路径 Phase 1-2

- **Layout**: Z-pattern / waterfall
- **Title**: 实施路径与优先级 (Phase 1-2)
- **Content**:
  - Phase 1 数据打通 (P1 最高优先级): 1.1 AMZN→VOC同步 / 1.2 LASEN→VOC回流 / 1.3 COLOR→VOC打通
  - Phase 2 流程串联 (P2 高优先级): 2.1 内嵌YFB利润计算器 / 2.2 全流程在线化 / 2.3 评分预警自动通知

#### Slide 12 - 实施路径 Phase 3-4

- **Layout**: Z-pattern / waterfall
- **Title**: 实施路径与优先级 (Phase 3-4)
- **Content**:
  - Phase 3 智能升级 (P3 中优先级): 3.1 品类机会自动推荐 / 3.2 爆款预测与补货 / 3.3 RAG知识库全业务 / 3.4 色彩方案推荐
  - Phase 4 平台统一 (P4 长期目标): 4.1 统一数据库 / 4.2 统一前端 / 4.3 统一部署DevOps

### Part 8: 技术栈与结论

#### Slide 13 - 技术栈现状与统一建议

- **Layout**: Matrix grid (2×2)
- **Title**: 技术栈现状与统一建议
- **Content**:
  - 上: 当前5系统技术栈表格 (VOC/AMZN/COLOR/YFB/LASEN × 前端/后端/数据库/部署)
  - 下: 4个统一建议卡片 (统一前端/统一后端/统一数据层/统一部署)

#### Slide 14 - 核心结论

- **Layout**: Single column centered with split cards
- **Title**: 核心结论
- **Content**:
  - 左: 核心优势5条 (业务闭环完整/VOC中枢清晰/色彩体系差异化/自动化扎实/已有集成意识)
  - 右: 核心挑战5条 (数据孤岛/技术栈碎片/缺少统一身份/供应链未覆盖/多平台未扩展)
  - 底部: 核心结论 — 以VOC为统一平台基座，一个入口·一套数据·一个闭环

---

## X. Speaker Notes Requirements

Generate corresponding speaker note files for each page, saved to the `notes/` directory:

- **File naming**: Match SVG names, e.g., `01_封面.md`
- **Content includes**: Script key points, timing cues, transition phrases

---

## XI. Technical Constraints Reminder

### SVG Generation Must Follow:

1. viewBox: `0 0 1920 1080`
2. Background uses `<rect>` elements
3. Text wrapping uses `<tspan>` (`<foreignObject>` FORBIDDEN)
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` FORBIDDEN
5. FORBIDDEN: `mask`, `<style>`, `class`, `foreignObject`
6. FORBIDDEN: `textPath`, `animate*`, `script`
7. `marker-start` / `marker-end` conditionally allowed
8. `clipPath` conditionally allowed only on `<image>` elements

### PPT Compatibility Rules:

- `<g opacity="...">` FORBIDDEN; set on each child element individually
- Image transparency uses overlay mask layer
- Inline styles only; external CSS and `@font-face` FORBIDDEN
