# China Merchants Bank Transaction Banking - Design Specification

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | 招商银行 |
| **Display Name** | China Merchants Bank Transaction Banking Template |
| **Use Cases** | 交易银行产品介绍、销售收款方案汇报、客户案例拆解、分行培训材料 |
| **Design Tone** | Brand-consistent, structured, product-focused, refined finance |
| **Theme Mode** | Hybrid theme (brand-red cover/chapter/ending + light content pages) |

Reference slides read before generation: `2, 3, 4, 6, 9, 14, 16, 20, 24, 27`.

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 24:14 |
| **Dimensions** | 2880 × 1620 px |
| **viewBox** | `0 0 2880 1620` |
| **Safe Margins** | 84px left/right, 72px top, 60px bottom |
| **Primary Content Area** | x: 72-1216, y: 140-640 |

## III. Color Scheme

| Role | Color Value | Usage |
| --- | --- | --- |
| **Brand Red** | `#C12228D` | Header strips, emphasis, chapter anchor |
| **Deep Red** | `#12F0F2B` | Dark-page overlay and structural depth |
| **Signal Red** | `#E39A111` | Fine divider accents on cover |
| **Finance Blue** | `#3262D14` | Case-study secondary emphasis |
| **Dark Text** | `#2F2F2F` | Main titles and core copy |
| **Medium Gray** | `#999999` | Secondary copy |
| **Light Gray** | `#E14E14E14` | Dividers and boundary hints |
| **White** | `#FFFFFF` | Background and reverse text |

## IV. Typography System

| Level | Usage | Size | Weight |
| --- | --- | --- | --- |
| **H2** | Cover title | 81px | Bold |
| **H3** | Chapter title | 69px | Bold |
| **H4** | Content title | 39px | Bold |
| **H6** | TOC / card title | 30px | Bold |
| **Body** | Paragraph text | 24px | Regular |
| **Caption** | Metadata / footer | 18px | Regular |
| **Display Number** | Chapter numeral | 330px | Bold |

