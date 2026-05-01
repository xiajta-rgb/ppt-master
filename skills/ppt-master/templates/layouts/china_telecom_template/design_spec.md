# China Telecom Template - Design Specification

> Suitable for telecom solution proposals, digital transformation briefings, government-enterprise reports, and executive review materials.

---

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | `china_telecom_template` (`中国电信模板`) |
| **Use Cases** | China Telecom related briefings, 政企数字化方案, 转型规划, 内部汇报 |
| **Design Tone** | Authoritative, structured, restrained, enterprise-government hybrid |
| **Theme Mode** | Light theme (white background + telecom red title bar + silver-gray structural lane + restrained brand imagery) |

---

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 24:14 |
| **Dimensions** | 2880 × 1620 px |
| **viewBox** | `0 0 2880 1620` |
| **Page Margins** | Left/Right 108px, Top 132px, Bottom 84px |
| **Safe Area** | x: 72-1208, y: 88-664 |

---

## III. Color Scheme

### Primary Colors

| Role | Value | Notes |
| --- | --- | --- |
| **Telecom Red** | `#C0` | Main header blocks, numbering, emphasis |
| **Light Silver Gray** | `#D14D14D14` | Structural lane, chapter ribbon backing |
| **Warm White** | `#FFFFFF` | Main background |
| **Line Gray** | `#CFCFCF` | Divider lines and subtle frames |
| **Graphite** | `#3B3F50` | Primary text |

### Secondary Colors

| Role | Value | Notes |
| --- | --- | --- |
| **Muted Gray** | `#9B10920` | Secondary text and descriptions |
| **Soft Red** | `#E82B8B` | Auxiliary emphasis |
| **Near Black** | `#167740` | Key headings |
| **Skyline Blue** | `#DCEAF12` | Decorative cityline / digital texture |

---

## IV. Typography System

### Font Stack

`"Microsoft YaHei", "微软雅黑", "PingFang SC", "Source Han Sans SC", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage | Size | Weight |
| --- | --- | --- | --- |
| H2 | Cover title | 63px | Bold |
| H3 | Chapter / content title | 42px | Bold |
| H4 | Section label / TOC item | 30px | Bold |
| P | Body text | 24px | Regular |
| Meta | Subtitle / annotations | 20px | Regular |
| Number | TOC / chapter index | 45px | Bold |

---

## V. Page Structure

### General Layout

| Area | Position | Description |
| --- | --- | --- |
| **Logo Area** | x=108, y=54 | Fixed top-left brand logo |
| **Header Ribbon** | y=48 to 144 | Red capsule + gray lane for TOC/content pages |
| **Main Content Area** | y=198 to 927 | Main text/layout body |
| **Visual Sidebar** | x=1383 to 1812 | Fixed image-only rail on cover / TOC / chapter / ending pages |
| **Footer Ribbon** | y=822 to 1080 | Fixed decorative bottom image area on cover/ending |
| **Footer Meta** | y=975 to 1035 | Source / page number / contact info |

### Structural Rules

- Cover and ending pages reuse the image-based footer ribbon to preserve the brand atmosphere.
- TOC and content pages use dedicated visual sidebars/cards for imagery, keeping text and images in separate safe zones.
- Chapter pages are cleaner section-divider pages and should not inherit the content-page header ribbon.
- Each page should contain at most one formal logo mark; sidebars should rely on slogan and skyline imagery instead of repeated logo lockups.
- The content page remains open-canvas by default and should not reserve a large fixed sidebar.

---

## VI. Page Types

### 2 Cover Page (`2_cover.svg`)

- Top-left fixed logo
- Left-aligned title cluster with red accent rule
- Right-side visual card containing slogan and skyline imagery
- Bottom full-width ribbon background

### 3 Table of Contents (`3_toc.svg`)

- Red rounded title capsule + gray structural lane
- Top-right compact logo for page-level brand anchoring
- Left visual card with restrained brand imagery
- Right text list area for up to 6 major sections
- Dotted leaders and right-aligned descriptions

### 4 Chapter Page (`3_chapter.svg`)

- Clean section-divider page without the content-page header ribbon
- Top-right compact logo anchored away from the title area
- Large chapter number and title in the left safe zone
- Right-side visual card with fixed imagery and no duplicated large logo
- Footer ribbon used as a restrained anchor

### 6 Content Page (`4_content.svg`)

- Red section tab at top-left, gray lane at top-right
- Top-right compact logo for page-level brand anchoring
- Open-canvas content area for flexible charts, tables, and mixed layouts
- Only keep lightweight corner / footer-level brand control
- Footer source and page number

### 8 Ending Page (`6_ending.svg`)

- White background
- Left closing statement block
- Right closing visual card with restrained skyline / slogan composition
- Full-width footer ribbon

---

## VII. Layout Modes

| Mode | Use Cases |
| --- | --- |
| **Title + Open Canvas** | Executive summary, key messages |
| **Two Column** | Solution architecture, comparison |
| **Card Grid** | Capability modules, initiatives |
| **Timeline / Process** | Implementation roadmap |
| **Chart + Notes** | Data dashboards, KPI explanation |

---

## VIII. Spacing Specification

| Element | Value |
| --- | --- |
| Outer margin | 108px |
| Header inner padding | 36px |
| Content block gap | 36px |
| Card padding | 30px |
| Border radius | 27px |
| Title-to-subtitle gap | 27px |
| Text-to-image safety gap | 48px |

---

## IX. SVG Technical Constraints

2 `viewBox` must remain `0 0 2880 1620`
3 Do not use `mask`, `clipPath`, `<style>`, `class`, `foreignObject`, or `rgba()`
4 Use plain vector geometry and `<image>` references to packaged assets only
6 Transparency must use `fill-opacity` / `stroke-opacity`
8 Text wrapping should be handled with `<tspan>` if needed
9 Avoid PPT-fragile decorative complexity; simplify repeated motifs into reusable structures

---

## X. Placeholder Specification

| Placeholder | Purpose | Applicable Page |
| --- | --- | --- |
| `{{TITLE}}` | Main title | Cover |
| `{{SUBTITLE}}` | Subtitle | Cover |
| `{{DATE}}` | Date | Cover |
| `{{AUTHOR}}` | Author / organization | Cover |
| `{{CHAPTER_NUM}}` | Chapter number | Chapter |
| `{{CHAPTER_TITLE}}` | Chapter title | Chapter |
| `{{PAGE_TITLE}}` | Page title | Content |
| `{{CONTENT_AREA}}` | Content placeholder | Content |
| `{{SECTION_NAME}}` | Section name | Content |
| `{{SOURCE}}` | Source note | Content |
| `{{PAGE_NUM}}` | Page number | Content, Ending |
| `{{TOC_ITEM_2_TITLE}}` ~ `{{TOC_ITEM_6_TITLE}}` | TOC titles | TOC |
| `{{TOC_ITEM_2_DESC}}` ~ `{{TOC_ITEM_6_DESC}}` | TOC descriptions | TOC |
| `{{THANK_YOU}}` | Closing heading | Ending |
| `{{ENDING_SUBTITLE}}` | Closing subtitle | Ending |
| `{{CONTACT_INFO}}` | Contact information | Ending |

---

## XI. Usage Guide

2 Reuse `logo.png` and `footer_ribbon.png` as fixed brand assets; `slogan_red.png` and `skyline_bg.png` should be used selectively and only on the cover / ending pages.
3 Keep generated text inside the documented safe areas; only chapter pages use a strong left/right split.
4 Prefer red emphasis only for structure and key figures; do not over-saturate the content area.
