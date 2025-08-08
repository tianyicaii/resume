#!/bin/bash
# Resume Generation Pipeline
# Orchestrates the complete resume generation process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/data"
OUTPUT_DIR="$PROJECT_ROOT/output"
TEMPLATE_DIR="$PROJECT_ROOT/templates/default"
SRC_DIR="$PROJECT_ROOT/src"

# Parse command line arguments
COMPILER="xelatex"  # Default to XeLaTeX for Chinese support
VERBOSE=false
KEEP_TEMP=false
CLEAN_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_ONLY=true
            shift
            ;;
        --pdflatex)
            COMPILER="pdflatex"
            shift
            ;;
        --xelatex)
            COMPILER="xelatex"
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --keep-temp)
            KEEP_TEMP=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --clean       Clean output directory and exit"
            echo "  --xelatex     Use XeLaTeX compiler (default, supports Chinese)"
            echo "  --pdflatex    Use pdflatex compiler (English only)"
            echo "  --verbose,-v  Show detailed output"
            echo "  --keep-temp   Keep temporary files (combined.yaml)"
            echo "  --help,-h     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Handle clean operation
if [ "$CLEAN_ONLY" = true ]; then
    echo -e "${YELLOW}Cleaning output directory...${NC}"
    
    # Check if output directory exists
    if [ -d "$OUTPUT_DIR" ]; then
        # Count files before cleaning
        FILE_COUNT=$(find "$OUTPUT_DIR" -type f | wc -l)
        
        # Remove everything except .gitkeep
        find "$OUTPUT_DIR" -type f ! -name '.gitkeep' -delete 2>/dev/null || true
        
        echo -e "${GREEN}✓ Cleaned $FILE_COUNT files from output directory${NC}"
        echo -e "${GREEN}  Preserved: .gitkeep${NC}"
    else
        echo -e "${YELLOW}  Output directory doesn't exist${NC}"
    fi
    
    echo -e "\n${GREEN}✨ Clean complete!${NC}"
    exit 0
fi

# Header
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Resume Generation Pipeline       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to process one language
process_language() {
    local LANG=$1
    local SUFFIX="-$LANG"
    
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Processing: ${LANG^^} version${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}\n"
    
    # Step 1: Combine YAML files
    echo -e "${YELLOW}Step 1: Combining modular YAML files (${LANG})...${NC}"
    if python3 "$SRC_DIR/combine_yaml.py" "$DATA_DIR" "$OUTPUT_DIR/combined${SUFFIX}.yaml" "$LANG"; then
        echo -e "${GREEN}✓ Step 1 completed${NC}\n"
    else
        echo -e "${RED}✗ Step 1 failed${NC}"
        return 1
    fi
    
    # Step 2: Generate LaTeX
    echo -e "${YELLOW}Step 2: Generating LaTeX from YAML (${LANG})...${NC}"
    if python3 "$SRC_DIR/generate_latex.py" "$OUTPUT_DIR/combined${SUFFIX}.yaml" "$OUTPUT_DIR/resume${SUFFIX}.tex" "$LANG"; then
        echo -e "${GREEN}✓ Step 2 completed${NC}\n"
    else
        echo -e "${RED}✗ Step 2 failed${NC}"
        return 1
    fi
    
    # Step 3: Copy cls file
    echo -e "${YELLOW}Step 3: Copying LaTeX class file (${LANG})...${NC}"
    if python3 "$SRC_DIR/copy_cls.py" "$TEMPLATE_DIR" "$OUTPUT_DIR"; then
        echo -e "${GREEN}✓ Step 3 completed${NC}\n"
    else
        echo -e "${RED}✗ Step 3 failed${NC}"
        return 1
    fi
    
    # Step 4: Compile PDF
    echo -e "${YELLOW}Step 4: Compiling PDF with $COMPILER (${LANG})...${NC}"
    if python3 "$SRC_DIR/compile_pdf.py" "$OUTPUT_DIR/resume${SUFFIX}.tex" "$COMPILER"; then
        echo -e "${GREEN}✓ Step 4 completed${NC}\n"
    else
        echo -e "${RED}✗ Step 4 failed${NC}"
        return 1
    fi
    
    return 0
}

# Process English version
if ! process_language "en"; then
    echo -e "${RED}✗ English version failed${NC}"
    exit 1
fi

# Process Chinese version
if ! process_language "cn"; then
    echo -e "${RED}✗ Chinese version failed${NC}"
    exit 1
fi

# Clean up temporary files
if [ "$KEEP_TEMP" = false ]; then
    echo -e "${YELLOW}Cleaning up temporary files...${NC}"
    rm -f "$OUTPUT_DIR"/*.aux "$OUTPUT_DIR"/*.log "$OUTPUT_DIR"/*.out "$OUTPUT_DIR"/*.synctex.gz
    if [ "$VERBOSE" = false ]; then
        rm -f "$OUTPUT_DIR/combined-en.yaml" "$OUTPUT_DIR/combined-cn.yaml"
    fi
    echo -e "${GREEN}✓ Cleanup completed${NC}\n"
fi

# Success message
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         ✅ Pipeline Complete!          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "📄 Resumes generated:"
echo -e "   English: ${BLUE}$OUTPUT_DIR/resume-en.pdf${NC}"
echo -e "   Chinese: ${BLUE}$OUTPUT_DIR/resume-cn.pdf${NC}"
echo ""

