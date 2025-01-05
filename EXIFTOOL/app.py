from flask import Flask,request,render_template,jsonify
import os
import subprocess

app=Flask(__name__)

UPLOAD_FOLDER='upload'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    exiftool_path=r'C:\exiftool-13.11_64\exiftool-13.11_64\exiftool.exe'

    try:
        
        result = subprocess.run(
            [exiftool_path, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        metadata = result.stdout
    except Exception as e:
        return f"Error processing file: {str(e)}", 500
    finally:
        
        os.remove(filepath)

    return render_template('result.html', metadata=metadata)


if __name__=='__main__':
    app.run(debug=True)        
