from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def lock_pdf():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        
        if file and password:
            # Save the uploaded PDF to a temporary file
            input_pdf_path = os.path.join('static', file.filename)
            file.save(input_pdf_path)
            
            output_pdf_path = os.path.join('static', 'locked_' + file.filename)
            
            # Create a PDF writer object to write the new PDF
            pdf_writer = PdfWriter()
            # Create a PDF reader object to read the original PDF
            pdf_reader = PdfReader(input_pdf_path)
            
            # Loop through all the pages of the original PDF and add them to the new PDF
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            
            # Encrypt the new PDF with the specified password
            pdf_writer.encrypt(password)
            
            # Save the locked PDF
            with open(output_pdf_path, 'wb') as out:
                pdf_writer.write(out)
            
            # Provide the locked PDF for download
            return send_file(output_pdf_path, as_attachment=True)
    
    return render_template('index.html')

