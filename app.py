import streamlit as st
import re

def filter_numbers(input_text):
    # Mengambil angka 3 atau 4 digit
    numbers = re.findall(r'\b\d{3,4}\b', input_text)
    
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

    GENAP = set("02468")
    GANJIL = set("13579")
    BESAR = set("56789")
    KECIL = set("01234")

    for num in numbers:
        # 1. Buang jika ada kembar 3 atau lebih
        if any(num.count(digit) >= 3 for digit in set(num)):
            continue

        num_set = set(num)
        
        # 2. Filter Jenis Digit
        if num_set.issubset(GENAP):
            results["Semua Genap (0,2,4,6,8)"].append(num)
        if num_set.issubset(GANJIL):
            results["Semua Ganjil (1,3,5,7,9)"].append(num)
        if num_set.issubset(BESAR):
            results["Semua Besar (5,6,7,8,9)"].append(num)
        if num_set.issubset(KECIL):
            results["Semua Kecil (0,1,2,3,4)"].append(num)

        # 3. Filter Pola Kembar
        length = len(num)
        if length == 4:
            # Mengambil tiap posisi digit
            d1, d2, d3, d4 = num[0], num[1], num[2], num[3]
            
            if len(num_set) == 4:
                results["Tanpa Kembar"].append(num)
            elif d1 == d2 and d3 == d4:
                results["Two Pair (xxyy)"].append(num)
            elif d1 == d3 or d2 == d4 or d1 == d4:
                results["Kembar Selang-Seling"].append(num)
            elif d1 == d2:
                results["Kembar Depan"].append(num)
            elif d2 == d3:
                results["Kembar Tengah"].append(num)
            elif d3 == d4:
                results["Kembar Belakang"].append(num)

        elif length == 3:
            d1, d2, d3 = num[0], num[1], num[2]
            if len(num_set) == 3:
                results["Tanpa Kembar"].append(num)
            elif d1 == d2:
                results["Kembar Depan"].append(num)
            elif d2 == d3:
                results["Kembar Belakang"].append(num)
            elif d1 == d3:
                results["Kembar Selang-Seling"].append(num)

    return results

# --- UI STREAMLIT ---
st.set_page_config(page_title="Pilah Angka Pro", layout="wide")
st.title("🔢 Pemilah Angka Pro (3D/4D)")

input_data = st.text_area("Masukkan angka (pisahkan spasi/koma/bintang):", height=200)

if st.button("Proses Sekarang"):
    if input_data:
        processed = filter_numbers(input_data)
        
        # Tampilkan hasil
        cols = st.columns(2)
        idx = 0
        for category, items in processed.items():
            if items:
                with cols[idx % 2]:
                    st.subheader(f"📂 {category}")
                    st.caption(f"Total: {len(items)}")
                    # Format output dengan bintang di antara angka dan di akhir
                    output_text = "*".join(items) + "*"
                    st.code(output_text, language="text")
                idx += 1
    else:
        st.warning("Silahkan masukkan angka dulu!")
