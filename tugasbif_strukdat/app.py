import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
# Mengimpor fungsi komputasi dari pipeline.py
from pipeline import jalankan_pipeline

app = Flask(__name__)

# Konfigurasi direktori penyimpanan data raw
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Spesifikasi ekstensi file yang valid
ALLOWED_EXTENSIONS = {'fasta', 'fastq', 'fa', 'fq'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validasi transmisi file
        if 'file_sekuens' not in request.files:
            return "Error: Tidak ada parameter file_sekuens."
        
        file = request.files['file_sekuens']
        
        if file.filename == '':
            return "Error: File belum dipilih."
            
        if file and allowed_file(file.filename):
            # Sanitasi nama file dan penyimpanan lokal
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Eksekusi komputasi pipeline menggunakan file yang baru diunggah
            top_3, plot_path, csv_path = jalankan_pipeline(filepath)
            
            # Render hasil ke antarmuka sekunder
            return render_template('hasil.html', top_3=top_3)
            
        else:
            return "Error: Format file tidak didukung. Harap unggah format FASTA/FASTQ."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)