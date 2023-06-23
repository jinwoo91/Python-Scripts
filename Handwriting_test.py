from flask import Flask, request, send_file
import svgwrite
from svgwrite import cm, mm 
import cairosvg
import pdfkit
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        filename = generate_worksheet(text)
        return send_file(filename, as_attachment=True)
    return '''
        <form method="POST">
        Text: <textarea name="text" rows="10" cols="50"></textarea><br>
        <input type="submit" value="Submit"><br>
        </form>
    '''

def generate_worksheet(text):
    # Create an SVG drawing
    dwg = svgwrite.Drawing('temp.svg', profile='tiny')

    # Define the style for the guideline and guide text
    style = "fill:gray;fill-opacity:0.3;"

    # Add a guideline and guide text every 30 pixels
    y = 30
    for line in text.split('\n'):
        dwg.add(dwg.line(start=(10, y), end=(780, y), stroke=svgwrite.rgb(0, 0, 0, '0.3')))
        dwg.add(dwg.line(start=(10, y+10), end=(780, y+10), stroke=svgwrite.rgb(0, 0, 0, '0.3')))
        dwg.add(dwg.text(line, insert=(20, y+20), style=style))
        y += 40

    # Save the SVG file
    dwg.save()

    # Convert the SVG file to PDF
    cairosvg.svg2pdf(url='./temp.svg', write_to='output.pdf')

    # Delete the temporary SVG file
    os.remove('temp.svg')

    return 'output.pdf'

if __name__ == '__main__':
    app.run(port=5000)