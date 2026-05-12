import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="4D Filter Pro", layout="wide")
st.title("🎯 4D Number Matcher & Formatter")

# 1. Database Internal (0000 - 9999)
@st.cache_data
def load_database():
    return [str(i).zfill(4) for i in range(10000)]

all_numbers = load_database()

# 2. Area Input
st.subheader("Input Data")
raw_input = st.text_area(
    "Masukkan nomor 4D (bisa pakai spasi, koma, bintang, atau baris baru):", 
    placeholder="Contoh: 1234, 5566*7788 9900",
    height=150
)

# 3. Logika Pemrosesan
if raw_input:
    # Membersihkan segala karakter non-digit menjadi spasi, lalu split
    import re
    # Mengambil hanya sekumpulan 4 angka
    input_list = re.findall(r'\d{4}', raw_input)
    # Hapus duplikat dan urutkan
    input_list = sorted(list(set(input_list)))
    
    # Filter Nomor
    pernah_keluar = input_list
    belum_keluar_total = [n for n in all_numbers if n not in input_list]
    
    def is_kembar(n):
        return len(set(n)) < 4

    belum_keluar_polos = [n for n in belum_keluar_total if not is_kembar(n)]
    belum_keluar_kembar = [n for n in belum_keluar_total if is_kembar(n)]

    # --- Tampilan Hasil ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"Pernah Keluar: {len(pernah_keluar)}")
        if st.checkbox("Tampilkan Pernah Keluar"):
            # Output format: 1234*2345*
            output_1 = "*".join(pernah_keluar) + "*" if pernah_keluar else ""
            st.code(output_1)

    with col2:
        st.info(f"Belum Keluar (No Kembar): {len(belum_keluar_polos)}")
        if st.checkbox("Tampilkan Belum Keluar (No Kembar)"):
            output_2 = "*".join(belum_keluar_polos) + "*" if belum_keluar_polos else ""
            st.code(output_2)

    with col3:
        st.warning(f"Belum Keluar (Ada Kembar): {len(belum_keluar_kembar)}")
        if st.checkbox("Tampilkan Belum Keluar (Kembar)"):
            output_3 = "*".join(belum_keluar_kembar) + "*" if belum_keluar_kembar else ""
            st.code(output_3)
else:
    st.info("Masukkan data untuk diproses.")
