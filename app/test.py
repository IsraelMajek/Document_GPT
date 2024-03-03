# Import necessary libraries
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS module for handling Cross-Origin Resource Sharing
from PyPDF2 import PdfReader  # Import PdfReader for reading PDF files
import io

# Initialize Flask application
app = Flask(__name__)
# Apply CORS to our Flask app for handling cross-origin requests
CORS(app)

# Define a route for both POST and GET requests
@app.route('/', methods=['POST', 'GET'])
def upload():
    # Handle GET request: return the upload form template
    if request.method == 'GET':
        return render_template("upload.html")

    # Fetch the file from the form data
    file = request.files.get('file')

    # Check if the file is not submitted
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    try:
        # Check if the submitted file is a PDF
        if file.filename.endswith('.pdf'):
            reader = PdfReader(file)  # Initialize PdfReader with the uploaded file

            # Check if the PDF is encrypted
            if reader.is_encrypted:
                return jsonify({'error': 'Encrypted PDFs are not supported'}), 400

            text = ''
            # Loop through each page of the PDF
            for page_num in range(len(reader.pages)):
                # Extract text from the current page and append it to the text variable
                text += reader.pages[page_num].extract_text()

            # Check if no text was extracted from the PDF
            if not text.strip():
                return jsonify({'error': 'No text found in the PDF'}), 400

        # Check if the submitted file is a TXT file
        elif file.filename.endswith('.txt'):
            try:
                # Attempt to read and decode the file's content as UTF-8
                text = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return jsonify({'error': 'Unable to decode text file. Ensure it is UTF-8 encoded.'}), 400

        else:
            # Return an error if the file type is unsupported
            return jsonify({'error': 'Unsupported file type'}), 400

        # Return the extracted text as JSON
        return jsonify({'text': text})

    except Exception as e:
        # Return any other errors encountered during processing
        return jsonify({'error': str(e)}), 500

    
# Check if the script is the main program and run the app
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development purposes
