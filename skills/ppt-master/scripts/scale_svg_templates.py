"""Scale SVG template files from 1280x720 to 1920x1080.

Usage:
    python scale_svg_templates.py [--dry-run]

Scales all SVG files in templates/layouts/ subdirectories by 1.5x
(1920/1280 = 1080/720 = 1.5).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCALE = 1.5
OLD_W, OLD_H = 1280, 720
NEW_W, NEW_H = 1920, 1080

TEMPLATES_DIR = Path(__file__).parent.parent / 'templates' / 'layouts'

SVG_COORD_ATTRS = {
    'x', 'y', 'x1', 'y1', 'x2', 'y2',
    'width', 'height',
    'cx', 'cy', 'rx', 'ry', 'r',
    'dx', 'dy',
    'font-size',
    'stroke-width',
    'letter-spacing',
}


def _scale_value(num_str: str) -> str:
    try:
        val = float(num_str)
        scaled = val * SCALE
        if num_str.isdigit() or (num_str.startswith('-') and num_str[1:].isdigit()):
            return str(int(round(scaled)))
        if '.' in num_str:
            decimals = len(num_str.split('.')[1])
            return f"{scaled:.{decimals}f}"
        return f"{scaled:.1f}"
    except ValueError:
        return num_str


def scale_path_data(d: str) -> str:
    return re.sub(r'[-\d.]+', lambda m: _scale_value(m.group(0)), d)


def scale_points_attr(points: str) -> str:
    nums = re.findall(r'[-\d.]+', points)
    scaled = [_scale_value(n) for n in nums]
    separators = re.findall(r'[,\s]+', points)
    result = scaled[0]
    for i, sep in enumerate(separators):
        result += sep + scaled[i + 1]
    return result


def scale_transform(value: str) -> str:
    def _scale_translate(m):
        tx = m.group(1)
        ty = m.group(2) or '0'
        return f'translate({_scale_value(tx)}, {_scale_value(ty)})'

    def _scale_rotate(m):
        angle = m.group(1)
        if m.group(2) is not None:
            cx = m.group(2)
            cy = m.group(3)
            return f'rotate({_scale_value(angle)}, {_scale_value(cx)}, {_scale_value(cy)})'
        return f'rotate({angle})'

    result = value
    result = re.sub(
        r'translate\(\s*([-\d.]+)(?:[\s,]+([-\d.]+))?\s*\)',
        _scale_translate, result,
    )
    result = re.sub(
        r'rotate\(\s*([-\d.]+)(?:[\s,]+([-\d.]+)[\s,]+([-\d.]+))?\s*\)',
        _scale_rotate, result,
    )
    return result


def scale_svg_content(content: str) -> str:
    def replace_attr(match):
        attr_name = match.group(1)
        quote = match.group(2)
        value = match.group(3)

        if attr_name == 'd':
            return f'{attr_name}={quote}{scale_path_data(value)}{quote}'
        if attr_name == 'points':
            return f'{attr_name}={quote}{scale_points_attr(value)}{quote}'
        if attr_name == 'transform':
            return f'{attr_name}={quote}{scale_transform(value)}{quote}'
        if attr_name in SVG_COORD_ATTRS:
            try:
                float(value)
                return f'{attr_name}={quote}{_scale_value(value)}{quote}'
            except ValueError:
                return match.group(0)
        return match.group(0)

    content = re.sub(r'(\w[\w-]*)=([\'"])([^\'"]*)\2', replace_attr, content)

    content = content.replace(f'viewBox="0 0 {OLD_W} {OLD_H}"', f'viewBox="0 0 {NEW_W} {NEW_H}"')

    return content


def main():
    dry_run = '--dry-run' in sys.argv

    target_dir = TEMPLATES_DIR
    for i, arg in enumerate(sys.argv):
        if arg == '--dir' and i + 1 < len(sys.argv):
            target_dir = Path(sys.argv[i + 1])

    svg_files = sorted(target_dir.rglob('*.svg'))
    print(f"Found {len(svg_files)} SVG files in {target_dir}")

    updated = 0
    for svg_path in svg_files:
        content = svg_path.read_text(encoding='utf-8')
        if f'viewBox="0 0 {OLD_W} {OLD_H}"' not in content and f'width="{OLD_W}"' not in content:
            continue

        new_content = scale_svg_content(content)
        if new_content == content:
            continue

        updated += 1
        rel = svg_path.relative_to(target_dir)
        if dry_run:
            print(f"  [DRY-RUN] Would update: {rel}")
        else:
            svg_path.write_text(new_content, encoding='utf-8')
            print(f"  Updated: {rel}")

    print(f"\n{'Would update' if dry_run else 'Updated'} {updated} files")


if __name__ == '__main__':
    main()
