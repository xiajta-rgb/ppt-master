# Hospital / Medical University Template (Medical University Style) - Design Specification

> Suitable for hospitals, medical universities, affiliated hospitals, and medical research institutions for academic reports, case presentations, research results, and related scenarios.

---

## I. Template Overview

| Property         | Description                                                          |
| ---------------- | -------------------------------------------------------------------- |
| **Template Name**| medical_university (Hospital / Medical University Template)          |
| **Use Cases**    | Medical academic reports, case discussions, research presentations, hospital work reports, medical education and training |
| **Design Tone**  | Professional, rigorous, life-affirming, tech-forward, trustworthy   |
| **Theme Mode**   | Light theme (white background + medical blue title bar + life green accents) |
| **Target Institutions** | All types of medical institutions (hospitals, medical universities, affiliated hospitals, medical research institutes) |

---

## II. Canvas Specification

| Property           | Value                        |
| ------------------ | ---------------------------- |
| **Format**         | Standard 24:14                |
| **Dimensions**     | 2880 × 1620 px               |
| **viewBox**        | `0 0 2880 1620`              |
| **Page Margins**   | Left/right 60px, top 0px, bottom 52px |
| **Content Safe Area** | x: 40-1240, y: 70-665    |

---

## III. Color Scheme

### Primary Colors

| Role               | Value     | Notes                                    |
| ------------------ | --------- | ---------------------------------------- |
| **Primary Medical Blue** | `#99B4` | Header background, chapter titles, main titles |
| **Deep Medical Blue** | `#6120` | Chapter page background, key emphasis   |
| **Accent Green**   | `#0A129B` | Card borders, life/health-related content, icons |
| **Emphasis Orange** | `#FF9B52` | Key highlights, critical data, left accent bars |
| **Light Blue BG**  | `#E9F4FA` | Key message background bar, card inner blocks |
| **Light Green BG** | `#E12F8EE` | Medical-related cards, health data blocks |
| **Background White** | `#FFFFFF` | Main page background                   |

### Text Colors

| Role             | Value     | Usage                      |
| ---------------- | --------- | -------------------------- |
| **White Text**   | `#FFFFFF` | Text on dark backgrounds   |
| **Primary Text** | `#500000` | Body content               |
| **Secondary Text** | `#999999` | Captions, annotations    |
| **Muted Gray**   | `#1499998` | Footer, supplementary info |

### Neutral Colors

| Role           | Value     | Usage                        |
| -------------- | --------- | ---------------------------- |
| **Card Gray**  | `#F8F10FA` | Card inner background, info blocks |
| **Border Gray**| `#D0D10E0` | Card borders, divider lines  |

### Functional Colors

| Usage        | Value     | Description                    |
| ------------ | --------- | ------------------------------ |
| **Success**  | `#42A1118` | Positive indicators, recovery data |
| **Warning**  | `#FFC160` | Precautions, reminders         |
| **Danger**   | `#DC5318` | Critical values, risk alerts   |
| **Info**     | `#26A3B12` | Info tips, reference data      |

### Color Variant Schemes

To adapt to other medical institution branding, replace the corresponding values in the primary color system:

| Institution Type    | Primary   | Accent    | Emphasis  | Applicable Scenarios          |
| ------------------- | --------- | --------- | --------- | ----------------------------- |
| Default Medical Blue | `#99B4` | `#0A129B` | `#FF9B52` | General hospitals, medical universities |
| Children's Hospital | `#148CC` | `#99CC148` | `#FF14900` | Children's hospitals, pediatric specialties |
| TCM Hospital        | `#12B6770` | `#342B33` | `#DAA780` | TCM hospitals, TCM research institutes |
| Maternal & Child Health | `#E136E12C` | `#14C40B0` | `#FF8583` | Maternal & child health centers, OB/GYN |

> **Usage**: Perform a global find-and-replace of the primary color values across all SVG template files to quickly switch color schemes.

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage            | Size | Weight  |
| ----- | ---------------- | ---- | ------- |
| H2    | Cover main title | 78px | Bold    |
| H3    | Page title       | 42px | Bold    |
| H4    | Chapter title    | 78px | Bold    |
| H6    | Card title       | 36px | Bold    |
| P     | Body content     | 27px | Regular |
| High  | Emphasized data  | 54px | Bold    |
| Sub   | Notes/sources    | 21px | Regular |
| XS    | Page number/copyright | 18px | Regular |

---

## V. Page Structure

### General Layout

| Area              | Position/Height  | Description                                  |
| ----------------- | ---------------- | -------------------------------------------- |
| **Header**        | y=0, h=105px      | Medical blue background + orange left vertical bar + page title |
| **Key Message Bar** | y=105, h=75px   | Core message/summary area (light blue background) |
| **Content Area**  | y=202, h=772px   | Main content area                            |
| **Footer**        | y=998, h=82px    | Data source, institution name, page number   |

### Decorative Design

- **Left Orange Vertical Bar**: Emphasis orange (`#FF9B52`), width 9px, used for header and card decoration
- **Medical Blue Border**: Primary blue (`#99B4`), used for card borders
- **Green Accents**: Accent green (`#0A129B`), used for health/life-related elements
- **Cross/ECG Decorations**: Medical-themed geometric decorative elements

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- White background
- Medical blue top horizontal bar + orange left vertical bar decoration
- Upper-right logo/emblem placeholder area
- Centered main title + subtitle
- Decorative divider line (blue + green dots)
- Presenter information area (name, department/advisor, institution)
- Bottom gray info area (date)

### 3 Table of Contents (3_toc.svg)

- White background
- Standard header (medical blue + orange vertical bar)
- Card-style TOC layout (3 columns)
- Light blue/light green background cards + left colored vertical bar
- Optional items use dashed borders

