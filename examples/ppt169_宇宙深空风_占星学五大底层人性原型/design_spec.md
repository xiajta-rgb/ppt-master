# astrology_archetypes - Design Spec

> This document is the human-readable design narrative — rationale, audience, style, color choices, content outline. It is read once by downstream roles for context.
>
> The machine-readable execution contract lives in `spec_lock.md` (short form of color / typography / icon / image decisions). Executor re-reads `spec_lock.md` before every SVG page to resist context-compression drift. Keep the two files in sync; if they diverge, `spec_lock.md` wins.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | astrology_archetypes |
| **Canvas Format** | PPT 16:9 (1280×720) |
| **Page Count** | 18 |
| **Design Style** | General Versatile — Dark cosmic theme with gold/blue accents |
| **Target Audience** | 对占星学、心理学、人性分析感兴趣的专业人士 |
| **Use Case** | 学术分享、专业培训、跨学科研究演示 |
| **Created Date** | 2026-04-26 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280×720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | Left/Right: 60px, Top/Bottom: 50px |
| **Content Area** | 1160×620 (x:60-1220, y:50-670) |

---

## III. Visual Theme

### Theme Style

- **Style**: General Versatile — Dark cosmic theme
- **Theme**: Dark theme
- **Tone**: 神秘、学术、专业、跨学科深度

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#0a0e1a` | 深蓝黑页面背景 |
| **Secondary bg** | `#151d35` | 卡片背景 |
| **Primary** | `#c9a84c` | 金色标题、装饰、图标 |
| **Accent** | `#4a7cf7` | 蓝色高亮、关键信息 |
| **Secondary accent** | `#7c5cbf` | 紫色辅助强调 |
| **Body text** | `#e8e6e1` | 浅色正文 |
| **Secondary text** | `#9a98a0` | 注释、说明文字 |
| **Tertiary text** | `#6e6e73` | 占位符文字 |
| **Border/divider** | `#2a3050` | 卡片边框、分割线 |
| **Success** | `#4caf7d` | 绿色积极指标 |
| **Warning** | `#e05555` | 红色警告指标 |
| **Cyan accent** | `#4ac9c9` | 青色辅助强调 |
| **Gold light** | `#e8d48b` | 金色高亮 |
| **Gold dim** | `#8a7234` | 金色暗部 |
| **Blue light** | `#6b9bff` | 蓝色高亮 |
| **Blue dim** | `#2a4a8a` | 蓝色暗部 |
| **Purple light** | `#a78bfa` | 紫色高亮 |
| **Red dim** | `#8a3333` | 红色暗部 |

### Gradient Scheme

```xml
<!-- Title gradient -->
<linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#c9a84c"/>
  <stop offset="50%" stop-color="#e8d48b"/>
  <stop offset="100%" stop-color="#c9a84c"/>
</linearGradient>

<!-- Background decorative gradient -->
<radialGradient id="bgDecor" cx="80%" cy="20%" r="50%">
  <stop offset="0%" stop-color="#c9a84c" stop-opacity="0.12"/>
  <stop offset="100%" stop-color="#c9a84c" stop-opacity="0"/>
</radialGradient>

<!-- Blue accent gradient -->
<radialGradient id="bgDecorBlue" cx="20%" cy="80%" r="40%">
  <stop offset="0%" stop-color="#4a7cf7" stop-opacity="0.08"/>
  <stop offset="100%" stop-color="#4a7cf7" stop-opacity="0"/>
</radialGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: 现代中文无衬线 + 学术衬线标题

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei", "PingFang SC"` | `Georgia` | `serif` |
| **Body** | `"Microsoft YaHei", "PingFang SC"` | `Arial` | `sans-serif` |
| **Emphasis** | `—` | `Georgia` | `serif` |
| **Code** | `—` | `Consolas, "Courier New"` | `monospace` |

**Per-role font stacks**:

- Title: `Georgia, "Microsoft YaHei", "PingFang SC", serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `Georgia, "Times New Roman", serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 18px

| Purpose | Ratio to body | Size | Weight |
| ------- | ------------- | ---- | ------ |
| Cover title (hero headline) | 2.5-5x | 45-90px | Bold/Heavy |
| Chapter / section opener | 2-2.5x | 36-45px | Bold |
| Page title | 1.5-2x | 27-36px | Bold |
| Hero number | 1.5-2x | 27-36px | Bold |
| Subtitle | 1.2-1.5x | 22-27px | SemiBold |
| **Body content** | **1x** | **18px** | **Regular** |
| Annotation / caption | 0.7-0.85x | 13-15px | Regular |
| Page number / footnote | 0.5-0.65x | 9-12px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 60px height — section label + page title
- **Content area**: 560px height — main content (cards, tables, grids)
- **Footer area**: 50px height — page number, subtle divider

