# 🛒 Store Sales - Daily Transactions Forecasting

Bu proje, Kaggle'ın "Store Sales" veri setini kullanarak perakende mağazalarının günlük müşteri trafik hacmini  tahmin etmek amacıyla geliştirilmiştir.

## 🎯 Proje Amacı
Mağazaların gelecekteki günlük işlem yoğunluğunu tahmin ederek personel planlaması, lojistik ve operasyonel süreçlerin optimize edilmesini sağlamak.

## 📊 Teknik Özellikler & Metrikler
- **Model:** Random Forest Regressor (Rastgele Orman Regresyonu)
- **Hata Metriği (MAE):** ~247.90 İşlem (Günlük ortalama ~1690 işlemde yüksek doğruluk)
- **Veri Bölme:** Zaman serisi mantığına uygun olarak, gelecek sızıntısını (data leakage) önlemek adına kronolojik sıra bozulmadan `shuffle=False` ile %20 test seti ayrılmıştır.

## 🔑 Özellik Mühendisliği (Feature Engineering)
- Ham tarih verisinden periyodik döngüleri yakalamak için **Yıl, Ay, Gün ve Haftanın Günü (0-6)** özellikleri türetilmiştir.
- Hafta sonu yoğunluğunu modele öğretmek için **is_weekend** (0/1) bayrağı eklenmiştir.
- Mağaza tipi (`type`) ve şehir (`city`) gibi kategorik veriler **LabelEncoder** ile sayısallaştırılmıştır.

## 📂 Dosya Yapısı
- `app.py`: Streamlit canlı tahmin arayüzü kodları.
- `store_transactions_model.pkl`: Eğitilmiş yapay zeka modeli.
- `le_city.pkl` & `le_type.pkl`: Kategorik etiket dönüştürücüler.
- `requirements.txt`: Gerekli kütüphaneler listesi.
