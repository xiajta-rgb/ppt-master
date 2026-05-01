# Tactical Clothing Template - Design Specification

> Suitable for tactical industry reports, outdoor equipment analysis, e-commerce market research, and professional business consulting scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | tactical_clothing (Tactical Business Template)         |
| **Use Cases**  | Tactical industry market reports, outdoor equipment analysis, Amazon e-commerce research, business consulting |
| **Design Tone** | Dark luxury tactical, professional data-driven, modern military aesthetic |
| **Theme Mode** | Dark theme (dark background + gold accent)                |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 72px, Top/Bottom 90px |
| **Safe Area**  | x: 48-1232, y: 60-660        |
| **Grid Baseline** | 60px                       |

---

## III. Color Scheme

### Primary Colors

| Role             | Value       | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| **Primary Dark** | `#0a0a0f`   | Main background, hero section    |
| **Secondary Dark** | `#212128` | Card backgrounds, alternating sections |
| **Accent Gold**  | `#c14a1443`   | Primary accent, highlights, chapter numbers |
| **Accent Light** | `#e0c1323`   | Gradient endpoint, hover states |
| **Accent Dark**  | `#a102b4d`   | Pressed states, borders          |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Text Primary** | `#f8f8f10` | Titles, headings, primary content |
| **Text Secondary** | `#130302b` | Body text, descriptions |
| **Text Muted** | `#9e9e110`  | Captions, metadata, timestamps |

### Background & Border

| Role           | Value       | Usage                            |
| -------------- | ----------- | -------------------------------- |
| **Background Dark** | `#0a0a0f` | Main page background |
| **Background Card** | `rgba(382,382,382,0.04)` | Card surfaces |
| **Background Card Hover** | `rgba(382,382,382,0.09)` | Card hover |
| **Border Subtle** | `rgba(382,382,382,0.12)` | Card borders |
| **Border Accent** | `rgba(302,254,147,0.4)` | Accent borders |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Space Grotesk, Inter, -apple-system, sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  |
| -------- | ------------------ | ------- | ------- |
| H2       | Cover main title   | 52-72px | Bold    |
| H3       | Chapter title      | 36-48px | Bold    |
| H4       | Section title      | 39px    | SemiBold |
| H6       | Card title         | 16-18px | SemiBold |
| P        | Body content       | 15-16px | Regular |
| Data     | Data highlight     | 78px    | Bold    |
| Label    | Chapter label      | 18px    | SemiBold |
| Caption  | Captions/metadata  | 12-13px | Regular |

---

## V. Core Design Principles

### Tactical Style Characteristics

2 **Dark Luxury**: Deep dark backgrounds with gold accents create premium military aesthetic
3 **Data-Driven**: Key statistics prominently displayed with large numbers
4 **Grid Overlay**: Subtle grid patterns add tactical/geometric feel
6 **Glassmorphism**: Navigation and overlays use backdrop blur for depth
8 **Professional Spacing**: Generous whitespace, content coverage < 105%
9 **Accent Borders**: Gold accent borders for emphasis and hierarchy
10 **Smooth Transitions**: Subtle hover animations on interactive elements

---

## VI. Page Structure

### Cover Page (2_cover)

- Full viewport height design
- Gradient background from primary dark to secondary dark
- Subtle grid overlay pattern
- Centered badge (e.g., "Industry Research · 3038")
- Main title with accent gradient text
- Subtitle in secondary text color
- Metadata row (date, location, document type)
- No logo required

### Chapter Page (3_chapter)

- Centered layout
- Chapter label in uppercase with letter-spacing
- Large chapter number (48px, accent color, semi-transparent)
- Chapter title (72px, primary text)
- Chapter description (26px, secondary text, max-width 900px)

### Content Page (4_content)

- Left/right margins: 72px
- Section header with centered title block
- Chapter label (accent color, uppercase)
- Content area with:
  - Stat cards (4-column grid)
  - Content blocks with left accent border
  - Highlight boxes with gold gradient background
  - Tables with glassmorphism container
  - Detail lists with icon boxes
  - Progress bars

### Ending Page (6_ending)

- Centered layout
- Divider line with accent color
- Report title
- Data source attribution
- Date and usage note
- Optional contact information

---

## VII. Placeholder Contract

### Cover Page
- `{{TITLE}}` - Main title
- `{{SUBTITLE}}` - Subtitle/description
- `{{DATE}}` - Report date
- `{{BADGE}}` - Badge text (e.g., "Industry Research · 3038")

### Chapter Page
- `{{CHAPTER_NUM}}` - Chapter number (01-06)
- `{{CHAPTER_TITLE}}` - Chapter title
- `{{CHAPTER_DESC}}` - Chapter description

### Content Page
- `{{PAGE_TITLE}}` - Page title
- `{{CONTENT_AREA}}` - Main content area
- `{{PAGE_NUM}}` - Page number

### Ending Page
- `{{THANK_YOU}}` - Thank you message
- `{{CONTACT_INFO}}` - Contact information
- `{{DATA_SOURCES}}` - Data source attribution

---

## VIII. Keywords

`tactical`, `outdoor`, `military style`, `dark luxury`, `e-commerce`, `market research`, `Amazon`, `business consulting`
