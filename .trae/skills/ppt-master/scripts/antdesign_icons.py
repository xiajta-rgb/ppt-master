#!/usr/bin/env python3
"""
Robust SVG Emoji to AntDesign Icon Converter

This script properly handles emojis that are incorrectly embedded within <text> tags
by restructuring the SVG to put icons outside text elements.
"""

import re
from pathlib import Path
from typing import Dict, Tuple, List

# AntDesign-style icon paths
ANTDESIGN_ICONS: Dict[str, str] = {
    '🏭': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/></svg>''',
    '🚀': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>''',
    '🔥': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>''',
    '📈': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>''',
    '🎯': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>''',
    '💡': '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c9a962" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>''',
}


def extract_text_attributes(text_tag: str) -> str:
    """Extract attributes from a <text...> opening tag"""
    match = re.search(r'<text([^>]*)>', text_tag)
    if match:
        return match.group(1)
    return ''


def fix_text_with_embedded_svg(content: str) -> Tuple[str, List[str]]:
    """
    Find <text> tags that contain <svg> (from failed emoji replacement)
    and restructure them properly.

    Returns: (fixed_content, list_of_fixes)
    """
    fixes = []

    # Pattern to match text tags containing SVG elements
    # This handles cases like: <text ...><svg ...>...</svg> Some Text</text>
    pattern = r'<text([^>]*)>([^<]*<svg[^>]*>.*?</svg>[^<]*)([^<]*)</text>'

    def fix_match(match):
        attrs = match.group(1)  # text tag attributes
        before_svg = match.group(2)  # text before SVG (usually empty)
        after_text = match.group(3).strip()  # text after SVG

        # Extract the SVG part
        svg_match = re.search(r'(<svg[^>]*>.*?</svg>)', before_svg + after_text, re.DOTALL)
        if not svg_match:
            svg_match = re.search(r'(<svg[^>]*>.*?</svg>)', match.group(0), re.DOTALL)

        if svg_match:
            svg_element = svg_match.group(1)

            # Extract text content - look for any text after the SVG in the original
            original = match.group(0)
            text_after_svg = re.sub(r'<svg[^>]*>.*?</svg>', '', original, flags=re.DOTALL)
            text_after_svg = re.sub(r'<[^>]+>', '', text_after_svg).strip()

            if text_after_svg:
                # Return: SVG + new text tag with the text
                return f'{svg_element}<text{attrs}>{text_after_svg}</text>'
            else:
                return svg_element
        return match.group(0)

    fixed = re.sub(pattern, fix_match, content, flags=re.DOTALL)

    if fixed != content:
        fixes.append("Fixed text tags with embedded SVG")

    return fixed, fixes


def replace_emojis_properly(content: str) -> Tuple[str, int, List[str]]:
    """
    Properly replace emoji characters with SVG icons.
    This handles emojis that are:
    1. Alone in a text tag
    2. At the start/end of text
    3. In the middle of text
    """
    replacements = []
    result = content

    for emoji, svg_icon in ANTDESIGN_ICONS.items():
        if emoji in result:
            # Strategy: Replace emoji with a placeholder, then restructure
            placeholder = f'__EMOJI_PLACEHOLDER_{len(replacements)}__'

            # Check if emoji is inside a text tag
            # Pattern: <text...>text before [emoji] text after</text>
            text_pattern = rf'(<text[^>]*>)([^<]*){re.escape(emoji)}([^<]*)(</text>)'

            def replace_in_text_tag(m):
                prefix_attrs = extract_text_attributes(m.group(1))
                before = m.group(2).strip()
                after = m.group(3).strip()

                parts = []
                if before:
                    parts.append(f'<text{prefix_attrs}>{before}</text>')
                parts.append(svg_icon)
                if after:
                    parts.append(f'<text{prefix_attrs}>{after}</text>')

                return ''.join(parts)

            new_result = re.sub(text_pattern, replace_in_text_tag, result)

            if new_result != result:
                replacements.append(emoji)
                result = new_result
            else:
                # Fallback: direct replacement (for emojis not in text tags)
                result = result.replace(emoji, svg_icon)
                if emoji in result:
                    replacements.append(emoji)

    return result, len(replacements), replacements


def process_svg_file(svg_path: Path, output_path: Path = None, dry_run: bool = False) -> Tuple[bool, int, List[str]]:
    """Process a single SVG file"""
    if output_path is None:
        output_path = svg_path

    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Step 1: Fix any existing broken SVG-in-text structures
        # This handles cases where SVG is embedded inside <text> tags
        content, _ = fix_text_with_embedded_svg(content)

        # Step 2: Replace emojis properly
        content, num_replacements, emojis = replace_emojis_properly(content)

        # Step 3: Fix any remaining text-with-embedded-svg issues
        content, _ = fix_text_with_embedded_svg(content)

        if content != original and not dry_run:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return True, num_replacements, emojis

    except Exception as e:
        return False, 0, [str(e)]


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 antdesign_icons.py <svg_file> [--dry-run]")
        print("       python3 antdesign_icons.py <directory> [--dry-run]")
        sys.exit(1)

    target = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if target.is_dir():
        svg_files = list(target.glob('**/*.svg'))
        print(f"Processing {len(svg_files)} SVG files in {target}...")

        total = 0
        for svg_file in svg_files:
            ok, count, emojis = process_svg_file(svg_file, dry_run=dry_run)
            if count > 0:
                print(f"  {svg_file.name}: {count} → {', '.join(emojis)}")
                total += count

        print(f"\nTotal: {total} replacements")
    else:
        ok, count, emojis = process_svg_file(target, dry_run=dry_run)
        if count > 0:
            print(f"Replaced {count} emoji(s): {', '.join(emojis)}")
        else:
            print("No emojis found or replaced")
