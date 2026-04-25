#!/usr/bin/env python3
"""
Test the SVG validation and sanitization module.
"""

from pathlib import Path
import sys

# Add the scripts directory to path
script_dir = Path(__file__).parent / '.trae' / 'skills' / 'ppt-master' / 'scripts'
sys.path.insert(0, str(script_dir))

from svg_finalize.validate_sanitize import validate_and_sanitize_svg

# Test with the P04 file that was fixed earlier
test_file = Path(__file__).parent / 'examples' / 'ppt169_战术服装_市场分析' / 'svg_final' / 'P04_产品设计DNA.svg'

if test_file.exists():
    print(f"Testing validation with: {test_file.name}")
    print("=" * 60)
    
    # Test without auto-fix first
    is_valid, _, errors, _ = validate_and_sanitize_svg(test_file, auto_fix=False)
    print(f"Validation without auto-fix: {'✅ PASS' if is_valid else '❌ FAIL'}")
    if errors:
        print("Errors:", errors)
    
    print()
    
    # Test with auto-fix
    print("Testing with auto-fix:")
    is_valid, _, errors, fixes = validate_and_sanitize_svg(test_file, auto_fix=True)
    print(f"Validation with auto-fix: {'✅ PASS' if is_valid else '❌ FAIL'}")
    if errors:
        print("Errors:", errors)
    if fixes:
        print("Fixes applied:", fixes)
    
else:
    print(f"Test file not found: {test_file}")
    print("Please ensure you have the project set up correctly.")
