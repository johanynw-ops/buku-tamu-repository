import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Buku Tamu Digital", layout="centered")

# ==========================
# CSS UI Redesign
# ==========================
st.markdown("""
<style>

    /* ====== WRAPPER ====== */
    .main {
        padding-top: 1rem;
    }

    /* ====== HEADER ====== */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #4f8cff, #6f5bff);
        -webkit-background-clip: text;
        color: transparent;
    }

    /* ====== SUBTITLE ====== */
    .subtitle {
        font-size: 1.1rem;
        color: #cfcfcf;
        margin-top: -15px;
        margin-bottom: 25px;
    }

    /* ====== FORM CARD ====== */
    .form-card {
        padding: 25px;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* ====== BUTTON ====== */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        padding: 10px 0;
        background: linear-gradient(90deg, #4f8cff, #6f5bff);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 1.05rem;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        transition: 0.2s;
        cursor: pointer;
    }

    /* ====== SIDEBAR ====== */
    section[data-testid="stSidebar"] {
        background: #1b1b1d;
        padding-top: 30px;
    }

    .css-1d391kg {
        background: #1b1b1d !important;
    }

</style>
""", unsafe_allow_html=True)




# ==========================
# 1. Google Sheets Connector
# ==========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# 🔥 GANTI DENGAN GOOGLE SHEET ID KAMU
SHEET_ID = "1hZwOnl2qnRHgIXvDDCNJho7ux4JafkRF_awYQPY6rUs"

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
except Exception as e:
    st.error(f"❌ Google Sheet tidak ditemukan.\n\nError: {e}\n\nPastikan:\n1. Sheet sudah dibuat\n2. Service account sudah diberi akses editor.")
    st.stop()



# ==========================
# 2. Sidebar Menu
# ==========================
menu = st.sidebar.radio("Menu", ["Isi Buku Tamu", "Lihat Data Tamu"])



# ==========================
# 3. FORM INPUT BUKU TAMU
# ==========================
if menu == "Isi Buku Tamu":

    st.markdown("<h1>📘 Buku Tamu Digital</h1>", unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Silakan isi data berikut:</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    with st.form("form_bukutamu"):
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        instansi = st.text_input("Instansi / Perusahaan")
        pesan = st.text_area("Pesan / Keperluan")

        submit = st.form_submit_button("Kirim")

    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not nama:
            st.warning("⚠ Nama wajib diisi!")
        else:
            sheet.append_row([nama, email, instansi, pesan, str(datetime.now())])
            st.success("🎉 Terima kasih! Data kamu sudah tersimpan.")



# ==========================
# 4. HALAMAN ADMIN – LIHAT DATA TAMU
# ==========================
elif menu == "Lihat Data Tamu":

    st.markdown("<h1>📄 Data Tamu Masuk</h1>", unsafe_allow_html=True)

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if len(df) == 0:
        st.info("Belum ada data tamu.")
    else:
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download CSV", csv, "data_buku_tamu.csv", "text/csv")
