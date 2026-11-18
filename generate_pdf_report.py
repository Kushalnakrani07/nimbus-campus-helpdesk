import re
import os
import sys

class SimplePDF:
    def __init__(self, filename, page_width=595.28, page_height=841.89): # A4
        self.filename = filename
        self.width = page_width
        self.height = page_height
        self.pages = []
        self.current_stream = []
        self.margin_left = 50
        self.margin_right = 50
        self.margin_top = 50
        self.margin_bottom = 50
        self.usable_width = self.width - self.margin_left - self.margin_right
        self.y = self.height - self.margin_top
        self.current_page_num = 0
        self.new_page()

    def new_page(self):
        if self.current_page_num > 0:
            self.pages.append("\n".join(self.current_stream))
            self.current_stream = []
        self.current_page_num += 1
        self.y = self.height - self.margin_top
        # Header line
        self.current_stream.append("0.5 0.5 0.5 RG 0.5 w")
        self.current_stream.append(f"{self.margin_left} {self.height - 35} m {self.width - self.margin_right} {self.height - 35} l S")
        # Header text
        self.draw_text_line(self.margin_left, self.height - 30, "Nimbus Labs Campus Helpdesk Agent — B.Tech CSE Assignment Report", "F1", 8, (0.4, 0.4, 0.4))

    def ensure_space(self, needed_height):
        if self.y - needed_height < self.margin_bottom:
            self.new_page()

    def draw_text_line(self, x, y, text, font="F1", size=10, color=(0.1, 0.1, 0.1)):
        # Escape parenthesis
        clean_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        r, g, b = color
        self.current_stream.append(f"{r:.2f} {g:.2f} {b:.2f} rg")
        self.current_stream.append(f"BT /{font} {size} Tf {x:.2f} {y:.2f} Td ({clean_text}) Tj ET")

    def draw_rect(self, x, y, w, h, fill_color=None, stroke_color=None, line_width=1):
        cmds = []
        if fill_color:
            r, g, b = fill_color
            cmds.append(f"{r:.2f} {g:.2f} {b:.2f} rg")
        if stroke_color:
            r, g, b = stroke_color
            cmds.append(f"{r:.2f} {g:.2f} {b:.2f} RG {line_width} w")
        
        op = "B" if (fill_color and stroke_color) else ("f" if fill_color else "S")
        cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")
        self.current_stream.append(" ".join(cmds))

    def add_h1(self, text):
        self.ensure_space(38)
        self.y -= 15
        self.draw_text_line(self.margin_left, self.y, text, "F2", 15, (0.05, 0.15, 0.45))
        self.y -= 5
        self.current_stream.append("0.15 0.35 0.75 RG 1.5 w")
        self.current_stream.append(f"{self.margin_left} {self.y} m {self.width - self.margin_right} {self.y} l S")
        self.y -= 14

    def add_h2(self, text):
        self.ensure_space(28)
        self.y -= 12
        self.draw_text_line(self.margin_left, self.y, text, "F2", 12, (0.1, 0.25, 0.6))
        self.y -= 4
        self.current_stream.append("0.7 0.75 0.85 RG 0.8 w")
        self.current_stream.append(f"{self.margin_left} {self.y} m {self.width - self.margin_right} {self.y} l S")
        self.y -= 10

    def add_h3(self, text):
        self.ensure_space(20)
        self.y -= 8
        self.draw_text_line(self.margin_left, self.y, text, "F2", 10.5, (0.15, 0.2, 0.35))
        self.y -= 10

    def add_p(self, text, size=9.5, color=(0.12, 0.12, 0.12)):
        words = text.split()
        if not words:
            return
        lines = []
        cur_line = []
        char_limit = int(self.usable_width / (size * 0.52))
        
        for w in words:
            test_line = " ".join(cur_line + [w])
            if len(test_line) > char_limit:
                lines.append(" ".join(cur_line))
                cur_line = [w]
            else:
                cur_line.append(w)
        if cur_line:
            lines.append(" ".join(cur_line))
            
        for line in lines:
            self.ensure_space(size + 4)
            self.draw_text_line(self.margin_left, self.y, line, "F1", size, color)
            self.y -= (size + 4)
        self.y -= 3

    def add_bullet(self, text, size=9.2):
        words = text.split()
        if not words:
            return
        char_limit = int((self.usable_width - 15) / (size * 0.52))
        lines = []
        cur_line = []
        for w in words:
            if len(" ".join(cur_line + [w])) > char_limit:
                lines.append(" ".join(cur_line))
                cur_line = [w]
            else:
                cur_line.append(w)
        if cur_line:
            lines.append(" ".join(cur_line))
            
        for i, l in enumerate(lines):
            self.ensure_space(size + 4)
            if i == 0:
                self.draw_text_line(self.margin_left + 2, self.y, "\u2022", "F2", size + 1, (0.2, 0.4, 0.8))
            self.draw_text_line(self.margin_left + 15, self.y, l, "F1", size, (0.12, 0.12, 0.12))
            self.y -= (size + 4)

    def add_code_block(self, lines, size=7.5):
        line_height = size + 3
        needed = len(lines) * line_height + 14
        self.ensure_space(min(needed, 100)) # start block
        
        block_y_start = self.y
        # Draw background container in chunks if needed
        self.y -= 6
        for line in lines:
            if self.y - line_height < self.margin_bottom:
                # Fill box on current page
                h = block_y_start - self.y + 6
                self.draw_rect(self.margin_left, self.y - 2, self.usable_width, h, fill_color=(0.95, 0.96, 0.98), stroke_color=(0.8, 0.85, 0.9), line_width=0.6)
                self.new_page()
                block_y_start = self.y
                self.y -= 6
                
            clean_line = line[:100]
            self.draw_text_line(self.margin_left + 8, self.y, clean_line, "F3", size, (0.1, 0.15, 0.3))
            self.y -= line_height
            
        box_h = block_y_start - self.y + 4
        self.draw_rect(self.margin_left, self.y, self.usable_width, box_h, fill_color=None, stroke_color=(0.8, 0.85, 0.9), line_width=0.6)
        self.y -= 8

    def add_table(self, headers, rows):
        col_count = len(headers)
        if col_count == 0:
            return
            
        col_w = self.usable_width / col_count
        row_height = 20
        
        self.ensure_space(row_height * 2)
        # Header row
        self.draw_rect(self.margin_left, self.y - row_height, self.usable_width, row_height, fill_color=(0.9, 0.93, 0.98), stroke_color=(0.7, 0.75, 0.85), line_width=0.5)
        for i, h in enumerate(headers):
            self.draw_text_line(self.margin_left + (i * col_w) + 4, self.y - 14, h[:24], "F2", 8.5, (0.05, 0.15, 0.4))
        self.y -= row_height
        
        # Rows
        for r_idx, row in enumerate(rows):
            self.ensure_space(row_height)
            bg = (0.98, 0.99, 1.0) if r_idx % 2 == 1 else (1.0, 1.0, 1.0)
            self.draw_rect(self.margin_left, self.y - row_height, self.usable_width, row_height, fill_color=bg, stroke_color=(0.85, 0.88, 0.92), line_width=0.5)
            for i, val in enumerate(row):
                if i < col_count:
                    self.draw_text_line(self.margin_left + (i * col_w) + 4, self.y - 14, str(val)[:30], "F1", 8, (0.15, 0.15, 0.15))
            self.y -= row_height
        self.y -= 8

    def build_pdf(self):
        if self.current_stream:
            self.pages.append("\n".join(self.current_stream))
            
        total_pages = len(self.pages)
        # Append footer page numbering to each page stream
        for idx in range(total_pages):
            footer_stream = []
            footer_stream.append("0.5 0.5 0.5 RG 0.5 w")
            footer_stream.append(f"{self.margin_left} 35 m {self.width - self.margin_right} 35 l S")
            # Page number
            p_text = f"Page {idx + 1} of {total_pages} — Nimbus Labs Campus Helpdesk Project Report"
            clean_p = p_text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            footer_stream.append(f"0.4 0.4 0.4 rg BT /F1 8 Tf {self.margin_left} 24 Td ({clean_p}) Tj ET")
            self.pages[idx] = self.pages[idx] + "\n" + "\n".join(footer_stream)

        # Build PDF structure
        objects = []
        
        # 1. Catalog
        objects.append("<< /Type /Catalog /Pages 2 0 R >>")
        
        # 2. Pages
        page_refs = [f"{4 + i * 2} 0 R" for i in range(total_pages)]
        objects.append(f"<< /Type /Pages /Kids [ {' '.join(page_refs)} ] /Count {total_pages} >>")
        
        # 3. Fonts
        # F1 = Helvetica, F2 = Helvetica-Bold, F3 = Courier
        font_dict = (
            "<< /Font << "
            "/F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
            "/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> "
            "/F3 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> "
            ">> >>"
        )
        objects.append(font_dict)
        
        # Generate page objects and stream objects
        for idx, page_content in enumerate(self.pages):
            stream_bytes = page_content.encode("latin-1", "replace")
            page_obj_idx = 4 + idx * 2
            stream_obj_idx = page_obj_idx + 1
            
            # Page object
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Contents {stream_obj_idx} 0 R "
                f"/Resources 3 0 R >>"
            )
            objects.append(page_obj)
            
            # Stream object
            stream_obj = (
                f"<< /Length {len(stream_bytes)} >>\n"
                f"stream\n"
            ).encode("latin-1") + stream_bytes + b"\nendstream"
            objects.append(stream_obj)

        # Write cross-reference table & file
        with open(self.filename, "wb") as f:
            f.write(b"%PDF-1.4\n")
            offsets = [0]
            
            for i, obj in enumerate(objects, 1):
                offsets.append(f.tell())
                f.write(f"{i} 0 obj\n".encode("latin-1"))
                if isinstance(obj, str):
                    f.write(obj.encode("latin-1"))
                else:
                    f.write(obj)
                f.write(b"\nendobj\n")
                
            xref_pos = f.tell()
            f.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
            f.write(b"0000000000 65535 f \n")
            for offset in offsets[1:]:
                f.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
                
            f.write(b"trailer\n")
            f.write(f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("latin-1"))
            f.write(b"startxref\n")
            f.write(f"{xref_pos}\n".encode("latin-1"))
            f.write(b"%%EOF\n")

print("PDF Generator module compiled.")
