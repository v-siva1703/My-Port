import os
import sys

# Standard character widths for Helvetica (in 1/1000 of font size)
CHAR_WIDTHS_HELVETICA = {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667, "'": 191,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 278, ';': 278, '<': 584, '=': 584, '>': 584, '?': 556,
    '@': 1015, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469, '_': 556,
    '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 500, 'f': 278, 'g': 556,
    'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556,
    'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722,
    'x': 500, 'y': 500, 'z': 500, '{': 334, '|': 260, '}': 334, '~': 584
}

CHAR_WIDTHS_BOLD = {
    ' ': 278, '!': 333, '"': 474, '#': 556, '$': 556, '%': 889, '&': 722, "'": 238,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 333, ';': 333, '<': 584, '=': 584, '>': 584, '?': 611,
    '@': 975, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 584, '_': 556,
    '`': 333, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611,
    'h': 611, 'i': 278, 'j': 278, 'k': 556, 'l': 278, 'm': 889, 'n': 611, 'o': 611,
    'p': 611, 'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'w': 778,
    'x': 556, 'y': 556, 'z': 500, '{': 389, '|': 280, '}': 389, '~': 584
}

def string_width(text, font_size, is_bold=False):
    table = CHAR_WIDTHS_BOLD if is_bold else CHAR_WIDTHS_HELVETICA
    w = 0
    for ch in text:
        w += table.get(ch, 520)
    return (w / 1000.0) * font_size

