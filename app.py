import streamlit as st
import re

def filter_numbers(input_text):
    # Mengambil semua deretan angka 3 atau 4 digit
    numbers = re.findall(r'\b\d{3,4}\b', input_text)
    
    # Inisialisasi kategori
    results = {
        "Semua Genap (0,2,4,6,8)": [],
        "Semua Ganjil (1,3,5,7,9)": [],
        "Semua Besar (5,6,7,8,9)": [],
        "Semua Kecil (0,1,2,3,4)": [],
        "Tanpa Kembar": [],
        "Two Pair (xxyy)": [],
        "Kembar Depan": [],
        "Kembar Tengah": [],
        "Kembar Belakang": [],
        "Kembar Selang-Seling": [],
    }

    # Set pembantu
    GENAP = set("02468")
    GANJIL = set("13579")
    BESAR = set("56789")
    KECIL = set("01234")

    for num in numbers:
        # 1. VALIDASI: Buang jika ada kembar 3 atau lebih (misal 1112, 222)
        if any(num.count(digit) >= 3 for digit in set(num)):
            continue

        # 2. FILTER BERDASARKAN JENIS DIGIT
        num_set = set(num)
        if num_set.issubset(GENAP):
            results["Semua Genap (0,2,4,6,8)"].append(num)
        if num_set.issubset(GANJIL):
            results["Semua Ganjil (1,3,5,7,9)"].append(num)
        if num_set.issubset(BESAR):
            results["Semua Besar (5,6,7,8,9)"].append(num)
        if num_set.issubset(KECIL):
            results["Semua Kecil (0,1,2,3,4)"].append(num)

        # 3. FILTER BERDASARKAN POLA KEMBAR
        length = len(num)
        if length == 4:
            a, b, c, d = num[0], num[1], num[2], num[3]
            if len(num_set) == 4:
                results["Tanpa Kembar"].append(num)
            elif a == b and c == d:
                results["Two Pair (xxyy)"].append(num)
            elif a == c or b == d or a == d: # Selang seling atau ABAC / ABCA
                results["Kembar Selang-Seling"].append(num)
            elif a == b:
                results["Kembar Depan"].append(num)
            elif b == c:
                results["Kembar Tengah"].append(num)
            elif c == d:
                results["Kembar Belakang"].append(num)

        elif length == 3:
            a, b, c = num[0], num[1], num[2]
            if len(num_set) == 3:
                results["Tanpa Kembar"].append(num)
            elif a == b:
                results["Kembar Depan"].append(num)
            elif b == c:
                results["Kembar Belakang"].append(num)
            elif a == c:
                results["Kembar Selang-Seling"].append(num)

    return results

# --- UI STREAMLIT ---
st.set_page_config(page_title="Pilah Angka V2", layout="wide")
st.title("🔢 Pemilah Angka Pro (3D/4D)")
st.write("Saring ribuan angka berdasarkan pola kembar, ganjil-genap, dan besar-kecil secara otomatis.")

input_data = st.text_area("Tempelkan angka di sini (pisahkan pakai spasi, koma, atau bintang):", height=200)

if st.button("Proses Sekarang"):
    if input_data:
        processed = filter_numbers(input_data)
        
        # Tampilkan hasil dalam kolom agar rapi
        cols = st.columns(2)
        for i, (category, items) in enumerate(processed.items()):
            col = cols[i % 2]
            with col:
                if items:
                    st.subheader(f"📂 {category}")
                    st.caption(f"Total: {len(items)} angka")
                    output_text = "*".join(items) + "*"
                    st.code(output_text, language="text")
                else:
                    st.info(f"📂 {category}: Tidak ada data")
    else:
        st.warning("Silahkan masukkan angka dulu!")
