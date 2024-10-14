from flask import Flask, render_template, request, redirect, url_for
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
            
            return f"File processed. Output saved at: {output_file}"

    return '''
    <!doctype html>
    <title>Fuzzy Match Application</title>
    <h1>Upload Excel File for Fuzzy Matching</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Run the app
if __name__ == "__main__":
    # Create an 'uploads' folder if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True)
# Route to download the processed file
@app.route('/download/<filename>')
def download_file(filename):
    uploads = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads, filename)
# Process the file with fuzzy matching
output_file = fuzzy_match(file_path)

# Redirect to download the processed file
return redirect(url_for('download_file', filename='output_with_match_scores.xlsx'))
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
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

# Route to download the processed file
@app.route('/download/<filename>')
def download_file(filename):
    uploads = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads, filename)

if __name__ == "__main__":
    app.run(debug=True)
