# 🐄 Organik Hayvansal Üretim

**Organik Hayvansal Üretim dersi için etkileşimli, Türkçe öğretim uygulaması: organik hayvancılığın kuralları ve bu kuralların dayandığı hayvan davranışı ve refahı**

© 2026 Emine Dilşat Yeğenoğlu & Tevfik Hasan Can. Tüm hakları saklıdır.

---

## Nedir?

Organik hayvancılığın ilke ve kurallarını (hayvan kaynağı, barınma, besleme, geçiş süreleri, sağlık,
taşıma-kesim-kayıt) hayvan davranışı ve refahı bilgisiyle birlikte işleyen bir web uygulamasıdır.
Şemalar, hesaplayıcılar ve oyunlar içerir. Bilgisayardan ve telefondan tarayıcıyla açılır. Bütün
şemalar bu uygulama için özgün olarak çizilmiştir.

## İçerik

| Bölüm | Konu ve etkileşimli öğeler |
|---|---|
| 1 · Neden organik? | Yoğun üretimin sorunları (BSE dahil), nüfus grafiği, gıda güvencesi ve gıda güvenliği, Türkiye hayvan sayıları, avantajlar, dezavantajlar |
| 2 · Tanım, ilkeler, mevzuat | Kapalı çiftlik döngüsü şeması, primum non nocere, 5262 sayılı Kanun ve yönetmelik, ABD NOP mantığı, "organik mi?" oyunu |
| 3 · Hayvan kaynağı ve üreme | Irk seçimi, doğal aşım, suni tohumlama, embriyo transferi yasağı, konvansiyonel hayvan alımında yaş denetimi |
| 4 · Barınma ve açık alan | İç/dış alan hesaplayıcı, konvansiyonel ve organik tavuk yoğunluğu çizimi, 170 kg N/ha hesaplayıcı |
| 5 · Besleme | Su, kolostrum, sütle besleme süreleri ve sütten kesme tarihi, ad libitum, izinli–yasak oyunu, rasyon denetleyici |
| 6 · Geçiş süreleri | Zaman çizelgesi, organik satış tarihi hesaplayıcı, ömrün 3/4'ü kuralı, arazi geçişi |
| 7 · Hayvan sağlığı ve tedavi | Yasak işlemler, tedavi akışı, kür sayacı (3 / 1 kuralı), organik bekleme süresi hesabı, homeopati üzerine bilimsel not |
| 8 · Taşıma, kesim, kayıt, karar | 8 saatte bir mola hesabı, ayrı kesim, kayıt, etiketler, "organik hayvancılık bana uygun mu?" kontrol listesi |
| 9 · Hayvan refahı | Refah göstergeleri, Brambell (1965), beş özgürlük şeması ve "hangi özgürlük çiğneniyor?" oyunu, AB mevzuatı |
| 10 · Etholoji | Davranışın kökenleri, duyular, sinir sistemi, hormon–davranış şeması |
| 11 · Barınak çevresi | Sekiz çevre faktörü, yüzey/hacim, nem ve gürültü denetimi |
| 12 · Türlere göre davranış | Sığır, koyun, keçi, tavuk: 24 saatlik otlama halkası, geviş hesabı, tohumlama saati, koç sayısı, aydınlatma döngüsü, sosyal hiyerarşi |
| 13 · Davranış bozuklukları | Neden–önleme tablosu, "hangi türde?" oyunu, gaga kesimi konusunda konvansiyonel–organik farkı |
| 14 · Genel tekrar | Hafıza kartları, sözlük ve tüm konulardan karışık sorular |

Her bölümün sonunda **10, 20 ya da 30 soruluk seçmeli alıştırma** vardır (öğrenci seçer). Yanıt
seçilince kilitlenir; doğru/yanlış ve açıklama o zaman açılır. "Yeni sorular" düğmesiyle yeni sorular
üretilir.

## Kurulum ve çalıştırma

```bash
pip install -r requirements.txt
streamlit run organik_streamlit.py
```

Linux / WSL'de kısaca: `bash baslat.sh`. Ardından tarayıcıda http://localhost:8501

## Yayına alma

GitHub reposuna `organik_streamlit.py` ve `requirements.txt` yüklenir; share.streamlit.io'da
"Create app" ile ana dosya olarak `organik_streamlit.py` seçilir.

## Bilinen sınırlamalar

- Sayısal kurallar (süreler, oranlar, alanlar) Türkiye'deki Organik Tarımın Esasları ve Uygulanmasına İlişkin Yönetmelik (RG 18.08.2010, 27676 ve değişiklikleri) ve onunla uyumlu AB kurallarına (889/2008) göre **öğretici olarak** özetlenmiştir. Hayvan başına alan ve 170 kg N/ha eşdeğerleri AB 889/2008 eklerinden alınmıştır. Mevzuat değişebilir; uygulamada yürürlükteki metin ve kontrol kuruluşu esas alınır.
- Türkiye istatistikleri ders notundaki TÜİK 2015–2016 verileridir; güncel değildir.
- Otlama saatleri ve şemalar öğretici yaklaşık gösterimlerdir.
- Öğrenci yanıtları kaydedilmez; uygulama öğrenmek için tasarlanmıştır.

## Telif ve kullanım

© 2026 Emine Dilşat Yeğenoğlu & Tevfik Hasan Can. Tüm hakları saklıdır. Ayrıntılar için
`LICENSE` dosyasına bakın.

İletişim ve izin talepleri: dilsat.yegenoglu@cbu.edu.tr
