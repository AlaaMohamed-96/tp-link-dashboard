import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="TP-Link Dashboard", layout="wide")

@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRq97qApWyUNKF-ISWQcl_th6m9d5wx2RR82hZoOy2Wo7bRvmj-TyFG9D8nofbBnlHqLdPZULZIKE5D/pub?output=csv"
    response = requests.get(sheet_url)
    data = StringIO(response.text)
    df = pd.read_csv(data)

    if "السعر" in df.columns:
        df["السعر"] = pd.to_numeric(
            df["السعر"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+)", expand=False),
            errors="coerce"
        )
    return df

st.title("📊 TP-Link Products Dashboard")

df = load_data()

if df.empty:
    st.warning("لا توجد بيانات للعرض.")
else:
    st.dataframe(df)

    # فلاتر جانبية
    st.sidebar.header("🔍 فلاتر البحث")
    
    product_names = df["اسم المنتج"].dropna().unique()
    sellers = df["اسم التاجر"].dropna().unique()

    selected_product = st.sidebar.selectbox("اختار منتج", ["الكل"] + list(product_names))
    selected_seller = st.sidebar.selectbox("اختار التاجر", ["الكل"] + list(sellers))

    filtered_df = df.copy()
    if selected_product != "الكل":
        filtered_df = filtered_df[filtered_df["اسم المنتج"] == selected_product]
    if selected_seller != "الكل":
        filtered_df = filtered_df[filtered_df["اسم التاجر"] == selected_seller]

    st.subheader("📋 النتائج بعد الفلترة")
    st.dataframe(filtered_df)
