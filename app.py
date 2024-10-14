from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
from fuzzywuzzy import fuzz
import os

# Initialize Flask app
app = Flask(__name__)

# Fuzzy match function
def fuzzy_match(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    def get_fuzzy_match_score(row):
        name_a = row['Company A']
        name_b = row['Company B']
        return fuzz.ratio(name_a, name_b)
    df['Match Score'] = df.apply(get_fuzzy_match_score, axis=1)
    output_file = os.path.join(os.path.dirname(file_path), 'output_with_match_scores.xlsx')
    df.to_excel(output_file, index=False)
    return output_file

# Route to upload file
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            # Process the file with fuzzy matching
            output_file = fuzzy_match(file_path)

            # Redirect to download the processed file
            return redirect(url_for('download_file', filename='output_with_match_scores.xlsx'))

    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fuzzy Match Application</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 50%;
                margin: 100px auto;
                background-color: white;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                text-align: center;
            }
            h1 {
                color: #333;
            }
            form {
                margin-top: 20px;
            }
            input[type="file"] {
                padding: 10px;
                margin-bottom: 20px;
                font-size: 16px;
            }
            input[type="submit"] {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #218838;
            }
            img {
                max-width: 150px;  /* Adjust size of the logo */
                margin-bottom: 20px;
            }
            p.instructions {
                font-size: 16px;
                color: #555;
            }
            a {
                text-decoration: none;
                color: #007bff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.png" alt="Logo">
            <h1>Upload Excel File for Fuzzy Matching</h1>
            <p class="instructions">Please upload an Excel file with two columns: <strong>'Company A'</strong> and <strong>'Company B'</strong>.</p>
            <p class="instructions">Download a <a href="/static/sample_file.xlsx" target="_blank">sample file</a> for reference.</p>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <br>
                <input type="submit" value="Upload">
            </form>
        </div>
    </body>
    </html>
    '''

# Route to download the processed file
@app.route('/download/<filename>')
def download_file(filename):
    uploads = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads, filename)

# Create 'uploads' directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

if __name__ == "__main__":
    app.run(debug=True)
