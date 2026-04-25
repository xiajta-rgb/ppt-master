#!/usr/bin/env python3
"""
PPT Master - SVG Validation and Sanitization Module

Validates SVG files for XML validity and fixes common issues:
- Unescaped XML entities (& -> &amp;, < -> &lt;, > -> &gt;)
- Invalid characters
- Incomplete tags
- Proper namespace declarations

Usage:
    from svg_finalize.validate_sanitize import validate_and_sanitize_svg
    
    is_valid, fixed_content, errors = validate_and_sanitize_svg(svg_path)
"""

import re
import html
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Tuple, List, Optional


def escape_xml_entities(text: str) -> str:
    """
    Escape XML entities in text content (not in tags).
    Only escapes &, <, > in text, preserves existing entities.
    
    Args:
        text: Raw SVG content
        
    Returns:
        SVG with entities properly escaped
    """
    # First, unescape to avoid double-escaping
    text = html.unescape(text)
    
    # Re-escape but only the necessary characters
    # Use a more careful approach to avoid breaking XML structure
    result = []
    in_tag = False
    in_entity = False
    entity_buffer = []
    
    for char in text:
        if char == '<':
            in_tag = True
            result.append(char)
        elif char == '>':
            in_tag = False
            result.append(char)
        elif char == '&' and not in_tag:
            # Start of entity, check if it's a valid entity
            in_entity = True
            entity_buffer = ['&']
        elif in_entity:
            entity_buffer.append(char)
            if char == ';':
                # End of entity
                entity_str = ''.join(entity_buffer)
                # Check if it's a valid XML entity
                valid_entities = ['&amp;', '&lt;', '&gt;', '&quot;', '&apos;']
                if entity_str in valid_entities:
                    result.extend(entity_buffer)
                else:
                    # Escape the & separately
                    result.append('&amp;')
                    result.extend(entity_buffer[1:])  # Skip the initial &
                in_entity = False
                entity_buffer = []
        elif in_tag:
            # Inside tag, pass through
            result.append(char)
        else:
            # In text content, escape special chars
            if char == '&':
                result.append('&amp;')
            elif char == '<':
                result.append('&lt;')
            elif char == '>':
                result.append('&gt;')
            elif char == '"':
                result.append('&quot;')
            elif char == "'":
                result.append('&apos;')
            else:
                result.append(char)
    
    # Handle any remaining entity buffer
    if entity_buffer:
        result.extend(entity_buffer)
    
    return ''.join(result)


