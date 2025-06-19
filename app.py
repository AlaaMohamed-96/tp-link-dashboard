import streamlit as st
import pandas as pd
import requests
from io import StringIO

# إعداد واجهة الصفحة
st.set_page_config(page_title="لوحة متابعة منتجات TP-Link", layout="wide")

# تحميل البيانات من Google Sheets
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRq97qApWyUNKF-ISWQcl_th6m9d5wx2RR82hZoOy2Wo7bRvmj-TyFG9D8nofbBnlHqLdPZULZIKE5D/pub?output=csv"
    response = requests.get(sheet_url)
    data = StringIO(response.text)
    df = pd.read_csv(data)

    # تحويل عمود السعر إلى أرقام
    if "السعر" in df.columns:
        df["السعر"] = pd.to_numeric(
            df["السعر"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+)", expand=False),
            errors="coerce"
        )
    return df

# العنوان الرئيسي
st.title("📊 لوحة متابعة منتجات TP-Link")

# تحميل البيانات
df = load_data()

# التحقق من وجود بيانات
if df.empty:
    st.warning("⚠️ لا توجد بيانات متاحة حاليًا.")
else:
    # عرض البيانات الأصلية
    st.subheader("📋 جميع المنتجات")
    st.dataframe(df)

    # فلاتر جانبية
    st.sidebar.header("🔍 خيارات الفلترة")

    product_names = df["اسم المنتج"].dropna().unique()
    sellers = df["اسم التاجر"].dropna().unique()

    selected_product = st.sidebar.selectbox("اختر منتجًا:", ["الكل"] + list(product_names))
    selected_seller = st.sidebar.selectbox("اختر التاجر:", ["الكل"] + list(sellers))

    # تطبيق الفلاتر
    filtered_df = df.copy()
    if selected_product != "الكل":
        filtered_df = filtered_df[filtered_df["اسم المنتج"] == selected_product]
    if selected_seller != "الكل":
        filtered_df = filtered_df[filtered_df["اسم التاجر"] == selected_seller]

    st.subheader("📦 المنتجات بعد الفلترة")
    st.dataframe(filtered_df)
