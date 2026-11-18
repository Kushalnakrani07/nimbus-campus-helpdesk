import re
import os
import sys

from generate_pdf_report import SimplePDF

def parse_and_render(md_path, pdf_path):
    pdf = SimplePDF(pdf_path)
    
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    in_code = False
    code_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    
    for line_raw in lines:
        line = line_raw.rstrip("\r\n")
        
        # Code block handler
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
                continue
            else:
                in_code = False
                pdf.add_code_block(code_lines)
                continue
                
        if in_code:
            code_lines.append(line)
            continue
            
        # Table handler
        if "|" in line and (line.strip().startswith("|") or line.strip().endswith("|")):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", p) for p in parts if p):
                continue
            if not in_table:
                in_table = True
                table_headers = parts
                table_rows = []
            else:
                table_rows.append(parts)
            continue
        else:
            if in_table:
                in_table = False
                pdf.add_table(table_headers, table_rows)
                
        if not line.strip():
            continue
            
        # Headings
        if line.startswith("# "):
            pdf.add_h1(line[2:].strip())
        elif line.startswith("## "):
            pdf.add_h2(line[3:].strip())
        elif line.startswith("### "):
            pdf.add_h3(line[4:].strip())
        elif line.startswith("- ") or line.startswith("* "):
            clean_text = re.sub(r"[*_`]", "", line[2:].strip())
            pdf.add_bullet(clean_text)
        elif re.match(r"^\d+\.\s+", line):
            clean_text = re.sub(r"[*_`]", "", re.sub(r"^\d+\.\s+", "", line))
            pdf.add_bullet(clean_text)
        elif line.startswith(">"):
            clean_text = re.sub(r"[*_`]", "", line.lstrip("> ").strip())
            pdf.add_p(f"[NOTE] {clean_text}", size=8.5, color=(0.1, 0.25, 0.5))
        elif line.startswith("---"):
            continue
        else:
            clean_text = re.sub(r"[*_`]", "", line.strip())
            pdf.add_p(clean_text)
            
    if in_table:
        pdf.add_table(table_headers, table_rows)
        
    pdf.build_pdf()
    print(f"Generated {pdf_path} ({pdf.current_page_num} pages) successfully.")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(base, "ASSIGNMENT_REPORT.md")
    pdf_file = os.path.join(base, "Nimbus_Labs_Helpdesk_Assignment_Report.pdf")
    parse_and_render(md_file, pdf_file)