def escape_pdf_str(text):
    replacements = {
        '–': '-', '—': '-', '‘': "'", '’': "'", '“': '"', '”': '"',
        '•': '*', '➔': '>', '❖': '*', '●': '*', '…': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    return text

def wrap_text(text, max_width, font_size, is_bold=False):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if string_width(test_line, font_size, is_bold) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

class PDFCanvas:
    def __init__(self, width=595.28, height=841.89):
        self.width = width
        self.height = height
        self.pages = []
        self.current_page_ops = []
        self.current_annots = []
        self.page_annots = []

    def new_page(self):
        if self.current_page_ops:
            self.pages.append(self.current_page_ops)
            self.page_annots.append(self.current_annots)
        self.current_page_ops = []
        self.current_annots = []

    def finish(self):
        if self.current_page_ops:
            self.pages.append(self.current_page_ops)
            self.page_annots.append(self.current_annots)
            self.current_page_ops = []
            self.current_annots = []

    def rect(self, x, y, w, h, fill_color=(0,0,0), stroke_color=None, stroke_width=1):
        ops = ["q"]
        if fill_color:
            ops.append(f"{fill_color[0]:.3f} {fill_color[1]:.3f} {fill_color[2]:.3f} rg")
            ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
        if stroke_color:
            ops.append(f"{stroke_color[0]:.3f} {stroke_color[1]:.3f} {stroke_color[2]:.3f} RG")
            ops.append(f"{stroke_width:.2f} w")
            ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")
        ops.append("Q")
        self.current_page_ops.append("\n".join(ops))

    def line(self, x1, y1, x2, y2, color=(0,0,0), width=1):
        ops = [
            "q",
            f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} RG",
            f"{width:.2f} w",
            f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S",
            "Q"
        ]
        self.current_page_ops.append("\n".join(ops))

    def text(self, text, x, y, font="F1", size=10, color=(0,0,0)):
        escaped = escape_pdf_str(text)
        ops = [
            "BT",
            f"/{font} {size:.2f} Tf",
            f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg",
            f"1 0 0 1 {x:.2f} {y:.2f} Tm",
            f"({escaped}) Tj",
            "ET"
        ]
        self.current_page_ops.append("\n".join(ops))

    def add_link(self, x1, y1, x2, y2, uri):
        self.current_annots.append({
            'rect': [x1, y1, x2, y2],
            'uri': uri
        })

    def build_pdf_bytes(self):
        self.finish()
        
        catalog_id = 1
        pages_id = 2
        font_f1_id = 3
        font_f2_id = 4
        font_f3_id = 5
        res_id = 6
        
        next_id = 7
        page_ids = []
        stream_ids = []
        annot_id_map = {}
        
        for p_idx in range(len(self.pages)):
            p_id = next_id; next_id += 1
            s_id = next_id; next_id += 1
            page_ids.append(p_id)
            stream_ids.append(s_id)
            ann_ids = []
            for a in self.page_annots[p_idx]:
                ann_ids.append(next_id)
                next_id += 1
            annot_id_map[p_idx] = ann_ids

        obj_dict = {}
        obj_dict[catalog_id] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode('latin1')
        kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
        obj_dict[pages_id] = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>".encode('latin1')
        
        obj_dict[font_f1_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        obj_dict[font_f2_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        obj_dict[font_f3_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"
        obj_dict[res_id] = f"<< /Font << /F1 {font_f1_id} 0 R /F2 {font_f2_id} 0 R /F3 {font_f3_id} 0 R >> /ProcSet [/PDF /Text] >>".encode('latin1')
        
        for idx, (p_id, s_id) in enumerate(zip(page_ids, stream_ids)):
            ann_list = annot_id_map[idx]
            ann_str = f"/Annots [{' '.join([f'{aid} 0 R' for aid in ann_list])}]" if ann_list else ""
            obj_dict[p_id] = f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] /Contents {s_id} 0 R /Resources {res_id} 0 R {ann_str} >>".encode('latin1')
            
            stream_data = "\n".join(self.pages[idx]).encode('latin1')
            obj_dict[s_id] = f"<< /Length {len(stream_data)} >>\nstream\n".encode('latin1') + stream_data + b"\nendstream"
            
            for a_idx, aid in enumerate(ann_list):
                ann = self.page_annots[idx][a_idx]
                r = ann['rect']
                uri = ann['uri']
                obj_dict[aid] = f"<< /Type /Annot /Subtype /Link /Rect [{r[0]:.2f} {r[1]:.2f} {r[2]:.2f} {r[3]:.2f}] /Border [0 0 0] /A << /S /URI /URI ({escape_pdf_str(uri)}) >> >>".encode('latin1')

        out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
        offsets = {}
        total_objs = max(obj_dict.keys())
        
        for oid in range(1, total_objs + 1):
            if oid in obj_dict:
                offsets[oid] = len(out)
                out.extend(f"{oid} 0 obj\n".encode('latin1'))
                out.extend(obj_dict[oid])
                out.extend(b"\nendobj\n")
                
        xref_offset = len(out)
        out.extend(f"xref\n0 {total_objs + 1}\n0000000000 65535 f \n".encode('latin1'))
        for oid in range(1, total_objs + 1):
            off = offsets.get(oid, 0)
            out.extend(f"{off:010d} 00000 n \n".encode('latin1'))
            
        out.extend(f"trailer\n<< /Size {total_objs + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin1'))
        return bytes(out)

class ResumeBuilder:
    def __init__(self, filename="public/Resume.pdf"):
        self.filename = filename
        self.canvas = PDFCanvas(595.28, 841.89)
        self.left_margin = 42
        self.right_margin = 553.28
        self.content_width = self.right_margin - self.left_margin
        self.top_margin = 802
        self.bottom_margin = 42
        self.y = self.top_margin
        self.current_page_num = 1
        
        # Color palette
        self.c_primary = (0.09, 0.18, 0.36)       # #172e5c Deep navy
        self.c_accent = (0.24, 0.35, 0.70)        # #3d59b3 Royal blue
        self.c_text = (0.15, 0.20, 0.28)          # #273347 Charcoal dark text
        self.c_muted = (0.38, 0.44, 0.53)         # #617087 Slate grey
        self.c_divider = (0.80, 0.84, 0.90)       # Light border line
        self.c_bullet = (0.24, 0.35, 0.70)        # Bullet dot

    def start_page(self, continuation=False):
        self.canvas.rect(0, 0, 595.28, 841.89, fill_color=(1, 1, 1))
        # Top subtle colored bar
        self.canvas.rect(0, 836.89, 595.28, 5, fill_color=self.c_primary)
        
        if continuation:
            self.canvas.text("YOGASUNDER S  |  Resume", self.left_margin, 818, font="F2", size=8.5, color=self.c_muted)
            self.canvas.text(f"Page {self.current_page_num} of 2", self.right_margin - 50, 818, font="F1", size=8.5, color=self.c_muted)
            self.canvas.line(self.left_margin, 812, self.right_margin, 812, color=self.c_divider, width=0.75)
            self.y = 794
        else:
            self.y = self.top_margin

    def ensure_space(self, needed_pt):
        if self.y - needed_pt < self.bottom_margin:
            self.canvas.line(self.left_margin, self.bottom_margin + 12, self.right_margin, self.bottom_margin + 12, color=self.c_divider, width=0.5)
            self.canvas.text(f"Page {self.current_page_num} of 2", 270, self.bottom_margin, font="F1", size=8, color=self.c_muted)
            
            self.canvas.new_page()
            self.current_page_num += 1
            self.start_page(continuation=True)

    def draw_header(self):
        # Name
        self.canvas.text("YOGASUNDER S", self.left_margin, self.y, font="F2", size=20, color=self.c_primary)
        self.y -= 16
        
        # Title / Designation
        self.canvas.text("Techno-Functional Consultant  |  Full Stack Developer", self.left_margin, self.y, font="F2", size=10.5, color=self.c_accent)
        self.y -= 15
        
        # Contact line 1: Email, Phone, Location
        self.canvas.text("E-Mail: yogasunders@gmail.com   |   Mobile: +91 8524867725   |   Coimbatore, Tamil Nadu", self.left_margin, self.y, font="F1", size=9, color=self.c_text)
        email_w = string_width("E-Mail: yogasunders@gmail.com", 9)
        self.canvas.add_link(self.left_margin, self.y - 2, self.left_margin + email_w, self.y + 9, "mailto:yogasunders@gmail.com")
        self.y -= 13
        
        # Contact line 2: GitHub, LinkedIn, Portfolio
        cur_x = self.left_margin
        gh_prefix = "GitHub: "
        gh_url = "https://github.com/yogasunders-hub"
        li_prefix = "   |   LinkedIn: "
        li_url = "https://www.linkedin.com/in/yogasunder-s-059ba6265"
        port_suffix = "   |   Portfolio: Yogasunder S-portfolio"
        
        self.canvas.text(gh_prefix, cur_x, self.y, font="F2", size=8.5, color=self.c_muted)
        cur_x += string_width(gh_prefix, 8.5, is_bold=True)
        
        self.canvas.text(gh_url, cur_x, self.y, font="F1", size=8.5, color=self.c_accent)
        gh_w = string_width(gh_url, 8.5)
        self.canvas.add_link(cur_x, self.y - 2, cur_x + gh_w, self.y + 8, gh_url)
        cur_x += gh_w
        
        self.canvas.text(li_prefix, cur_x, self.y, font="F1", size=8.5, color=self.c_muted)
        cur_x += string_width(li_prefix, 8.5)
        
        self.canvas.text("linkedin.com/in/yogasunder-s", cur_x, self.y, font="F1", size=8.5, color=self.c_accent)
        li_w = string_width("linkedin.com/in/yogasunder-s", 8.5)
        self.canvas.add_link(cur_x, self.y - 2, cur_x + li_w, self.y + 8, li_url)
        cur_x += li_w
        
        self.canvas.text(port_suffix, cur_x, self.y, font="F1", size=8.5, color=self.c_muted)
        self.y -= 14
        
        self.canvas.line(self.left_margin, self.y, self.right_margin, self.y, color=self.c_primary, width=1.2)
        self.y -= 14

    def draw_section_heading(self, title):
        self.ensure_space(32)
        self.canvas.text(title.upper(), self.left_margin, self.y, font="F2", size=10.5, color=self.c_primary)
        self.canvas.line(self.left_margin, self.y - 3, self.right_margin, self.y - 3, color=self.c_divider, width=0.8)
        self.y -= 13

    def draw_paragraph(self, text, font_size=9, line_height=12.5, is_bold=False):
        lines = wrap_text(text, self.content_width, font_size, is_bold)
        self.ensure_space(len(lines) * line_height + 4)
        for line in lines:
            self.canvas.text(line, self.left_margin, self.y, font="F2" if is_bold else "F1", size=font_size, color=self.c_text)
            self.y -= line_height
        self.y -= 4

    def draw_skill_item(self, label, items):
        self.ensure_space(14)
        label_str = f"{label} : "
        self.canvas.text(label_str, self.left_margin, self.y, font="F2", size=8.8, color=self.c_text)
        label_w = string_width(label_str, 8.8, is_bold=True)
        
        rem_width = self.content_width - label_w
        item_lines = wrap_text(items, rem_width, 8.8, is_bold=False)
        for i, line in enumerate(item_lines):
            x_pos = self.left_margin + label_w if i == 0 else self.left_margin + 15
            if i > 0:
                self.ensure_space(12)
            self.canvas.text(line, x_pos, self.y, font="F1", size=8.8, color=self.c_text)
            self.y -= 11.5
        self.y -= 1

    def draw_experience_item(self, title, company_location, period, bullets):
        self.ensure_space(36 + len(bullets) * 14)
        self.canvas.text(title, self.left_margin, self.y, font="F2", size=9.8, color=self.c_primary)
        period_w = string_width(period, 9, is_bold=True)
        self.canvas.text(period, self.right_margin - period_w, self.y, font="F2", size=9, color=self.c_accent)
        self.y -= 12
        
        self.canvas.text(company_location, self.left_margin, self.y, font="F3", size=8.8, color=self.c_muted)
        self.y -= 11
        
        for bullet in bullets:
            bullet_lines = wrap_text(bullet, self.content_width - 16, 8.6, is_bold=False)
            self.ensure_space(len(bullet_lines) * 11.5 + 2)
            self.canvas.text(">", self.left_margin + 2, self.y, font="F2", size=8.5, color=self.c_accent)
            for bline in bullet_lines:
                self.canvas.text(bline, self.left_margin + 12, self.y, font="F1", size=8.6, color=self.c_text)
                self.y -= 11.2
        self.y -= 4

    def draw_project_item(self, title, tech_str, period, bullets):
        self.ensure_space(36 + len(bullets) * 14)
        self.canvas.text(title, self.left_margin, self.y, font="F2", size=9.8, color=self.c_primary)
        if period:
            period_w = string_width(period, 8.8, is_bold=True)
            self.canvas.text(period, self.right_margin - period_w, self.y, font="F2", size=8.8, color=self.c_accent)
        self.y -= 11.5
        
        tech_lines = wrap_text(f"Tech Stack: {tech_str}", self.content_width, 8.5, is_bold=False)
        for tline in tech_lines:
            self.ensure_space(11)
            self.canvas.text(tline, self.left_margin, self.y, font="F3", size=8.5, color=self.c_muted)
            self.y -= 10.5
            
        for bullet in bullets:
            bullet_lines = wrap_text(bullet, self.content_width - 16, 8.6, is_bold=False)
            self.ensure_space(len(bullet_lines) * 11.2 + 2)
            self.canvas.text(">", self.left_margin + 2, self.y, font="F2", size=8.5, color=self.c_accent)
            for bline in bullet_lines:
                self.canvas.text(bline, self.left_margin + 12, self.y, font="F1", size=8.6, color=self.c_text)
                self.y -= 11.2
        self.y -= 4

    def draw_education(self, institution, period, degree, cgpa):
        self.ensure_space(28)
        self.canvas.text(institution, self.left_margin, self.y, font="F2", size=9.8, color=self.c_primary)
        p_w = string_width(period, 9, is_bold=True)
        self.canvas.text(period, self.right_margin - p_w, self.y, font="F2", size=9, color=self.c_accent)
        self.y -= 12
        
        deg_str = f"{degree}  |  {cgpa}"
        self.canvas.text(deg_str, self.left_margin, self.y, font="F1", size=9, color=self.c_text)
        self.y -= 12

    def draw_bullet_list(self, items):
        for item in items:
            lines = wrap_text(item, self.content_width - 16, 8.6, is_bold=False)
            self.ensure_space(len(lines) * 11.5 + 2)
            self.canvas.text("*", self.left_margin + 2, self.y, font="F2", size=9, color=self.c_accent)
            for line in lines:
                self.canvas.text(line, self.left_margin + 12, self.y, font="F1", size=8.6, color=self.c_text)
                self.y -= 11.2
            self.y -= 1
        self.y -= 4

    def generate(self):
        # PAGE 1
        self.start_page(continuation=False)
        self.draw_header()
        
        # PROFESSIONAL SUMMARY
        self.draw_section_heading("Professional Summary")
        summary_text = (
            "B.E. graduate (2020-2024) and Techno-Functional Consultant with expertise in technical "
            "development (HTML, CSS, JavaScript, React JS, Angular, Node.js, SQL) and functional ERP processes. "
            "Experienced in building full-cycle web-based ERP systems, SAP Business One add-ons, and hardware-ERP integration. "
            "Served as lead Functional Consultant across projects while also owning technical delivery. "
            "Completed a 90-day Full Stack Master Class and SAP Business One training at Techconz Nexora AI Pvt. Ltd."
        )
        self.draw_paragraph(summary_text)
        
        # EDUCATION
        self.draw_section_heading("Education")
        self.draw_education(
            "Karpagam College of Engineering",
            "2020 - 2024",
            "Bachelor of Engineering",
            "CGPA - 8.83"
        )

        # SKILLS SUMMARY
        self.draw_section_heading("Skills Summary")
        self.draw_skill_item("Programming Languages", "Python, JavaScript, C/C++")
        self.draw_skill_item("Frontend Development", "HTML, CSS, React JS, Redux Toolkit (RTK Query), Angular")
        self.draw_skill_item("Backend Development", "SQL, PostgreSQL, Prisma ORM, Node.js, Express.js")
        self.draw_skill_item("ERP & Functional Consulting", "SAP Business One, ERP Systems, Techno-Functional Analysis, Business Requirement Gathering")
        self.draw_skill_item("AI Tools", "Prompt Engineering, AI Code Generation, LLM Tools")
        self.y -= 4
        
        # EXPERIENCE
        self.draw_section_heading("Experience")
        self.draw_experience_item(
            "Associate Software Engineer",
            "( Techconz Nexora Pvt Ltd ) , Coimbatore, India",
            "Sept 2025 - Present",
            [
                "Work as a Full Stack Developer, owning both frontend and backend delivery across ERP and business applications.",
                "Built a CRM application delivering a low-latency, responsive web experience for customer and business data management.",
                "Handle customer requirements directly through on-site client visits, translating business needs into technical specifications.",
                "Built working proficiency with AI-assisted development tools to accelerate delivery.",
                "Leveraged AI-assisted development tools for faster delivery, debugging, and code review across full-stack projects."
            ]
        )
        
        self.draw_experience_item(
            "SAP Business One Trainee - Techno-Functional Consultant",
            "( Techconz Nexora Pvt Ltd ) , Coimbatore, India",
            "Aug 2024 - June 2025",
            [
                "Completed an 11-month internship focused on SAP Business One as a Techno-Functional Consultant, covering both technical development and functional consulting.",
                "Built low-latency SAP Business One add-on screens using the SAP B1 SDK and SQL.",
                "Visited clients on-site to gather, validate, and translate business requirements into technical specifications.",
                "Gained hands-on experience configuring and supporting SAP B1 software for client environments."
            ]
        )
        
        # LANGUAGES
        self.draw_section_heading("Languages")
        self.canvas.text("English, Tamil", self.left_margin, self.y, font="F1", size=9, color=self.c_text)
        self.y -= 14
        
        # Page 1 Footer
        self.canvas.line(self.left_margin, self.bottom_margin + 12, self.right_margin, self.bottom_margin + 12, color=self.c_divider, width=0.5)
        self.canvas.text("Page 1 of 2", 270, self.bottom_margin, font="F1", size=8, color=self.c_muted)
        
        # PAGE 2: PROJECTS & ACHIEVEMENTS
        self.canvas.new_page()
        self.current_page_num = 2
        self.start_page(continuation=True)
        
        # PROJECTS SECTION
        self.draw_section_heading("Projects")
        self.draw_project_item(
            "FoodOne",
            "React JS, RTK Query, Node.js, Express.js, Prisma, PostgreSQL",
            "Nov 2026 - Present",
            [
                "Developed a food-industry management platform end-to-end, covering Hotel Management, Catering Management, and related operations.",
                "Owned frontend and backend delivery, using RTK Query on the client and Prisma with PostgreSQL for data modelling and persistence."
            ]
        )
        
        self.draw_project_item(
            "TechCare",
            "React JS, RTK Query, Node.js, Express.js, Prisma, PostgreSQL",
            "Sept 2026 - Nov 2026",
            [
                "Developed a business management application end-to-end as a full-stack developer, covering both Trading and Service modules.",
                "Built a responsive React frontend with RTK Query for data fetching and caching, backed by Node.js and Express.js APIs using Prisma ORM with PostgreSQL."
            ]
        )
        
        self.draw_project_item(
            "POS (Billing ERP)",
            "React JS, RTK Query, Node.js, Express.js, Prisma, PostgreSQL",
            "",
            [
                "Contributed to a team-built Billing ERP and Point-of-Sale system, developing selected modules across frontend and backend.",
                "Implemented module features using React with RTK Query, and Node.js/Express.js APIs with Prisma and PostgreSQL."
            ]
        )
        
        self.draw_project_item(
            "ERP Management System",
            "Angular, Node.js, Express.js, SQL",
            "June 2026 - Sept 2026",
            [
                "Working in a team to build a complete ERP system managing end-to-end business operations, owning both frontend and backend development.",
                "Delivering a responsive, low-latency ERP dashboard as the sole full-stack contributor on the team."
            ]
        )
        
        self.draw_project_item(
            "Lead Generation System",
            "React JS, Node.js, Express.js, SQL",
            "Apr 2026 - June 2026",
            [
                "Working in a team to build a lead capture and tracking system automating prospect qualification and sales pipeline management, owning both frontend and backend development.",
                "Delivering a complete lead-to-customer tracking system with real-time analytics."
            ]
        )
        
        self.draw_project_item(
            "CRM System",
            "React JS, Node.js, Express.js, SQL",
            "Nov 2025 - Mar 2026",
            [
                "Designed and built an end-to-end CRM system solo as a full-stack developer to manage customers, inventory, and sales records.",
                "Independently delivered a responsive, low-latency dashboard for efficient business data management."
            ]
        )
        
        self.draw_project_item(
            "SAP Business One Add-on Development",
            "SAP B1 SDK, SQL",
            "Dec 2024 - Oct 2025",
            [
                "Developed custom add-on screens and modules for SAP Business One to extend ERP functionality based on client requirements.",
                "Improved workflow efficiency by creating customized SAP B1 add-on interfaces."
            ]
        )
        
        # ACHIEVEMENTS & CERTIFICATIONS
        self.draw_section_heading("Achievements & Certifications")
        achievements_list = [
            "Received 1st Rank and Certificate of Excellence at the department level during B.E.",
            "Presented projects at the International Conference on Artificial Intelligence, Cybersecurity and Game Design.",
            "Presented research at the Second International Conference on Renewable and Sustainable Energy Technologies.",
            "Organized the 'Brain Busters' puzzle event in college, demonstrating leadership and event management skills.",
            "Completed Embedded Systems Hands-on Training at Vector India, Bangalore.",
            "Completed PCB Design and Fabrication Internship at Enthu Technology Solutions.",
            "Completed 90-Day Full Stack Master Class and SAP Business One training at Techconz Nexora AI Pvt. Ltd."
        ]
        self.draw_bullet_list(achievements_list)
        
        # Page 2 Footer
        self.canvas.line(self.left_margin, self.bottom_margin + 12, self.right_margin, self.bottom_margin + 12, color=self.c_divider, width=0.5)
        self.canvas.text("Page 2 of 2", 270, self.bottom_margin, font="F1", size=8, color=self.c_muted)
        
        # Build and write PDF file
        pdf_bytes = self.canvas.build_pdf_bytes()
        with open(self.filename, 'wb') as f:
            f.write(pdf_bytes)
        print(f"Successfully generated {self.filename} ({len(pdf_bytes)} bytes across {len(self.canvas.pages)} pages).")

if __name__ == "__main__":
    builder = ResumeBuilder("public/Resume.pdf")
    builder.generate()
