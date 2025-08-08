# Resume LaTeX Project

A modular LaTeX-based resume/CV generation system with bilingual support (English/Chinese) that generates professional resumes from structured YAML data.

## Architecture

The system is composed of independent modules, each with a single responsibility:

```
resume/
├── src/                      # Python processing modules
│   ├── combine_yaml.py      # Combines modular YAML files
│   ├── generate_latex.py    # Translates YAML to LaTeX
│   ├── copy_cls.py          # Manages LaTeX class file
│   └── compile_pdf.py       # Compiles LaTeX to PDF
├── scripts/                  # Shell scripts
│   └── run.sh               # Orchestrates the pipeline
├── data/                     # Resume content in YAML format
│   ├── personal-en.yaml     # Personal information (English)
│   ├── personal-cn.yaml     # Personal information (Chinese)
│   ├── education/           # Education history
│   │   ├── 02-yale-en.yaml
│   │   ├── 02-yale-cn.yaml
│   │   ├── 01-arizona-en.yaml
│   │   └── 01-arizona-cn.yaml
│   ├── experience/          # Work experience
│   │   ├── 06-moore-2025-*.yaml
│   │   ├── 05-bytedance-2021-*.yaml
│   │   ├── 04-highflyer-2021-*.yaml
│   │   ├── 03-bytedance-2019-*.yaml
│   │   ├── 02-google-2018-*.yaml
│   │   └── 01-datera-2016-*.yaml
│   ├── skills-en.yaml       # Technical skills (English)
│   └── skills-cn.yaml       # Technical skills (Chinese)
├── templates/                # LaTeX templates and class files
│   ├── default/             # Default resume template
│   └── 20250807/            # Alternative template
└── output/                   # Generated files
    ├── resume-en.pdf        # English resume
    ├── resume-cn.pdf        # Chinese resume
    └── *.tex                # Generated LaTeX sources
```

**Numbering Convention**: Higher numbers = more recent (appear first in resume)

## Prerequisites

### 1. LaTeX Compiler
Install TeX Live (comprehensive LaTeX distribution):

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y texlive-full

# Alternative: Minimal installation with required packages
sudo apt-get install -y texlive texlive-latex-extra texlive-fonts-recommended texlive-xetex

# Additional packages for icons and better font support
sudo apt-get install -y texlive-fonts-extra  # For fontawesome icons

# Verify installation
pdflatex --version
xelatex --version
```

### 2. Python Dependencies
```bash
# Install from requirements file
pip install -r requirements.txt

# Or install directly
pip install PyYAML
```

### 3. Chinese Font Support (Optional but Recommended)
For better Chinese typography, install Noto CJK fonts:
```bash
# Install Noto CJK fonts for professional Chinese typography
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra
```

### 4. VS Code Extensions (Optional)
- **LaTeX Workshop** - Main LaTeX extension for PDF compilation and preview
- **LaTeX Utilities** - Additional LaTeX tools and snippets

### 5. Optional Tools
```bash
# Install latexmk for automatic compilation
sudo apt-get install -y latexmk
```

## Usage

### Quick Start

```bash
# Navigate to scripts directory
cd scripts/

# Generate both English and Chinese resumes (default: XeLaTeX)
./run.sh

# Use pdflatex (English only, faster but no Chinese support)
./run.sh --pdflatex

# Keep intermediate files for debugging
./run.sh --keep-temp --verbose

# Clean output directory
./run.sh --clean

# Show help
./run.sh --help
```

### Individual Modules

You can run each module separately for debugging:

```bash
# Step 1: Combine YAML files
python3 src/combine_yaml.py data/ output/combined.yaml en

# Step 2: Generate LaTeX
python3 src/generate_latex.py output/combined.yaml output/resume.tex en

# Step 3: Copy class file
python3 src/copy_cls.py templates/default/ output/