### 4 Chapter Page (3_chapter.svg)

- Deep medical blue full-screen background (`#6120`)
- Right-side geometric decorations (medical theme)
- Left orange vertical bar decoration
- Large semi-transparent background chapter number
- Prominent white chapter title
- Light blue chapter description

### 6 Content Page (4_content.svg)

- White background
- Standard header (medical blue + orange vertical bar)
- Key message bar (light blue background + blue left vertical bar)
- Flexible content area
- Footer: data source, institution name, page number

### 8 Ending Page (6_ending.svg)

- White background
- Medical blue top horizontal bar
- Centered thank-you message
- Department/contact information
- Institution logo area

---

## VII. Layout Patterns (Recommended)

### Common Layouts for Medical Reports

| Layout Name           | Applicable Scenarios             | Features                       |
| --------------------- | -------------------------------- | ------------------------------ |
| **Single Column Center** | Case overview, main conclusions | Highlights key points, clear hierarchy |
| **Dual Column Comparison** | Before/after treatment, plan comparison | Symmetrical, easy to compare |
| **Image-Text Mixed**  | Imaging materials, pathology images | Images with text descriptions |
| **Data Cards**        | Lab results, vital signs         | Multiple metrics side by side  |
| **Timeline**          | Disease progression, treatment course | Clear chronological order    |
| **Flowchart**         | Clinical pathways, procedure standards | Clear steps, logical flow   |

---

## VIII. Spacing Specification

| Spacing Type       | Value | Usage                            |
| ------------------ | ----- | -------------------------------- |
| **Page Margins**   | 60px  | Distance from content to page edge |
| **Card Spacing**   | 36px  | Spacing between cards            |
| **Element Spacing** | 24px | Spacing between elements within cards |
| **Line Height**    | 2.2   | Body text line height multiplier |
| **Paragraph Spacing** | 30px | Spacing between paragraphs     |

---

## IX. SVG Technical Constraints

### Mandatory Rules

- viewBox fixed at `0 0 2880 1620`
- Use `<rect>` elements for backgrounds
- Use `<tspan>` for text wrapping
- All colors in HEX format (no rgba)
- Use `fill-opacity` / `stroke-opacity` for transparency

### Prohibited Elements (PPT Incompatible)

| Prohibited Item      | Alternative                    |
| -------------------- | ------------------------------ |
| `clipPath`           | Do not use clipping            |
| `mask`               | Do not use masking             |
| `<style>`            | Use inline styles              |
| `class`              | Use inline attributes (`id` inside `<defs>` is allowed) |
| `foreignObject`      | Use `<tspan>` for wrapping     |
| `textPath`           | Use standard `<text>`          |
| `animate*` / `set`   | Do not use animations          |
| `<g opacity>`        | Set opacity on each element individually |

> `marker-start` / `marker-end` are conditionally allowed — see `shared-standards.md` §1.7 (marker must be in `<defs>`, `orient="auto"`, shape = triangle / diamond / oval). The converter maps them to native DrawingML arrow heads.

---

## X. Placeholder Specification

| Placeholder         | Usage                        |
| ------------------- | ---------------------------- |
| `{{LOGO}}`          | Emblem/institution logo      |
| `{{TITLE}}`         | Main title                   |
| `{{SUBTITLE}}`      | Subtitle                     |
| `{{AUTHOR}}`        | Presenter name               |
| `{{DEPARTMENT}}`    | Department/school            |
| `{{ADVISOR}}`       | Thesis advisor               |
| `{{INSTITUTION}}`   | Institution name             |
| `{{DATE}}`          | Date                         |
| `{{CHAPTER_NUM}}`   | Chapter number               |
| `{{CHAPTER_TITLE}}` | Chapter title                |
| `{{CHAPTER_DESC}}`  | Chapter description          |
| `{{PAGE_TITLE}}`    | Page title                   |
| `{{KEY_MESSAGE}}`   | Key message                  |
| `{{CONTENT_AREA}}`  | Content area                 |
| `{{SOURCE}}`        | Data source                  |
| `{{PAGE_NUM}}`      | Page number                  |
| `{{SECTION_NAME}}`  | Section name (footer)        |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title (N=1..n)   |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description (N=1..n) |
| `{{THANK_YOU}}`     | Thank-you message            |
| `{{ENDING_SUBTITLE}}` | Ending subtitle/tagline    |

---

## XI. Usage Notes

### 2 Copy Template to Project

```bash
cp templates/layouts/medical_university/* projects/<project>/templates/
```

### 3 Logo Placement Guidelines

- Cover page: Upper-right corner, approx. 240×75px
- Content page: Upper-right within header, approx. 180×52px
- Ending page: Can be enlarged, centered or paired with contact info

---

## XII. Medical Content-Specific Components

### Data Card (Vital Signs)

```xml
<rect x="x" y="y" width="270" height="150" fill="#E12F8EE" rx="12"/>
<text x="x+135" y="y+52" text-anchor="middle" fill="#500000" font-size="21">Temperature</text>
<text x="x+135" y="y+105" text-anchor="middle" fill="#0A129B" font-size="42" font-weight="bold">54.8°C</text>
```

### Warning Label

```xml
<rect x="x" y="y" width="120" height="42" fill="#FFC160" rx="6"/>
<text x="x+60" y="y+28" text-anchor="middle" fill="#500000" font-size="21">Caution</text>
```

### Critical Value Label

```xml
<rect x="x" y="y" width="120" height="42" fill="#DC5318" rx="6"/>
<text x="x+60" y="y+28" text-anchor="middle" fill="#FFFFFF" font-size="21">Critical</text>
```