### Layout Pattern Library

| Pattern | Suitable Scenarios |
| ------- | ----------------- |
| **Single column centered** | 封面、结论、关键要点 |
| **Symmetric split (5:5)** | 对比内容（左右对照表） |
| **Asymmetric split (3:7 / 2:8)** | 一侧主导 — 图表+说明 |
| **Three/four column cards** | 特性列表、并行要点、模块展示 |
| **Matrix grid (2×2)** | 四象限分类展示 |
| **Full-bleed + floating text** | 封面、章节过渡页 |
| **Negative-space-driven** | 单一核心概念页面 |

### Spacing Specification

**Universal**:

| Element | Recommended Range | Current Project |
| ------- | ---------------- | --------------- |
| Safe margin from canvas edge | 40-60px | 60px |
| Content block gap | 24-40px | 24px |
| Icon-text gap | 8-16px | 12px |

**Card-based layouts**:

| Element | Recommended Range | Current Project |
| ------- | ---------------- | --------------- |
| Card gap | 20-32px | 16px |
| Card padding | 20-32px | 20px |
| Card border radius | 8-16px | 10px |
| Single-row card height | 530-600px | 自适应 |
| Double-row card height | 265-295px each | 自适应 |
| Three-column card width | 360-380px each | 自适应 |

---

## VI. Icon Usage Specification

| Item | Decision |
| ---- | -------- |
| **Icon Source** | Built-in icon library |
| **Library** | `tabler-filled` — 平滑贝塞尔曲线风格，温暖有机感，匹配占星学神秘氛围 |
| **Icon Style** | Fill, rounded contours |

### Icon Inventory

| Icon Name | Purpose | Usage Pages |
| --------- | ------- | ----------- |
| `tabler-filled/star` | 星体、占星符号 | 封面、引言、星体页 |
| `tabler-filled/moon` | 月亮、情感 | 月亮/等级服从页 |
| `tabler-filled/sun` | 太阳、核心 | 太阳/互惠交换页 |
| `tabler-filled/planet` | 行星 | 星体概览页 |
| `tabler-filled/shield` | 保护、边界 | 领域意识页 |
| `tabler-filled/alert-triangle` | 警告、风险 | 损失厌恶页 |
| `tabler-filled/crown` | 权威、等级 | 等级服从页 |
| `tabler-filled/users` | 群体、部落 | 部落归属页 |
| `tabler-filled/handshake` | 交换、契约 | 互惠交换页 |
| `tabler-filled/arrows-exchange` | 流动、交换 | 飞宫理论页 |
| `tabler-connected` | 连接、相位 | 相位理论页 |
| `tabler-filled/layers-intersect` | 交叉、互动 | 相位互动页 |
| `tabler-filled/grid-4` | 四象限 | 四象限页 |
| `tabler-filled/books` | 学术、跨学科 | 跨学科对照页 |
| `tabler-filled/lightbulb` | 洞察、结论 | 结论页 |
| `tabler-filled/home` | 宫位、家庭 | 宫位相关页 |
| `tabler-filled/chart-bar` | 数据、对照 | 对照表页 |
| `tabler-filled/list` | 目录、列表 | 目录页 |
| `tabler-filled/zodiac-aries` | 星座 | 星座相关页 |
| `tabler-filled/compass` | 方向、导航 | 章节页 |

> **Mandatory**: Executor may ONLY use icons from this list. If an icon is missing, find the closest alternative within `tabler-filled` library.

---

## VII. Visualization Reference List

| Page | Visualization Type | Purpose |
| ---- | ----------------- | ------- |
| P02 目录 | `icon_grid` | 五章内容图标网格展示 |
| P03 引言 | `kpi_cards` | 四大模块（星体/星座/宫位/相位）卡片 |
| P04 第一章概览 | `icon_grid` | 五大人性原型图标网格 |
| P05-P09 各人性页 | `vertical_list` | 占星要素与人性对照列表 |
| P10 飞宫概览 | `hub_spoke` | 飞宫理论核心概念辐射图 |
| P11 飞宫-人性 | `comparison_table` | 飞宫与五大人性的对照表 |
| P12 相位类型 | `numbered_steps` | 五种相位的角度与含义 |
| P13 相位-人性 | `comparison_table` | 相位类型与人性互动模式 |
| P14 四象限 | `matrix_2x2` | 四象限分类展示 |
| P15 应用场景 | `vertical_list` | 应用场景列表 |
| P16 跨学科对照 | `comparison_table` | 占星学×心理学×游戏设计对照 |
| P17 结论 | `hub_with_described_spokes` | 五大核心结论辐射图 |

