#!/usr/bin/env python3
"""
Step 2: Generate LaTeX from combined YAML data
"""

import yaml
import sys
from pathlib import Path

def load_yaml_content(yaml_file):
    """Load resume content from YAML file"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def escape_latex(text):
    """Escape special LaTeX characters"""
    if not text:
        return text
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    for char, escape in special_chars.items():
        text = text.replace(char, escape)
    return text

def generate_latex_header(data, lang='en'):
    """Generate LaTeX document header"""
    if lang == 'cn':
        # Chinese version with kaishu font for contact info
        return f"""% Generated Resume from YAML
% Auto-generated - Edit YAML files for content changes

\\documentclass[
    a4paper,
    11pt,
]{{resume}}

\\usepackage{{ebgaramond}}
\\usepackage[UTF8]{{ctex}}

\\name{{{data['personal']['name']}}}
\\address{{ \\kaishu 电话（微信）： {data['personal']['phone']} {{}} {{}} {{}} {{}} 邮箱： {data['personal']['email']} }}

\\begin{{document}}
"""
    else:
        # English version
        return f"""% Generated Resume from YAML
% Auto-generated - Edit YAML files for content changes

\\documentclass[
    a4paper,
    11pt,
]{{resume}}

\\usepackage{{ebgaramond}}
\\usepackage[UTF8]{{ctex}}

\\name{{{data['personal']['name']}}}
\\address{{Phone (Wechat): {data['personal']['phone']} {{}} {{}} {{}} {{}} E-mail: {data['personal']['email']}}}

\\begin{{document}}
"""

def generate_education_section(education_list, lang='en'):
    """Generate education section"""
    if not education_list:
        return ""
    
    section_title = "教育背景" if lang == 'cn' else "Education"
    latex = f"\n\\begin{{rSection}}{{{section_title}}}\n"
    
    for edu in education_list:
        if lang == 'cn':
            latex += f"""    
    \\textbf{{{edu['school']}}} \\hfill \\textit{{{edu['dates']}}} \\\\ 
    {{\\kaishu {edu['degree']}，GPA: {edu['gpa']} }} \\hfill \\textit{{{edu['location']}}}
"""
        else:
            latex += f"""    
    \\textbf{{{edu['school']}}} \\hfill \\textit{{{edu['dates']}}} \\\\ 
    {{{edu['degree']}, GPA: {edu['gpa']}}} \\hfill \\textit{{{edu['location']}}}
"""
    
    latex += "\n\\end{rSection}\n"
    return latex

def generate_experience_section(experience_list, lang='en'):
    """Generate experience section"""
    if not experience_list:
        return ""
    
    section_title = "工作经历" if lang == 'cn' else "Experience"
    latex = f"\n\\begin{{rSection}}{{{section_title}}}\n"
    
    for exp in experience_list:
        # Use 'product' and 'team' if available
        if 'product' in exp and 'team' in exp:
            title = f"{exp['team']}, {exp['product']}" if exp['product'] else exp['team']
        else:
            title = exp.get('team', '')
        
        latex += f"""
    \\begin{{rSubsection}}{{{exp['company']}}}{{{exp['dates']}}}{{{title}}}{{{exp['location']}}}
"""
        for bullet in exp.get('bullets', []):
            # Preserve special LaTeX formatting like \textit{}
            bullet_formatted = bullet.replace('epoll', '\\textit{epoll}')
            latex += f"        \\item {bullet_formatted}\n"
        
        latex += "    \\end{rSubsection}\n"
    
    latex += "\n\\end{rSection}\n"
    return latex

def generate_skills_section(skills, lang='en'):
    """Generate technical skills section"""
    if not skills:
        return ""
    
    section_title = "技术背景" if lang == 'cn' else "Technical Strengths"
    latex = f"\n\\begin{{rSection}}{{{section_title}}}\n\n"
    latex += "    \\begin{tabular}{@{} >{\\bfseries}l @{\\hspace{6ex}} l @{}}\n"
    
    if 'languages' in skills:
        lang_label = "编程语言" if lang == 'cn' else "Programming Languages"
        latex += f"        {lang_label} & {', '.join(skills['languages'])} \\\\\n"
    
    if 'technologies' in skills:
        tech_label = "大数据 \\& 分布式系统" if lang == 'cn' else "Big Data \\& Distributed Systems"
        latex += f"        {tech_label} & {', '.join(skills['technologies'])} \\\\\n"
    
    latex += "    \\end{tabular}\n\n"
    latex += "\\end{rSection}\n"
    return latex

def generate_latex(data, lang='en'):
    """Generate complete LaTeX document from data"""
    latex = generate_latex_header(data, lang)
    latex += generate_education_section(data.get('education', []), lang)
    latex += generate_experience_section(data.get('experience', []), lang)
    latex += generate_skills_section(data.get('skills', {}), lang)
    latex += "\n\\end{document}\n"
    return latex

def main():
    # Default paths
    script_dir = Path(__file__).parent
    input_file = script_dir / '..' / 'output' / 'combined.yaml'
    output_file = script_dir / '..' / 'output' / 'resume.tex'
    lang = 'en'
    
    # Override with command line arguments if provided
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    if len(sys.argv) > 3:
        lang = sys.argv[3]
    
    print(f"[2/4] Generating LaTeX from {input_file} (language: {lang})...")
    
    # Load combined YAML
    data = load_yaml_content(input_file)
    print(f"  ✓ Loaded combined data")
    
    # Generate LaTeX
    latex = generate_latex(data, lang)
    
    # Save LaTeX file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex)
    print(f"  → Generated LaTeX: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())