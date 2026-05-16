import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime as dt

st.set_page_config(page_title="Mağaza Trafik Tahmincisi", page_icon="🛒", layout="centered")

st.title("🛒 Store Transactions Tahmin Modeli")
st.write("Mağaza özelliklerine ve takvime göre günlük müşteri işlem sayısını tahmin edin.")

# Önbelleksiz, en güncel dosyaları doğrudan diskten okuma
try:
    model = joblib.load('store_transactions_model.pkl')
    le_city = joblib.load('le_city.pkl')
    le_type = joblib.load('le_type.pkl')
    st.success("✅ Güncel yapay zeka modeli ve dönüştürücüler başarıyla yüklendi!")
except Exception as e:
    st.error(f"❌ Model dosyaları yüklenemedi! Hata: {e}")

st.subheader("🔮 Tahmin Parametreleri")

col1, col2 = st.columns(2)

with col1:
    store_nbr = st.number_input("Mağaza Numarası (store_nbr)", min_value=1, max_value=54, value=1)
    city = st.selectbox("Şehir (City)", list(le_city.classes_))

with col2:
    target_date = st.date_input("Tahmin Tarihi", value=dt.date.today())
    store_type = st.selectbox("Mağaza Tipi (Type)", list(le_type.classes_))
    cluster = st.slider("Mağaza Kümesi (Cluster)", min_value=1, max_value=17, value=13)

# Zaman Özelliklerini Hesaplama (Notebook ile milimetrik aynı mantık)
date_converted = dt.datetime.combine(target_date, dt.datetime.min.time())
year = date_converted.year
month = date_converted.month
day = date_converted.day
dayofweek = date_converted.weekday()
is_weekend = 1 if dayofweek in [5, 6] else 0

if st.button("🚀 İşlem Sayısını Tahmin Et"):
    try:
        # Metin kategorileri sayısal kodlara çevriliyor
        city_encoded = le_city.transform([city])[0]
        type_encoded = le_type.transform([store_type])[0]
        
        # DataFrame yapısı ve sütun sıralaması modelin beklediği 9 özellikle birebir eşleniyor
        input_data = pd.DataFrame([{
            'store_nbr': int(store_nbr),
            'city': int(city_encoded),
            'type': int(type_encoded),
            'cluster': int(cluster),
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'dayofweek': int(dayofweek),
            'is_weekend': int(is_weekend)
        }])
        
        # Sütun sırasını garanti altına alma
        input_data = input_data[['store_nbr', 'city', 'type', 'cluster', 'year', 'month', 'day', 'dayofweek', 'is_weekend']]
        
        # Model tahmini
        prediction = model.predict(input_data)[0]
        
        st.markdown("---")
        st.metric(label="📊 Tahmin Edilen Günlük İşlem Sayısı", value=f"{int(prediction)} İşlem")
        
        if is_weekend == 1:
             st.warning("⚠️ Seçilen tarih hafta sonuna denk geldiği için işlem hacmi yüksek çıkabilir.")
             
    except Exception as e:
        st.error(f"Tahmin yapılırken hata oluştu: {e}")