# Step 4: Compile PDF
python3 src/compile_pdf.py output/resume.tex xelatex
```

## Chinese Language Support

The system is fully configured for Chinese support with:

### Installed Components
- **XeLaTeX** - Unicode-aware TeX engine (required for Chinese)
- **texlive-lang-chinese** - Chinese language support package
- **texlive-lang-cjk** - CJK (Chinese/Japanese/Korean) base support
- **Chinese Fonts** - Noto CJK fonts pre-installed

### Compiling Chinese Documents
The pipeline automatically uses XeLaTeX for Chinese documents:
```bash
./run.sh  # Automatically detects and processes both languages
```

### Chinese LaTeX Template
```latex
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{Noto Serif CJK SC}  % or other Chinese fonts

\begin{document}
中文内容...
\end{document}
```

## Adding New Content

### New Job Experience

1. Create new YAML files for both languages:
   ```bash
   # Use the next sequential number
   cp data/experience/06-moore-2025-en.yaml data/experience/07-newjob-2025-en.yaml
   cp data/experience/06-moore-2025-cn.yaml data/experience/07-newjob-2025-cn.yaml
   ```

2. Edit the content in both files

3. Regenerate resumes:
   ```bash
   cd scripts/
   ./run.sh
   ```

### New Education

Follow the same process in the `data/education/` directory.

### Updating Personal Information or Skills

Edit the appropriate files:
- `data/personal-en.yaml` / `data/personal-cn.yaml`
- `data/skills-en.yaml` / `data/skills-cn.yaml`

## Output Files

All generated files are placed in `output/`:
- `resume-en.pdf` - English resume
- `resume-cn.pdf` - Chinese resume
- `resume-en.tex` - Generated English LaTeX source
- `resume-cn.tex` - Generated Chinese LaTeX source
- `combined-*.yaml` - Merged data (when using --keep-temp)
- `resume.cls` - LaTeX class file

## VS Code Integration

### LaTeX Workshop Settings
Add to your VS Code settings.json for optimal configuration:
```json
{
    "latex-workshop.latex.autoBuild.run": "onSave",
    "latex-workshop.latex.outDir": "./output",
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.latex.tools": [
        {
            "name": "xelatex",
            "command": "xelatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        },
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "latex-workshop.latex.recipes": [{
        "name": "xelatex",
        "tools": ["xelatex"]
    }],
    "latex-workshop.latex.recipe.default": "xelatex"
}
```

## Features

### Visual Enhancements
- **Icon Support**: Phone (📞), WeChat, and Email (✉️) icons using fontawesome
- **Gray Icons**: Subtle gray coloring for contact icons
- **Improved Spacing**: Better visual separation between icons and text
- **Chinese Typography**: Optimized font selection with heiti (黑体) for names and kaishu (楷书) for contact info

### Data Structure
- **Separated Degree/Major**: Education entries now have separate `degree` and `major` fields that combine in output
  - Example: `degree: B.S.` + `major: Computer Science` → "B.S. in Computer Science"

## Benefits

- **Modular Data**: Edit individual experiences/education independently
- **Bilingual Support**: Maintain parallel English and Chinese versions
- **Clean Separation**: Content separate from formatting
- **Easy Updates**: Just edit YAML, no LaTeX knowledge needed
- **Version Control Friendly**: Track changes per module
- **Pipeline Architecture**: Each step is independent and testable
- **Professional Output**: High-quality PDF resumes with icons

## Tips

- Use `xelatex` for documents with Chinese text (default)
- Use `pdflatex` for English-only documents (faster compilation)
- The `.cls` files define the resume format and styling
- Modify templates in the `templates/` directory to create new resume styles
- Keep different versions in `data/` for different job applications
- Available Chinese fonts: Noto Serif CJK SC, Noto Sans CJK SC, AR PL UMing

## Troubleshooting

- **Chinese characters not displaying**: Ensure you're using XeLaTeX, not pdflatex
- **Compilation errors**: Check that all required LaTeX packages are installed
- **Missing fonts**: Install the Noto CJK font family
- **YAML parsing errors**: Validate YAML syntax in your data files