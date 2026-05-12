import streamlit as st
import re

def filter_numbers(input_text):
    numbers = re.findall(r'\b\d{3,4}\b', input_text)
    
    results = {
        "Semua Genap (0,2,4,6,8)": [],
        "Semua Ganjil (1,3,5,7,9)": [],
        "Semua Besar (5,6,7,8,9)": [],
        "Semua Kecil (0,1,2,3,4)": [],
        "Angka Campuran (Murni Random)": [], # Kategori Baru
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
        if any(num.count(digit) >= 3 for digit in set(num)):
            continue

        num_set = set(num)
        
        # Cek status spesifik
        is_all_genap = num_set.issubset(GENAP)
        is_all_ganjil = num_set.issubset(GANJIL)
        is_all_besar = num_set.issubset(BESAR)
        is_all_kecil = num_set.issubset(KECIL)
        is_no_twin = len(num_set) == len(num)

        # 1. Masukkan ke kategori spesifik digit
        if is_all_genap: results["Semua Genap (0,2,4,6,8)"].append(num)
        if is_all_ganjil: results["Semua Ganjil (1,3,5,7,9)"].append(num)
        if is_all_besar: results["Semua Besar (5,6,7,8,9)"].append(num)
        if is_all_kecil: results["Semua Kecil (0,1,2,3,4)"].append(num)

        # 2. LOGIKA BARU: Angka Campuran
        # Syarat: Tidak kembar DAN bukan salah satu dari 4 kategori di atas
        if is_no_twin and not (is_all_genap or is_all_ganjil or is_all_besar or is_all_kecil):
            results["Angka Campuran (Murni Random)"].append(num)

        # 3. Masukkan ke kategori pola kembar (seperti sebelumnya)
        length = len(num)
        if is_no_twin:
            results["Tanpa Kembar"].append(num)
        elif length == 4:
            a, b, c, d = num[0], num[1], num[2], num[3]
            if a == b and c == d: results["Two Pair (xxyy)"].append(num)
            elif a == c or b == d or a == d: results["Kembar Selang-Seling"].append(num)
            elif a == b: results["Kembar Depan"].append(num)
            elif b == c: results["Kembar Tengah"].append(num)
            elif c == d: results["Kembar Belakang"].append(num)
        elif length == 3:
            a, b, c = num[0], num[1], num[2]
            if a == b: results["Kembar Depan"].append(num)
            elif b == c: results["Kembar Belakang"].append(num)
            elif a == c: results["Kembar Selang-Seling"].append(num)

    return results

# (Bagian UI Streamlit tetap sama seperti kode sebelumnya)
