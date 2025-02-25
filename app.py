from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)

def pdf_to_latex(pdf_file):
    # Read the PDF file using PyPDF2
    reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n\n"
    
    # Wrap the extracted text in a basic LaTeX document structure
    latex_template = r"""\documentclass{article}
\begin{document}
%s
\end{document}""" % extracted_text
    
    return latex_template

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file provided", 400
        file = request.files['pdf_file']
        if file.filename == '':
            return "No file selected", 400
        
        # Convert PDF to LaTeX
        latex_content = pdf_to_latex(file)
        return render_template('result.html', latex_content=latex_content)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
