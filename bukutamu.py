import streamlit as st
import pandas as pd
from datetime import datetime

# --- Judul Aplikasi ---
st.title("📖 Buku Tamu Digital")
st.write("Selamat datang! Silakan isi buku tamu di bawah ini.")

# --- Inisialisasi DataFrame untuk menyimpan data tamu ---
if "buku_tamu" not in st.session_state:
    st.session_state.buku_tamu = pd.DataFrame(columns=["Waktu", "Nama", "Email", "Pesan"])

# --- Form Input Buku Tamu ---
with st.form("form_buku_tamu"):
    nama = st.text_input("Nama Lengkap")
    email = st.text_input("Email")
    pesan = st.text_area("Pesan")

    submitted = st.form_submit_button("Kirim")

    if submitted:
        if nama and email and pesan:
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[waktu, nama, email, pesan]], columns=["Waktu", "Nama", "Email", "Pesan"])
            st.session_state.buku_tamu = pd.concat([st.session_state.buku_tamu, new_data], ignore_index=True)
            st.success("✅ Terima kasih! Data Anda telah disimpan.")
        else:
            st.warning("⚠️ Harap isi semua kolom terlebih dahulu.")

# --- Tampilkan Data Buku Tamu ---
st.markdown("---")
st.subheader("📋 Daftar Buku Tamu")

if not st.session_state.buku_tamu.empty:
    st.dataframe(st.session_state.buku_tamu, use_container_width=True)
else:
    st.info("Belum ada data tamu yang masuk.")

# --- Opsi Simpan ke File CSV ---
if not st.session_state.buku_tamu.empty:
    csv = st.session_state.buku_tamu.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Data Buku Tamu (CSV)",
        data=csv,
        file_name='buku_tamu.csv',
        mime='text/csv',
    )