---

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Layout Suggestion | Purpose | Type | Status | Generation Description |
|----------|-----------|-------|-------------------|---------|------|--------|----------------------|
| — | — | — | — | — | — | No images | N/A |

> **Note**: 本项目不使用图片，全部通过SVG图形元素（渐变、几何图形、图标）构建视觉层次。

---

## IX. Content Outline

| Page | Title | Content Summary | Visualization | Page Rhythm |
| ---- | ----- | --------------- | ------------- | ----------- |
| P01 | 封面 | 标题"西方占星学五大底层人性原型体系报告"、副标题、拉丁文"As Above, So Below"、五大标签 | Full-bleed + floating text | breathing |
| P02 | 报告目录 | 五章内容卡片网格：静态映射、飞宫理论、相位理论、四象限、跨学科对照 | icon_grid | dense |
| P03 | 引言 | 核心公理、四大模块卡片（星体/星座/宫位/相位）、核心论点 | kpi_cards | dense |
| P04 | 第一章概览 | 五大底层人性原型卡片：领域意识、损失厌恶、等级服从、部落归属、互惠交换 | icon_grid | dense |
| P05 | 领域意识 | 土星对应关系表、进化心理学对照 | vertical_list | anchor |
| P06 | 损失厌恶 | 火星对应关系表、进化心理学对照 | vertical_list | anchor |
| P07 | 等级服从 | 月亮对应关系表、进化心理学对照 | vertical_list | anchor |
| P08 | 部落归属 | 冥王星对应关系表、进化心理学对照 | vertical_list | anchor |
| P09 | 互惠交换 | 太阳对应关系表、进化心理学对照 | vertical_list | anchor |
| P10 | 飞宫理论概览 | 飞宫核心逻辑表、飞宫与五大人性的关系 | hub_spoke | anchor |
| P11 | 飞宫-五大人性 | 飞宫表现详细对照表 | comparison_table | dense |
| P12 | 相位理论 | 五种相位类型（合相/六分相/四分相/三分相/对分相） | numbered_steps | dense |
| P13 | 相位-五大人性 | 相位类型与人性互动模式对照 | comparison_table | dense |
| P14 | 四象限体系 | 四象限结构表（个体化/家庭/社会/集体） | matrix_2x2 | anchor |
| P15 | 应用场景 | 个人发展、关系咨询、职业规划、团队建设 | vertical_list | breathing |
| P16 | 跨学科对照 | 占星学×进化心理学×社会心理学×游戏设计学三组对照表 | comparison_table | dense |
| P17 | 结论 | 五大核心结论总结、占星学体系本质 | hub_with_described_spokes | breathing |
| P18 | 终 | 感谢阅读 | Full-bleed + floating text | breathing |

---

## X. Speaker Notes Requirements

| Item | Value |
| ---- | ----- |
| **Total Duration** | 约30-40分钟 |
| **Notes Style** | 正式、学术性、跨学科深度 |
| **Presentation Purpose** | Inform + Persuade — 传达占星学作为人性演化心理学模型的核心观点 |
| **File Naming** | `notes/P01_cover.md`, `notes/P02_toc.md`, etc. |
| **Split Rule** | notes/total.md 使用 `#` 标题行，拆分后的文件不包含 `#` 标题行 |

---

## XI. Technical Constraints Reminder

1. **Canvas**: 1280×720, viewBox `0 0 1280 720`
2. **Safe margins**: 60px left/right, 50px top/bottom
3. **Font stacks**: Must end with PPT-safe fallbacks
4. **Icons**: Only `tabler-filled` library, from the approved inventory
5. **Colors**: Only use colors defined in the color scheme
6. **No images**: All visuals via SVG elements (gradients, shapes, icons)
7. **Dark theme**: Background `#0a0e1a`, text `#e8e6e1`
8. **Page rhythm**: Follow `page_rhythm` tags (anchor/dense/breathing)
9. **One theme per page**: Max 4 colors per page
10. **Text contrast**: >= 4.5:1 ratio for all text
