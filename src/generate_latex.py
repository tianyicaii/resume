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
\\usepackage{{fontawesome}}
\\usepackage{{xcolor}}

\\name{{\\heiti {data['personal']['name']}}}
\\address{{ \\kaishu {{\\color{{gray}}\\faPhone\\ \\faWeixin}}\\ \\ {data['personal']['phone']} {{}} {{}} {{}} {{}} {{\\color{{gray}}\\faEnvelope}}\\ \\ {data['personal']['email']} }}

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
\\usepackage{{fontawesome}}
\\usepackage{{xcolor}}

\\name{{{data['personal']['name']}}}
\\address{{{{\\color{{gray}}\\faPhone\\ \\faWeixin}}\\ \\ {data['personal']['phone']} {{}} {{}} {{}} {{}} {{\\color{{gray}}\\faEnvelope}}\\ \\ {data['personal']['email']}}}

\\begin{{document}}
"""

def generate_education_section(education_list, lang='en'):
    """Generate education section"""
    if not education_list:
        return ""
    
    section_title = "教育背景" if lang == 'cn' else "Education"
    latex = f"\n\\begin{{rSection}}{{{section_title}}}\n"
    
    for edu in education_list:
        # Combine degree and major if both exist
        if 'major' in edu:
            if lang == 'cn':
                degree_text = f"{edu['degree']}，{edu['major']}"
            else:
                degree_text = f"{edu['degree']} in {edu['major']}"
        else:
            degree_text = edu['degree']
        
        if lang == 'cn':
            latex += f"""    
    \\textbf{{{edu['school']}}} \\hfill \\textit{{{edu['dates']}}} \\\\ 
    {{\\kaishu {degree_text}，GPA: {edu['gpa']} }} \\hfill \\textit{{{edu['location']}}}
"""
        else:
            latex += f"""    
    \\textbf{{{edu['school']}}} \\hfill \\textit{{{edu['dates']}}} \\\\ 
    {{{degree_text}, GPA: {edu['gpa']}}} \\hfill \\textit{{{edu['location']}}}
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
            title = f"{exp['product']}, {exp['team']}" if exp['product'] else exp['team']
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
        latex += f"        {lang_label} & {skills['languages'][0] if isinstance(skills['languages'], list) and len(skills['languages']) == 1 else ', '.join(skills['languages'])} \\\\\n"
    
    if 'systems' in skills:
        sys_label = "系统架构" if lang == 'cn' else "Systems"
        latex += f"        {sys_label} & {skills['systems'][0] if isinstance(skills['systems'], list) and len(skills['systems']) == 1 else ', '.join(skills['systems'])} \\\\\n"
    
    if 'databases' in skills:
        db_label = "数据库" if lang == 'cn' else "Databases"
        latex += f"        {db_label} & {skills['databases'][0] if isinstance(skills['databases'], list) and len(skills['databases']) == 1 else ', '.join(skills['databases'])} \\\\\n"
    
    if 'infrastructure' in skills:
        infra_label = "基础设施" if lang == 'cn' else "Infrastructure"
        latex += f"        {infra_label} & {skills['infrastructure'][0] if isinstance(skills['infrastructure'], list) and len(skills['infrastructure']) == 1 else ', '.join(skills['infrastructure'])} \\\\\n"
    
    if 'technologies' in skills:
        tech_label = "大数据 \\& 分布式系统" if lang == 'cn' else "Big Data \\& Distributed Systems"
        latex += f"        {tech_label} & {skills['technologies'][0] if isinstance(skills['technologies'], list) and len(skills['technologies']) == 1 else ', '.join(skills['technologies'])} \\\\\n"
    
    latex += "    \\end{tabular}\n\n"
    latex += "\\end{rSection}\n"
    return latex

def generate_credit_section(credit, lang='en'):
    """Generate credit/acknowledgement section"""
    if not credit or 'acknowlegement' not in credit:
        return ""
    
    latex = "\n\\vfill\n"  # Push to bottom of page
    latex += "\\begin{center}\n"
    latex += "    \\footnotesize\\textit{"
    
    # Process each line separately
    lines = []
    for line in credit['acknowlegement']:
        # Escape special LaTeX characters in URLs
        escaped_line = line.strip().replace('_', '\\_')
        lines.append(escaped_line)
    
    # Join with line breaks
    latex += ' \\\\\n    '.join(lines)
    
    latex += "}\n"
    latex += "\\end{center}\n"
    return latex

def generate_latex(data, lang='en'):
    """Generate complete LaTeX document from data"""
    latex = generate_latex_header(data, lang)
    latex += generate_education_section(data.get('education', []), lang)
    latex += generate_experience_section(data.get('experience', []), lang)
    latex += generate_skills_section(data.get('skills', {}), lang)
    latex += generate_credit_section(data.get('credit', {}), lang)
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