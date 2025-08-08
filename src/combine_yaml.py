#!/usr/bin/env python3
"""
Step 1: Combine modular YAML files into a single consolidated YAML
"""

import yaml
import sys
from pathlib import Path

def load_yaml_file(yaml_file):
    """Load a single YAML file"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def combine_yaml_files(data_dir, lang='en'):
    """Combine all modular YAML files into one structure"""
    combined = {}
    suffix = f'-{lang}'
    
    # Load personal info
    personal_file = data_dir / f'personal{suffix}.yaml'
    if personal_file.exists():
        combined['personal'] = load_yaml_file(personal_file)
        print(f"  ✓ Loaded personal info ({lang})")
    
    # Load education entries (sorted by filename in reverse for newest first)
    education_dir = data_dir / 'education'
    if education_dir.exists():
        education_files = sorted(education_dir.glob(f'*{suffix}.yaml'), reverse=True)
        combined['education'] = [load_yaml_file(f) for f in education_files]
        print(f"  ✓ Loaded {len(education_files)} education entries ({lang})")
    
    # Load experience entries (sorted by filename in reverse for newest first)
    experience_dir = data_dir / 'experience'
    if experience_dir.exists():
        experience_files = sorted(experience_dir.glob(f'*{suffix}.yaml'), reverse=True)
        combined['experience'] = [load_yaml_file(f) for f in experience_files]
        print(f"  ✓ Loaded {len(experience_files)} experience entries ({lang})")
    
    # Load skills
    skills_file = data_dir / f'skills{suffix}.yaml'
    if skills_file.exists():
        combined['skills'] = load_yaml_file(skills_file)
        print(f"  ✓ Loaded skills ({lang})")
    
    # Load credit/acknowledgement
    credit_file = data_dir / f'credit{suffix}.yaml'
    if credit_file.exists():
        combined['credit'] = load_yaml_file(credit_file)
        print(f"  ✓ Loaded credit ({lang})")
    
    return combined

def save_combined_yaml(data, output_file):
    """Save combined data to a YAML file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def main():
    # Default paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / '..' / 'data'
    output_file = script_dir / '..' / 'output' / 'combined.yaml'
    lang = 'en'
    
    # Override with command line arguments if provided
    if len(sys.argv) > 1:
        data_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    if len(sys.argv) > 3:
        lang = sys.argv[3]
    
    print(f"[1/4] Combining YAML files from {data_dir} (language: {lang})...")
    
    # Combine files
    data = combine_yaml_files(data_dir, lang)
    
    # Save combined YAML
    save_combined_yaml(data, output_file)
    print(f"  → Saved combined data to {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())