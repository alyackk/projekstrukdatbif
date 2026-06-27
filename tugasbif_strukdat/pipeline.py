import matplotlib
matplotlib.use('Agg')  
import csv
import matplotlib.pyplot as plt
import os

def jalankan_pipeline(filepath):
    sekuens_list = [] 
    
    # 1. Parsing data FASTA / FASTQ
    with open(filepath, 'r') as file:
        header = ""
        seq = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    sekuens_list.append({"header": header, "sekuens": seq})
                header = line[1:]
                seq = ""
            elif not line.startswith("@") and not line.startswith("+"): # Abaikan baris kualitas FASTQ
                seq += line
        if header:
            sekuens_list.append({"header": header, "sekuens": seq})

    hasil_analisis = []
    
    # 2. Analisis Komprehensif
    for item in sekuens_list:
        seq = item["sekuens"].upper()
        frekuensi = {'A': seq.count('A'), 'T': seq.count('T'), 'G': seq.count('G'), 'C': seq.count('C')}
        total = sum(frekuensi.values())
        
        # Kalkulasi Metrik
        gc_content = ((frekuensi['G'] + frekuensi['C']) / total * 100) if total > 0 else 0
        gc_skew = (frekuensi['G'] - frekuensi['C']) / (frekuensi['G'] + frekuensi['C']) if (frekuensi['G'] + frekuensi['C']) > 0 else 0
        
        hasil_analisis.append({
            "header": item["header"],
            "frekuensi": frekuensi,
            "gc_content": gc_content,
            "gc_skew": round(gc_skew, 4),
            "length": total
        })

    # 3. Sorting untuk Top 3
    sorted_data = sorted(hasil_analisis, key=lambda x: x['gc_content'], reverse=True)
    top_3 = sorted_data[:3]

    # 4. Visualisasi Grafik 
    os.makedirs('static', exist_ok=True)
    plot_path = 'static/gc_plot.png'
    
    plt.figure(figsize=(8, 5), facecolor='#1b1b3a')
    ax = plt.axes()
    ax.set_facecolor('#1b1b3a')
    
    plt.hist([x['gc_content'] for x in hasil_analisis], bins=20, color='#FF00A0', edgecolor='#FEFFD9')
    plt.title('Distribusi GC Content', color='#FEFFD9', fontsize=14, pad=15)
    plt.xlabel('GC Content (%)', color='#FEFFD9')
    plt.ylabel('Frekuensi', color='#FEFFD9')
    plt.tick_params(colors='#FEFFD9')
    
    plt.savefig(plot_path)
    plt.close()

    # 5. Ekspor SEMUA data ke CSV
    csv_path = 'static/hasil_analisis.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Header', 'Length', 'GC_Content', 'GC_Skew']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in hasil_analisis: 
            writer.writerow({
                'Header': item['header'],
                'Length': item['length'],
                'GC_Content': round(item['gc_content'], 2),
                'GC_Skew': item['gc_skew']
            })

    return top_3, plot_path, csv_path