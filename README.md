# Bioinformatic Pipeline: GC Content Analyzer
Pipeline bioinformatika berbasis web untuk analisis sekuens genomik.

## Fitur
- Parsing data FASTA/FASTQ.
- Kalkulasi metrik: GC Content, GC Skew, dan Sequence Length.
- Visualisasi data statistik (distribusi GC).
- Ekspor hasil analisis ke format CSV.

## Struktur Folder
```text
projekstrukdatbif/
├── app.py
├── README.md
├── static/
│   ├── dna_video.mp4
│   ├── foto_bioinfo.jpg
│   ├── gc_plot.png
│   ├── hasil_analisis.csv
│   ├── logo_fmipa.png
│   └── logo_ipb.png
└── templates/
    ├── hasil.html
    └── index.html

## Cara Menjalankan
1. Clone repository ini.
2. Install dependensi: `pip install flask matplotlib`
3. Jalankan aplikasi: `python app.py`
4. Akses melalui browser di: `http://127.0.0.1:5000`

## Teknologi
- Backend: Flask (Python)
- Frontend: HTML/CSS (Futuristic UI)
- Visualization: Matplotlib
