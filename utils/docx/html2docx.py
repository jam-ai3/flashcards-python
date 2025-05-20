import io
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import RGBColor, Pt
import re

def css_color_to_wd_color_index(css_color):
    color_map = {
        'var(--tt-highlight-yellow)': WD_COLOR_INDEX.YELLOW,
        '#fff59d': WD_COLOR_INDEX.YELLOW,
        'yellow': WD_COLOR_INDEX.YELLOW,
        'var(--tt-highlight-green)': WD_COLOR_INDEX.BRIGHT_GREEN,
        '#b7e1cd': WD_COLOR_INDEX.BRIGHT_GREEN,
        'green': WD_COLOR_INDEX.BRIGHT_GREEN,
        'var(--tt-highlight-blue)': WD_COLOR_INDEX.BLUE,
        '#00b0f0': WD_COLOR_INDEX.BLUE,
        'blue': WD_COLOR_INDEX.BLUE,
        'var(--tt-highlight-red)': WD_COLOR_INDEX.PINK,
        '#ffd6e0': WD_COLOR_INDEX.PINK,
        'pink': WD_COLOR_INDEX.PINK,
        'var(--tt-highlight-purple)': WD_COLOR_INDEX.VIOLET,
        '#ee82ee': WD_COLOR_INDEX.VIOLET,
        'purple': WD_COLOR_INDEX.VIOLET,
        'red': WD_COLOR_INDEX.PINK, # No direct red highlight
    }
    if not css_color:
        return WD_COLOR_INDEX.YELLOW
    css_color = css_color.strip().lower()
    return color_map.get(css_color, WD_COLOR_INDEX.YELLOW)

def get_combined_formatting(node):
    formatting = {
        'bold': False,
        'italic': False,
        'underline': False,
        'strike': False,
        'highlight': None,
        'hyperlink': None,
        'code': False,
        'sup': False,
        'sub': False,
    }
    current = node
    while isinstance(current, Tag):
        name = current.name
        if name in ['strong', 'b']:
            formatting['bold'] = True
        if name in ['em', 'i']:
            formatting['italic'] = True
        if name == 'u':
            formatting['underline'] = True
        if name in ['s', 'strike']:
            formatting['strike'] = True
        if name == 'mark':
            bg_color = None
            if current.get('data-color'):
                bg_color = current['data-color']
            if not bg_color and current.get('style'):
                match = re.search(r'background-color:\s*([^;]+)', current['style'])
                if match:
                    bg_color = match.group(1).strip()
            formatting['highlight'] = css_color_to_wd_color_index(bg_color)
        if name == 'a' and current.get('href'):
            formatting['hyperlink'] = current['href']
        if name == 'code':
            formatting['code'] = True
        if name == 'sup':
            formatting['sup'] = True
        if name == 'sub':
            formatting['sub'] = True
        current = current.parent
    return formatting

def add_hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0000FF')
    rPr.append(color)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    new_run.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def process_runs(node, paragraph):
    if isinstance(node, NavigableString):
        text = str(node)
        if text.strip():
            formatting = get_combined_formatting(node.parent)
            if formatting['hyperlink']:
                add_hyperlink(paragraph, formatting['hyperlink'], text)
            else:
                run = paragraph.add_run(text)
                run.bold = formatting['bold']
                run.italic = formatting['italic']
                run.underline = formatting['underline']
                run.font.strike = formatting['strike']
                if formatting['highlight'] is not None:
                    run.font.highlight_color = formatting['highlight']
                if formatting['code']:
                    run.font.name = 'Consolas'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(68, 84, 106)
                if formatting['sup']:
                    vertalign = OxmlElement('w:vertAlign')
                    vertalign.set(qn('w:val'), 'superscript')
                    run._element.rPr.append(vertalign)
                if formatting['sub']:
                    vertalign = OxmlElement('w:vertAlign')
                    vertalign.set(qn('w:val'), 'subscript')
                    run._element.rPr.append(vertalign)
    elif isinstance(node, Tag):
        for child in node.children:
            process_runs(child, paragraph)

def html_to_docx_convertion(html) -> io.BytesIO:
    document = Document()
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body if soup.body else soup
    for element in body.children:
        if isinstance(element, str):
            continue  # Skip text nodes outside tags
        if not isinstance(element, Tag):
            continue
        # Headings
        if element.name and element.name.startswith('h'):
            level = int(element.name[1])
            paragraph = document.add_paragraph()
            paragraph.style = f'Heading {level}'
            if element.get('style'):
                style = element.get('style')
                if 'text-align: center' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif 'text-align: right' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif 'text-align: justify' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                elif 'text-align: left' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            process_runs(element, paragraph)
        # Paragraphs (with alignment)
        elif element.name == 'p':
            if not element.get_text(strip=True):
                continue
            paragraph = document.add_paragraph()
            if element.get('style'):
                style = element.get('style')
                if 'text-align: center' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif 'text-align: right' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif 'text-align: justify' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                elif 'text-align: left' in style:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            process_runs(element, paragraph)
        # Code blocks
        elif element.name == 'pre':
            paragraph = document.add_paragraph()
            paragraph.style = 'Normal'
            for code in element.find_all('code'):
                run = paragraph.add_run(code.get_text())
                run.font.name = 'Consolas'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(68, 84, 106)
        # Blockquote
        elif element.name == 'blockquote':
            paragraph = document.add_paragraph()
            paragraph.style = 'Intense Quote'
            for child in element.children:
                process_runs(child, paragraph)
        # Unordered List (normal bullets)
        elif element.name == 'ul' and element.get('data-type', None) != 'taskList':
            for li in element.find_all('li', recursive=False):
                p = document.add_paragraph(style='List Bullet')
                # If <li> contains <p>, process only its content
                found_p = li.find('p', recursive=False)
                if found_p:
                    for child in found_p.children:
                        process_runs(child, p)
                else:
                    for child in li.children:
                        if isinstance(child, NavigableString):
                            process_runs(child, p)
                        elif isinstance(child, Tag) and child.name not in ['ul', 'ol']:
                            process_runs(child, p)
        # Ordered List
        elif element.name == 'ol':
            for li in element.find_all('li', recursive=False):
                p = document.add_paragraph(style='List Number')
                found_p = li.find('p', recursive=False)
                if found_p:
                    for child in found_p.children:
                        process_runs(child, p)
                else:
                    for child in li.children:
                        if isinstance(child, NavigableString):
                            process_runs(child, p)
                        elif isinstance(child, Tag) and child.name not in ['ul', 'ol']:
                            process_runs(child, p)
        # Task List (checkboxes)
        elif element.name == 'ul' and element.get('data-type', None) == 'taskList':
            for li in element.find_all('li', recursive=False):
                checked = li.get('data-checked', 'false') == 'true'
                box = '☑' if checked else '☐'
                p = document.add_paragraph()
                p.add_run(box + " ")
                div = li.find('div')
                if div:
                    for child in div.children:
                        process_runs(child, p)
        file_stream = io.BytesIO()
        document.save(file_stream)
        file_stream.seek(0)
        return file_stream