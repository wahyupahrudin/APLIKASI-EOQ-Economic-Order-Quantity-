import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io

st.set_page_config(page_title="EOQ Calculator Lengkap", layout="centered")
st.title("📦 Aplikasi Perhitungan EOQ Lengkap")
st.markdown("Masukkan nilai-nilai berikut untuk menghitung EOQ, melihat grafik, dan mengunduh hasil.")

# Input pengguna
D = st.number_input("Permintaan Tahunan (D)", min_value=1, step=1)
S = st.number_input("Biaya Pemesanan per Order (S)", min_value=1)
H = st.number_input("Biaya Penyimpanan per Unit (H)", min_value=1)
work_days = st.number_input("Jumlah Hari Kerja dalam Setahun", value=360, min_value=1)

if st.button("Hitung EOQ"):
    EOQ = np.sqrt((2 * D * S) / H)
    total_order = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H
    interval_days = work_days / total_order  # penambahan fitur ini

    # Tampilkan hasil
    st.success(f"EOQ: {EOQ:.2f} unit")
    st.info(f"Jumlah Pemesanan per Tahun: {total_order:.2f} kali")
    st.info(f"Total Biaya Persediaan: Rp {total_cost:,.2f}")
    st.info(f"Permintaan Barang Setiap: {interval_days:.2f} hari sekali")

    # Tabel hasil
    hasil_df = pd.DataFrame({
        "Parameter": [
            "Permintaan Tahunan (D)",
            "Biaya Pemesanan (S)",
            "Biaya Penyimpanan (H)",
            "Hari Kerja per Tahun",
            "EOQ",
            "Jumlah Pemesanan",
            "Interval Permintaan (hari)",
            "Total Biaya"
        ],
        "Nilai": [D, S, H, work_days, EOQ, total_order, interval_days, total_cost]
    })
    st.subheader("📋 Tabel Hasil")
    st.dataframe(hasil_df, use_container_width=True)

    # Grafik Interaktif Total Biaya vs Q
    Q_range = np.arange(1, int(EOQ * 2))
    biaya_pemesanan = (D / Q_range) * S
    biaya_penyimpanan = (Q_range / 2) * H
    total_biaya = biaya_pemesanan + biaya_penyimpanan

    grafik_df = pd.DataFrame({
        "Q": Q_range,
        "Biaya Pemesanan": biaya_pemesanan,
        "Biaya Penyimpanan": biaya_penyimpanan,
        "Total Biaya": total_biaya
    })

    st.subheader("📊 Grafik Interaktif Total Biaya vs Jumlah Pemesanan")
    fig = px.line(grafik_df, x="Q", y=["Biaya Pemesanan", "Biaya Penyimpanan", "Total Biaya"],
                  labels={"value": "Biaya", "Q": "Jumlah Pemesanan"},
                  title="Analisis Biaya EOQ")
    fig.add_vline(x=EOQ, line_dash="dot", line_color="green", annotation_text=f"EOQ: {EOQ:.0f}", annotation_position="top left")
    st.plotly_chart(fig, use_container_width=True)

    # Unduh hasil ke Excel
    st.subheader("⬇️ Unduh Hasil ke Excel")
    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine="xlsxwriter") as writer:
        hasil_df.to_excel(writer, index=False, sheet_name="Hasil Perhitungan")
        grafik_df.to_excel(writer, index=False, sheet_name="Grafik Biaya")
    st.download_button("📥 Download Excel", data=excel_output.getvalue(),
                       file_name="hasil_perhitungan_eoq.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
