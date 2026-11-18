import re
import html
import os
import subprocess

def md_to_html(md_text):
    lines = md_text.splitlines()
    html_out = []
    in_code = False
    code_lang = ""
    code_lines = []
    in_table = False
    table_header_done = False
    
    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
                code_lines = []
                continue
            else:
                in_code = False
                escaped = html.escape("\n".join(code_lines))
                html_out.append(f'<pre><code class="language-{code_lang}">{escaped}</code></pre>')
                continue
        if in_code:
            code_lines.append(line)
            continue
            
        # Table detection
        if "|" in line and (line.strip().startswith("|") or line.strip().endswith("|")):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", p) for p in parts if p):
                table_header_done = True
                continue
            if not in_table:
                in_table = True
                table_header_done = False
                html_out.append("<table>")
                html_out.append("<thead><tr>" + "".join(f"<th>{inline_format(p)}</th>" for p in parts) + "</tr></thead><tbody>")
            else:
                html_out.append("<tr>" + "".join(f"<td>{inline_format(p)}</td>" for p in parts) + "</tr>")
            continue
        else:
            if in_table:
                in_table = False
                html_out.append("</tbody></table>")
                
        # Empty lines
        if not line.strip():
            continue
            
        # Headers
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            hdr_text = inline_format(m.group(2))
            html_out.append(f"<h{lvl}>{hdr_text}</h{lvl}>")
            continue
            
        # Blockquote / Alert
        if line.startswith(">"):
            content = line.lstrip("> ").strip()
            html_out.append(f"<blockquote>{inline_format(content)}</blockquote>")
            continue
            
        # Horizontal rule
        if re.match(r"^(\*{3,}|-{3,}|_{3,})$", line.strip()):
            html_out.append("<hr/>")
            continue
            
        # Lists
        if re.match(r"^[-*]\s+(.*)$", line):
            content = re.sub(r"^[-*]\s+", "", line)
            html_out.append(f"<ul><li>{inline_format(content)}</li></ul>")
            continue
        if re.match(r"^\d+\.\s+(.*)$", line):
            content = re.sub(r"^\d+\.\s+", "", line)
            html_out.append(f"<ol><li>{inline_format(content)}</li></ol>")
            continue
            
        # Normal paragraph
        html_out.append(f"<p>{inline_format(line)}</p>")
        
    if in_table:
        html_out.append("</tbody></table>")
        
    return "\n".join(html_out)

def inline_format(text):
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text

def build():
    with open("ASSIGNMENT_REPORT.md", "r", encoding="utf-8") as f:
        md_content = f.read()
        
    body_html = md_to_html(md_content)
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Nimbus Labs Campus Helpdesk Agent - Report</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.5;
    font-size: 10.5pt;
    padding: 0;
    margin: 0;
  }}
  h1 {{
    font-size: 18pt;
    color: #0f172a;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 24pt;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 14pt;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
    margin-top: 18pt;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 11.5pt;
    color: #1e293b;
    margin-top: 12pt;
    page-break-after: avoid;
  }}
  p {{
    margin: 6pt 0;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 600;
    color: #0f172a;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10pt;
    border-radius: 4px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8pt;
    overflow-x: auto;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0969da;
    padding: 1pt 3pt;
    border-radius: 3px;
  }}
  pre code {{
    background-color: transparent;
    color: inherit;
    padding: 0;
  }}
  blockquote {{
    border-left: 4px solid #3b82f6;
    margin: 8pt 0;
    padding: 6pt 12pt;
    background-color: #eff6ff;
    color: #1e40af;
  }}
  ul, ol {{
    margin: 4pt 0 8pt 20pt;
    padding: 0;
  }}
  li {{
    margin-bottom: 3pt;
  }}
  hr {{
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 16pt 0;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 8pt;
  }}
  a {{
    color: #2563eb;
    text-decoration: none;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    with open("ASSIGNMENT_REPORT.html", "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("Generated ASSIGNMENT_REPORT.html successfully.")
    
    # Render PDF using headless Chrome
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--print-to-pdf=Nimbus_Labs_Helpdesk_Assignment_Report.pdf",
        "ASSIGNMENT_REPORT.html"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("Generated Nimbus_Labs_Helpdesk_Assignment_Report.pdf successfully!")
    else:
        print("Chrome error:", res.stderr)

if __name__ == "__main__":
    build()