def validate_svg(svg_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate an SVG file for XML validity.
    
    Args:
        svg_path: Path to SVG file
        
    Returns:
        (is_valid, error_list)
    """
    errors = []
    
    try:
        # Try to parse with ElementTree
        tree = ET.parse(str(svg_path))
        root = tree.getroot()
        
        # Check for SVG namespace
        if 'svg' not in root.tag:
            errors.append(f"Root tag is not SVG: {root.tag}")
        
        # Check for viewBox attribute
        if 'viewBox' not in root.attrib:
            errors.append("Missing viewBox attribute")
        
        return len(errors) == 0, errors
        
    except ET.ParseError as e:
        errors.append(f"XML parse error: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Validation error: {e}")
        return False, errors


def sanitize_svg_content(content: str) -> Tuple[str, List[str]]:
    """
    Sanitize SVG content by fixing common issues.
    
    Args:
        content: Raw SVG content
        
    Returns:
        (sanitized_content, list_of_fixes)
    """
    fixes = []
    original_length = len(content)
    
    # Step 1: Escape XML entities
    sanitized = escape_xml_entities(content)
    if sanitized != content:
        fixes.append("Escaped XML entities")
        content = sanitized
    
    # Step 2: Fix common namespace issues
    # Ensure proper SVG namespace if missing
    svg_tag_match = re.search(r'<svg([^>]*)>', content, re.IGNORECASE)
    if svg_tag_match:
        svg_attrs = svg_tag_match.group(1)
        if 'xmlns=' not in svg_attrs.lower():
            # Add default SVG namespace
            new_svg_tag = f'<svg xmlns="http://www.w3.org/2000/svg"{svg_attrs}>'
            content = content.replace(svg_tag_match.group(0), new_svg_tag)
            fixes.append("Added SVG namespace declaration")
    
    # Step 3: Remove control characters (except whitespace)
    def remove_control_chars(text):
        return ''.join(char for char in text if char == '\t' or char == '\n' or char == '\r' or ord(char) >= 32)
    
    cleaned = remove_control_chars(content)
    if cleaned != content:
        fixes.append("Removed control characters")
        content = cleaned
    
    # Step 4: Ensure proper closing tags for common elements
    # Fix self-closing tags that might cause issues (e.g., <path ...> -> <path .../>)
    # This is a heuristic fix for common issues
    
    return content, fixes


def validate_and_sanitize_svg(svg_path: Path, auto_fix: bool = True) -> Tuple[bool, Optional[str], List[str], List[str]]:
    """
    Validate and sanitize an SVG file.
    
    Args:
        svg_path: Path to SVG file
        auto_fix: Whether to automatically fix issues
        
    Returns:
        (is_valid, fixed_content, errors, fixes)
    """
    errors = []
    fixes = []
    
    # Read file
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
        return False, None, errors, fixes
    
    # First try to validate as-is
    is_valid, validate_errors = validate_svg(svg_path)
    
    if not is_valid and auto_fix:
        # Try to sanitize
        sanitized_content, sanitize_fixes = sanitize_svg_content(content)
        fixes.extend(sanitize_fixes)
        
        # Write temporarily to re-validate
        temp_path = svg_path.parent / (svg_path.stem + '_temp.svg')
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            
            # Re-validate
            is_valid, new_errors = validate_svg(temp_path)
            
            if is_valid:
                content = sanitized_content
                errors = []
            else:
                errors.extend(validate_errors)
                errors.append("Sanitization attempt failed to fix all issues")
                
        except Exception as e:
            errors.append(f"Sanitization error: {e}")
        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()
    else:
        errors.extend(validate_errors)
    
    return is_valid, content if auto_fix else None, errors, fixes


def process_svg_file(svg_path: Path, dry_run: bool = False, verbose: bool = True) -> Tuple[bool, int, List[str]]:
    """
    Process a single SVG file: validate and sanitize.
    
    Args:
        svg_path: Path to SVG file
        dry_run: Preview only, don't modify
        verbose: Show detailed output
        
    Returns:
        (success, num_fixes, error_list)
    """
    errors = []
    fixes_count = 0
    
    try:
        is_valid, fixed_content, errors, fixes = validate_and_sanitize_svg(
            svg_path, auto_fix=True
        )
        
        fixes_count = len(fixes)
        
        if verbose:
            if is_valid:
                if fixes_count > 0:
                    print(f"      [FIXED] {svg_path.name}: {', '.join(fixes)}")
                else:
                    print(f"      [OK] {svg_path.name}: Valid, no fixes needed")
            else:
                print(f"      [ERROR] {svg_path.name}: {', '.join(errors)}")
        
        if not dry_run and fixed_content is not None and fixes_count > 0:
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
        
        return is_valid, fixes_count, errors
        
    except Exception as e:
        errors.append(f"Processing error: {e}")
        if verbose:
            print(f"      [ERROR] {svg_path.name}: {e}")
        return False, 0, errors


if __name__ == '__main__':
    # Test code
    import sys
    
    if len(sys.argv) > 1:
        svg_file = Path(sys.argv[1])
        if svg_file.exists():
            print(f"Validating: {svg_file.name}")
            print("=" * 60)
            
            success, fixes, errors = process_svg_file(
                svg_file, dry_run='--dry-run' in sys.argv
            )
            
            if success:
                if fixes > 0:
                    print(f"\n✓ Success - {fixes} fix(es) applied")
                else:
                    print(f"\n✓ Success - SVG is already valid")
            else:
                print(f"\n✗ Failed - {len(errors)} error(s)")
        else:
            print(f"File not found: {svg_file}")
    else:
        print("Usage: python3 validate_sanitize.py <svg_file> [--dry-run]")
