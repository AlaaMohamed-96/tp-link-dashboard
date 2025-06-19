import streamlit as st
import pandas as pd

st.set_page_config(page_title="منتجات TP-Link", layout="wide")

# رابط Google Sheets بصيغة CSV
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRq97qApWyUNKF-ISWQcl_th6m9d5wx2RR82hZoOy2Wo7bRvmj-TyFG9D8nofbBnlHqLdPZULZIKE5D/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)

    # طباعة الأعمدة
    st.write("🧾 الأعمدة الموجودة:", df.columns.tolist())

    # تنظيف عمود "السعر"
    if "السعر" in df.columns:
        # تحويل القيم النصية إلى أرقام، وتجاهل "غير متوفر"
        df["السعر"] = (
            df["السعر"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+)", expand=False)
        )
        df["السعر"] = pd.to_numeric(df["السعر"], errors="coerce")
        df = df.dropna(subset=["السعر"])
    else:
        st.error("❌ عمود 'السعر' غير موجود في البيانات")

    return df

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
