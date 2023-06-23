from flask import Flask, render_template, request, send_from_directory
import svgwrite
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        filename = generate_worksheet(text)
        return send_from_directory('.', filename, as_attachment=True)
    return render_template('home.html')

def generate_worksheet(text):
    lines = text.split('\n')
    max_length = 90  # The maximum length of a line of text. Adjust as needed.
    line_height = 40  # the height of a line of text, adjust as needed
    
    # Split long lines
    split_lines = []
    for line in lines:
        while len(line) > max_length:
            split_point = line[:max_length].rfind(' ')
            if split_point == -1:
                split_point = max_length
            split_lines.append(line[:split_point])
            line = line[split_point:].lstrip()  # Remove leading white space
        split_lines.append(line)
    
    svg_height = line_height * len(split_lines)  # set the height of the svg

    dwg = svgwrite.Drawing(profile='tiny', size=('100%', f'{svg_height}px'))  # set the height of the svg
    y = line_height
    y1 = -18
    y2 = -9
    y3 = 1
    y4 = 10
    y5 = 0
    for line in split_lines:
        dwg.add(dwg.line(start=(10, y+y1), end=(780, y+y1), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.5, stroke_dasharray="2 2"))  # ascender line
        dwg.add(dwg.line(start=(10, y+y2), end=(780, y+y2), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.5, stroke_dasharray="2 2"))  # median line
        dwg.add(dwg.line(start=(10, y+y3), end=(780, y+y3), stroke=svgwrite.rgb(150, 0, 0, "%"), stroke_opacity=0.5))  # descender line
        dwg.add(dwg.line(start=(10, y+y4), end=(780, y+y4), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.5, stroke_dasharray="2 2"))  # base line
        dwg.add(dwg.text(line, insert=(20, y+y5), fill="grey", fill_opacity=0.8, font_size="20px", font_family="'Pacifico', cursive"))
        dwg.add(dwg.line(start=(10, y+y1), end=(10, y+y3), stroke=svgwrite.rgb(150, 0, 0, "%"), stroke_opacity=0.5))  # left vertical line
        dwg.add(dwg.line(start=(780, y+y1), end=(780, y+y3), stroke=svgwrite.rgb(150, 0, 0, "%"), stroke_opacity=0.5))  # right vertical line
        y += line_height  # adjust line spacing as needed

    firstline = lines[0].replace("\"","").replace("\r","")
    clean_filename = re.sub(r'\W+', '', firstline.replace(' ', '_')) + '.html'
    filename = clean_filename
    filename = clean_filename
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<html><head><link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet"></head><body style="margin: 0; padding: 0;">')
        f.write('<div style="position: relative;">')
        f.write(dwg.tostring())
        f.write('</div></body></html>')
    return filename


if __name__ == "__main__":
    app.run()
