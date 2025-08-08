#!/usr/bin/env python3
"""
Step 3: Copy resume.cls file from templates to output directory
"""

import shutil
import sys
from pathlib import Path

def copy_cls_file(template_dir, output_dir):
    """Copy resume.cls from templates to output directory"""
    template_cls = template_dir / 'resume.cls'
    output_cls = output_dir / 'resume.cls'
    
    if not template_cls.exists():
        print(f"  ✗ Error: Template file not found: {template_cls}")
        return False
    
    try:
        shutil.copy2(template_cls, output_cls)
        print(f"  ✓ Copied resume.cls to {output_dir}")
        return True
    except Exception as e:
        print(f"  ✗ Error copying file: {e}")
        return False

def main():
    # Default paths
    script_dir = Path(__file__).parent
    template_dir = script_dir / '..' / 'templates' / 'default'
    output_dir = script_dir / '..' / 'output'
    
    # Override with command line arguments if provided
    if len(sys.argv) > 1:
        template_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    print(f"[3/4] Copying LaTeX class file...")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy cls file
    success = copy_cls_file(template_dir, output_dir)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())