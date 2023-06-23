from flask import Flask, render_template, request, send_from_directory
import svgwrite
import os

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
    line_height = 60  # the height of a line of text, adjust as needed
    svg_height = line_height * len(lines)  # set the height of the svg

    dwg = svgwrite.Drawing(profile='tiny', size=('100%', f'{svg_height}px'))  # set the height of the svg
    y = line_height
    for line in lines:
        dwg.add(dwg.line(start=(10, y-20), end=(780, y-20), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.3, stroke_dasharray="2 2"))  # ascender line
        dwg.add(dwg.line(start=(10, y), end=(780, y), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.3))  # median line
        dwg.add(dwg.line(start=(10, y+20), end=(780, y+20), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.3, stroke_dasharray="2 2"))  # descender line
        dwg.add(dwg.line(start=(10, y+40), end=(780, y+40), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_opacity=0.3))  # base line
        dwg.add(dwg.text(line, insert=(20, y+20), fill="black", fill_opacity=0.3, font_size="20px", font_family="'Pacifico', cursive"))
        y += line_height  # adjust line spacing as needed

    filename = 'test.html'
    with open(filename, 'w') as f:
        f.write('<html><head><link href="https://fonts.googleapis.com/css?family=Indie+Flower&display=swap" rel="stylesheet"></head><body>')
        f.write(dwg.tostring())
        f.write('</body></html>')
    return filename

if __name__ == "__main__":
    app.run()
