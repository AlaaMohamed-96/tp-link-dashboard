import streamlit as st
import pandas as pd

st.set_page_config(page_title="منتجات TP-Link", layout="wide")

# رابط Google Sheets بصيغة CSV
sheet_url = "https://docs.google.com/spreadsheets/d/15dYSSNVbKHoPtKIIPdPockpJm1hXUnBl-ZZG0C5RD70/edit?gid=0#gid=0"

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df["السعر"] = pd.to_numeric(df["السعر"].astype(str).str.replace(",", "").str.extract("(\\d+)", expand=False), errors="coerce")
    return df.dropna(subset=["السعر"])

df = load_data()

st.title("📦 منتجات TP-Link - أمازون مصر")

product_filter = st.text_input("🔍 ابحث باسم المنتج")
if product_filter:
    df = df[df["اسم المنتج"].str.contains(product_filter, case=False, na=False)]

sellers = ["الكل"] + sorted(df["اسم التاجر"].dropna().unique().tolist())
selected_seller = st.selectbox("🏪 اختر اسم التاجر", sellers)
if selected_seller != "الكل":
    df = df[df["اسم التاجر"] == selected_seller]

if not df.empty:
    min_price, max_price = int(df["السعر"].min()), int(df["السعر"].max())
    price_range = st.slider("💰 نطاق السعر", min_price, max_price, (min_price, max_price))
    df = df[(df["السعر"] >= price_range[0]) & (df["السعر"] <= price_range[1])]
else:
    st.warning("❗ لا توجد بيانات بعد الفلترة.")

# عرض المنتجات
if df.empty:
    st.info("🔎 لا توجد منتجات تطابق الفلاتر المحددة.")
else:
    for _, row in df.iterrows():
        st.markdown(f"### [{row['اسم المنتج']}]({row['رابط المنتج']})")
        st.write(f"**السعر:** {int(row['السعر'])} جنيه")
        st.write(f"**البائع:** {row['اسم التاجر']}")
        st.markdown("---")
