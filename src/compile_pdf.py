#!/usr/bin/env python3
"""
Step 4: Compile LaTeX to PDF using XeLaTeX or pdflatex
"""

import subprocess
import sys
import os
from pathlib import Path

def compile_with_xelatex(tex_file, output_dir):
    """Compile LaTeX file with XeLaTeX (supports Chinese)"""
    try:
        # Change to output directory for compilation
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Run XeLaTeX
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', tex_file.name],
            capture_output=True,
            text=True
        )
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"  ✓ Compiled with XeLaTeX: {tex_file.stem}.pdf")
            return True
        else:
            print(f"  ✗ XeLaTeX compilation failed")
            print(f"    Error: {result.stderr[:500]}")
            return False
            
    except FileNotFoundError:
        print(f"  ✗ XeLaTeX not found. Please install texlive-xetex")
        return False
    except Exception as e:
        print(f"  ✗ Error during compilation: {e}")
        return False

def compile_with_pdflatex(tex_file, output_dir):
    """Compile LaTeX file with pdflatex (English only)"""
    try:
        # Change to output directory for compilation
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Run pdflatex
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_file.name],
            capture_output=True,
            text=True
        )
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"  ✓ Compiled with pdflatex: {tex_file.stem}.pdf")
            return True
        else:
            print(f"  ✗ pdflatex compilation failed")
            print(f"    Error: {result.stderr[:500]}")
            return False
            
    except FileNotFoundError:
        print(f"  ✗ pdflatex not found. Please install texlive")
        return False
    except Exception as e:
        print(f"  ✗ Error during compilation: {e}")
        return False

def main():
    # Default settings
    script_dir = Path(__file__).parent
    output_dir = script_dir / '..' / 'output'
    tex_file = output_dir / 'resume.tex'
    use_xelatex = True  # Default to XeLaTeX for Chinese support
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        tex_file = Path(sys.argv[1])
        output_dir = tex_file.parent
    if len(sys.argv) > 2:
        compiler = sys.argv[2].lower()
        use_xelatex = (compiler == 'xelatex')
    
    print(f"[4/4] Compiling PDF...")
    
    # Check if tex file exists
    if not tex_file.exists():
        print(f"  ✗ Error: LaTeX file not found: {tex_file}")
        return 1
    
    # Compile
    if use_xelatex:
        print(f"  Using XeLaTeX (Chinese support enabled)")
        success = compile_with_xelatex(tex_file, output_dir)
    else:
        print(f"  Using pdflatex (English only)")
        success = compile_with_pdflatex(tex_file, output_dir)
    
    if success:
        pdf_file = output_dir / f"{tex_file.stem}.pdf"
        print(f"\n✅ Success! Resume generated: {pdf_file}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())