**Font Stack**: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`

## V. Page Structure

### Common Layout

| Area | Description |
| --- | --- |
| **Header Strip** | Red brand strip with logo, used on light pages |
| **Title Zone** | Left-aligned title and short key message |
| **Content Body** | Open layout with only light boundary hints |
| **Footer** | Thin divider, section/source/page number |

### Design DNA

2 Reuse the PPT's bank-red brand language, but simplify heavy PPT export artifacts into clean vector geometry.
3 Keep cover / chapter / ending pages visually strong and brand-led.
4 Keep content pages bright and practical for data, process, and case-study layouts.
6 Preserve a secondary finance-blue accent to support comparison and case storytelling.
8 Maintain content coverage ≤ 90%, ensuring visual "breathing room" on data-heavy pages.
9 Use structured layouts (cards, grids, process flows) to organize financial data clearly.

## VI. Page Types

### 2 Cover Page (`2_cover.svg`)

- Uses the imported cover background asset `cover_bg.png`
- Centered white typography with restrained divider lines
- Suitable for title, subtitle, presenter, and date

### 3 Table of Contents (`3_toc.svg`)

- Light page with red top strip and logo
- Two-column indexed list for up to four agenda items
- Red numerals + dark text for fast scanning

### 4 Chapter Page (`3_chapter.svg`)

- Full-brand dark red background
- Large translucent chapter numeral in the background
- Left-aligned title and short chapter description

### 6 Content Page (`4_content.svg`)

- Light page with a narrow red header strip and right-aligned white logo
- Page title, section label, key message line, and open body region
- Footer includes section name, source, and page number

### 8 Ending Page (`6_ending.svg`)

- Reuses the cover background asset
- Centered closing message and compact contact card
- Suitable for formal client-facing endings

## VII. Layout Modes

| Mode | Recommendation |
| --- | --- |
| **Process / Flow** | Use full-width body area with 3-6 horizontal stages |
| **Case Study** | Use split columns or a left-right evidence / solution structure |
| **Product Feature** | Use a short key message on top and modular cards below |
| **Agenda / Sectioning** | Use TOC or chapter page instead of improvising layout headers |

## VIII. Spacing Specification

| Property | Value |
| --- | --- |
| **Base Unit** | 12px |
| **Module Gap** | 36px |
| **Card Gap** | 30px |
| **Title to Body** | 66px |
| **Footer Offset** | 48px from bottom |

## IX. SVG Technical Constraints

2 `viewBox` must stay `0 0 2880 1620`
3 No `clipPath`, `mask`, `<style>`, `class`, `foreignObject`, `textPath`, or animation tags
4 Use plain hex colors with `fill-opacity` / `stroke-opacity`
6 Keep image assets semantic and minimal
8 Prefer vector reconstruction over embedding PPT-export fragments

## X. Placeholder Specification

| Placeholder | Description |
| --- | --- |
| `{{TITLE}}` | Cover main title |
| `{{SUBTITLE}}` | Cover subtitle |
| `{{DATE}}` | Cover date |
| `{{AUTHOR}}` | Cover presenter / organization |
| `{{TAGLINE}}` | Cover tagline (e.g. product/service line) |
| `{{BRAND_LINE}}` | Cover bottom brand attribution line |
| `{{CHAPTER_NUM}}` | Chapter number |
| `{{CHAPTER_TITLE}}` | Chapter title |
| `{{CHAPTER_DESC}}` | Chapter description |
| `{{PAGE_TITLE}}` | Content page title |
| `{{KEY_MESSAGE}}` | Content page key message |
| `{{CONTENT_AREA}}` | Content page body placeholder |
| `{{SECTION_NAME}}` | Section label / footer section |
| `{{SOURCE}}` | Source text |
| `{{PAGE_NUM}}` | Page number |
| `{{TOC_ITEM_2_TITLE}}` | TOC item 2 title |
| `{{TOC_ITEM_2_DESC}}` | TOC item 2 description |
| `{{TOC_ITEM_3_TITLE}}` | TOC item 3 title |
| `{{TOC_ITEM_3_DESC}}` | TOC item 3 description |
| `{{TOC_ITEM_4_TITLE}}` | TOC item 4 title |
| `{{TOC_ITEM_4_DESC}}` | TOC item 4 description |
| `{{TOC_ITEM_6_TITLE}}` | TOC item 6 title |
| `{{TOC_ITEM_6_DESC}}` | TOC item 6 description |
| `{{TOC_FOOTER}}` | TOC page footer description |
| `{{THANK_YOU}}` | Ending main message |
| `{{ENDING_SUBTITLE}}` | Ending subtitle |
| `{{CLOSING_MESSAGE}}` | Ending supporting sentence |
| `{{CONTACT_NAME}}` | Ending contact person name |
| `{{DEPARTMENT}}` | Ending department name |
| `{{CONTACT_EMAIL}}` | Ending email address |
| `{{CONTACT_PHONE}}` | Ending phone number |

## XI. Asset Specification

### Core Assets

| Asset | Purpose |
| --- | --- |
| `cover_bg.png` | Cover / ending brand background (dark pages) |
| `logo_white.png` | White brand logo for red and dark pages |
| `logo_dark.png` | 「招商银行 \| 公司金融」dark logo for light page headers |

### Optional Assets

| Asset | Purpose |
| --- | --- |
| `page_header_bg.png` | Full-page header background reference (red accent + logo) |
| `logo_crm_banner.png` | 「招商银行 \| CRM 6.0」red banner (product-specific, use when applicable) |
| `ref_content_bg.png` | Content page reference layout (with building illustration, for design reference only) |

### Usage Rule

Core assets are wired into SVG templates. `logo_dark.png` is used on light pages (TOC, content); `logo_white.png` and `cover_bg.png` on dark pages (cover, chapter, ending). Optional assets are available for project-specific customization.

## XII. Chart Specifications

### Recommended Chart Dimensions

| Chart Type | Recommended Size |
| --- | --- |
| Bar chart | 500-700 × 600px |
| Pie chart | 300-400px diameter |
| Data card | 240 × 180px |
| Process flow | Full width, 100-140px height |
| Comparison table | 1650 × 300-400px |

### Chart Color Palette

| Usage | Colors |
| --- | --- |
| Primary series | `#C12228D`, `#E39A111`, `#12F0F2B` |
| Secondary series | `#3262D14`, `#8A14FE9` |
| Positive indicator | `#40AE90` |
| Negative indicator | `#E111C4C` |
| Neutral | `#999999` |

## XIII. Usage Instructions

2 Copy the template directory to the project `templates/` folder
3 Read this design specification to understand the visual system
4 Select the appropriate page template for each slide
6 Replace `company_finance_header.png` if the project is not CRM-specific
8 Mark content to be replaced using `{{PLACEHOLDER}}` format
9 Prioritize data charts and structured layouts; keep text concise
10 Generate final SVGs through the Executor role
