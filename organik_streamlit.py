# -*- coding: utf-8 -*-
"""
Organik Hayvansal Üretim · Hayvan Davranışı ve Refahı - Öğretici Streamlit Uygulaması
====================================================================================
© 2026 Emine Dilşat Yeğenoğlu & Tevfik Hasan Can. Tüm hakları saklıdır.

Organik hayvansal üretimin ilkeleri ve mevzuatı, hayvan kaynağı, barınma, besleme,
geçiş süreleri, hayvan sağlığı, taşıma-kesim-kayıt, hayvan refahı, etholoji, barınak
çevresi, türlere göre davranış ve davranış bozuklukları. Her konunun sonunda 10 / 20 / 30
seçmeli alıştırma ve açıklamalı çözüm.

Kurulum   : pip install -r requirements.txt
Çalıştırma: streamlit run organik_streamlit.py
"""

import math


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Organik Hayvansal Üretim", page_icon="🐄", layout="wide")

TELIF = "© 2026 Emine Dilşat Yeğenoğlu & Tevfik Hasan Can. Tüm hakları saklıdır."

# Renkler
MAVI, PEMBE, YESIL, TURUNCU = "#3B6FB6", "#D9577A", "#3C9A5F", "#E8A33B"
MOR, GRI_K, SARI = "#8E5BB5", "#5F6B7A", "#F2C94C"
SIVI, CAM, CAM_K = "#9CC3E6", "#EAF3FB", "#4A5A6A"   # sıvı, cam dolgu, cam çizgi
YAZI = 'font-family="Source Sans Pro, Segoe UI, Arial, sans-serif"'

st.markdown("""
<style>
.kutucuk {border-left:5px solid #3B6FB6; background:rgba(59,111,182,0.08);
          padding:10px 14px; border-radius:6px; margin:6px 0 10px 0;}
.uyari {border-left:5px solid #D9534F; background:rgba(217,83,79,0.08);
        padding:10px 14px; border-radius:6px; margin:6px 0 10px 0;}
.ipucu {border-left:5px solid #3C9A5F; background:rgba(60,154,95,0.08);
        padding:10px 14px; border-radius:6px; margin:6px 0 10px 0;}
.kartlar {display:flex; flex-wrap:wrap; gap:12px; margin:8px 0 14px 0;}
.kart {flex:1 1 220px; border:1px solid rgba(128,128,128,0.35); border-radius:10px;
       padding:12px 14px; background:rgba(128,128,128,0.05);}
.kart h4 {margin:0 0 6px 0; font-size:1.02rem;}
.kart p {margin:0; font-size:0.93rem;}
.dizi {font-family:monospace; font-size:18px; letter-spacing:1px; line-height:2.0;
       overflow-x:auto; white-space:nowrap; padding:6px 10px; border-radius:8px;
       background:rgba(128,128,128,0.07);}
.baz {display:inline-block; min-width:20px; text-align:center; border-radius:4px;
      margin:1px; padding:0 2px; color:#111; font-weight:700;}
.kodon {display:inline-block; border:1.5px solid rgba(128,128,128,0.6); border-radius:6px;
        padding:2px 6px; margin:3px; text-align:center; font-family:monospace;}
.kodon small {display:block; font-family:sans-serif; font-size:11px;}
.zaman {border-left:4px solid #3B6FB6; padding:4px 0 4px 12px; margin:6px 0;}
.zaman b.yil {color:#3B6FB6; font-size:1.05rem;}
.flash {border:2px solid #3B6FB6; border-radius:14px; padding:26px; text-align:center;
        font-size:1.4rem; font-weight:700; margin:10px 0;}
.flash-cevap {font-size:1.05rem; font-weight:400; margin-top:12px;}
.adim-baslik {font-size:1.15rem; font-weight:700; color:#3B6FB6; margin-top:18px;
              border-bottom:2px solid rgba(59,111,182,0.3);}
.etiket {border:2px dashed #5F6B7A; border-radius:10px; padding:12px 16px; max-width:420px;
          background:rgba(242,201,76,0.12); font-family:monospace; line-height:1.6;}
.ekran {font-family:monospace; font-size:1.6rem; background:#1d2b1f; color:#8CF59A;
        padding:8px 14px; border-radius:8px; display:inline-block; letter-spacing:2px;}
.renk-kutu {width:100%; height:110px; border-radius:12px; border:1px solid #999;}
</style>
""", unsafe_allow_html=True)


def ipucu(metin):
    st.markdown(f'<div class="ipucu">{metin}</div>', unsafe_allow_html=True)


def kartlar(liste):
    """liste: [(başlık, metin), ...]"""
    icerik = "".join(f'<div class="kart"><h4>{b}</h4><p>{m}</p></div>' for b, m in liste)
    st.markdown(f'<div class="kartlar">{icerik}</div>', unsafe_allow_html=True)


def kutu(metin):
    st.markdown(f'<div class="kutucuk">{metin}</div>', unsafe_allow_html=True)


def uyari(metin):
    st.markdown(f'<div class="uyari">{metin}</div>', unsafe_allow_html=True)


def ciz(fig, yukseklik=380):
    fig.update_layout(height=yukseklik, margin=dict(l=40, r=20, t=50, b=40),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def tablo(df):
    try:
        st.dataframe(df, hide_index=True, width="stretch")
    except TypeError:
        st.dataframe(df, hide_index=True, use_container_width=True)


def rng():
    if "rng" not in st.session_state:
        st.session_state.rng = np.random.default_rng()
    return st.session_state.rng


SORU_SAYISI = 10


def _md(t):
    return ("md", t)


def _tx(t):
    return ("tex", t)


def _fmt(x, ondalik=4):
    if abs(x - round(x)) < 1e-9 and abs(x) >= 1:
        return f"{int(round(x))}"
    return f"{x:.{ondalik}f}"


def soru_sayi(metin, dogru, cozum, yanlis=(), ondalik=4, tol=None):
    """Sayısal soru; sık yapılan hatalardan türetilen yanlış seçeneklerle seçmeliye çevrilir."""
    return {"tip": "sayi", "metin": metin, "dogru": float(dogru), "yanlis": list(yanlis),
            "ondalik": ondalik, "cozum": cozum}


def soru_secim(r, metin, dogru, yanlislar, cozum):
    return {"tip": "secim", "metin": metin, "dogru": dogru, "yanlis": list(yanlislar),
            "cozum": cozum}


def _secmeliye_cevir(r, s):
    if s["tip"] == "secim":
        secenekler = [s["dogru"]] + s["yanlis"]
    else:
        x, od = s["dogru"], s["ondalik"]
        dogru = _fmt(x, od)
        olasilik = 0 < x < 1
        secenekler = [dogru]
        for v in s["yanlis"]:
            if v is None or not math.isfinite(v) or (v < 0 <= x) or (olasilik and v > 1):
                continue
            t = _fmt(v, od)
            if t not in secenekler:
                secenekler.append(t)
            if len(secenekler) == 4:
                break
        deneme = 0
        while len(secenekler) < 4 and deneme < 200:
            deneme += 1
            if abs(x - round(x)) < 1e-9 and abs(x) >= 1:
                adim_ = max(3, int(round(abs(x) * 0.25)))
                v = x + int(r.choice([-1, 1])) * int(r.integers(1, adim_ + 1))
            elif deneme > 40 or abs(x) < 10 ** (-od + 1):
                v = abs(x) + float(r.integers(5, 400)) * 10 ** (-od)
            else:
                v = x * (1 + float(r.choice([-1, 1])) * float(r.uniform(0.12, 0.6)))
            if (v < 0 <= x) or (olasilik and v >= 1):
                continue
            t = _fmt(v, od)
            if t not in secenekler:
                secenekler.append(t)
        s = dict(s, dogru=dogru)
    sira = r.permutation(len(secenekler))
    s["secenekler"] = [secenekler[i] for i in sira]
    return s


def _sec(r, liste):
    return liste[int(r.integers(0, len(liste)))]


def _kavram_sec(r, havuz, adet):
    idx = r.permutation(len(havuz))[:adet]
    return [havuz[i] for i in idx]


def _al_cevapla(k, i):
    v = st.session_state.get(f"{k}_c{i}")
    if v is not None and f"{k}_cevap{i}" not in st.session_state:
        st.session_state[f"{k}_cevap{i}"] = v


ADET_SECENEK = [10, 20, 30]


def _temizle(k):
    for i in range(1, max(ADET_SECENEK) + 1):
        for ek in ("c", "cevap", "kilit"):
            st.session_state.pop(f"{k}_{ek}{i}", None)


def _al_yenile(k, uretici):
    _temizle(k)
    st.session_state[k] = _uret(uretici, st.session_state.get(f"{k}_adet", SORU_SAYISI))


def _uret(uretici, adet=SORU_SAYISI):
    """Üreticiyi gerektiği kadar çağırıp metni tekrarlanmayan 'adet' soru toplar."""
    r = rng()
    sorular, gorulen = [], set()
    for _ in range(40):
        for s in uretici(r):
            if s["metin"] not in gorulen:
                gorulen.add(s["metin"])
                sorular.append(_secmeliye_cevir(r, s))
            if len(sorular) >= adet:
                return sorular
    return sorular


def alistirma_blogu(anahtar, baslik, uretici):
    st.divider()
    st.subheader(f"✍️ Alıştırmalar: {baslik}")
    st.caption("Her soruda bir seçenek işaretleyin. Yanıtınız kilitlenir; doğru ya da yanlış "
               "olduğu ve **adım adım çözüm** o zaman açılır. Önce kâğıt-kalemle hesaplayın!")
    k = f"al_{anahtar}"
    st.radio("Kaç soru?", ADET_SECENEK, horizontal=True, key=f"{k}_adet",
             on_change=_al_yenile, args=(k, uretici))
    if k not in st.session_state:
        st.session_state[k] = _uret(uretici, st.session_state.get(f"{k}_adet", SORU_SAYISI))
    sorular = st.session_state[k]
    dogru_say = cevap_say = 0
    for i, s in enumerate(sorular, 1):
        with st.container(border=True):
            st.markdown(f"**Soru {i} / {len(sorular)}.** {s['metin']}")
            secili = st.session_state.get(f"{k}_cevap{i}")
            if secili is None:
                st.radio("Seçiniz", s["secenekler"], index=None, key=f"{k}_c{i}",
                         label_visibility="collapsed", on_change=_al_cevapla, args=(k, i))
            else:
                cevap_say += 1
                st.radio("Yanıtınız", s["secenekler"], index=s["secenekler"].index(secili),
                         key=f"{k}_kilit{i}", disabled=True, label_visibility="collapsed")
                if secili == s["dogru"]:
                    dogru_say += 1
                    st.success("✅ Doğru!")
                else:
                    st.error(f"❌ Yanlış. Doğru yanıt: **{s['dogru']}**")
                with st.expander("📖 Nasıl hesaplanır?", expanded=True):
                    for tur, icerik in s["cozum"]:
                        if tur == "tex":
                            for parca in icerik.split(r"\qquad"):
                                st.latex(parca)
                        else:
                            st.markdown(icerik)
    st.progress(cevap_say / len(sorular),
                text=f"Yanıtlanan: {cevap_say} / {len(sorular)}  ·  Doğru: {dogru_say}")
    if cevap_say == len(sorular):
        oran = dogru_say / len(sorular)
        mesaj = (f"🎉 Tebrikler! {dogru_say}/{len(sorular)}" if oran >= 0.8 else
                 f"👍 {dogru_say}/{len(sorular)}: yanlışların çözümlerini tekrar inceleyin"
                 if oran >= 0.5 else
                 f"📚 {dogru_say}/{len(sorular)}: konuyu yukarıdan bir kez daha okuyup yeni "
                 "sorularla deneyin")
        (st.success if oran >= 0.8 else st.info if oran >= 0.5 else st.warning)(mesaj)
    st.button("🎲 Yeni sorular", key=f"{k}_yeni", on_click=_al_yenile, args=(k, uretici))


def svg_goster(svg):
    import base64
    veri = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    st.markdown(f'<div style="width:100%;margin:6px 0 14px 0;text-align:center">'
                f'<img src="data:image/svg+xml;base64,{veri}" style="width:100%;'
                f'max-width:1000px;background:white;border-radius:12px"/></div>',
                unsafe_allow_html=True)


def _krom(x, y, h, w, renk, sent=0.33):
    yc = y + h * sent
    return (f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{yc - y - 3}" rx="{w / 2}" '
            f'fill="{renk}" stroke="#444" stroke-width="1.4"/>'
            f'<rect x="{x - w / 2}" y="{yc + 3}" width="{w}" height="{y + h - yc - 3}" '
            f'rx="{w / 2}" fill="{renk}" stroke="#444" stroke-width="1.4"/>'
            f'<ellipse cx="{x}" cy="{yc}" rx="{w * 0.3}" ry="5" fill="{renk}" stroke="#444" '
            f'stroke-width="1.2"/>')


def _bant(x, y, w, renk, h=12):
    return (f'<rect x="{x - w / 2 + 1.5}" y="{y - h / 2}" width="{w - 3}" height="{h}" '
            f'fill="{renk}" stroke="#222" stroke-width="0.8"/>')


def _yazi(x, y, t, boy=14, renk="#222", hiza="middle", kalin=False):
    k = ' font-weight="700"' if kalin else ""
    return (f'<text x="{x}" y="{y}" {YAZI} font-size="{boy}" fill="{renk}" '
            f'text-anchor="{hiza}"{k}>{t}</text>')


def _ok(x1, y1, x2, y2, renk="#555"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{renk}" stroke-width="2.2" '
            f'marker-end="url(#okucu)"/>')


_OK_TANIM = ('<defs><marker id="okucu" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
             'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
             'fill="#555"/></marker></defs>')


def _yarim_daire(cx, cy, r, sol, sag):
    return (f'<path d="M{cx},{cy - r} A{r},{r} 0 0 0 {cx},{cy + r} Z" fill="{sol}"/>'
            f'<path d="M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} Z" fill="{sag}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#333" stroke-width="1.4"/>')


# ===========================================================================
# ORTAK ŞEMA YARDIMCILARI
# ===========================================================================
KIRMIZI, YESIL_A, KAHVE = "#C0392B", "#2E8B57", "#8B5A2B"


def svg_ac(w, h, maks=None):
    m = f"max-width:{maks}px;" if maks else ""
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" style="{m}" '
            f'xmlns="http://www.w3.org/2000/svg">' + _OK_TANIM +
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="white"/>')


def _kutu_svg(x, y, w, h, renk, yazi, boy=14, dolgu=None, kalin=True, renk_yazi="#222"):
    d = dolgu or "white"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{d}" stroke="{renk}" '
            f'stroke-width="2"/>' +
            "".join(_yazi(x + w / 2, y + h / 2 + 5 + (i - (len(yazi) - 1) / 2) * (boy + 3), t, boy,
                          renk_yazi, kalin=(kalin and i == 0))
                    for i, t in enumerate(yazi if isinstance(yazi, (list, tuple)) else [yazi])))


def _iki_satir(t, sinir=14):
    if len(t) <= sinir:
        return [t]
    k = t.split(" ")
    yarim = len(k) // 2 + len(k) % 2
    return [" ".join(k[:yarim]), " ".join(k[yarim:])]


def _carpi(cx, cy, r=16, renk=KIRMIZI):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="{renk}" stroke-width="3"/>'
            f'<line x1="{cx - r * 0.5}" y1="{cy - r * 0.5}" x2="{cx + r * 0.5}" y2="{cy + r * 0.5}" '
            f'stroke="{renk}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<line x1="{cx + r * 0.5}" y1="{cy - r * 0.5}" x2="{cx - r * 0.5}" y2="{cy + r * 0.5}" '
            f'stroke="{renk}" stroke-width="3.5" stroke-linecap="round"/>')


def _tik(cx, cy, r=16, renk=YESIL_A):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="{renk}" stroke-width="3"/>'
            f'<path d="M{cx - r * 0.5},{cy} L{cx - r * 0.1},{cy + r * 0.45} L{cx + r * 0.55},{cy - r * 0.45}" '
            f'fill="none" stroke="{renk}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')


# ===========================================================================
# ŞEMALAR
# ===========================================================================
def svg_kapali_sistem(sec=None):
    """Organik çiftlik: toprak - bitki - hayvan - gübre döngüsü."""
    W, H = 900, 500
    s = [svg_ac(W, H, 900)]
    cx, cy, RX, RY = 320, 245, 225, 165
    dugum = [("Toprak", ["verimlilik korunur"], KAHVE), ("Yem bitkileri, mera", ["organik yem çiftlikte"], YESIL),
             ("Hayvanlar", ["refah, doğal davranış"], MAVI), ("Gübre", ["organik gübre", "en çok 170 kg N/ha"], TURUNCU)]
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="none" stroke="#bbb" stroke-width="3" stroke-dasharray="8 7"/>')

    def nokta(a):
        return cx + RX * math.cos(a), cy + RY * math.sin(a)
    for i in range(4):
        a1 = -math.pi / 2 + i * math.pi / 2 + 0.55
        a2 = -math.pi / 2 + (i + 1) * math.pi / 2 - 0.55
        (x1, y1), (x2, y2) = nokta(a1), nokta(a2)
        s.append(_ok(x1, y1, x2, y2, "#777"))
    for i, (ad, alt, renk) in enumerate(dugum):
        x, y = nokta(-math.pi / 2 + i * math.pi / 2)
        kal = 4 if sec == i else 2
        dol = "#FFF7E0" if sec == i else "white"
        h = 64 if len(alt) == 1 else 80
        s.append(f'<rect x="{x - 88}" y="{y - h / 2}" width="176" height="{h}" rx="14" fill="{dol}" stroke="{renk}" stroke-width="{kal}"/>')
        s.append(_yazi(x, y - h / 2 + 26, ad, 16, renk, kalin=True))
        for j, t in enumerate(alt):
            s.append(_yazi(x, y - h / 2 + 48 + j * 17, t, 12, "#444"))
    s.append(_yazi(cx, cy - 8, "ORGANİK ÇİFTLİK", 17, "#333", kalin=True))
    s.append(_yazi(cx, cy + 14, "kendi içinde kapalı döngü", 13, "#555"))
    s.append(_ok(410, cy + RY - 10, 655, cy + 110, MAVI))
    s.append(_kutu_svg(665, cy + 50, 210, 120, MOR, ["İnsan", "süt, et, yumurta,", "yapağı, bal", "(sertifikalı ürün)"], 13))
    s.append(_kutu_svg(665, 50, 210, 80, KIRMIZI, ["Dışarıdan girmez", "GDO, sentetik ilaç,", "hormon, kimyasal gübre"], 12))
    s.append(_carpi(770, 150, 13))
    s.append(_yazi(W / 2, H - 14, "Hayvanın yemi çiftlikte üretilir; gübresi aynı tarlaya döner. Döngüyü bozan sentetik girdiler dışarıda kalır.", 12, "#555"))
    s.append("</svg>")
    return "".join(s)


def svg_yogun_sorun():
    W, H = 900, 330
    s = [svg_ac(W, H, 900)]
    s.append(_kutu_svg(330, 18, 240, 66, KIRMIZI, ["YOĞUN (ENTANSİF) ÜRETİM", "birim alandan en çok ürün"], 14, "#FDECEA"))
    kol = [("Yetiştirme", ["Birim alanda çok hayvan", "Yüksek yerleşim sıklığı", "Bakım sorunları"], TURUNCU),
           ("Besleme", ["Kadavra unu → BSE", "(deli dana hastalığı)", "GDO'lu yemler"], MOR),
           ("Sağlık ve refah", ["İskelet, metabolik hastalık", "Davranış bozuklukları", "Kafes, doğal davranış yok"], MAVI),
           ("Çevre", ["Monokültür, biyoçeşitlilik", "Toprak ve su kirliliği", "İklim değişikliği"], YESIL)]
    for i, (b, maddeler, renk) in enumerate(kol):
        x = 20 + i * 220
        s.append(_ok(450, 86, x + 100, 140, "#888"))
        s.append(f'<rect x="{x}" y="144" width="200" height="160" rx="12" fill="white" stroke="{renk}" stroke-width="2.5"/>')
        s.append(_yazi(x + 100, 172, b, 16, renk, kalin=True))
        for j, m in enumerate(maddeler):
            s.append(_yazi(x + 100, 206 + j * 30, m, 13, "#333"))
    s.append("</svg>")
    return "".join(s)


OZGURLUKLER = [("Açlık ve susuzluktan", "Yeterli, taze yem ve su", "#E8A33B"),
               ("Rahatsızlıktan", "Uygun barınak ve çevre", "#3B6FB6"),
               ("Acı, yaralanma, hastalıktan", "Korunma, hızlı tedavi", "#C0392B"),
               ("Normal davranışı gösterme", "Yeterli alan, tür arkadaşları", "#3C9A5F"),
               ("Korku ve stresten", "Ruhsal acıyı önleyen koşullar", "#8E5BB5")]


def svg_bes_ozgurluk(sec=None):
    W, H = 820, 520
    s = [svg_ac(W, H, 820)]
    cx, cy, R = 410, 270, 190
    nokta = [(cx + R * math.cos(-math.pi / 2 + i * 2 * math.pi / 5), cy + R * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    s.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in nokta) + '" fill="#F4F8FC" stroke="#9db4d3" stroke-width="2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="white" stroke="{MAVI}" stroke-width="3"/>')
    s.append(_yazi(cx, cy - 4, "HAYVAN", 17, MAVI, kalin=True))
    s.append(_yazi(cx, cy + 18, "REFAHI", 17, MAVI, kalin=True))
    for i, ((bas, alt, renk), (x, y)) in enumerate(zip(OZGURLUKLER, nokta)):
        kal = 5 if sec == i else 2.5
        dol = "#FFF7E0" if sec == i else "white"
        s.append(f'<rect x="{x - 110}" y="{y - 34}" width="220" height="68" rx="14" fill="{dol}" stroke="{renk}" stroke-width="{kal}"/>')
        s.append(_yazi(x, y - 10, f"{i + 1}. {bas}", 14, renk, kalin=True))
        s.append(_yazi(x, y + 8, "özgürlük" if i != 3 else "özgürlüğü", 12, "#555"))
        s.append(_yazi(x, y + 25, alt, 12, "#333"))
    s.append(_yazi(cx, H - 12, "FAWC'ın beş özgürlüğü (ilk kez 1979; bugünkü biçimiyle 1993)", 13, "#555"))
    s.append("</svg>")
    return "".join(s)


GECIS = [("Büyükbaş, et", 52, "12 ay", KAHVE), ("Küçükbaş ve domuz, et", 26, "6 ay", TURUNCU),
         ("Süt hayvanları", 26, "6 ay", MAVI), ("Etlik kanatlı", 10, "10 hafta", YESIL),
         ("Yumurta tavuğu", 6, "6 hafta", MOR)]


def svg_gecis(sec=None):
    W, H = 820, 330
    s = [svg_ac(W, H, 820)]
    x0, olcek = 230, 10.5
    for ay in range(0, 13, 2):
        x = x0 + ay * 52 / 12 * olcek
        s.append(f'<line x1="{x}" y1="40" x2="{x}" y2="{H - 40}" stroke="#e3e3e3"/>')
        s.append(_yazi(x, H - 20, f"{ay} ay", 12, "#666"))
    for i, (ad, hafta, et, renk) in enumerate(GECIS):
        y = 50 + i * 50
        op = "1" if sec in (None, i) else "0.3"
        s.append(_yazi(x0 - 12, y + 22, ad, 14, "#333", "end", kalin=(sec == i)))
        s.append(f'<rect x="{x0}" y="{y}" width="{hafta * olcek}" height="32" rx="6" fill="{renk}" opacity="{op}"/>')
        s.append(_yazi(x0 + hafta * olcek + 8, y + 22, et, 14, renk, "start", kalin=True))
    s.append(_yazi(W / 2, 26, "Geçiş süreleri: bu süre dolmadan ürün organik diye satılamaz", 14, "#333", kalin=True))
    s.append("</svg>")
    return "".join(s)


def svg_tedavi_akis(adim=None):
    W, H = 900, 380
    s = [svg_ac(W, H, 900)]
    kutular = [(20, 30, "1 · Koruma", ["Uygun ırk, barınak, yem", "hijyen, aşı"], YESIL),
               (245, 30, "2 · Alternatif tedavi", ["Fitoterapi, homeopati,", "mineral, iz element"], MAVI),
               (470, 30, "3 · Kimyasal ilaç", ["Yalnız gerekirse, kayıtla,", "bekleme süresi x2 (≥48 sa)"], TURUNCU),
               (695, 30, "4 · Sayıyı say", ["Aşı, parazit, zorunlu", "programlar sayılmaz"], MOR)]
    for i, (x, y, b, alt, renk) in enumerate(kutular):
        kal = 5 if adim == i else 2.5
        s.append(f'<rect x="{x}" y="{y}" width="190" height="100" rx="14" fill="{"#FFF7E0" if adim == i else "white"}" stroke="{renk}" stroke-width="{kal}"/>')
        s.append(_yazi(x + 95, y + 30, b, 15, renk, kalin=True))
        for j, t in enumerate(alt):
            s.append(_yazi(x + 95, y + 58 + j * 20, t, 12, "#333"))
        if i < 3:
            s.append(_ok(x + 192, y + 50, x + 222, y + 50))
    s.append(_ok(790, 132, 790, 168))
    s.append(f'<rect x="560" y="172" width="320" height="86" rx="14" fill="#FDECEA" stroke="{KIRMIZI}" stroke-width="{5 if adim == 4 else 2.5}"/>')
    s.append(_yazi(720, 200, "Yılda 3'ten fazla kür", 15, KIRMIZI, kalin=True))
    s.append(_yazi(720, 222, "(verimli ömrü 1 yıldan kısa: 1'den fazla)", 12, "#333"))
    s.append(_yazi(720, 244, "→ organik satılamaz, yeniden geçiş", 13, KIRMIZI, kalin=True))
    s.append(f'<rect x="40" y="172" width="460" height="86" rx="14" fill="#E9F6EE" stroke="{YESIL}" stroke-width="2.5"/>')
    s.append(_yazi(270, 200, "Sınır aşılmadıysa", 15, YESIL, kalin=True))
    s.append(_yazi(270, 224, "Bekleme süresi dolunca ürün yeniden organik satılır.", 13, "#333"))
    s.append(_yazi(270, 246, "Her tedavi kayıt defterine işlenir.", 13, "#333"))
    s.append(_yazi(W / 2, 300, "Yasak: büyütme ya da verim artırıcı ilaç, koruyucu amaçlı antibiyotik,", 13, "#555"))
    s.append(_yazi(W / 2, 322, "kızgınlığı uyarmak ya da eşzamanlamak için hormon kullanımı.", 13, "#555"))
    s.append(_yazi(W / 2, 352, "Önce zarar verme (primum non nocere): hayvan acı çekiyorsa tedavi geciktirilmez.", 13, MAVI, kalin=True))
    s.append("</svg>")
    return "".join(s)


YASAK_ISLEM = ["Kuyruğu bantla boğma", "Kuyruk kesme", "Diş kesme", "Gaga ve ibik kesme", "Boynuz çıkarma"]


def svg_yasak_islem():
    W, H = 880, 200
    s = [svg_ac(W, H, 880)]
    s.append(_yazi(W / 2, 30, "Organik üretimde rutin olarak yapılmayan işlemler", 16, KIRMIZI, kalin=True))
    for i, t in enumerate(YASAK_ISLEM):
        x = 20 + i * 172
        s.append(f'<rect x="{x}" y="50" width="160" height="110" rx="14" fill="#FDECEA" stroke="{KIRMIZI}" stroke-width="2"/>')
        s.append(_carpi(x + 80, 86, 18))
        for j, p in enumerate(_iki_satir(t, 13)):
            s.append(_yazi(x + 80, 128 + j * 18, p, 13, "#333", kalin=True))
    s.append(_yazi(W / 2, 188, "İstisna yalnızca kontrol kuruluşunun izniyle, uygun yaşta ve anestezi/ağrı kesiciyle olabilir.", 12, "#555"))
    s.append("</svg>")
    return "".join(s)


def _hiyerarsi_panel(x0, y0, tur):
    s = []
    if tur == "lineer":
        pts = [(x0 + 120, y0 + 48 + i * 52) for i in range(5)]
        for i in range(4):
            s.append(_ok(pts[i][0], pts[i][1] + 16, pts[i + 1][0], pts[i + 1][1] - 18))
        baslik, aciklama = "Lineer (doğrusal)", "Her hayvan altındakilere üstün"
    elif tur == "alfa":
        pts = [(x0 + 120, y0 + 70)] + [(x0 + 30 + i * 60, y0 + 210) for i in range(4)]
        for i in range(1, 5):
            s.append(_ok(pts[0][0], pts[0][1] + 18, pts[i][0], pts[i][1] - 18))
        baslik, aciklama = "Alfa tipi", "Tek lider, diğerleri arasında belirgin sıra yok"
    else:
        pts = [(x0 + 120, y0 + 70), (x0 + 200, y0 + 200), (x0 + 40, y0 + 200), (x0 + 120, y0 + 270)]
        s.append(_ok(pts[0][0] + 12, pts[0][1] + 14, pts[1][0] - 8, pts[1][1] - 16))
        s.append(_ok(pts[1][0] - 18, pts[1][1], pts[2][0] + 18, pts[2][1]))
        s.append(_ok(pts[2][0] + 8, pts[2][1] - 16, pts[0][0] - 12, pts[0][1] + 14))
        s.append(_ok(pts[2][0] + 14, pts[2][1] + 12, pts[3][0] - 14, pts[3][1] - 10))
        s.append(_ok(pts[1][0] - 14, pts[1][1] + 12, pts[3][0] + 14, pts[3][1] - 10))
        baslik, aciklama = "Karmaşık (üçgen)", "Döngüsel ilişki: sıra net değil"
    for i, (x, y) in enumerate(pts):
        s.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{MAVI if i == 0 else "#dfe8f4"}" stroke="{MAVI}" stroke-width="2"/>')
        s.append(_yazi(x, y + 5, "ABCDE"[i], 14, "white" if i == 0 else "#223", kalin=True))
    s.append(_yazi(x0 + 120, y0 + 18, baslik, 15, "#333", kalin=True))
    s.append(_yazi(x0 + 120, y0 + 308, aciklama, 12, "#555"))
    return "".join(s)


def svg_hiyerarsi():
    W, H = 840, 340
    s = [svg_ac(W, H, 840)]
    for i, t in enumerate(["lineer", "alfa", "karmasik"]):
        s.append(_hiyerarsi_panel(20 + i * 280, 10, t))
    s.append("</svg>")
    return "".join(s)


def svg_hormon(sec=None):
    W, H = 900, 470
    s = [svg_ac(W, H, 900)]
    s.append(_kutu_svg(40, 20, 210, 60, MOR, ["Epifiz", "melatonin (gün uzunluğu)"], 13))
    s.append(_kutu_svg(345, 20, 210, 60, MAVI, ["Hipotalamus", "duyuları toplar, hipofizi yönetir"], 13))
    s.append(_ok(252, 50, 342, 50))
    s.append(_ok(450, 82, 300, 128))
    s.append(_ok(450, 82, 600, 128))
    s.append(_kutu_svg(170, 132, 260, 64, MAVI, ["Ön hipofiz", "FSH, LH, prolaktin, TSH, ACTH, GH"], 12, "#EEF3FA"))
    s.append(_kutu_svg(480, 132, 260, 64, MAVI, ["Arka hipofiz", "oksitosin, ADH"], 12, "#EEF3FA"))
    hedef = [("Yumurtalık", "östrojen", "kızgınlık davranışı", PEMBE),
             ("Testis", "testosteron", "erkek cinsel davranışı", MAVI),
             ("Tiroid", "T4, T3", "enerji, cinsel döngü", YESIL),
             ("Adrenal", "adrenalin", "kaç ya da savaş", KIRMIZI),
             ("Meme", "prolaktin / oksitosin", "süt sentezi / süt indirme", TURUNCU)]
    for i, (o, h, d, renk) in enumerate(hedef):
        x = 15 + i * 176
        kal = 5 if sec == i else 2.5
        kaynak_x = 300 if i < 4 else 610
        s.append(_ok(kaynak_x if i < 4 else 610, 198, x + 82, 262, "#999"))
        if i == 4:
            s.append(_ok(400, 198, x + 60, 262, "#999"))
        s.append(f'<rect x="{x}" y="266" width="164" height="120" rx="14" fill="{"#FFF7E0" if sec == i else "white"}" stroke="{renk}" stroke-width="{kal}"/>')
        s.append(_yazi(x + 82, 294, o, 15, renk, kalin=True))
        s.append(_yazi(x + 82, 324, h, 13, "#333"))
        s.append(_yazi(x + 82, 352, d, 12, "#555"))
    s.append(_yazi(W / 2, 420, "Uyarı (duyu) → sinir sistemi → hormon → davranış.", 14, "#333", kalin=True))
    s.append(_yazi(W / 2, 446, "Örnek: emme uyarısı → hipotalamus → oksitosin → süt indirme.", 13, "#555"))
    s.append("</svg>")
    return "".join(s)


def _tavuk(cx, cy, k=1.0, renk="#C87533"):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{9 * k}" ry="{7 * k}" fill="{renk}"/>'
            f'<circle cx="{cx + 7 * k}" cy="{cy - 6 * k}" r="{4 * k}" fill="{renk}"/>'
            f'<path d="M{cx + 10 * k},{cy - 6 * k} l{4 * k},{1 * k} l{-4 * k},{2 * k} z" fill="#E8A33B"/>'
            f'<path d="M{cx + 5 * k},{cy - 10 * k} q{2 * k},{-4 * k} {4 * k},0" fill="#C0392B"/>')


def svg_yogunluk(n_sol, n_sag, bas_sol, bas_sag, birim="1 m²"):
    W, H = 820, 390
    s = [svg_ac(W, H, 820)]
    for j, (n, bas, renk) in enumerate([(n_sol, bas_sol, KIRMIZI), (n_sag, bas_sag, YESIL_A)]):
        x0, y0, L = 60 + j * 400, 60, 280
        s.append(f'<rect x="{x0}" y="{y0}" width="{L}" height="{L}" fill="#FAF6EE" stroke="{renk}" stroke-width="3"/>')
        s.append(_yazi(x0 + L / 2, 40, bas, 15, renk, kalin=True))
        k = max(1, math.ceil(math.sqrt(max(n, 1))))
        ad = L / k
        say = 0
        for a in range(k):
            for b in range(k):
                if say >= n:
                    break
                s.append(_tavuk(x0 + ad * (b + 0.5), y0 + ad * (a + 0.55), min(1.6, ad / 22)))
                say += 1
        s.append(_yazi(x0 + L / 2, y0 + L + 26, f"{birim} içinde {n} hayvan", 14, "#333"))
    s.append("</svg>")
    return "".join(s)


# Otlama halkası: 24 saat
OTLAMA = {"Sığır": [(5, 8), (11, 13), (15, 17), (18.5, 20.5)],
          "Koyun": [(5, 9), (15, 20)],
          "Keçi": [(6, 9.5), (16.5, 20)]}


def svg_otlama(tur):
    W, H = 760, 420
    s = [svg_ac(W, H, 760)]
    cx, cy, R = 230, 210, 150

    def nokta(saat, r):
        a = -math.pi / 2 + saat / 24 * 2 * math.pi
        return cx + r * math.cos(a), cy + r * math.sin(a)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#F3F5F8" stroke="#bbb" stroke-width="2"/>')
    # gece yarım daire koyu
    x1, y1 = nokta(19.5, R)
    x2, y2 = nokta(6, R)
    s.append(f'<path d="M{cx},{cy} L{x1},{y1} A{R},{R} 0 0 1 {x2},{y2} Z" fill="#DCE3EE"/>')
    for (b, e) in OTLAMA[tur]:
        xa, ya = nokta(b, R)
        xb, yb = nokta(e, R)
        buyuk = 1 if (e - b) > 12 else 0
        s.append(f'<path d="M{cx},{cy} L{xa},{ya} A{R},{R} 0 {buyuk} 1 {xb},{yb} Z" fill="{YESIL}" opacity="0.85"/>')
    for sa in range(0, 24, 3):
        x, y = nokta(sa, R + 18)
        s.append(_yazi(x, y + 5, f"{sa:02d}", 13, "#444"))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="white" stroke="#bbb"/>')
    s.append(_yazi(cx, cy + 6, tur, 16, "#333", kalin=True))
    bilgi = {"Sığır": ["Günde 4 yoğun otlama dönemi", "Günlük yürüme ~4 km", "Otu az çiğneyip yutar", "Geviş: günde 4–9 saat"],
             "Koyun": ["En uzun: sabah erken ve", "öğleden sonra–gün batımı", "Günlük yürüme 3–10 km", "Geviş: ~8 dönem, ~8 saat"],
             "Keçi": ["En uzun: sabah ve akşam", "Günde 8–9 saat otlama", "%65–70'i yüksekten (dal, yaprak)", "Ağılda gevişin %75'i gece"]}[tur]
    s.append(f'<rect x="430" y="110" width="300" height="190" rx="14" fill="white" stroke="{YESIL}" stroke-width="2"/>')
    for i, t in enumerate(bilgi):
        s.append(_yazi(580, 150 + i * 38, t, 14, "#333"))
    s.append(f'<rect x="440" y="330" width="18" height="14" fill="{YESIL}"/>')
    s.append(_yazi(466, 342, "yoğun otlama", 13, "#333", "start"))
    s.append(f'<rect x="580" y="330" width="18" height="14" fill="#DCE3EE"/>')
    s.append(_yazi(606, 342, "gece", 13, "#333", "start"))
    s.append(_yazi(W / 2, H - 14, "Saatler öğretici yaklaşık değerlerdir; mevsim, ırk ve meraya göre değişir.", 12, "#777"))
    s.append("</svg>")
    return "".join(s)


BARINAK_FAKTOR = ["Yaşam alanı", "Sıcaklık", "Nem", "Aydınlatma", "Havalandırma", "Gürültü",
                  "Hayvan-hayvan etkileşimi", "Hayvan-insan etkileşimi"]


def svg_barinak(sec=None):
    W, H = 840, 430
    s = [svg_ac(W, H, 840)]
    cx, cy = 420, 215
    s.append(f'<path d="M{cx - 110},{cy + 60} L{cx - 110},{cy - 20} L{cx},{cy - 90} L{cx + 110},{cy - 20} L{cx + 110},{cy + 60} Z" '
             f'fill="#F6EFE4" stroke="{KAHVE}" stroke-width="3"/>')
    s.append(f'<rect x="{cx - 25}" y="{cy + 10}" width="50" height="50" fill="#e0cfb5" stroke="{KAHVE}" stroke-width="2"/>')
    s.append(_yazi(cx, cy - 18, "BARINAK", 16, KAHVE, kalin=True))
    s.append(_yazi(cx, cy + 2, "refah · sağlık · verim", 12, "#555"))
    for i, f in enumerate(BARINAK_FAKTOR):
        a = -math.pi / 2 + i * 2 * math.pi / 8
        x, y = cx + 300 * math.cos(a), cy + 165 * math.sin(a)
        renk = [MAVI, KIRMIZI, "#2a9d8f", SARI, YESIL, MOR, TURUNCU, PEMBE][i]
        s.append(f'<line x1="{cx + 120 * math.cos(a)}" y1="{cy + 80 * math.sin(a)}" x2="{x - 70 * math.cos(a)}" '
                 f'y2="{y - 22 * math.sin(a)}" stroke="#bbb" stroke-width="2"/>')
        kal = 5 if sec == i else 2.5
        s.append(f'<rect x="{x - 95}" y="{y - 22}" width="190" height="44" rx="12" fill="{"#FFF7E0" if sec == i else "white"}" stroke="{renk}" stroke-width="{kal}"/>')
        parca = _iki_satir(f, 18)
        for j, p in enumerate(parca):
            s.append(_yazi(x, y + 5 + (j - (len(parca) - 1) / 2) * 16, p, 13, "#333", kalin=True))
    s.append("</svg>")
    return "".join(s)


def svg_aydinlatma(isik_saat, dongu=24, gun_say=3):
    W, H = 840, 200
    s = [svg_ac(W, H, 840)]
    toplam = 72
    x0, L = 40, 760
    olcek = L / toplam
    t = 0
    while t < toplam:
        isik = min(isik_saat, toplam - t)
        s.append(f'<rect x="{x0 + t * olcek}" y="60" width="{isik * olcek}" height="50" fill="{SARI}"/>')
        kar = min(dongu - isik_saat, toplam - t - isik)
        if kar > 0:
            s.append(f'<rect x="{x0 + (t + isik) * olcek}" y="60" width="{kar * olcek}" height="50" fill="#2C3E50"/>')
        t += dongu
    for g in range(4):
        x = x0 + g * 24 * olcek
        s.append(f'<line x1="{x}" y1="50" x2="{x}" y2="125" stroke="#C0392B" stroke-width="2" stroke-dasharray="4 3"/>')
        s.append(_yazi(x, 145, f"{g}. gün" if g else "başlangıç", 12, "#C0392B"))
    s.append(_yazi(W / 2, 30, f"{dongu} saatlik döngü: {isik_saat} saat ışık + {dongu - isik_saat} saat karanlık (3 takvim günü)", 15, "#333", kalin=True))
    s.append(_yazi(W / 2, 180, "Sarı: ışık · Lacivert: karanlık · Kırmızı kesikli çizgi: takvim günü sınırı", 12, "#666"))
    s.append("</svg>")
    return "".join(s)


def svg_koken():
    W, H = 900, 300
    s = [svg_ac(W, H, 900)]
    s.append(_kutu_svg(330, 14, 240, 50, MAVI, ["DAVRANIŞIN KÖKENLERİ"], 15, "#EEF3FA"))
    kol = [("Refleksler", ["Refleks: doğuştan, otomatik", "Şartlı refleks: deneyimle", "kazanılan (ör. sağım sesi)"], YESIL),
           ("Kalıtım", ["Genetik yapı: türün", "ortak davranışları", "İçgüdü: kalıtsal iç eğilim"], MOR),
           ("Çevre", ["Güdü, öğrenme,", "geçmiş deneyimler", "Yer değiştirme aktivitesi"], TURUNCU)]
    for i, (b, m, renk) in enumerate(kol):
        x = 30 + i * 290
        s.append(_ok(450, 66, x + 130, 104))
        s.append(f'<rect x="{x}" y="108" width="260" height="160" rx="14" fill="white" stroke="{renk}" stroke-width="2.5"/>')
        s.append(_yazi(x + 130, 138, b, 16, renk, kalin=True))
        for j, t in enumerate(m):
            s.append(_yazi(x + 130, 176 + j * 28, t, 13, "#333"))
    s.append("</svg>")
    return "".join(s)


def svg_yuzey_hacim():
    """Küçük hayvanın yüzey/ağırlık oranı büyüktür: aynı küp yaklaşımıyla gösterim."""
    W, H = 820, 260
    s = [svg_ac(W, H, 820)]
    for i, (a, ad) in enumerate([(30, "Fare kadar"), (70, "Tavşan kadar"), (140, "Koyun kadar (ölçeksiz)")]):
        x = 120 + i * 250
        y = 200 - a
        s.append(f'<rect x="{x}" y="{y}" width="{a}" height="{a}" fill="#dfe8f4" stroke="{MAVI}" stroke-width="2"/>')
        oran = 6 / (a / 10)
        s.append(_yazi(x + a / 2, 228, ad, 13, "#333", kalin=True))
        s.append(_yazi(x + a / 2 + (0 if i < 2 else 0), y - 10, f"göreli yüzey/hacim: {oran:.2f}".replace(".", ","), 12, KIRMIZI if i == 0 else "#555"))
    s.append(_yazi(W / 2, 22, "Küçük hayvan → birim ağırlık başına daha çok yüzey → daha hızlı ısı kaybı → termoregülasyona daha çok enerji", 13, "#333", kalin=True))
    s.append("</svg>")
    return "".join(s)


# ===========================================================================
# VERİLER (ders notları + mevzuat)
# ===========================================================================
# Geçiş süreleri (hayvan ve ürün)
GECIS_TUR = {
    "Büyükbaş (sığır, manda) · et": ("ay", 12),
    "Küçükbaş (koyun, keçi) · et": ("ay", 6),
    "Domuz · et": ("ay", 6),
    "Süt hayvanı · süt": ("ay", 6),
    "Etlik kanatlı · et (3 günlükten küçükken alınmış)": ("hafta", 10),
    "Yumurta tavuğu · yumurta": ("hafta", 6),
}

# Yavruların sütle beslenmesi gereken asgari süre (gün)
SUT_SURE = {"Büyükbaş (buzağı) ve tek tırnaklı (tay)": 90, "Küçükbaş (kuzu, oğlak)": 45, "Domuz (domuz yavrusu)": 40}

# Organik olmayan işletmeden alınabilecek yavruların üst yaş sınırı
ALIM_YAS = {"Buzağı / tay": ("ay", 6, "6 aylıktan küçük"), "Kuzu / oğlak": ("gün", 60, "60 günden büyük olmamalı"),
            "Etlik civciv": ("gün", 3, "3 günlükten büyük olmamalı")}

# Hayvan başına en az alan, m² (iç, dış) - AB 889/2008 Ek III'e göre öğretici özet
YOGUNLUK = {
    "Süt ineği": (6.0, 4.5),
    "Damızlık boğa": (10.0, 30.0),
    "Sığır, 100 kg'a kadar": (1.5, 1.1),
    "Sığır, 200 kg'a kadar": (2.5, 1.9),
    "Sığır, 350 kg'a kadar": (4.0, 3.0),
    "Koyun / keçi": (1.5, 2.5),
    "Yavrulu ana domuz (40 güne kadar)": (7.5, 2.5),
    "Besi domuzu, 50 kg'a kadar": (0.8, 0.6),
    "Besi domuzu, 85 kg'a kadar": (1.1, 0.8),
    "Besi domuzu, 110 kg'a kadar": (1.3, 1.0),
    "Yumurta tavuğu": (1 / 6, 4.0),
    "Etlik piliç (sabit kümes)": (1 / 10, 4.0),
}

# 170 kg N/ha/yıl sınırına karşılık gelen hayvan sayısı (hayvan/ha) - AB 889/2008 Ek IV
AZOT_ESDEGER = {
    "Süt ineği": 2.0, "Besi buzağısı": 5.0, "1-2 yaş dişi sığır": 3.3, "Koyun": 13.3, "Keçi": 13.3,
    "Damızlık ana domuz": 6.5, "Besi domuzu": 14.0, "Yumurta tavuğu": 230.0, "Etlik piliç": 580.0,
}

# Konvansiyonel ve organik tavuk yoğunluğu karşılaştırması
TAVUK_KARS = {
    "Yumurta tavuğu": {"Konvansiyonel kümes (notta 460 cm²/tavuk)": 21, "Organik (iç alan en çok 6 tavuk/m²)": 6},
    "Etlik piliç": {"Konvansiyonel (notta 17–22 piliç/m²)": 20, "Organik sabit kümes (en çok 10 piliç/m²)": 10},
}

# Oyunlar
ORGANIK_MI = [
    ("Sertifikası olmayan 'köy yumurtası'", "Organik değil"),
    ("Ambalajında yalnız 'doğal' yazan süt", "Organik değil"),
    ("'Kafessiz' etiketli, sertifikasız yumurta", "Organik değil"),
    ("'Gezen tavuk' yazan, sertifikasız piliç", "Organik değil"),
    ("'Özgür' yazan, sertifikasız tavuk eti", "Organik değil"),
    ("Yetkili kuruluşça sertifikalanmış, logolu peynir", "Organik"),
    ("Geçiş süresinde sağılan süt", "Organik değil"),
    ("Geçiş süresi dolmuş, sertifikalı kuzu eti", "Organik"),
    ("Yılda 4 kez antibiyotikle tedavi edilmiş inekten süt", "Organik değil"),
    ("Sertifikalı işletmede, bekleme süresi dolduktan sonra sağılan süt", "Organik"),
    ("Embriyo transferiyle doğmuş buzağının eti", "Organik değil"),
    ("GDO'lu soya küspesiyle beslenmiş piliç", "Organik değil"),
]

IZIN_YASAK = [
    ("Ağız sütü (kolostrum)", "İzinli"), ("Probiyotik", "İzinli"), ("Melas", "İzinli"), ("Tuz", "İzinli"),
    ("Doğal kaynaklı vitamin", "İzinli"), ("Enzim", "İzinli"), ("Organik asit", "İzinli"),
    ("Makro ve mikro mineraller", "İzinli"),
    ("GDO'lu mısır", "Yasak"), ("Hayvansal yağ (rasyona)", "Yasak"), ("Büyütme hormonu", "Yasak"),
    ("Yem katkısı olarak antibiyotik", "Yasak"), ("Koksidiyostat (yem katkısı)", "Yasak"),
    ("Kimyasal solventle çıkarılmış küspe", "Yasak"), ("Sentetik yumurta sarısı renklendiricisi", "Yasak"),
    ("Zorla besleme", "Yasak"), ("Nakil sırasında sakinleştirici", "Yasak"),
    ("Kızgınlığı eşzamanlamak için hormon", "Yasak"), ("Embriyo transferi", "Yasak"),
    ("Doğal yolla alınmış spermayla suni tohumlama", "İzinli"), ("Fitoterapi (bitkisel tedavi)", "İzinli"),
    ("Aşı", "İzinli"),
]

OZGURLUK_DURUM = [
    ("Suluk iki gündür bozuk, hayvanlar susuz", 0), ("Yemlik sayısı az, zayıf hayvanlar yem alamıyor", 0),
    ("Barınak çok sıcak ve havasız", 1), ("Zemin ıslak ve çamurlu, yatacak kuru yer yok", 1),
    ("Topallayan inek günlerdir tedavi edilmiyor", 2), ("Keskin kenarlı bölmede yaralanan buzağılar", 2),
    ("Kafeste kanat çırpamayan, eşinemeyen tavuk", 3), ("Tek başına tutulan, tür arkadaşı görmeyen buzağı", 3),
    ("Bakıcı hayvanlara bağırıp vuruyor", 4), ("Yüksek gürültülü makinenin yanında tutulan koyunlar", 4),
]

ANORMAL = [
    ("Kuyruk ısırma", "Domuz", "Sıkışıklık, uğraşı yokluğu (saman, kök materyali yok), havasız ortam",
     "Yeterli alan, saman ve kök materyali, havalandırma"),
    ("Kanibalizm (yamyamlık)", "Tavuk", "Kalabalık, aşırı ışık, eşinme ve kum banyosu imkânı yok",
     "Alan, loş ışık, altlık, açık alan, yeterli protein"),
    ("Dil oynatma", "Sığır", "Kaba yem az, yeme süresi kısa, emme isteği karşılanmamış",
     "Bol kaba yem, ad libitum yemleme, buzağının anayla emmesi"),
    ("Yapağı ısırma", "Koyun", "Kaba yem eksikliği, sıkışıklık", "Yeterli kaba yem ve alan"),
    ("Kloak gagalama", "Tavuk", "Yumurtlamaya başlama dönemi hormon değişimi, güçlü ışık",
     "Işık şiddetini düşürmek"),
    ("Polidipsi (aşırı su içme)", "Tavuk", "Kafeste uğraşı yokluğu, nipelle oynama", "Yemi sık karıştırıp dikkati yeme çekmek"),
    ("Yumurta yeme", "Tavuk", "Besin eksikliği, grid yokluğu, kırık yumurta bulma",
     "Loş folluk, yumurtayı hemen toplamak, iyi kabuk için besleme, alışkanlık yapanı ayırmak"),
    ("Birbirini emme (kulak, göbek)", "Sığır", "Büyük buzağıda besin yetersizliği, emme isteği",
     "Yeterli süt süresi, emzikli besleme, iyi rasyon"),
]

# Sözlük
TERIMLER = [
    ("Organik hayvansal üretim", "Sentetik girdilerin kullanılmadığı (zorunluysa en az düzeyde kullanıldığı), organik yemle ve refah gözetilerek yapılan, her aşaması kontrollü ve sertifikalı hayvansal üretim."),
    ("Primum non nocere", "'Önce zarar verme.' Organik hayvancılıkta hayvanı hasta etmeme, acı çektirmeme ilkesi."),
    ("Geçiş süreci", "Konvansiyonelden organiğe geçerken ürünün henüz organik satılamadığı süre (ör. sığır eti 12 ay, süt 6 ay)."),
    ("Konvansiyonel üretim", "Sentetik girdilerin serbestçe kullanıldığı geleneksel/yoğun üretim."),
    ("Entansif sistem", "Çok sayıda hayvanın dar alanda, yüksek girdiyle yetiştirildiği yoğun sistem."),
    ("Ekstansif sistem", "Hayvanların geniş alanda, merada, düşük girdiyle yetiştirildiği yaygın sistem."),
    ("Kolostrum (ağız sütü)", "Doğumdan sonraki ilk süt; yavrunun bağışıklığını güçlendirir."),
    ("Ad libitum", "Hayvanın istediği zaman, istediği kadar yem ya da su alabilmesi."),
    ("GDO", "Genetiği değiştirilmiş organizma; organik üretimde ve yemde yasaktır."),
    ("BSE (deli dana)", "Sığırlarda süngerimsi beyin hastalığı; kadavra unu içeren yemlerle yayılmıştır."),
    ("Fitoterapi", "Bitkilerle ya da bitkisel preparatlarla tedavi."),
    ("Homeopati", "Organik hayvancılıkta öncelik verilen alternatif tedavi yaklaşımı (bilimsel kanıtı tartışmalıdır)."),
    ("Bekleme süresi", "İlaç verildikten sonra ürünün (süt, et, yumurta) gıda olarak kullanılamadığı süre; organikte yasal sürenin iki katı, en az 48 saat."),
    ("Sertifikasyon", "Yetkili kuruluşun üretimin kurallara uygunluğunu denetleyip belgelemesi."),
    ("Hayvan refahı", "Hayvanın fiziksel ve ruhsal olarak iyi durumda, çevresiyle uyum içinde olması, acı çekmemesi, doğal davranışlarını gösterebilmesi."),
    ("Beş özgürlük", "Açlık-susuzluk, rahatsızlık, acı-yaralanma-hastalık, korku-stresten uzak olma ve normal davranışı gösterme özgürlükleri (FAWC)."),
    ("Brambell Komitesi", "1965'te İngiltere'de kurulan, hayvanın dönebilmesi, kalkıp yatabilmesi, kendini temizleyebilmesi ve uzuvlarını gerebilmesi gerektiğini vurgulayan komite."),
    ("Etholoji", "Hayvan davranışını biyolojik olarak inceleyen bilim dalı."),
    ("Refleks", "Uyarana karşı doğuştan gelen, istemsiz ve otomatik yanıt."),
    ("Şartlı refleks", "Deneyimle öğrenilen refleks; ör. sağım makinesinin sesini duyunca süt indirme."),
    ("İçgüdü", "Türün bireylerinde aynı biçimde görülen, uyaranla başlayan, kalıtsal davranış eğilimi."),
    ("Güdü", "Davranışı başlatan, yönünü ve sürekliliğini belirleyen içsel güç."),
    ("Yer değiştirme aktivitesi", "İki zıt güdü arasında kalan hayvanın ilgisiz bir davranış göstermesi."),
    ("Feromon", "Aynı türün bireyleri arasında iletişim sağlayan koku maddesi."),
    ("Flehmen", "Erkeğin dişinin idrarını kokladıktan sonra üst dudağını kıvırması; koku algısını güçlendirir."),
    ("Ruminasyon (geviş getirme)", "Az çiğnenip rumende biriken yemin ağza geri getirilip çiğnenmesi ve yeniden yutulması."),
    ("Sessiz kızgınlık", "Dişinin kızgınlıkta olduğu hâlde belirti göstermemesi."),
    ("Sosyal hiyerarşi", "Grupta hayvanlar arasında oluşan üstünlük sıralaması."),
    ("Gagalama düzeni", "Tavuklarda üstünlük sıralaması."),
    ("Alfa hayvan", "Grubun en üstün bireyi (ör. alfa teke)."),
    ("Agonistik davranış", "Tehdit, saldırı, kaçma, boyun eğme gibi mücadeleyle ilgili davranışlar."),
    ("Gurkluk", "Tavuğun kuluçkaya yatma isteği."),
    ("Folluk", "Tavukların yumurtladığı yuva kutusu."),
    ("Kanibalizm", "Tavuklarda birbirini gagalayıp yaralama, yeme."),
    ("Polidipsi", "Aşırı su içme."),
    ("Problem kuzu", "Anası ölen, sütsüz, reddeden ya da zayıf doğup ilgi görmeyen kuzu."),
    ("Termoregülasyon", "Vücut sıcaklığının düzenlenmesi."),
    ("Oksitosin", "Arka hipofiz hormonu; süt indirme ve rahim kasılmaları."),
    ("Prolaktin", "Ön hipofiz hormonu; süt sentezi, analık davranışıyla ilişkili."),
    ("Melatonin", "Epifiz hormonu; gün uzunluğuna göre salgılanır, mevsimsel üremeyi düzenler."),
    ("170 kg N/ha", "Organik işletmede gübreyle bir hektara yılda verilebilecek en çok azot; hayvan sayısını sınırlar."),
    ("Embriyo transferi", "Embriyonun başka bir dişiye aktarılması; organik üretimde yasak."),
]


# ===========================================================================
# SAYFALAR
# ===========================================================================
import datetime as _dt


def _mini_oyun(anahtar, liste, secenekler, soru, aciklama=None):
    """liste: [(metin, doğru_seçenek), ...]"""
    if f"{anahtar}_i" not in st.session_state:
        st.session_state[f"{anahtar}_i"] = int(rng().integers(0, len(liste)))
        st.session_state[f"{anahtar}_puan"] = [0, 0]
    metin, dogru = liste[st.session_state[f"{anahtar}_i"]]
    st.markdown(f'<div class="flash" style="font-size:1.1rem">{metin}</div>', unsafe_allow_html=True)
    st.caption(soru)
    kol = st.columns(len(secenekler) + 1)
    yanit = None
    for k, sec in zip(kol, secenekler):
        if k.button(sec, key=f"{anahtar}_{sec}"):
            yanit = sec
    if kol[-1].button("➡️ Başka", key=f"{anahtar}_yeni"):
        st.session_state[f"{anahtar}_i"] = int(rng().integers(0, len(liste)))
        st.rerun()
    if yanit is not None:
        p = st.session_state[f"{anahtar}_puan"]
        p[1] += 1
        if yanit == dogru:
            p[0] += 1
            st.success(f"✅ Doğru: **{dogru}**")
        else:
            st.error(f"❌ Doğrusu: **{dogru}**")
        if aciklama:
            st.caption(aciklama(metin, dogru))
    p = st.session_state[f"{anahtar}_puan"]
    if p[1]:
        st.caption(f"Puanınız: {p[0]} / {p[1]}")


def sayfa_giris():
    st.title("🐄 Organik Hayvansal Üretim")
    st.markdown("""
**Organik Hayvansal Üretim** dersi için hazırlanmış etkileşimli bir ders uygulaması. Organik
hayvancılığın kurallarını (hayvan kaynağı, barınma, besleme, geçiş süreleri, sağlık) ve bu
kuralların dayandığı **hayvan davranışı ve refahı** bilgisini birlikte işler. Şemalar,
hesaplayıcılar ve oyunlar var; her bölümün sonunda **10, 20 ya da 30 soruluk alıştırma** ve
açıklamalı çözümler bulunur.""")
    svg_goster(svg_kapali_sistem())
    kartlar([
        ("1 · Neden organik?", "Yoğun üretimin sorunları, nüfus, Türkiye'de hayvancılık, avantaj ve dezavantajlar"),
        ("2 · Tanım, ilkeler, mevzuat", "Kapalı çiftlik döngüsü, primum non nocere, 5262 sayılı Kanun, 'organik mi?' oyunu"),
        ("3 · Hayvan kaynağı ve üreme", "Irk seçimi, doğal aşım, suni tohumlama, konvansiyonel hayvan alımında yaş sınırı"),
        ("4 · Barınma ve açık alan", "Alan hesaplayıcı, konvansiyonel–organik tavuk yoğunluğu, 170 kg N/ha hesabı"),
        ("5 · Besleme", "Su, ağız sütü, sütle besleme süreleri, izinli–yasak yem oyunu, rasyon denetleyici"),
        ("6 · Geçiş süreleri", "Zaman çizelgesi, organik satış tarihi hesaplayıcı, ömrün 3/4'ü kuralı"),
        ("7 · Hayvan sağlığı ve tedavi", "Yasak işlemler, tedavi akışı, kür sayacı, bekleme süresi hesabı"),
        ("8 · Taşıma, kesim, kayıt, karar", "8 saatte bir mola, ayrı kesim, kayıt, 'organik hayvancılık bana uygun mu?'"),
        ("9 · Hayvan refahı", "Refah göstergeleri, Brambell, beş özgürlük oyunu, AB mevzuatı"),
        ("10 · Etholoji ve davranışın temelleri", "Davranışın kökenleri, duyular, sinir sistemi, hormonlar"),
        ("11 · Barınak çevresi", "Alan, sıcaklık, nem, ışık, hava, gürültü, sosyal etkileşim; nem denetimi"),
        ("12 · Türlere göre davranış", "Sığır, koyun, keçi, tavuk: otlama saatleri, tohumlama zamanı, koç sayısı, aydınlatma"),
        ("13 · Davranış bozuklukları", "Kuyruk ısırma, kanibalizm, dil oynatma, yumurta yeme; organik çözümler"),
        ("14 · Genel tekrar", "Hafıza kartları, sözlük ve tüm konulardan karışık sorular"),
    ])
    st.markdown("**Hazırlayanlar:** Emine Dilşat Yeğenoğlu & Tevfik Hasan Can")
    ipucu("Telefonda bölümleri sayfanın en üstündeki <b>Bölüm</b> kutusundan ya da sayfa sonundaki "
          "<b>Önceki / Sonraki</b> bağlantılarından seçebilirsiniz.")
    uyari("Sayısal kurallar (süreler, oranlar, alanlar) Türkiye'deki <b>Organik Tarımın Esasları ve Uygulanmasına "
          "İlişkin Yönetmelik</b> (RG 18.08.2010, 27676 ve değişiklikleri) ve onunla uyumlu AB kurallarına göre "
          "öğretici olarak özetlenmiştir. Mevzuat değişebilir; uygulamada her zaman yürürlükteki metne ve kontrol "
          "kuruluşuna başvurulur.")


# ---------------------------------------------------------------------------
NUFUS = [(0, 250), (1650, 500), (1830, 1000), (1930, 2000), (1975, 4000), (1998, 5900)]
TR_HAYVAN_2016 = {"Kültür sığır": 6588527, "Kültür melezi sığır": 5758336, "Yerli sığır": 1733292,
                  "Manda": 142073, "Merinos koyun": 2151264, "Yerli koyun": 28832669,
                  "Kıl keçisi": 10137534, "Tiftik keçisi": 207765}


def sayfa_neden():
    st.title("1 · Neden organik hayvancılık?")
    st.header("Yoğun üretim ve sorunları")
    st.markdown("""
Hızla artan nüfusun **gıda, barınma, lif ve yakıt** gereksinimi ve ekonomik kazanç isteği, bitkisel
ve hayvansal üretimi **yoğun (entansif)** hâle getirdi. Amaç: pestisit, gübre, büyüme uyarıcılar
gibi **yoğun girdiyle birim alandan daha çok ürün**. Bunun bedeli şemada.""")
    svg_goster(svg_yogun_sorun())
    uyari("<b>BSE (deli dana hastalığı):</b> Sığır besisinde kullanılan kesif yemlere, scrapie hastalığından ölen "
          "koyunların kadavra unlarının karışmasıyla ortaya çıktı. Organik hayvancılıkta hayvansal yağ ve "
          "yan ürünlerin rasyona katılmaması bu deneyimin bir sonucudur.")

    st.header("Nüfus ve gıda")
    fig = go.Figure(go.Scatter(x=[y for y, _ in NUFUS], y=[n / 1000 for _, n in NUFUS], mode="lines+markers",
                               line=dict(color=MAVI, width=3)))
    fig.update_layout(title="Dünya nüfusu (milyar)", xaxis_title="Yıl", yaxis_title="Milyar kişi")
    ciz(fig, 330)
    yil = st.select_slider("İkiye katlanma süresine bakın", [f"{a}→{b}" for (a, _), (b, _) in zip(NUFUS[:-1], NUFUS[1:])],
                           value="1930→1975", key="nufus_yil")
    a, b = [int(t) for t in yil.split("→")]
    na = dict(NUFUS)[a]
    nb = dict(NUFUS)[b]
    st.markdown(f"{a}'den {b}'e nüfus **{na:,} → {nb:,} milyon** oldu; {b - a} yılda ×{nb / na:.1f}.".replace(",", "."))
    kartlar([("Gıda güvencesi", "Herkesin yeterli, besleyici gıdaya her zaman ulaşabilmesi (miktar ve erişim)."),
             ("Gıda güvenliği", "Gıdanın sağlığa zarar vermemesi: kalıntı, hastalık etkeni, bulaşanlar (kalite ve sağlık)."),
             ("Adil dağıtım", "Dünyada gıda üretimi yetersiz değildir; sorun büyük ölçüde dağıtımdadır.")])
    st.caption("Nüfus tablosu ders notundan alınmıştır (1998'e kadar). Dünya nüfusu bugün 8 milyarı aşmıştır.")

    st.header("Türkiye'de hayvancılık")
    st.markdown("""
- Gelişmiş ülkelerde hayvansal üretimin tarımsal üretimdeki payı **%60–70**'in üzerindeyken Türkiye'de
  **%25–30** düzeyindedir (ders notu, 2009 verisi).
- Türkiye'de bitkisel ve hayvansal üretim, diğer Akdeniz ülkelerindeki gibi **entegre değildir**.
- Farklı ekosistemler, iklim bölgeleri ve zengin biyoçeşitlilik organik hayvancılık için **büyük potansiyel**dir.""")
    fig = go.Figure(go.Bar(x=list(TR_HAYVAN_2016.values()), y=list(TR_HAYVAN_2016.keys()), orientation="h",
                           marker_color=[KAHVE, KAHVE, KAHVE, GRI_K, TURUNCU, TURUNCU, MOR, MOR]))
    fig.update_layout(title="Türkiye hayvan sayıları, 2016 (TÜİK, baş)", xaxis_title="Baş")
    ciz(fig, 380)
    st.caption("Ders notundaki TÜİK 2015–2016 verisi. Güncel sayılar için TÜİK Hayvansal Üretim İstatistiklerine bakın. "
               "Dikkat: yerli koyunlar koyunların %93'ü, yerli sığırlar ise sığırların yalnızca %12'si.")

    st.header("Avantajlar, dezavantajlar, amaçlar")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("👍 Avantajlar")
        st.markdown("""
- Kalıntısız, sağlıklı gıda üretimine yardımcı
- Hayvan refahı yüksek
- Kimyasal gübre, pestisit, hormon, antibiyotik gibi girdilerden tasarruf
- Ürünler daha yüksek fiyatla satılabilir
- Yeni istihdam alanları
- Bitkisel ve hayvansal üretim birbirine bağlanır
- Gübre toprağa döner; biyoçeşitlilik korunur""")
    with c2:
        st.subheader("👎 Dezavantajlar")
        st.markdown("""
- Uygulaması zor, kurallı ve denetimli bir sistem
- Hayvan ve yem kaynağının organik olması gerekir
- Yemden yemlemeye kadar organik bütünlük korunmalı
- Maliyet daha yüksek, verim çoğu zaman daha düşük
- Sertifika ve kayıt yükü""")
    kartlar([("Çevre", "Çevreye dost bir üretim sistemi"), ("Sağlık", "Hayvanları sağlıklı tutmak"),
             ("Refah", "Hayvan refahında yüksek standart"), ("Kalite", "Yüksek kaliteli ürün")])
    ipucu("Ekonomik önem: organik hayvancılık, organik işletmenin kazancının <b>%50'den fazlasını</b> "
          "oluşturabilir. Ekolojik önem: ruminantlar çayır, mera ve baklagil yem bitkilerini iyi değerlendirir; "
          "gübreleri toprak verimliliğini korur.")
    st.markdown("Organik hayvancılıkta öne çıkan ülkeler: **ABD, Kanada ve Avrupa Birliği**. AB içinde sertifikalı "
                "organik süt sığırcılığının en yaygın olduğu ülke **Avusturya**'dır (ders notu).")
    alistirma_blogu("neden", "Neden organik?", gen_neden)


# ---------------------------------------------------------------------------
def sayfa_tanim():
    st.title("2 · Tanım, ilkeler ve mevzuat")
    kutu("<b>Organik hayvansal üretim:</b> Sentetik olarak üretilen maddelerin doğrudan ya da dolaylı olarak "
         "<b>kullanılmadığı</b> (kullanımı zorunluysa en az düzeyde kullanıldığı), <b>organik yemle</b> besleme ve "
         "sağlıklı hayvan yetiştiriciliği ilkesiyle, <b>hayvan refahı gözetilerek</b>, her aşaması <b>kontrollü ve "
         "sertifikalı</b> yapılan hayvansal üretimdir.")
    st.header("Kapalı çiftlik döngüsü")
    sec = st.radio("Döngüde bir halkaya bakın", ["Toprak", "Yem bitkileri, mera", "Hayvanlar", "Gübre"], horizontal=True,
                   key="dongu_sec")
    i = ["Toprak", "Yem bitkileri, mera", "Hayvanlar", "Gübre"].index(sec)
    svg_goster(svg_kapali_sistem(i))
    st.markdown({0: "Toprak verimliliği organik gübre ve ekim nöbetiyle korunur; kimyasal gübre kullanılmaz.",
                 1: "Yem çoğunlukla çiftlikte üretilir. Yem bitkilerinde kimyasal gübre ve pestisit kullanılmaz.",
                 2: "Hayvanlar sistemin canlı ve duyarlı parçasıdır; refahları ve doğal davranışları gözetilir.",
                 3: "Gübre tarlaya döner. Hayvan sayısı, gübreyle verilen azot 170 kg N/ha/yılı aşmayacak şekilde sınırlanır."}[i])
    st.header("Temel ilkeler")
    kartlar([("Sentetik girdi yok", "Sentetik ilaç, hormon, büyütme maddesi, kimyasal gübre kullanılmaz."),
             ("GDO yok", "Ne hayvanda, ne yemde, ne katkıda."),
             ("Doğal üreme", "Doğal aşım esas; embriyo transferi ve hormonla kızgınlık eşzamanlama yok."),
             ("Bedene müdahale yok", "Gaga kesimi, boynuz köreltme, kuyruk kesme gibi işlemler rutin olarak yapılmaz."),
             ("Kendi yemi", "Üretici yeminin çoğunu kendisi üretir."),
             ("Primum non nocere", "'Önce zarar verme': hayvanı hasta etmemek, acı çektirmemek.")])
    st.header("Mevzuat")
    st.markdown("""
| Düzey | Düzenleme |
|---|---|
| Türkiye | **5262 sayılı Organik Tarım Kanunu** (RG 03.12.2004, sayı 25659) |
| Türkiye | **Organik Tarımın Esasları ve Uygulanmasına İlişkin Yönetmelik** (RG 18.08.2010, sayı 27676) ve değişiklikleri (ör. 2013, 10 Ocak 2018) |
| Avrupa Birliği | 834/2007 ve 889/2008 tüzükleri; 1 Ocak 2022'den beri yerini **2018/848** sayılı tüzük aldı |
| ABD | National Organic Program (NOP) ve izinli/yasak maddeler "National List" |
""")
    st.markdown("Yönetmelik organik hayvancılığı şu başlıklarda düzenler: **hayvan kaynağı · barınma · açık havaya "
                "erişim · hayvan refahı · besleme · hastalıkların önlenmesi ve veteriner tedavisi**.")
    with st.expander("🇺🇸 ABD (NOP) mantığı: izinli ve yasak maddeler"):
        st.markdown("""
- **Doğal** madde: özellikle yasaklanmadıkça **izinli**
- **Sentetik** madde: özellikle izin verilmedikçe **yasak**
- Kesin yasaklar: **genetik değişiklik / klonlama, iyonlaştırıcı radyasyon, arıtma çamuru**
- Organik hayvan için mera ve açık alan sertifikalı olmalı; arazide **son 3 yılda** yasaklı madde kullanılmamış olmalı.
- Yeni ürünler kullanılmadan önce onaylanmalı.""")
    st.header("🎮 Organik mi, değil mi?")
    st.markdown("**Doğal, kafessiz, köy, özgür, gezen** gibi ifadeler **sertifika olmadıkça organik ürün anlamına gelmez.**")
    _mini_oyun("orgmi", ORGANIK_MI, ["Organik", "Organik değil"], "Bu ürün organik diye satılabilir mi?")
    alistirma_blogu("tanim", "Tanım, ilkeler ve mevzuat", gen_tanim)


# ---------------------------------------------------------------------------
def sayfa_kaynak():
    st.title("3 · Hayvan kaynağı ve üreme")
    st.header("Irk seçimi")
    st.markdown("Organik hayvancılıkta **çevre koşullarına uyumu yüksek ve hastalıklara dayanıklı** ırklar seçilir. "
                "Bunun için o bölgeye **adapte olmuş yerli ırklar ve melezleri** önceliklidir.")
    kartlar([("Yerel koşullara uyum", "İklim, mera ve yem kaynağına uyum"), ("Yaşama gücü (dirilik)", "Yavru kaybı az, uzun ömür"),
             ("Hastalığa dayanıklılık", "İlaç gereksinimi düşük"),
             ("Kaçınılacaklar", "Belirli hastalıklara yatkın ya da sağlık sorunu olan ırk ve hatlar")])
    ipucu("Neden yerli ırk? Yüksek verimli kültür ırkları çoğu zaman yoğun yem, kapalı barınak ve sık ilaç ister; "
          "organik sistemin kısıtları altında sağlıklı kalmaları zordur. Yerli ırkın verimi düşük olabilir; bu bir "
          "<b>ödünleşimdir</b>.")
    st.header("Üreme")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**✅ İzinli**")
        st.markdown("- **Doğal aşım** (esas yöntem)\n- Damızlıklardan **doğal yöntemlerle** alınmış, saklanmış "
                    "spermayla **suni tohumlama**")
    with c2:
        st.markdown("**❌ Yasak**")
        st.markdown("- **Embriyo transferi**\n- Kızgınlığı uyarmak ya da **eşzamanlamak için hormon**\n"
                    "- Klonlama ve genetik değişiklik")
    st.markdown("Organik hayvanlar, organik üretimde yasaklanmış madde ve uygulamaları alan hayvanlardan **uzak** tutulur.")
    st.header("🧮 Konvansiyonel işletmeden hayvan alırken yaş denetimi")
    st.markdown("Yeterli organik hayvan bulunamazsa kontrol/sertifikasyon kuruluşunun izniyle, sürüyü kurmak ya da "
                "yenilemek için konvansiyonel hayvan alınabilir. Yavrular **sütten kesilir kesilmez** organik kurallara "
                "göre yetiştirilir ve alındıklarında belirli yaştan küçük olmalıdır:")
    tur = st.selectbox("Hayvan", list(ALIM_YAS), key="alim_tur")
    birim, sinir, kural = ALIM_YAS[tur]
    yas = st.number_input(f"Hayvanın yaşı ({birim})", 0, 400, 2 if birim == "gün" and sinir == 3 else 40, key="alim_yas")
    uygun = yas < sinir if tur == "Buzağı / tay" else yas <= sinir
    if uygun:
        st.success(f"✅ Uygun: kural '{kural}'. Hayvan sütten kesilir kesilmez organik kurallara göre yetiştirilir; "
                   "ürünü için geçiş süresi yine uygulanır.")
    else:
        st.error(f"❌ Uygun değil: kural '{kural}'.")
    tablo(pd.DataFrame([{"Hayvan": k, "Kural": v[2]} for k, v in ALIM_YAS.items()]))
    alistirma_blogu("kaynak", "Hayvan kaynağı ve üreme", gen_kaynak)


# ---------------------------------------------------------------------------
def sayfa_barinma():
    st.title("4 · Barınma ve açık alan")
    st.markdown("""
- Yalıtım, ısıtma ve havalandırma; hava akımı, **toz, sıcaklık, nem ve gaz** düzeyini hayvana zarar vermeyecek
  sınırlarda tutmalı.
- Barınak **bol doğal ışık ve doğal havalandırma** almalı.
- Hayvanlar **çayır, mera ve açık alanlara** rahatça ulaşabilmeli. Açık havada yaşanabilen iklimlerde kapalı
  barınak şart değildir; ama **açık alana erişim zorunludur**.
- Doğal davranışlara, egzersize ve güvenli dinlenmeye yetecek **alan** sağlanmalı.""")
    kartlar([("Ayrı birim", "Konvansiyonel hayvanlar aynı işletmede olabilir; barınak ve arazileri açıkça ayrı ve türleri farklı olmalı."),
             ("Ortak otlatma", "Organik ve konvansiyonel hayvanlar aynı merayı kullanabilir, ama aynı anda değil."),
             ("Açık alan", "Gezinti alanı, egzersiz alanı ya da mera: koşullar elverdikçe en az biri kullanılır.")])
    st.header("🧮 Alan hesaplayıcı")
    st.caption("Hayvan başına en az iç ve dış alan. Değerler AB 889/2008 Ek III'e göre öğretici özettir; "
               "Türkiye yönetmeliği AB ile uyumlu hazırlanmıştır. Kesin değerler için yürürlükteki yönetmeliğe bakın.")
    tur = st.selectbox("Hayvan", list(YOGUNLUK), key="alan_tur")
    ic_m, dis_m = YOGUNLUK[tur]
    c1, c2 = st.columns(2)
    ic = c1.number_input("Kapalı alan (m²)", 1.0, 5000.0, 120.0, 10.0, key="alan_ic")
    dis = c2.number_input("Açık alan (m²)", 0.0, 50000.0, 200.0, 10.0, key="alan_dis")
    n_ic = math.floor(ic / ic_m + 1e-9)
    n_dis = math.floor(dis / dis_m + 1e-9)
    n = min(n_ic, n_dis)
    ic_yazi = f"{1 / ic_m:.0f} hayvan/m²" if ic_m < 1 else f"{_v(ic_m)} m²/hayvan"
    st.markdown(f"**{tur}:** iç alan en az {ic_yazi}, dış alan en az {_v(dis_m)} m²/hayvan")
    c1, c2, c3 = st.columns(3)
    c1.metric("İç alana göre", f"{n_ic} baş")
    c2.metric("Dış alana göre", f"{n_dis} baş")
    c3.metric("Barındırılabilecek en çok", f"{n} baş")
    if n_ic != n_dis:
        st.info(f"Darboğaz: **{'iç' if n_ic < n_dis else 'dış'} alan**.")
    st.header("🐔 Konvansiyonel ve organik tavuk yoğunluğu")
    tt = st.radio("Üretim", list(TAVUK_KARS), horizontal=True, key="tavuk_kars")
    (b1, n1), (b2, n2) = TAVUK_KARS[tt].items()
    svg_goster(svg_yogunluk(n1, n2, b1, b2))
    st.caption("Organikte buna ek olarak tavuk başına yaklaşık 4 m² açık alan gerekir. Konvansiyonel değerler ders notundaki "
               "rakamlardır (460 cm²/tavuk ≈ 21,7 tavuk/m²).")
    st.header("🧮 170 kg N/ha sınırı: kaç hayvan?")
    st.markdown("Gübreyle bir hektara yılda verilen azot **170 kg**'ı aşamaz. Bu, hayvan sayısını dolaylı olarak sınırlar.")
    c1, c2, c3 = st.columns(3)
    at = c1.selectbox("Hayvan", list(AZOT_ESDEGER), key="azot_tur")
    say = c2.number_input("Hayvan sayısı", 1, 100000, 40, key="azot_say")
    ha = c3.number_input("Tarım alanı (ha)", 0.5, 10000.0, 15.0, 0.5, key="azot_ha")
    kg_bas = 170 / AZOT_ESDEGER[at]
    yuk = say * kg_bas / ha
    st.markdown(f"Bir {at.lower()} yılda yaklaşık **{_v(kg_bas)} kg N** gübre azotu üretir (170 ÷ {_v(AZOT_ESDEGER[at])}).")
    st.metric("Gübre azotu yükü", f"{_v(yuk)} kg N/ha/yıl", delta=f"{_v(yuk - 170)} sınıra göre", delta_color="inverse")
    st.markdown(f"Bu alanda en çok **{math.floor(AZOT_ESDEGER[at] * ha + 1e-9)} {at.lower()}** barındırılabilir.")
    _ = (st.success if yuk <= 170 else st.error)("✅ Sınırın içinde" if yuk <= 170 else "❌ Sınır aşılıyor: hayvan sayısı azaltılmalı ya da alan artırılmalı")
    st.caption("Hayvan/ha eşdeğerleri AB 889/2008 Ek IV'ten öğretici özettir.")
    alistirma_blogu("barinma", "Barınma ve açık alan", gen_barinma)


def _v(x):
    return _tr(x, 2)


import calendar as _takvim


def _ay_ekle(d, n):
    y = d.year + (d.month - 1 + n) // 12
    m = (d.month - 1 + n) % 12 + 1
    return d.replace(year=y, month=m, day=min(d.day, _takvim.monthrange(y, m)[1]))


def _tarih(d):
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    return f"{d.day} {aylar[d.month - 1]} {d.year}"


def sayfa_besleme():
    st.title("5 · Besleme")
    st.header("Su")
    st.markdown("İçme suyu hijyen bakımından **insan içme suyu** niteliklerine sahip olmalı; özellikle **nitrat** "
                "içeriğine dikkat edilir. Hayvanlar **istedikleri zaman, istedikleri kadar** su içebilmelidir.")
    st.header("Yavruların beslenmesi")
    st.markdown("""
1. **Ağız sütü (kolostrum):** bağışıklık sistemini güçlendirmek için ilk iş.
2. **Ana sütü**, yoksa aynı sürüden elde edilen süt, rumen gelişip yavru yeterince yem tüketene kadar.
3. **2. haftadan itibaren** önüne iyi kaliteli organik kuru ot ve yoğun yem konur; yeme alışır.
4. Sütten kesildikten sonra gereksinimini karşılayan **organik kaba ve yoğun yem**.""")
    fig = go.Figure(go.Bar(x=list(SUT_SURE), y=list(SUT_SURE.values()), marker_color=[KAHVE, TURUNCU, PEMBE],
                           text=[f"{v} gün" for v in SUT_SURE.values()], textposition="outside"))
    fig.update_layout(title="Sütle beslenmenin asgari süresi", yaxis_title="Gün", yaxis_range=[0, 105])
    ciz(fig, 340)
    uyari("Ders notunda bir slaytta 'kuzu ve oğlak için <b>en az 2 ay</b>' yazıyor; diğer slaytlarda ve mevzuatta asgari süre "
          "<b>45 gündür</b>. Daha uzun süre emzirmek elbette serbesttir; 45 gün yasal alt sınırdır.")
    st.subheader("🧮 En erken sütten kesme tarihi")
    c1, c2 = st.columns(2)
    yt = c1.selectbox("Yavru", list(SUT_SURE), key="sut_tur")
    dg = c2.date_input("Doğum tarihi", _dt.date(2026, 3, 1), key="sut_dogum")
    st.markdown(f"Sütle beslenme en az **{SUT_SURE[yt]} gün** → en erken sütten kesme: **{_tarih(dg + _dt.timedelta(days=SUT_SURE[yt]))}**")

    st.header("Yemleme biçimi: neden ad libitum?")
    st.markdown("Yemleme süresi kısa olursa ve yem sırayla verilirse **güçlü hayvanlar önce yemek ister**, zayıflarla "
                "dövüşür; iki taraf da strese girer, yaralanır. Bu yüzden büyükbaş ve küçükbaşlara da tavuklardaki gibi "
                "**istedikleri zaman yiyebilecekleri (ad libitum)** bir düzen sağlanır. **Zorla besleme** ve hayvanı "
                "**kansızlığa (anemi)** sürükleyecek rasyon yasaktır.")
    st.header("Yemde neler olmaz, neler olur?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**❌ Olmaz**")
        st.markdown("""
- Kimyasal gübre, pestisit, herbisitle yetişmiş yem
- Hayvansal yağ ve yan ürün
- Yumurta sayısını artıran, sarıyı koyulaştıran sentetik maddeler, doğal olmayan mineraller
- GDO'lu bitki ve yan ürünleri
- **Kimyasal solventle** işlenmiş küspe
- Antibiyotik, koksidiyostat, büyüme ya da verim artırıcı""")
    with c2:
        st.markdown("**✅ Olur**")
        st.markdown("""
- Makro ve mikro mineraller
- **Doğal kaynaklı** vitaminler
- Probiyotik, enzim, organik asit
- Tahıl kırıntısı, melas, tuz
- Silajda yalnız izin verilen fermantasyon yardımcıları
- Kanatlı ve domuzda günlük rasyona **kaba yem** (kuru ot, silaj)""")
    st.caption("Katkılar veteriner hekim ve ziraat mühendisi kontrolünde eklenir; kalıntı analizleri yapılıp kayda geçer.")
    st.subheader("🎮 İzinli mi, yasak mı?")
    _mini_oyun("izin", IZIN_YASAK, ["İzinli", "Yasak"], "Organik hayvancılıkta bu madde ya da uygulama...")

    st.header("🧮 Rasyon denetleyici")
    grup = st.radio("Hayvan grubu", ["Otçul (sığır, koyun, keçi)", "Domuz ve kanatlı"], horizontal=True, key="ras_grup")
    otcul = grup.startswith("Otçul")
    c1, c2 = st.columns(2)
    ciftlik = c1.slider("Çiftlikten (ya da aynı bölgeden) gelen yem, % KM", 0, 100, 55 if otcul else 25, key="ras_ciftlik")
    gecis = c2.slider("Geçiş dönemi yemi, % KM", 0, 100, 20, key="ras_gecis")
    kendi = c2.checkbox("Geçiş dönemi yemi kendi çiftliğimden", key="ras_kendi")
    if otcul:
        kaba = c1.slider("Kaba yem payı (günlük rasyon), % KM", 0, 100, 55, key="ras_kaba")
        erken = c1.checkbox("Süt hayvanı, laktasyonun ilk 3 ayı", key="ras_erken")
        mera = c2.slider("Organik olmayan merada otlama (yıllık rasyonun %)", 0, 30, 5, key="ras_mera")
    gdo = st.checkbox("Rasyonda GDO'lu madde var", key="ras_gdo")
    sonuc = []
    alt = 60 if otcul else 20
    sonuc.append((ciftlik >= alt, f"Çiftlikten gelen yem ≥ %{alt}", f"%{ciftlik}"))
    gsin = 100 if kendi else 30
    sonuc.append((gecis <= gsin, f"Geçiş dönemi yemi ≤ %{gsin}", f"%{gecis}"))
    if otcul:
        ksin = 50 if erken else 60
        sonuc.append((kaba >= ksin, f"Kaba yem ≥ %{ksin}", f"%{kaba}"))
        sonuc.append((mera <= 10, "Organik olmayan merada otlama ≤ %10", f"%{mera}"))
    sonuc.append((not gdo, "GDO yok", "var" if gdo else "yok"))
    tablo(pd.DataFrame([{"Kural": k, "Sizin rasyon": d, "Durum": "✅" if ok else "❌"} for ok, k, d in sonuc]))
    if all(ok for ok, _, _ in sonuc):
        st.success("✅ Rasyon bu öğretici kurallara uyuyor.")
    else:
        st.error("❌ En az bir kural sağlanmıyor.")
    with st.expander("Bu sınırlar nereden geliyor? (dürüst not)"):
        st.markdown("""
- **Çiftlikten gelen yem:** Ders notunun bir slaytında otçullar için **%50**, diğerinde **%60** yazıyor. Türkiye
  yönetmeliğinin 2013 değişikliği otçullarda **en az %60**, domuz ve kanatlıda **en az %20** der. AB'nin yeni
  2018/848 tüzüğü bu oranları otçulda %70, domuz-kanatlıda %30'a çıkarmıştır.
- **Kaba yem:** Notta 'süt üretiminde laktasyon başında 3 ay %50'ye indirme' istisnası çiftlikten gelen yem kuralının
  altında verilmiş. Bu istisna aslında **günlük rasyondaki kaba yem payı** kuralına aittir (otçulda en az %60 kaba yem,
  laktasyonun başında en çok 3 ay %50).
- **Geçiş dönemi yemi:** Notta '%30–60' yazıyor. AB kuralında üst sınır ortalama **%30**'dur; yem işletmenin kendi
  geçiş arazisinden geliyorsa **%100**'e kadar çıkabilir.
- **Organik olmayan merada otlama** (yaylacılık sırasında): yıllık rasyonun **%10**'unu geçemez.

Kesin sayılar için yürürlükteki yönetmelik metnine bakılmalıdır.""")
    alistirma_blogu("besleme", "Besleme", gen_besleme)


# ---------------------------------------------------------------------------
def sayfa_gecis():
    st.title("6 · Geçiş süreleri")
    st.markdown("Konvansiyonelden organiğe geçen bir hayvanın ürünü, **geçiş süresi** dolmadan organik diye satılamaz. "
                "Geçiş dönemindeki hayvansal ürünler 'organik' olarak pazarlanamaz.")
    sec = st.radio("Bir satırı vurgulayın", [g[0] for g in GECIS], horizontal=True, key="gecis_vurgu")
    svg_goster(svg_gecis([g[0] for g in GECIS].index(sec)))
    kartlar([("Süt sürüsünden ete ayrılan", "Organik süt işletmesinden et için ayrılan hayvanda geçiş, yaşam süresinin 3/4'ü."),
             ("Etlik kanatlı", "Geldiği çiftlikten ayrılırken 3 günlükten büyük olamaz; 10 hafta geçiş."),
             ("Buzağı, tay", "Alındığında 6 aylıktan küçük; sütten kesilir kesilmez organik kurallar."),
             ("Kuzu, oğlak", "Alındığında 60 günden büyük olmamalı.")])
    st.header("🧮 Organik satış tarihi hesaplayıcı")
    c1, c2 = st.columns(2)
    tur = c1.selectbox("Hayvan ve ürün", list(GECIS_TUR), key="gecis_tur")
    bas = c2.date_input("Organik yönetime başlama tarihi", _dt.date(2026, 1, 15), key="gecis_bas")
    birim, sure = GECIS_TUR[tur]
    bit = _ay_ekle(bas, sure) if birim == "ay" else bas + _dt.timedelta(weeks=sure)
    st.success(f"Geçiş süresi **{sure} {birim}** → ürün en erken **{_tarih(bit)}** tarihinden sonra organik satılabilir.")
    st.subheader("🧮 Ömrün 3/4'ü kuralı")
    omur = st.slider("Hayvanın toplam yaşam süresi (ay)", 6, 120, 24, key="gecis_omur")
    st.markdown(f"Organik süt işletmesinden et için ayrılan bu hayvanın geçiş süresi: 3/4 × {omur} = **{_v(omur * 0.75)} ay**")
    st.header("Arazi ve otlaklar")
    st.markdown("""
Hayvanın yanında yemini veren **arazinin** de geçişi vardır. Ders notundaki '24; 12; 6 ay' ifadesi şöyle açılabilir
(AB kuralına göre öğretici özet):
- **24 ay:** yem bitkisi tarlası ve çayır, ürünü organik yem sayılmadan önce
- **12 ay:** otçul olmayan hayvanların (domuz, kanatlı) kullandığı mera ve açık alanlar
- **6 ay:** bu alanlarda yakın zamanda yasaklı madde kullanılmadığı belgelenirse 12 ay 6 aya inebilir

ABD (NOP) kuralı ise arazide **son 3 yılda** yasaklı madde kullanılmamış olmasını ister.""")
    alistirma_blogu("gecis", "Geçiş süreleri", gen_gecis)


# ---------------------------------------------------------------------------
def sayfa_saglik():
    st.title("7 · Hayvan sağlığı ve veteriner tedavi")
    st.markdown("İyi barınak sağlandıktan sonra önemli olan, **hayvan etiğini gözeten dikkatli bakım**dır. Öncelik "
                "**hastalığı önlemek**tir: koruyucu tedbirler ve koruyucu hekimlik.")
    kartlar([("Irk ve yetiştirme", "Dayanıklı ırk, uygun yoğunluk, açık alan, iyi yem"),
             ("Hijyen", "Barınak ve ekipman temizliği, dezenfeksiyon; idrar, gübre, artık yem düzenli uzaklaştırılır"),
             ("Aşı", "Veteriner hekim önerisiyle aşı ve hijyen tedbirleri"),
             ("Hızlı müdahale", "Hasta ya da yaralı hayvan hemen tedavi edilir")])
    st.header("Yapılmayan işlemler")
    svg_goster(svg_yasak_islem())
    st.markdown("Koruyucu amaçla **kimyasal sentezlenmiş ilaç ve antibiyotik**, büyüme ya da verim artırıcı maddeler "
                "(antibiyotik, koksidiyostat), üremeyi kontrol etmek, kızgınlığı uyarmak ya da eşzamanlamak için "
                "**hormon** kullanılmaz.")
    st.header("Tedavi akışı")
    adim = st.select_slider("Adım", ["1 · Koruma", "2 · Alternatif tedavi", "3 · Kimyasal ilaç", "4 · Sayıyı say", "5 · Sınır aşıldı"],
                            key="tedavi_adim")
    svg_goster(svg_tedavi_akis(int(adim[0]) - 1))
    with st.expander("🔬 Bilimsel dürüstlük notu: homeopati"):
        st.markdown("Mevzuat fitoterapi ve homeopatiye **öncelik** verir. Ancak homeopatinin hayvanlarda (ve insanlarda) "
                    "plasebodan üstün etkisi bilimsel çalışmalarda **gösterilememiştir**. Bu yüzden alternatif tedavi "
                    "hayvanın acı çekmesine yol açacak kadar uzatılmamalı; yetersiz kalınca veteriner hekim kontrolünde "
                    "ilaç kullanılmalıdır. Mevzuat da bunu ister: hayvanın acı çekmemesi önceliklidir.")
    st.header("🧮 Kür sayacı")
    c1, c2 = st.columns(2)
    kimya = c1.number_input("Son 12 ayda kimyasal ilaç / antibiyotik kürü", 0, 20, 2, key="kur_kimya")
    asi = c2.number_input("Aşı, parazit tedavisi, zorunlu program uygulaması", 0, 20, 3, key="kur_asi")
    kisa = st.checkbox("Hayvanın verimli ömrü 1 yıldan kısa (ör. etlik piliç, besi kuzusu)", key="kur_kisa")
    sinir = 1 if kisa else 3
    st.markdown(f"Sınır: **{sinir}** kür. Aşı, parazit tedavisi ve zorunlu programlar ({asi}) **sayılmaz**.")
    if kimya > sinir:
        st.error(f"❌ {kimya} > {sinir}: hayvan ve ürünleri organik satılamaz, hayvan **yeniden geçiş sürecine** alınır.")
    else:
        st.success(f"✅ {kimya} ≤ {sinir}: bekleme süresi dolunca ürün organik satılabilir. Kayıt şart.")
    st.header("🧮 Organik bekleme süresi")
    c1, c2 = st.columns(2)
    yasal = c1.number_input("İlacın yasal bekleme süresi", 0.0, 400.0, 3.0, 0.5, key="bek_sure")
    birim = c2.radio("Birim", ["gün", "saat"], horizontal=True, key="bek_birim")
    saat = yasal * (24 if birim == "gün" else 1)
    org = max(2 * saat, 48)
    st.markdown(f"Organikte bekleme süresi yasal sürenin **iki katı**, yasal süre yazmıyorsa ya da daha kısaysa "
                f"**en az 48 saat**: 2 × {_v(saat)} saat = {_v(2 * saat)} saat → **{_v(org)} saat ({_v(org / 24)} gün)**")
    alistirma_blogu("saglik", "Hayvan sağlığı ve tedavi", gen_saglik)


# ---------------------------------------------------------------------------
KARAR = ["Çiftliğim organik hayvancılığa ne kadar uygun?", "Faaliyet için yeterli alanım var mı?",
         "Yeterli yem ya da yan ürün var mı?", "Bilgi birikimim var mı?", "Hayvanlar çiftliğime ne kadar fayda sağlayacak?",
         "Gübreyi uygun şekilde kullanabilir miyim?", "Kendi tüketim ya da satış ürünlerim neler?",
         "Hayvanlar bitkisel ürünlerimi nasıl etkiler?", "Yeterli iş gücü var mı?", "Uygun ırk hayvanları alabilir miyim?",
         "Ürünlerim için pazar bulabilir miyim?", "Fiyat bu çabaya değer mi?", "Diğer üreticilerle rekabet edebilir miyim?",
         "Verimliliğimi nasıl en üst düzeye çıkarırım?"]


def sayfa_tasima():
    st.title("8 · Taşıma, kesim, kayıt ve karar verme")
    st.header("Taşıma")
    st.markdown("Taşıma **en az stres** yaratacak ve **en kısa sürede** bitecek biçimde yapılır. Nakilde **sakinleştirici "
                "kullanılmaz**. Kara taşımacılığında **8 saatte bir** yemleme, sulama ve dinlenme molası verilir.")
    sure = st.slider("Yolculuk süresi (saat)", 1, 30, 11, key="yol_sure")
    mola = max(0, math.ceil(sure / 8) - 1)
    st.markdown(f"{sure} saatlik yolculukta en az **{mola} mola** gerekir" +
                (f" (≈ {', '.join(str(8 * (k + 1)) + '. saat' for k in range(mola))})." if mola else "."))
    st.header("Kesim")
    st.markdown("Organik ve konvansiyonel hayvanlar mümkünse **ayrı kesimhanelerde**, değilse aynı kesimhanede **farklı "
                "zamanlarda** kesilir. Kesimde hayvana stres yaratmayacak davranış ve uygun kesim yöntemi kullanılır. "
                "Davranış notu, piliçlerin çırpınıp kemik kırılması ve göğüs ezilmesini önlemek için **elektrikle "
                "bayıltılarak** kesilmesini önerir.")
    st.header("Kayıt ve sertifika")
    kutu("Organik tarım <b>sertifikalı, kontrollü, kurallı</b> bir üretim sistemidir. <b>Kayıt tutmak çok önemlidir.</b>")
    kartlar([("Hayvan", "Doğum, alım (nereden, kaç yaşında), satış, ölüm"), ("Yem", "Kaynağı, miktarı, organik belgesi, katkılar"),
             ("Sağlık", "Tanı, ilaç, doz, tarih, bekleme süresi, kür sayısı"), ("Hareket", "Mera, açık alan kullanımı, taşıma")])
    uyari("<b>DOĞAL · KAFESSİZ · KÖY · ÖZGÜR · GEZEN</b> yazan ürün, sertifikası olmadığı sürece organik tarım ürünü değildir.")
    st.header("🧭 Organik hayvancılık bana uygun mu?")
    st.caption("Karar vermeden önce kendinize sorun. 'Evet' diyebildiklerinizi işaretleyin.")
    evet = sum(st.checkbox(k, key=f"karar_{i}") for i, k in enumerate(KARAR))
    st.progress(evet / len(KARAR), text=f"{evet} / {len(KARAR)} soruya evet")
    if evet == len(KARAR):
        st.success("Hazırlıklı görünüyorsunuz. Bir sonraki adım: kontrol/sertifikasyon kuruluşuyla görüşmek.")
    elif evet >= len(KARAR) * 0.6:
        st.info("Temel hazır; işaretlemediğiniz konular için plan yapın.")
    else:
        st.warning("Henüz erken olabilir: alan, yem, iş gücü ve pazar sorularını netleştirin.")
    alistirma_blogu("tasima", "Taşıma, kesim, kayıt ve karar verme", gen_tasima)


AB_REFAH = [
    ("Bütün çiftlik hayvanları", "Avrupa Sözleşmesi (1976); 78/923/EEC; 98/58/EC; 2000/50/EC; 2006/778/EC"),
    ("Buzağılar", "91/629/EEC; 97/2/EC; 97/182/EC; 2008/119/EC"),
    ("Domuzlar", "91/630/EEC; 2001/88/EC; 2001/93/EC; 2008/120/EC"),
    ("Yumurta tavukları", "88/166/EEC (yürürlükte değil); 1999/74/EC; 2002/4/EC"),
    ("Etlik piliçler", "2007/43/EC"),
]


def sayfa_refah():
    st.title("9 · Hayvan refahı")
    st.markdown("""
Yetiştiricilikte amaç gelirdir: yüksek verimli hayvan, uygun çevre, uygun rasyon. Ama **entansif** sistemlerde
uygulanan bazı bakım kuralları (gaga kesimi, yumurta tavuklarının kafeste, damızlık domuzların gebelik boyunca
bireysel bölmede tutulması) **hijyen, ölüm oranı ve yem tüketimi** gibi gerekçelerle getirilmiş ama refahı
düşürmüştür. Refah sorunlarının çoğu **çevreyle** ilgilidir; davranış ihtiyacı karşılanmayınca **anormal
davranışlar** gelişir. Yönetim hataları da refahı bozar: ör. sığır ve koyunu uzun süre **çamurlu, ıslak zeminde**
tutmak ayak sorunlarına yol açar.""")
    st.header("Refah kavramı nasıl değişti?")
    c1, c2 = st.columns(2)
    c1.markdown("**1960–1970'ler**\n- Stres yok → refah iyi\n- Stres var → refah zayıf")
    c2.markdown("**Bugün**\n- Hayvanların **duyguları** vardır\n- Fiziksel sağlık kadar **ruhsal sağlık** da önemlidir")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ Refah iyi ise")
        st.markdown("- Çevresiyle uyum içinde\n- Uyum sağlarken ağrı, acı duymaz\n- Duygularını ifade edebilir\n- Doğal davranışlarını tam gösterir")
    with c2:
        st.subheader("⚠️ Refah zayıf ise")
        st.markdown("- Yaşam süresi kısalır\n- Büyüme, gelişme yetersiz\n- Yaralanma ve hastalık artar\n- Bağışıklık zayıflar\n"
                    "- Çevreye uyum sağlayamaz\n- Anormal davranış artar\n- Fizyolojik işlevler bozulur")
    st.header("Brambell Komitesi (1965)")
    st.markdown("İngiltere'de kurulan Brambell Komitesi, hayvanın en azından şunları **zorlanmadan** yapabilmesi "
                "gerektiğini söyledi: **dönebilme, kendini temizleyebilme (kaşınma), kalkabilme, yatabilme ve "
                "uzuvlarını gerebilme**. Bu ilk liste tamamen **hareket** özgürlüğüne odaklıdır.")
    st.header("Beş özgürlük")
    sec = st.radio("Bir özgürlük seçin", [o[0] for o in OZGURLUKLER], horizontal=True, key="ozg_sec")
    i = [o[0] for o in OZGURLUKLER].index(sec)
    svg_goster(svg_bes_ozgurluk(i))
    st.markdown(["Önlerinde yeterince **taze yem ve su** bulunmalı.",
                 "**Uygun barınak ve çevre** (dinlenme yeri, sıcaklık, zemin) sağlanmalı.",
                 "Çarpma, yaralanma ve hastalıktan **korunmalı**; olursa **hızla** tedavi edilmeli.",
                 "**Yeterli alan**, uygun araç-gereç ve **aynı türden** arkadaş sağlanmalı.",
                 "Korku ve strese yol açan olaylardan korunmalı; **ruhsal acıyı** önleyen koşullar sağlanmalı."][i])
    uyari("Ders notunda bu beş özgürlüğün 1993'te düzenlendiği yazıyor. Doğrusu: Çiftlik Hayvanları Refahı Konseyi (FAWC) "
          "<b>1979</b>'da kuruldu ve beş özgürlüğü ilk kez o yıl açıkladı; <b>1993</b>'te bugünkü biçimine getirildi.")
    st.subheader("🎮 Hangi özgürlük çiğneniyor?")
    _mini_oyun("ozg", [(m, OZGURLUKLER[k][0]) for m, k in OZGURLUK_DURUM], [o[0] for o in OZGURLUKLER],
               "Bu durumda hangi özgürlük ihlal ediliyor?")
    st.header("AB'de çiftlik hayvanı refahı mevzuatı")
    tablo(pd.DataFrame(AB_REFAH, columns=["Kapsam", "Düzenleme"]))
    with st.expander("98/58/EC: bütün çiftlik hayvanları için en düşük standartlar"):
        st.markdown("""
- Bakım **bilgili personel** tarafından yapılır.
- Hayvanlar **günde en az 1 kez** kontrol edilir; hasta ve yaralılara uygun bakım.
- Ölümler ve tedaviler **kayda geçer, 3 yıl saklanır**.
- Hareket özgürlüğü kısıtlanmaz; barınakta keskin kenar olmaz; havalandırma, sıcaklık, nem uygun; hayvan **sürekli karanlıkta** tutulmaz.
- Dışarıdaki hayvanlar kötü hava ve yırtıcılardan korunur; ekipman kontrol edilir; uygun yem ve su.""")
    with st.expander("Buzağılar (91/629 → 2008/119/EC)"):
        st.markdown("""
- Ekipman zararsız, kolay temizlenir ve dezenfekte edilir; elektrik tesisatı yalıtılır; ekipman **her gün** kontrol edilir.
- Mekanik havalandırmada arıza **alarmı** bulunur.
- Sürekli karanlıkta tutulmaz; yapay ışık en az **09.00–17.00** arasındaki doğal ışık süresine denk olmalı.
- İçerideki buzağılar **günde en az 2**, dışarıdakiler **en az 1** kez kontrol edilir.
- Rahatça yatıp kalkabileceği alan; **bağlanmaz**; zemin düz ama kaygan değil, altlıklı.
- **Günde en az 2 kez** yemlenir; doğumdan sonra **en kısa sürede kolostrum** alır.""")
    ipucu("Organik hayvancılık, refah için yasal en düşük standartların <b>üstüne</b> çıkar: açık alana erişim, daha geniş "
          "alan, bedene müdahale yasağı, ad libitum yemleme, sakinleştiricisiz taşıma.")
    alistirma_blogu("refah", "Hayvan refahı", gen_refah)


# ---------------------------------------------------------------------------
DUYU = [("Dokunma", "Ana-yavru tanıma ve hoşgörü, emme, çiftleşme, dinlenme, yalama"),
        ("Koklama", "Çiftleşme (feromon, kızgın dişinin kokusu), ana-yavru ilişkisi, beslenme"),
        ("Görme", "Çevre, sürü arkadaşı, yem, bakıcı, düşman tanıma; fotoperiyot ile çiftleşme düzeni"),
        ("İşitme", "Sosyal ve cinsel davranış, ana-yavru bağı; bazı sesler sakinleştirir, bazıları paniğe yol açar"),
        ("Tat alma", "Yem tercihi, seçici otlama, yavruyu tanıma")]


def sayfa_etholoji():
    st.title("10 · Etholoji ve davranışın temelleri")
    st.markdown("Hayvanlar onları yetiştiren insanlardan etkilenmiş ve onları etkilemiştir. Geçen yüzyılda hayvancılık "
                "çok yoğunlaştı: **çok hayvan, dar alan**. Kritik nokta, hayvanın buna **fizyolojik ve davranışsal** olarak "
                "uyum sağlayıp sağlayamadığıdır. Sorunların çoğuna davranış çalışmaları çözüm getirir.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Kim bilmeli?")
        st.markdown("Yetiştiriciler, bakıcılar, çiftlik yöneticileri, hayvan taşımacıları, barınak planlayıcıları, "
                    "ekipman tasarımcıları, zootekniştler, veteriner hekimler")
    with c2:
        st.subheader("Neden bilmeli?")
        st.markdown("Etkin yemleme-otlatma · üreme denetimi · kayıpları azaltma · doğru gruplama · korku, kavga, yaralanmayı "
                    "önleme · performans ve yem değerlendirme · karkas kalitesi · tedavi masrafı · uygun barınak")
    st.header("Etholoji nedir?")
    st.markdown("""
- Önceleri **'karakter bilimi'** denirdi. **Niko Tinbergen** etholojiyi 'davranışla ilgili biyolojik çalışmalar'
  olarak tanımladı.
- **Davranış:** hayvan ya da hayvan topluluklarının kolayca gözlenen ama çok karmaşık işlevleri.
- **Charles Darwin**'in *Türlerin Kökeni* ve *İnsan ve Hayvanlarda Duyguların İfadesi* eserleri etholojiye büyük katkı yaptı.
- **Konrad Lorenz, Niko Tinbergen ve Karl von Frisch** 1973'te Nobel Fizyoloji veya Tıp Ödülü'nü aldı; etholoji
  bilim dalı olarak tescillendi.""")
    uyari("Ders notunda Nobel yılı <b>1972</b> yazıyor; doğrusu <b>1973</b>. Ayrıca 'Charles Darvin' yazımı 'Darwin' olmalı.")
    st.header("Davranışın kökenleri")
    svg_goster(svg_koken())
    kutu("<b>Yer değiştirme (displacement) aktivitesi:</b> İki zıt güdüye (ör. saldırma ve kaçma) aynı anda yeterli şiddette ve "
         "sürede maruz kalan hayvanın, bu güdülerle ilgisiz bir davranış göstermesi (ör. kavga ortasında otlamaya başlamak).")
    st.header("Duyular")
    d = st.radio("Duyu", [x for x, _ in DUYU], horizontal=True, key="duyu_sec")
    st.info(dict(DUYU)[d])
    st.header("Sinir sistemi")
    st.markdown("""
- Uyarımlar sinirlerle **beyne** gider; beyin yorumlar ve tepki komutunu organlara iletir.
- **Dış alıcılar (eksteroseptör):** duyu organlarında; dış ortam uyarılarını alır.
- **İç alıcılar (interoseptör):** kas, tendon ve iç organlarda; vücuttaki uyarıları alır.
- **Serebral korteks:** beynin dış tabakası; vücut duyusu, görme, işitme ve koku alma merkezleri.
- **Hipotalamus:** beynin tabanında; sinirsel etkileri toplar, çoğu işi hipofizi yönetmektir. Emme ve çiftleşme gibi
  uyarılar, üreme ve süt indirme hormonlarını artırır.""")
    st.header("Endokrin sistem ve davranış")
    hs = st.radio("Hedef organ", ["Yumurtalık", "Testis", "Tiroid", "Adrenal", "Meme"], horizontal=True, key="hormon_sec")
    hi = ["Yumurtalık", "Testis", "Tiroid", "Adrenal", "Meme"].index(hs)
    svg_goster(svg_hormon(hi))
    st.markdown(["**Östrojen** olgunlaşan folliküllerden salgılanır; düzeyi en yüksek olduğunda **kızgınlık davranışı** görülür. "
                 "Ön hipofizden **FSH ve LH** üreme davranışını yönetir.",
                 "**Testosteron** tipik erkek davranışlarını oluşturur. Belli bir düzey yeterlidir; fazlası cinsel davranışı artırmaz.",
                 "TSH'nin etkisiyle **T4 ve T3** salgılanır; T4 enerji üretimini ve ilgili davranışları denetler, analık içgüdüsü, "
                 "dişi cinsel döngüsü ve cinsel güdü için de önemlidir.",
                 "Adrenal korteks steroidleri cinsel davranışı destekler. Adrenal öz (medulla) **adrenalin** salgılar: tehlikede "
                 "**kaçma ya da saldırma**.",
                 "**Prolaktin (LTH)** süt **sentezini** sağlar ve analık içgüdüsüyle ilişkilidir. **Oksitosin** (arka hipofiz) "
                 "sütün **indirilmesini** (salıverilmesini) ve rahim kasılmalarını sağlar."][hi])
    if hi == 4:
        uyari("Ders notunda 'prolaktin sütün salıverilmesini sağlar' yazıyor. Doğrusu: prolaktin süt <b>yapımını</b>, oksitosin "
              "süt <b>indirmeyi</b> sağlar.")
    st.markdown("**Epifiz** beynin derininde yer alır, **melatonin** salgılar. Melatonin gün uzunluğuna göre salgılanır ve "
                "**mevsimsel üremeyi** düzenler. Koyun ve keçi gibi **kısa gün** üreyenlerinde günler kısalınca artan melatonin "
                "kızgınlığı başlatır; at gibi **uzun gün** üreyenlerinde ise etki terstir.")
    alistirma_blogu("etholoji", "Etholoji ve davranışın temelleri", gen_etholoji)


# ---------------------------------------------------------------------------
def sayfa_cevre():
    st.title("11 · Barınak çevresi")
    st.markdown("**Barınak:** hayvanın sağlıklı yaşaması, beden işlevlerini dengede tutması, düşman ve hastalık "
                "etkenlerinden korunması için içinde yaşadığı sistem. Barınak içi koşullar **refah, sağlık ve verimi** "
                "doğrudan etkiler.")
    st.caption("Bu bölümdeki notların bir kısmı deney (laboratuvar) hayvanları için yazılmıştır; ilkeler çiftlik hayvanları için de geçerlidir.")
    f = st.radio("Faktör", BARINAK_FAKTOR, horizontal=True, key="faktor_sec")
    fi = BARINAK_FAKTOR.index(f)
    svg_goster(svg_barinak(fi))
    if fi == 0:
        st.markdown("Hayvan doğal davranışlarının tümünü rahatça yapabilmeli. Barınak kurulurken **hayvan başına birim alan** "
                    "hesaba katılır. Dar alan → hareketsizlik, **oburluk, aşırı yağlanma**.")
    elif fi == 1:
        st.markdown("İç sıcaklık ayarlanırken hayvanın **beden sıcaklığı** ve **iriliği** dikkate alınır. Küçük hayvanda yüzey/ağırlık "
                    "oranı büyüktür → ısı kaybı hızlı → termoregülasyona daha çok enerji.")
        svg_goster(svg_yuzey_hacim())
    elif fi == 2:
        nem = st.slider("Bağıl nem (%)", 10, 100, 55, key="nem_sl")
        if nem > 60:
            st.error("Yüksek nem: amonyak artar, yem ve altlık ıslanıp küflenir, mikroorganizmalar çoğalır.")
        elif nem < 50:
            st.warning("Düşük nem: toz artar, solunum yolu tahriş olur.")
        else:
            st.success("%50–60: mikroorganizmaların üremesi sınırlanır, uygun aralık.")
        st.caption("Birçok laboratuvar hayvanı terleyemez; ısıyı solunum hızını artırarak atar. Bu yüzden nem önemlidir.")
    elif fi == 3:
        st.markdown("Hayvan ışığı çevreyi, diğer canlıları, yem ve suyu görmek ve **üreme ile günlük ritmi** düzenlemek için "
                    "kullanır. Aydınlatmada günlük aktivite dönemi, ışık kaynağı, şiddeti, rengi ve süresi düşünülür; bütün "
                    "hayvanlar eşit ışık almalıdır.")
        uyari("Ders notunda 'ışık kaynağı olarak genellikle <b>UV ışık kaynakları</b> kullanılır' yazıyor; bu yanlış. Aydınlatma "
              "floresan ya da LED (tercihen gün ışığına yakın tayf) ile yapılır. UV lambalar <b>dezenfeksiyon</b> içindir; "
              "uzun süre UV gözü ve deriyi zedeler.")
    elif fi == 4:
        st.markdown("Havalandırma: yeterli oksijen; koku, zehirli gaz, toz ve enfeksiyon etkenlerini uzaklaştırma; sıcaklık, nem "
                    "ve hava hareketinin kontrolü. Miktarı tür ve sayı, ısı yükü, yalıtım, hacim ve enerji kaynağı belirler.")
    elif fi == 5:
        db = st.slider("Gürültü düzeyi (dB)", 40, 120, 70, key="gur_db")
        if db >= 95:
            st.error("95 dB ve üstü işitme sistemine fiziksel zarar verir.")
        else:
            st.info("Tepki türe göre değişir. Sese duyarlı ve az duyarlı türler aynı binada tutulmamalı; gürültülü işler "
                    "hayvanlardan uzakta yapılmalı.")
    elif fi == 6:
        st.markdown("**Faydaları:** toplanma, oyun gibi sosyal davranışlar gelişir. **Zararları:** gruplaşma, saldırı, yaralama; "
                    "güçlüler zayıfların yem ve suyuna saldırır. Hayvanlar ne kadar **erken** birlikte yaşarsa o kadar dostça olur.")
    else:
        st.markdown("Sıcakkanlı hayvanlar doğumdan beri kendisiyle ilgilenen bakıcıyı tanır, ona saldırmaz; yabancılara saldırgan "
                    "olabilir. Kötü muamele ve uyumsuz bakıcı sonuçları bozar. Yavruların erken dönemde **elle tutulması** ergin "
                    "dönem fizyolojisi ve davranışını önemli ölçüde etkiler.")
    alistirma_blogu("cevre", "Barınak çevresi", gen_cevre)


# ---------------------------------------------------------------------------
KOYUN_KECI = [("Otlama", "Yerden", "Yüksekten (%65–70)"), ("Çalılık arazi", "Zor (yapağı takılır)", "Rahat (Ankara keçisi hariç)"),
              ("Sürü içgüdüsü", "Güçlü", "Daha zayıf"), ("Soğuk-yağışlı hava", "Dayanıklı", "Korunacak yer arar"),
              ("Hareketlilik", "Daha sakin", "Çevik, meraklı"), ("Tehdit karşısında", "Kaçar", "Döner, pozisyon alır"),
              ("Üstünlük yapısı", "Daha az belirgin", "Belirgin"), ("İnsana yakınlık", "Daha az", "Daha çok")]


def sayfa_tur():
    st.title("12 · Türlere göre davranış")
    t1, t2, t3, t4 = st.tabs(["🐄 Sığır", "🐑 Koyun", "🐐 Keçi", "🐔 Tavuk"])
    with t1:
        svg_goster(svg_otlama("Sığır"))
        st.markdown("""
- **Otlama:** otu fazla çiğnemeden yutar; seçicidir (belirli tür, gelişme dönemi, bitki kısmı). Gençler daha seçicidir.
- **Yem yeme:** dilini **kepçe** gibi kullanır.
- **Su içme:** ağzını suya batırıp emerek çeker; tüketim ırk, yaş, kuru madde, sıcaklık, protein, gebelik ve laktasyona bağlı.
- **Emme:** buzağı doğumdan **2–5 saat** içinde emmeye başlar; dil meme başını sarar, ağızda vakum oluşur.""")
        st.subheader("🧮 Geviş hesabı")
        ot = st.slider("Günlük otlama süresi (saat)", 4.0, 12.0, 8.0, 0.5, key="gevis_ot")
        st.markdown(f"Geviş süresi yaklaşık otlama süresinin %75'i: 0,75 × {_v(ot)} = **{_v(0.75 * ot)} saat** "
                    f"(normal aralık 4–9 saat; geviş/otlama oranı 0,5–1 → {_v(0.5 * ot)}–{_v(ot)} saat).")
        st.subheader("🧮 Tohumlama zamanı")
        st.markdown("Çiftleştirme ya da tohumlama **kızgınlık başlangıcından yaklaşık 12 saat sonra** yapılırsa gebelik olasılığı en yüksektir.")
        sa = st.slider("Kızgınlığın fark edildiği saat", 0, 23, 6, key="kizg_saat")
        hedef = (sa + 12) % 24
        st.success(f"Kızgınlık saat {sa:02d}:00'de başladıysa tohumlama için hedef saat ≈ **{hedef:02d}:00**"
                   f"{' (ertesi gün)' if sa + 12 >= 24 else ''}.")
        st.markdown("""
- **Boğa:** kızgın dişiyi kokuyla bulur; ön ayakla yeri eşeler, baş ve boynu yere sürer, dişiyi izler, vulvayı koklar-yalar,
  çenesini sağrısına dayar. Yılda **50–80 aşım**; sperma merkezlerinde **haftada bir** sağım. Stres çiftleşmeyi engelleyebilir.
- **İnek:** kızgınken aktif, uyarana duyarlı; diğer dişilere **atlar** ve atlanmaya izin verir, kaçmaz. **Sessiz kızgınlık** olabilir.
- **Sosyal yapı:** ticari sürülerde doğal **anaerkil** yapı oluşmaz. Tehdit: baş yere yakın, gözler rakipte, ön ayakla eşeleme;
  kavgada amaç rakibe yandan ya da arkadan toslamak. Eylemleri **lider** hayvanlar başlatır.
- Yeni grupta üstünlük sıralaması çoğunlukla **2 saat** içinde oluşur; kargaşa sürerse kavgacı hayvanlardan biri başka gruba alınır.""")
        svg_goster(svg_hiyerarsi())
    with t2:
        svg_goster(svg_otlama("Koyun"))
        st.markdown("""
- **Otlama:** üst dudak **yarıktır**; otu dipten koparır (kesici dişlerle damak arasında sıkıştırıp başı ileri-yukarı hareketle).
  Sürü merada **alt gruplara** ayrılır; meranın belli bir yerini **konaklama** alanı yapar.
- **Su:** merada belli yerlerden içer; kuraklıkta bile oraya gider.
- **Üreme:** çoğu ırk **mevsimseldir**; kuzey yarımkürede çiftleşme mevsimi **sonbahar**. Koç yıl boyu aktiftir.
  Kızgınlık **20–30 saat**; tespitten **12 saat** sonra çiftleştirme başarılıdır.""")
        st.subheader("🧮 Kaç koç?")
        n = st.number_input("Koyun sayısı", 10, 2000, 120, 10, key="koc_n")
        en_az, en_cok = math.ceil(n / 30), math.ceil(n / 20)
        st.markdown(f"Koç başına 20–30 koyun → **{en_az}–{en_cok} koç**. ")
        ipucu("Üstün koç astın çiftleşmesini engellemeye çalışırken kendisi de çiftleşemez. 50–60 koyunluk gruba 2 değil "
              "<b>3 koç</b> önerilir; koçlar <b>aynı yaşta</b> seçilmeli ya da çiftleştirme <b>geniş alanda</b> yapılmalı.")
        st.markdown("""
- **Doğum:** huzursuzluk, sık yer değiştirme; kasılmalar; yatar, başını karnına uzatır, meler. Genellikle yardımsız doğar;
  kuzu yalanarak kurutulur. Ana kuzusunu önce **kokusundan**, sonra görme ve işitmeyle tanır.
- **Bağlılık** beslenmeyle ilgili değildir; anasından ayrılan kuzu başka bir canlıya, hatta cansız bir nesneye bağlanabilir.
- **Lider:** sürüdeki yaşlı koyunlar. İletişimde görme ve işitme önemlidir.""")
        with st.expander("Problem kuzular ve yapılacaklar"):
            st.markdown("""
**Problem kuzu:** anası ölen; anası sütsüz ya da sütü yetersiz; çoğuz doğup anasınca kaybedilen ya da beslenemeyen;
anasınca reddedilen; başka koyunca çalınıp terk edilen; zayıf doğup hareketsizliği yüzünden ilgi görmeyen.

**Yapılacaklar:** sütü fazla koyun tutularak emzirilir (iş gücü fazla) · kuzusu ölmüş koyuna adapte edilir · reddeden
ananın kabul etmesi sağlanır · kuzu çalma önlenir · zayıf kuzu kurutulur, elden süt içirilir, **en çok 8 saat** içinde anasına verilir.""")
    with t3:
        svg_goster(svg_otlama("Keçi"))
        tablo(pd.DataFrame(KOYUN_KECI, columns=["Özellik", "Koyun", "Keçi"]))
        st.markdown("""
- **Teke:** üreme mevsiminde penis ereksiyondayken idrar yapar; boynuzların arkasındaki bezlerden keçileri çeken **feromon**
  salgılar. Kızgın keçiyi vajinal akıntı ve kuyruk bezinin kokusundan bulur; **flehmen** gösterir. Bu dönemde asabi ve saldırgandır.
- **Kızgın keçi:** sık meler, kuyruk sallar, tekeyi izler, sık ve az idrar yapar, aşıma izin verir.
- **Alfa teke** diğerlerini engellerken kendisi de çiftleşemez → iki tekenin yeteceği gruba **üç teke** katılır.
- **Doğum:** huzursuzluk, yataklığı eşeleme; yatarak, **½–4 saatte** doğurur; zarları yeme eğilimindedir. Ana oğlağı yalar;
  bağlılık bu sırada büyük ölçüde oluşur.
- **Çit:** çitle çevrili alandaki keçiler sürekli çıkmaya çalışır → sağlam çit.
- **Orman:** fidan ve sürgünleri yiyerek vejetasyona zarar verebilir.""")
    with t4:
        st.markdown("""
- **Üreme:** erkekte **12–16**, dişide en erken **18** haftalıkta çiftleşme davranışı. Ağır ve üst sıradaki dişiler daha seyrek çiftleşir.
- **Horoz ve kuluçka randımanı:** deneyim; ağır erkek az, genç erkek çok çiftleşir; erkek/dişi oranı (1/5–1/12) randımanı
  değiştirmez; aydınlatma değişikliği sperm üretimini uyarır; susuzluk ve küflü yem sperm üretimini azaltır.
- **Gurkluk:** kuluçkaya yatma isteği. Doğal kuluçkada: yanmış gübre ya da torf üzerinde yuva (nem) · dış parazit temizliği ·
  1 gün taklit yumurta · cüsseye göre **10–15 yumurta** · yem, su, dışkı ve gezinme için çıkabilmeli · tüm civcivler çıkana dek yuvada kalmalı.
- **İletişim:** civcivler **12**, tavuklar **22** farklı sesle (yem çağrısı, yırtıcı alarmı, yumurtlama sesleri) ve duruşla anlaşır.""")
        uyari("Notta 'kuluçkanın 20. günü çıkım maksimum olur' yazıyor. Tavukta kuluçka süresi <b>21 gündür</b>; civciv 20. gün "
              "civarında hava boşluğunu ve kabuğu delmeye başlar, çıkım <b>21. günde</b> en yüksektir.")
        st.subheader("Gagalama düzeni")
        st.markdown("Tavuklarda üstünlük sıralaması **gagalama düzeni**dir. Hızla oturmazsa kavga olur, **yumurta verimi düşer**. Önlemler:")
        st.markdown("- Yeni grupları **yumurtlama başlamadan** kurmak\n- Yeterli alan\n- Yeterli sayıda ve iyi dağılmış yemlik-suluk\n"
                    "- Birleşen gruplardan **eşit sayıda** tavuk almak\n- Horoz katılacak grubu horozlu gruplardaki tavuklardan oluşturmak")
        uyari("Notta yeterli alan '460 cm²/tavuk' olarak geçer; bu konvansiyonel bir değerdir. Organikte iç alan <b>en çok 6 tavuk/m²</b> "
              "(≈1667 cm²/tavuk) ve ayrıca tavuk başına yaklaşık <b>4 m² açık alan</b> gerekir.")
        st.subheader("Gaga kesimi: konvansiyonel ve organik")
        c1, c2 = st.columns(2)
        c1.markdown("**Konvansiyonel (notta):** yamyamlığı önlemek için **5–7 günlük** civcivlerde gaganın **1/3**'ü kesilir.")
        c2.markdown("**Organik:** gaga ve ibik kesme **rutin olarak yapılmaz**. Yamyamlık; alan, loş ışık, altlık, açık alan, "
                    "iyi besleme ve uygun ırkla önlenir.")
        st.subheader("Aydınlatma programı")
        dongu = st.radio("Döngü", ["24 saat", "28 saat"], horizontal=True, key="isik_dongu")
        isik = st.slider("Işık süresi (saat)", 8, 20, 16, key="isik_saat")
        d = int(dongu.split()[0])
        svg_goster(svg_aydinlatma(min(isik, d - 1), d))
        if isik > 17:
            st.error("Günlük aydınlatma 17 saati geçmemelidir.")
        if d == 28:
            st.info("28 saatlik döngü: haftanın 168 saati ÷ 28 = **6 döngü**. Yumurta sayısı biraz azalır ama **yumurta büyür**.")
        st.markdown("""
- **Folluk:** içinde rahat hareket edilebilir; girişi tercihen **üçgen**; **yarı karanlık**; bol ve sık değişen altlık; dış parazit yok.
- **Folluk dışına yumurtlamayı önleme:** folluğu önce tabana koyup her gün biraz yükseltmek · altlık 7–8 cm'yi aşmasın ·
  yere yumurtlananları toplayıp folluğa taklit yumurta koymak · kümeste loş köşe bırakmamak.
- **Civciv:** sıcak, korunaklı yer arar; **hava akımına çok duyarlıdır**. Altına kağıt serip üzerine yem serpilir; suluk erişilebilir yükseklikte.
- **Etlik piliç:** yeterli suluk; yemlik civcivin yiyebileceği şekilde; her zaman taze yem; yemliğe en çok **2 m**; arıza alarmı;
  havalandırma yeterli ama soğutmasın. Yakalama-naklinde **berelenme (%3 ve üstü)**, sıcakta ve ağır hayvanda daha çok.""")
    alistirma_blogu("tur", "Türlere göre davranış", gen_tur)


# ---------------------------------------------------------------------------
def sayfa_bozukluk():
    st.title("13 · Davranış bozuklukları")
    st.markdown("Hayvanın davranış ihtiyacı karşılanmayınca (dar alan, uğraşı yokluğu, eksik kaba yem, kalabalık, güçlü ışık) "
                "**anormal davranışlar** gelişir. Bunlar refahın bozulduğunun **göstergesi**dir.")
    tablo(pd.DataFrame([{"Davranış": a, "Tür": t, "Olası neden": n, "Önleme": o} for a, t, n, o in ANORMAL]))
    st.header("🎮 Hangi türde görülür?")
    _mini_oyun("anormal", [(a, t) for a, t, _, _ in ANORMAL], ["Sığır", "Koyun", "Domuz", "Tavuk"],
               "Bu davranış bozukluğu en çok hangi türde görülür?")
    st.header("Tavuklarda üç sorun yakından")
    kartlar([("Kloak gagalama", "Yumurtlamaya başlayan piliçlerde, hormon değişimiyle. Öneri: ışık şiddetini düşürmek."),
             ("Polidipsi", "Kafeste; nipelle oynayıp aşırı su içme. Öneri: yemi sık karıştırıp dikkati yeme çekmek."),
             ("Yumurta yeme", "Hızla yayılır. Başlatanlar: besin eksikliği, yetersiz grid, kırık yumurta bulma.")])
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Yumurta yemeyi önleme (notta)**")
        st.markdown("- Gagasına sarı bulaşmış şüpheli tavukları ayıklamak\n- ~~Gaga kesimi~~ *(organikte rutin olarak yapılmaz)*\n"
                    "- Loş folluk\n- Folluk dışı yumurtayı hemen toplamak\n- Kırık yumurtayı ve artıklarını yok etmek\n"
                    "- Sağlam kabuk için uygun besleme")
    with c2:
        uyari("Davranış notu yumurta yemeye karşı 'gaga kesimi uygulanmalıdır' der. Bu, <b>konvansiyonel</b> yaklaşımdır. "
              "Organik hayvancılıkta gaga kesimi rutin olarak yasaktır; sorun nedenine (besleme, ışık, folluk, alan) "
              "inilerek çözülür. Sınavda ve uygulamada bu ayrıma dikkat!")
    ipucu("Organik bakış: davranış bozukluğunun 'semptomunu' kesip atmak yerine <b>nedenini</b> ortadan kaldırmak. Kuyruk "
          "kesmek kuyruk ısırmayı gizler; saman ve alan vermek ise ortadan kaldırır.")
    alistirma_blogu("bozukluk", "Davranış bozuklukları", gen_bozukluk)


# ---------------------------------------------------------------------------
def _kart_yeni():
    st.session_state.kart_i = int(rng().integers(0, len(TERIMLER)))
    st.session_state.kart_acik = False


def sayfa_tekrar():
    st.title("14 · Genel tekrar")
    st.header("🃏 Hafıza kartları")
    if "kart_i" not in st.session_state:
        _kart_yeni()
    terim, tanim = TERIMLER[st.session_state.kart_i]
    st.markdown(f'<div class="flash">{terim}' + (f'<div class="flash-cevap">{tanim}</div>' if st.session_state.kart_acik else "")
                + '</div>', unsafe_allow_html=True)
    c1, c2, _ = st.columns([1, 1, 2])
    if c1.button("👀 Tanımı göster"):
        st.session_state.kart_acik = True
        st.rerun()
    c2.button("➡️ Sonraki kart", on_click=_kart_yeni)
    with st.expander("📖 Sözlük"):
        ara = st.text_input("Terim ara", "")
        for t, d in TERIMLER:
            if ara.lower() in (t + d).lower():
                st.markdown(f"**{t}:** {d}")
    alistirma_blogu("tekrar", "Karışık sorular", gen_tekrar)


# ===========================================================================
# SORU ÜRETİCİLERİ
# ===========================================================================
def _secim(r, metin, dogru, yanlis, cozum):
    temiz = [y for y in dict.fromkeys(yanlis) if y != dogru][:3]
    return soru_secim(r, metin, dogru, temiz, [_md(c) if isinstance(c, str) else c for c in cozum])


def _tamamla(r, sabit, havuz):
    gerek = SORU_SAYISI - len(sabit)
    secilen = _kavram_sec(r, havuz, min(gerek, len(havuz)))
    hepsi = sabit + secilen
    sira = r.permutation(len(hepsi))
    return [hepsi[i] for i in sira]


def _ek(r, liste):
    return [_secim(r, m, d, y, [c]) for m, d, y, c in liste]


def _sec_bir(r, liste):
    return liste[int(r.integers(0, len(liste)))]


def _diger(r, tum, dogru, n=3):
    aday = [x for x in dict.fromkeys(tum) if x != dogru]
    return [aday[int(i)] for i in r.permutation(len(aday))[:n]]


def _tr(x, od=2):
    t = f"{x:.{od}f}".rstrip("0").rstrip(".") if od else f"{x:.0f}"
    tam, _, ond = t.partition(".")
    if abs(int(tam)) >= 10000:
        tam = f"{int(tam):,}".replace(",", ".")
    return tam + ("," + ond if ond else "")


# ---------------------------------------------------------------------------
S_NEDEN = [
    ("Yoğun (entansif) üretimin temel amacı nedir?", "Yoğun girdiyle birim alandan daha çok ürün almak",
     ["Hayvan refahını en üst düzeye çıkarmak", "Girdi kullanımını sıfırlamak", "Yalnızca yerli ırk yetiştirmek"], "Pestisit, gübre, büyüme uyarıcılarla birim alandan yüksek verim."),
    ("BSE (deli dana hastalığı) nasıl ortaya çıkmıştır?", "Kesif yemlere scrapie'li koyunların kadavra ununun karışmasıyla",
     ["GDO'lu mısırdan", "Aşırı tuz kullanımından", "Kene ile bulaşarak"], "Yem kaynaklı bir sorun; organikte hayvansal yan ürün rasyona girmez."),
    ("Ders notuna göre Türkiye'de hayvansal üretimin tarımsal üretimdeki payı yaklaşık ne kadardır?", "%25–30",
     ["%60–70", "%5–10", "%80–90"], "Gelişmiş ülkelerde %60–70'in üzerinde, Türkiye'de %25–30 (2009)."),
    ("Gelişmiş ülkelerde hayvansal üretimin tarımsal üretimdeki payı yaklaşık ne kadardır?", "%60–70'in üzerinde",
     ["%25–30", "%10'un altında", "%40"], "Ders notu."),
    ("Monokültürün çevreye etkisi hangisidir?", "Biyolojik çeşitliliğin daralması", ["Toprak veriminin artması",
     "Su kaynaklarının çoğalması", "Erozyonun azalması"], "Yoğun bitkisel üretimin sorunları: biyoçeşitlilik kaybı, çoraklaşma, su kirliliği."),
    ("Hangisi yoğun hayvancılığın sağlık ve refah sorunlarından biridir?", "Davranış problemleri", ["Ürün fiyatının düşmesi",
     "Gübre azlığı", "Mera fazlalığı"], "İskelet ve metabolik hastalıklar, davranış problemleri, kafeste barındırma."),
    ("'Gıda güvencesi' neyi anlatır?", "Herkesin yeterli gıdaya her zaman ulaşabilmesi", ["Gıdanın kalıntı içermemesi",
     "Gıdanın ambalajlı satılması", "Gıdanın ithal edilmesi"], "Güvence: miktar ve erişim. Güvenlik: sağlığa zararsızlık."),
    ("'Gıda güvenliği' neyi anlatır?", "Gıdanın sağlığa zarar vermemesi", ["Herkesin yeterli gıdaya ulaşması",
     "Gıdanın ucuz olması", "Gıdanın yerli üretilmesi"], "Kalıntı, hastalık etkeni, bulaşan olmaması."),
    ("Ders notuna göre dünyada gıda sorununun temel nedeni nedir?", "Adil dağıtım yapılamaması", ["Üretimin çok yetersiz olması",
     "Organik tarımın yaygınlaşması", "Hayvan sayısının çok olması"], "Dünyada gıda üretimi yetersiz değildir."),
    ("Hangisi organik hayvancılığın avantajıdır?", "Sentetik girdilerden tasarruf", ["Daha düşük maliyet",
     "Kayıt gerekmemesi", "Daha yüksek yoğunluk"], "Kimyasal gübre, pestisit, hormon, antibiyotik kullanılmaz."),
    ("Hangisi organik hayvancılığın dezavantajıdır?", "Maliyetin daha yüksek olması", ["Hayvan refahının yüksek olması",
     "Gübrenin toprağa dönmesi", "Yeni istihdam yaratması"], "Kurallı, denetimli, daha maliyetli bir sistem."),
    ("Organik hayvancılık bir organik işletmenin kazancının ne kadarını oluşturabilir?", "%50'den fazlasını",
     ["%5'ini", "%10'unu", "Hiçbir kısmını"], "Ekonomik önemi büyüktür."),
    ("Ruminantların organik sistemdeki ekolojik önemi nedir?", "Çayır, mera ve baklagil yem bitkilerini iyi değerlendirmeleri",
     ["Kesif yeme bağımlı olmaları", "Gübre üretmemeleri", "Kapalı alanda tutulmaları"], "Besin döngüsüne katkı."),
    ("Organik hayvancılıkta öne çıkan ülke/bölgeler hangileridir?", "ABD, Kanada ve Avrupa Birliği",
     ["Yalnızca Asya ülkeleri", "Yalnızca Afrika", "Yalnızca Türkiye"], "Ders notu."),
    ("AB içinde sertifikalı organik süt sığırcılığının en yaygın olduğu ülke hangisidir?", "Avusturya",
     ["Türkiye", "İspanya", "Yunanistan"], "Ders notu."),
    ("Türkiye neden organik hayvancılık için büyük potansiyele sahiptir?", "Farklı ekosistemler, iklimler ve zengin biyoçeşitlilik",
     ["Hayvan sayısı çok az olduğu için", "Hiç mera olmadığı için", "Tamamen yoğun üretim yapıldığı için"], "Ders notu."),
    ("Türkiye'de bitkisel ve hayvansal üretimin durumu nedir?", "Akdeniz ülkelerindeki gibi entegre değildir",
     ["Tamamen entegredir", "Hayvansal üretim bitkiselden büyüktür", "Bitkisel üretim yoktur"], "Şayan ve Polat (2005)."),
    ("2016 TÜİK verisine göre Türkiye'de en kalabalık hayvan grubu hangisidir?", "Yerli koyun",
     ["Kültür sığırı", "Manda", "Tiftik keçisi"], "Yaklaşık 28,8 milyon baş."),
    ("2016'da Türkiye koyunlarının yaklaşık yüzde kaçı yerli ırktı?", "%93", ["%12", "%50", "%25"], "Merinos yaklaşık %7."),
    ("2016'da Türkiye sığırlarının yaklaşık yüzde kaçı yerli ırktı?", "%12", ["%93", "%50", "%75"], "Kültür %47, melez %41, yerli %12."),
    ("Türkiye keçilerinin büyük kısmı hangi tiptir?", "Kıl keçisi", ["Tiftik (Ankara) keçisi", "Saanen", "Malta"], "Yaklaşık %98."),
    ("Ders notundaki tabloya göre dünya nüfusu 1930–1975 arasında kaç katına çıkmıştır?", "2 katına", ["4 katına", "10 katına", "Değişmemiş"],
     "2 milyar → 4 milyar."),
    ("Nüfus ikiye katlanma süresi zamanla nasıl değişmiştir?", "Kısalmıştır", ["Uzamıştır", "Hep aynı kalmıştır", "Ölçülemez"],
     "1650 yıl → 200 → 100 → 45 → 23 yıl."),
    ("Yoğun üretime geçişin nedenlerinden biri hangisidir?", "Artan nüfusun gıda, lif, yakıt gereksinimi", ["Mera alanlarının artması",
     "Organik ürün talebinin düşmesi", "Hayvan refahı kaygısı"], "Ekonomik kazanç isteği de eklenir."),
    ("Hangisi organik hayvancılığın amaçlarından biri değildir?", "Birim alanda en çok hayvanı barındırmak",
     ["Çevreye dost üretim", "Hayvanları sağlıklı tutmak", "Yüksek kaliteli ürün"], "Bu yoğun üretimin amacıdır."),
    ("Yoğun hayvancılıkta 'yerleşim sıklığının fazla olması' hangi sorun grubuna girer?", "Yetiştirme (bakım) sorunları",
     ["Gıda güvencesi", "Toprak çoraklaşması", "Mevzuat"], "Birim alandaki hayvan sayısı."),
    ("GDO'lu yemler yoğun üretimde hangi sorun grubunda anılır?", "Besleme sorunları", ["Barınak sorunları",
     "Taşıma sorunları", "Kesim sorunları"], "Yem kaynakları ve katkı maddeleri kaynaklı sorunlar."),
    ("Organik hayvancılık bitkisel üretimle ilişkisi bakımından ne sağlar?", "İki üretimi birbirine bağlar", ["İkisini tamamen ayırır",
     "Bitkisel üretimi bitirir", "Hiçbir ilişki kurmaz"], "Yem çiftlikte, gübre tarlaya."),
    ("Kafeste barındırma ve doğal davranışların yapılamaması hangi sorunu gösterir?", "Hayvan refahı sorunu",
     ["Gıda güvencesi sorunu", "Mevzuat eksikliği", "Pazar sorunu"], "Yoğun sistemin refah sorunları."),
    ("Toprakların çoraklaşması hangi üretim biçimiyle ilişkilendirilir?", "Yoğun (entansif) üretim", ["Organik üretim",
     "Ekstansif meracılık", "Ekim nöbeti"], "Ders notu, yoğun üretimin çevresel sonuçları."),
]

S_TANIM = [
    ("Organik hayvancılıkta 'primum non nocere' ne demektir?", "Önce zarar verme", ["Önce verim", "Önce kazanç", "Önce hız"],
     "Hayvanı hasta etmeme, acı çektirmeme önceliği."),
    ("5262 sayılı Organik Tarım Kanunu Resmî Gazete'de hangi tarihte yayımlandı?", "3 Aralık 2004", ["18 Ağustos 2010",
     "10 Ocak 2018", "1 Ocak 2022"], "RG 03.12.2004, sayı 25659."),
    ("Organik Tarımın Esasları ve Uygulanmasına İlişkin Yönetmelik hangi yıl yayımlandı?", "2010", ["2004", "1998", "2022"],
     "RG 18.08.2010, sayı 27676; sonradan değiştirildi."),
    ("AB'de 2022'den beri yürürlükte olan organik üretim tüzüğü hangisidir?", "2018/848", ["889/2008", "98/58/EC", "2007/43/EC"],
     "834/2007 ve 889/2008'in yerini aldı."),
    ("ABD organik programında doğal maddeler için kural nedir?", "Özellikle yasaklanmadıkça izinli", ["Hepsi yasak",
     "Özellikle izin verilmedikçe yasak", "Yalnız ithalse izinli"], "Doğal: yasaklanmadıkça izinli."),
    ("ABD organik programında sentetik maddeler için kural nedir?", "Özellikle izin verilmedikçe yasak", ["Hepsi izinli",
     "Yasaklanmadıkça izinli", "Yalnız yemde izinli"], "National List'te izin verilenler hariç."),
    ("Hangisi ABD organik programında kesin yasaktır?", "Arıtma çamuru", ["Hayvan gübresi", "Kompost", "Kuru ot"],
     "Genetik değişiklik/klonlama, iyonlaştırıcı radyasyon, arıtma çamuru."),
    ("ABD kuralına göre organik mera arazisinde son kaç yılda yasaklı madde kullanılmamış olmalıdır?", "3 yıl",
     ["1 yıl", "6 ay", "10 yıl"], "Bilgi yoksa 3 yıl geçiş."),
    ("Organik çiftlik nasıl bir sistem olarak tanımlanır?", "Kendi içinde kapalı bir döngü", ["Girdiye tamamen açık bir sistem",
     "Yalnızca hayvansal bir sistem", "Tek ürünlü bir sistem"], "Yem çiftlikte, gübre toprağa."),
    ("Organik çiftlikte gübrenin rolü nedir?", "Toprağa dönerek verimliliği korumak", ["Satılıp çiftlikten çıkarılmak",
     "Yakılmak", "Rasyona katılmak"], "Kapalı döngü."),
    ("Hangisi organik hayvancılığın ilkesi değildir?", "Gaga kesimiyle yamyamlığı önlemek", ["GDO kullanmamak",
     "Doğal üreme", "Yemi çoğunlukla çiftlikte üretmek"], "Bedene müdahale rutin olarak yasaktır."),
    ("'Köy yumurtası' etiketli, sertifikasız yumurta organik midir?", "Hayır", ["Evet", "Köyde üretildiyse evet", "Kahverengiyse evet"],
     "Sertifika yoksa organik değildir."),
    ("'Kafessiz' etiketi tek başına neyi garanti eder?", "Organik olduğunu garanti etmez", ["Organik olduğunu",
     "GDO'suz olduğunu", "İlaçsız olduğunu"], "Doğal, kafessiz, köy, özgür, gezen ≠ organik."),
    ("Bir ürünün organik olduğunu ne kanıtlar?", "Yetkili kuruluşun sertifikası", ["Ambalajdaki 'doğal' yazısı",
     "Üreticinin sözü", "Ürünün rengi"], "Organik: sertifikalı, kontrollü üretim."),
    ("Yönetmelik organik hayvancılığı hangi başlıklarla düzenler?", "Hayvan kaynağı, barınma, refah, besleme, sağlık",
     ["Yalnızca fiyat", "Yalnızca ambalaj", "Yalnızca ihracat"], "Ayrıca açık havaya erişim."),
    ("Organik hayvansal üretimde sentetik maddeler için genel kural nedir?", "Kullanılmaz; zorunluysa en az düzeyde",
     ["Serbestçe kullanılır", "Yalnızca yemde kullanılır", "Yalnızca kışın kullanılır"], "Tanımın parçası."),
    ("Organik ürünü konvansiyonelden ayıran en temel unsur hangisidir?", "Her aşamanın kontrollü ve sertifikalı olması",
     ["Ürünün daha büyük olması", "Ürünün daha ucuz olması", "Ürünün köyde üretilmesi"], "Tanım."),
    ("Organik hayvancılıkta GDO'nun yeri nedir?", "Hayvanda, yemde ve katkıda yasaktır", ["Yalnız yemde serbesttir",
     "Yalnız katkıda serbesttir", "İzinle serbesttir"], "GDO yok."),
    ("Organik hayvancılıkta yemin kaynağı ilke olarak nedir?", "Büyük ölçüde üreticinin kendi çiftliği", ["Tamamen ithal",
     "Konvansiyonel fabrika yemi", "Kadavra unu"], "Kapalı döngü ilkesi."),
    ("Organik hayvancılıkta hayvanların sistemdeki yeri nasıl tanımlanır?", "Canlı ve duyarlı bir parça; refahı gözetilir",
     ["Yalnızca bir üretim makinesi", "Önemsiz bir unsur", "Yalnızca gübre kaynağı"], "Ders notu."),
    ("Organik hayvancılıkta 'toprak, hayvan, bitki ve insan' arasında ne aranır?", "Uyum", ["Rekabet", "Ayrılık", "Bağımsızlık"],
     "Ders notu."),
    ("ABD organik programında izinli maddelerin listesine ne ad verilir?", "National List", ["Red List", "Codex Alimentarius",
     "Green Book"], "Bitkisel, hayvansal ve işleme için ayrı listeler."),
    ("Organik ürünlerin satışı için hangisi zorunludur?", "Kontrol ve sertifikasyon", ["Reklam", "İhracat izni", "Marka tescili"],
     "Organik tarım sertifikalı bir sistemdir."),
    ("Embriyo transferiyle doğan bir buzağının eti organik olabilir mi?", "Hayır", ["Evet", "Ana organikse evet", "Kesimden sonra evet"],
     "Embriyo transferi yasaktır."),
    ("Geçiş süresinde sağılan süt nasıl satılır?", "Organik olarak satılamaz", ["Organik olarak satılır", "Yarı organik etiketiyle satılır",
     "Fiyatı iki katına çıkarılarak satılır"], "Geçiş dönemi hayvansal ürünleri organik pazarlanamaz."),
    ("Organik tarım kanununun sayısı hangisidir?", "5262", ["6331", "5510", "2872"], "5262 sayılı Organik Tarım Kanunu."),
    ("Organik yönetmelikte 10 Ocak 2018 tarihi neyi ifade eder?", "Yönetmelikte değişiklik yapılmasını", ["Kanunun ilk yayımını",
     "AB'ye üyeliği", "NOP'un kuruluşunu"], "Değişiklik yönetmeliği."),
    ("Organik hayvancılık tanımında 'organik ve biyoçözünür girdiler' nereden gelir?", "Ekosistemden", ["Laboratuvardan",
     "Petrokimyadan", "Fabrika yeminden"], "Ekosistemden gelen girdilerle hayvansal üretim."),
    ("Organik ürünlerde 'gezen tavuk' ifadesi için doğru olan hangisidir?", "Sertifika yoksa organik anlamına gelmez",
     ["Organik anlamına gelir", "Yasal bir organik etikettir", "Sertifikadan üstündür"], "Ders notu."),
    ("ABD organik kuralında iyonlaştırıcı radyasyon için durum nedir?", "Yasaktır", ["İzinlidir", "Yalnız ette izinlidir",
     "Yalnız yemde izinlidir"], "Kesin yasaklar arasında."),
]

S_KAYNAK = [
    ("Organik hayvancılıkta ırk seçiminde öncelik nedir?", "Bölgeye adapte olmuş yerli ırklar ve melezleri", ["En yüksek verimli kültür ırkları",
     "İthal hibritler", "Rastgele ırklar"], "Uyum, dayanıklılık, yaşama gücü."),
    ("Hangisi organik hayvan seçim kriteri değildir?", "En hızlı büyüme ne olursa olsun", ["Yerel koşullara uyum",
     "Yaşama gücü", "Hastalığa dayanıklılık"], "Hızlı büyüme tek başına ölçüt değildir."),
    ("Organik hayvancılıkta esas üreme yöntemi nedir?", "Doğal aşım (tabii tohumlama)", ["Embriyo transferi",
     "Hormonla senkronizasyon", "Klonlama"], "Doğal aşım esastır."),
    ("Organik hayvancılıkta suni tohumlama yapılabilir mi?", "Evet, doğal yöntemlerle alınmış spermayla",
     ["Hayır, kesinlikle yasak", "Yalnızca GDO'lu hayvanlarda", "Yalnızca hormonla birlikte"], "Doğal yöntemlerle elde edilen, saklanan sperma."),
    ("Embriyo transferi organik hayvancılıkta...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnız sığırda serbesttir"], "Ders notu."),
    ("Kızgınlığı eşzamanlamak için hormon kullanımı organikte...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnız koyunda serbesttir"],
     "Üremenin kontrolü için hormon kullanılmaz."),
    ("Organik olmayan işletmeden alınan buzağı kaç aylıktan küçük olmalıdır?", "6 aylıktan", ["3 aylıktan", "12 aylıktan", "18 aylıktan"],
     "Buzağı ve tay her koşulda 6 aylıktan küçük."),
    ("Organik olmayan işletmeden alınan kuzu ve oğlak en çok kaç günlük olabilir?", "60 günlük", ["30 günlük", "120 günlük", "6 aylık"],
     "60 günden büyük olmamalı."),
    ("Etlik civcivler geldikleri çiftlikten ayrılırken en çok kaç günlük olabilir?", "3 günlük", ["10 günlük", "21 günlük", "6 haftalık"],
     "3 günlükten büyük olamaz."),
    ("Konvansiyonel hayvan hangi durumda organik sürüye katılabilir?", "Yeterli organik hayvan yoksa, kuruluşun izniyle",
     ["Her zaman serbestçe", "Hiçbir zaman", "Yalnız fiyatı ucuzsa"], "Sürünün kurulması ya da yenilenmesi için."),
    ("Konvansiyonelden alınan yavrular ne zamandan itibaren organik kurallara göre yetiştirilir?", "Sütten kesilir kesilmez",
     ["Bir yıl sonra", "Kesimden önce", "Hiçbir zaman"], "Ders notu."),
    ("Yerli ırkların organik sistem için avantajı hangisidir?", "Yerel koşullara uyum ve hastalığa dayanıklılık", ["En yüksek süt verimi",
     "En hızlı büyüme", "Kapalı alana uygunluk"], "Ödünleşim: verim daha düşük olabilir."),
    ("Belirli hastalıklara yatkın ırk ve hatlar için organikte ne önerilir?", "Uzak durulmalı", ["Tercih edilmeli",
     "Yalnız damızlık yapılmalı", "Hormonla desteklenmeli"], "Ders notu."),
    ("Organik hayvanlar, yasaklı madde alan hayvanlardan...", "Uzak tutulmalıdır", ["Aynı bölmede tutulmalıdır",
     "Aynı yemlikten yemelidir", "Birlikte taşınmalıdır"], "Ders notu."),
    ("Klonlama organik hayvancılıkta...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnızca boğada serbesttir"], "Genetik değişiklik/klonlama yasak."),
    ("'Yaşama gücü (dirilik)' hangi seçim ölçütünün adıdır?", "Hayvanın hayatta kalma ve sağlıklı yaşama yeteneği",
     ["Süt verimi", "Yapağı inceliği", "Karkas rengi"], "Organik seçim ölçütlerinden."),
    ("Yüksek verimli kültür ırkları organik sistemde neden zorlanabilir?", "Yoğun yem ve bakım isterler", ["Hiç hastalanmazlar",
     "Merayı çok iyi kullanırlar", "Doğal davranış göstermezler"], "Organik kısıtlarla sağlıklı kalmaları zordur."),
    ("Bir organik işletme 45 günlük kuzuyu konvansiyonel işletmeden alabilir mi?", "Evet, 60 günden küçük olduğu için",
     ["Hayır, 30 günden büyük", "Hayır, kuzu alınamaz", "Yalnızca kesim için"], "Sınır 60 gün."),
    ("Bir organik işletme 8 aylık buzağıyı konvansiyonel işletmeden alabilir mi?", "Hayır, 6 aylıktan büyük",
     ["Evet", "Evet, sütten kesildiyse", "Evet, organik yemle beslenirse"], "Buzağı 6 aylıktan küçük olmalı."),
    ("5 günlük civciv konvansiyonel kuluçkahaneden etlik organik üretime alınabilir mi?", "Hayır, 3 günlükten büyük",
     ["Evet", "Evet, aşılıysa", "Evet, erkekse"], "Etlik civciv en çok 3 günlük."),
    ("Doğal aşımın organikte esas olmasının bir nedeni nedir?", "Doğal üreme ilkesi", ["Daha ucuz sperma", "Daha hızlı genetik ilerleme",
     "Hormon gerektirmesi"], "Organik ilkeler: üreme doğal."),
    ("Organikte suni tohumlamada kullanılacak sperma nasıl elde edilmelidir?", "Damızlıklardan doğal yöntemlerle",
     ["Hormon uyarımıyla", "Genetik değişiklikle", "Klonlanmış boğadan"], "Ders notu."),
    ("Hangisi organik sürüye konvansiyonel hayvan getirmeyi gerektirebilir?", "Yeni işletmede yeterli organik hayvan olmaması",
     ["Ürün fiyatının artması", "Hayvanların kilo alması", "Merada ot bolluğu"], "Sürünün kurulması ya da yenilenmesi."),
    ("Tay için konvansiyonel işletmeden alım yaş sınırı hangisidir?", "6 aylıktan küçük", ["60 günden küçük", "3 günden küçük", "1 yaşından küçük"],
     "Buzağı ve tay aynı kural."),
    ("Oğlak için konvansiyonel işletmeden alım yaş sınırı hangisidir?", "60 günden büyük olmamalı", ["6 aylıktan küçük",
     "3 günden küçük", "1 yaşından küçük"], "Kuzu ve oğlak aynı kural."),
    ("Organikte üreme ile ilgili en doğru ifade hangisidir?", "Doğal yöntemler esas, teknik müdahale sınırlı",
     ["Her biyoteknoloji serbest", "Yalnız klonlama serbest", "Üreme tamamen yasak"], "Doğal aşım; SA sınırlı izinli; ET yasak."),
    ("Konvansiyonelden alınan bir hayvanın ürünü hemen organik satılabilir mi?", "Hayır, geçiş süresi uygulanır",
     ["Evet", "Yalnız sütü", "Yalnız gübresi"], "Geçiş süreleri bölümü."),
    ("Hangi özellik organik hayvanda 'hastalığa dayanıklılık' kadar önemlidir?", "Yerel koşullara uyum", ["Renk", "Boynuz uzunluğu",
     "Kulak şekli"], "Seçim ölçütleri."),
    ("Bölgeye adapte melezler organikte nasıl değerlendirilir?", "Önceliklidir", ["Yasaktır", "Yalnız kesimlik olabilir",
     "Hormonla kullanılabilir"], "Yerli ırklar ve melezlerine öncelik."),
    ("Organik hayvancılıkta 'hayvan kaynağı' başlığı neyi düzenler?", "Hayvanın kökenini, ırkını ve üremesini",
     ["Kesimhane yerini", "Ambalajı", "Pazar fiyatını"], "Yönetmelik başlıklarından."),
]

S_BARINMA = [
    ("Organik barınakta havalandırma ve ışık için ilke nedir?", "Bol doğal havalandırma ve doğal ışık", ["Tamamen yapay ışık",
     "Penceresiz kapalı bina", "Sürekli karanlık"], "Ders notu."),
    ("Açık havada yaşanabilen iklimlerde organik hayvanlar için ne zorunludur?", "Açık alana erişim", ["Kapalı barınak",
     "Kafes", "Bağlı duraklar"], "Mera, gezinti ya da egzersiz alanı."),
    ("Organik ve konvansiyonel hayvanlar aynı merada otlatılabilir mi?", "Evet, ama aynı anda değil", ["Hayır, asla",
     "Evet, aynı anda", "Yalnız kışın"], "Ders notu."),
    ("Konvansiyonel hayvanlar organik işletmede hangi koşulla bulunabilir?", "Barınak ve arazileri açıkça ayrı ve türleri farklıysa",
     ["Hiçbir koşulda", "Aynı bölmede", "Aynı tür olmak koşuluyla"], "Ayrı birim ve ayrı tür."),
    ("Gübreyle bir hektara yılda verilebilecek en çok azot ne kadardır?", "170 kg", ["70 kg", "300 kg", "17 kg"],
     "170 kg N/ha/yıl; hayvan sayısını sınırlar."),
    ("170 kg N/ha sınırı dolaylı olarak neyi sınırlar?", "Hayvan sayısını (yoğunluğunu)", ["Süt fiyatını", "Kesim yaşını", "Yem rengini"],
     "Ders notu."),
    ("Organik süt ineği için kapalı alanda hayvan başına en az alan ne kadardır?", "6 m²", ["1,5 m²", "2,5 m²", "10 m²"],
     "AB 889/2008 Ek III: 6 m² iç, 4,5 m² dış."),
    ("Organik koyun-keçi için kapalı alanda hayvan başına en az alan ne kadardır?", "1,5 m²", ["6 m²", "0,5 m²", "4 m²"],
     "İç 1,5 m², dış 2,5 m²."),
    ("Organik yumurta tavuğu için kapalı alanda en çok kaç tavuk/m² olabilir?", "6", ["21", "17", "12"], "İç alan en çok 6 tavuk/m²."),
    ("Organik yumurta tavuğu için tavuk başına açık alan yaklaşık ne kadardır?", "4 m²", ["460 cm²", "0,5 m²", "20 m²"],
     "AB kuralı: 4 m²/tavuk."),
    ("Organik etlik piliçte sabit kümeste en çok kaç piliç/m² olabilir?", "10", ["17–22", "34", "6"], "En çok 10 piliç ya da 21 kg/m²."),
    ("Ders notundaki 460 cm²/tavuk değeri hangi sisteme aittir?", "Konvansiyonel", ["Organik", "Mera", "Doğal kuluçka"],
     "Organikte ≈1667 cm²/tavuk + açık alan."),
    ("Barınakta zararlı olmaması gereken unsurlar hangileridir?", "Toz, sıcaklık, nem, gaz yoğunluğu", ["Yem rengi",
     "Bakıcının adı", "Yumurta büyüklüğü"], "Yalıtım, ısıtma ve havalandırma bunları düzenler."),
    ("Bir süt ineğinin yıllık gübre azotu yaklaşık ne kadardır? (170 ÷ 2)", "85 kg", ["170 kg", "34 kg", "13 kg"],
     "170 kg N/ha'ya 2 süt ineği karşılık gelir."),
    ("170 kg N/ha sınırına hektar başına kaç süt ineği karşılık gelir?", "2", ["13,3", "230", "6,5"], "AB 889/2008 Ek IV."),
    ("170 kg N/ha sınırına hektar başına kaç koyun karşılık gelir?", "13,3", ["2", "230", "580"], "AB 889/2008 Ek IV."),
    ("170 kg N/ha sınırına hektar başına kaç yumurta tavuğu karşılık gelir?", "230", ["580", "13,3", "2"], "AB 889/2008 Ek IV."),
    ("Organik hayvanlar açık alan seçeneklerinden en az kaçını kullanabilmelidir?", "En az birini", ["Hiçbirini", "Hepsini aynı anda",
     "Yalnızca yazın ikisini"], "Gezinti, egzersiz alanı ya da mera."),
    ("Organik barınakta yaşam koşulları için hangisi istenir?", "Doğal davranışa ve egzersize yetecek alan", ["En küçük alan",
     "Bireysel kafes", "Bağlı duraklar"], "Yaşam koşulları slaytı."),
    ("Organik damızlık boğa için açık alan en az ne kadardır?", "30 m²", ["4,5 m²", "1,5 m²", "10 m²"], "İç 10 m², dış 30 m²."),
    ("Organik besi domuzu (110 kg'a kadar) için kapalı alan en az ne kadardır?", "1,3 m²", ["0,8 m²", "6 m²", "7,5 m²"],
     "50 kg'a kadar 0,8; 85 kg'a kadar 1,1; 110 kg'a kadar 1,3 m²."),
    ("Yavrulu ana domuz (40 güne kadar) için kapalı alan en az ne kadardır?", "7,5 m²", ["1,3 m²", "2,5 m²", "15 m²"], "AB Ek III."),
    ("Ders notundaki etlik piliç yoğunluğu (17–22 piliç/m²) hangi sisteme aittir?", "Konvansiyonel çevre kontrollü kümes",
     ["Organik", "Doğal kuluçka", "Mera"], "Organikte en çok 10 piliç/m²."),
    ("Organik ve konvansiyonel üretim aynı işletmede yapılıyorsa en önemli şart nedir?", "Birimlerin açıkça ayrılması",
     ["Aynı yemin kullanılması", "Aynı bakıcının çalışması", "Aynı kayıt defteri"], "Karışmayı önlemek."),
    ("Barınağın amacı hangisidir?", "Uygun hava, sıcaklık, nem ve korunma sağlamak", ["Hayvanları dışarı hiç çıkarmamak",
     "Yoğunluğu en üste çıkarmak", "Işığı engellemek"], "Barınak ilkeleri."),
    ("İç alana göre 20, dış alana göre 14 hayvan sığıyorsa en çok kaç hayvan barındırılır?", "14", ["20", "34", "17"],
     "Küçük olan değer belirleyicidir."),
    ("Neden organikte konvansiyonelden daha geniş alan istenir?", "Doğal davranış ve refah için", ["Gübre azaltmak için",
     "Maliyeti düşürmek için", "Yem israfı için"], "Refah ve sağlık."),
    ("Organikte barınak iç havası için hangisi yanlıştır?", "Toz ve amonyak önemli değildir", ["Hava sirkülasyonu uygun olmalı",
     "Gaz yoğunluğu düşük olmalı", "Nem uygun olmalı"], "Hepsi hayvana zarar vermeyecek düzeyde olmalı."),
    ("Organik kanatlıda kapalı alanda 6 tavuk/m² kaç cm²/tavuk eder?", "≈1667 cm²", ["460 cm²", "600 cm²", "6000 cm²"],
     "10.000 ÷ 6 ≈ 1667."),
    ("Organik süt ineği için açık alan en az ne kadardır?", "4,5 m²", ["6 m²", "1,1 m²", "30 m²"], "AB Ek III."),
]

S_BESLEME = [
    ("Organik hayvanların içme suyu hangi niteliği taşımalıdır?", "İnsan içme suyu niteliği", ["Yalnızca bulanık olmaması",
     "Yalnızca sıcak olması", "Herhangi bir nitelik aranmaz"], "Özellikle nitrata dikkat."),
    ("Organik hayvan suyunda özellikle hangi içeriğe dikkat edilir?", "Nitrat", ["Şeker", "Protein", "Yağ"], "Ders notu."),
    ("Yeni doğan yavru ilk olarak neyle beslenmelidir?", "Ağız sütü (kolostrum)", ["Kuru ot", "Süt tozu", "Kesif yem"],
     "Bağışıklık için."),
    ("Ana sütü yoksa yavru neyle beslenmelidir?", "Aynı sürüden elde edilen sütle", ["Süt ikamesiyle", "Şekerli suyla", "Silajla"],
     "Ders notu."),
    ("Buzağılar ve taylar en az kaç gün sütle beslenmelidir?", "90 gün", ["45 gün", "40 gün", "30 gün"], "Büyükbaş ve tek tırnaklı: 90 gün (3 ay)."),
    ("Kuzu ve oğlaklar için sütle beslenmenin asgari süresi nedir?", "45 gün", ["90 gün", "40 gün", "15 gün"], "Mevzuat: 45 gün."),
    ("Domuz yavruları için sütle beslenmenin asgari süresi nedir?", "40 gün", ["45 gün", "90 gün", "20 gün"], "Mevzuat: 40 gün."),
    ("Genç hayvanların önüne organik kuru ot ve yoğun yem ne zamandan itibaren konur?", "2. haftadan itibaren",
     ["Doğum günü", "6. aydan itibaren", "Sütten kesimden sonra"], "Yeme alışmaları için."),
    ("'Ad libitum' yemleme ne demektir?", "Hayvanın istediği zaman, istediği kadar yemesi", ["Günde bir öğün", "Zorla besleme",
     "Sırayla yemleme"], "Organikte büyük ve küçükbaşa da önerilir."),
    ("Kısa süreli ve sırayla yemlemenin sakıncası nedir?", "Güçlülerin zayıflarla dövüşmesi, stres ve yaralanma",
     ["Yemin bozulması", "Suyun ısınması", "Hiç sakıncası yoktur"], "Ders notu."),
    ("Hangisi organik rasyona katılamaz?", "Hayvansal yağ", ["Melas", "Tuz", "Doğal vitamin"], "Hayvansal yağ ve yan ürün yasak."),
    ("Hangisi organik rasyonda izinli bir katkıdır?", "Probiyotik", ["Antibiyotik", "Koksidiyostat", "Büyütme hormonu"],
     "Probiyotik, enzim, organik asit, melas, tuz, mineral."),
    ("Organikte küspe hangi koşulda kullanılamaz?", "Kimyasal solventle işlenmişse", ["Soğuk preslenmişse", "Organikse",
     "Çiftlikte üretilmişse"], "Solvent ekstraksiyonu yasak."),
    ("Silaj hazırlarken organikte hangi katkılar kullanılabilir?", "Yalnız izin verilen fermantasyon yardımcıları",
     ["Her türlü kimyasal koruyucu", "Antibiyotik", "Sentetik boya"], "Ders notu."),
    ("Yumurta sarısını koyulaştıran sentetik maddeler organikte...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnız kışın serbesttir"],
     "Ders notu."),
    ("Zorla besleme organikte...", "Yasaktır", ["Serbesttir", "Kazda serbesttir", "Önerilir"], "Ders notu."),
    ("Hayvanı kansızlığa (anemiye) sürükleyecek rasyon organikte...", "Yasaktır", ["Beyaz et için serbesttir", "Önerilir",
     "Buzağıda serbesttir"], "Ders notu."),
    ("Kanatlı ve domuzun günlük rasyonunda organikte ne bulunmalıdır?", "Kaba yem (kuru ot, silaj)", ["Antibiyotik",
     "Hayvansal yağ", "Sentetik amino asit"], "Ders notu."),
    ("Türkiye yönetmeliğine (2013 değişikliği) göre otçulların yeminin en az ne kadarı çiftlikten sağlanmalıdır?", "%60",
     ["%20", "%10", "%100"], "Ders notunda bir slaytta %50 yazar; değişiklikle %60."),
    ("Türkiye yönetmeliğine göre domuz ve kanatlıların yeminin en az ne kadarı çiftlikten sağlanmalıdır?", "%20",
     ["%60", "%50", "%90"], "2013 değişikliği."),
    ("Organik olmayan merada otlatılarak tüketilen yem yıllık rasyonun en çok ne kadarı olabilir?", "%10", ["%30", "%50", "%60"],
     "Kuru madde üzerinden hesaplanır."),
    ("Otçulda günlük rasyondaki kaba yem payı en az ne kadar olmalıdır?", "%60 (kuru madde)", ["%10", "%30", "%90"],
     "Laktasyonun başında en çok 3 ay %50'ye inebilir."),
    ("Süt hayvanlarında kaba yem payı hangi dönemde %50'ye indirilebilir?", "Laktasyonun başında en çok 3 ay", ["Kuru dönem boyunca",
     "Tüm yıl", "Gebeliğin son 3 ayı"], "İstisna."),
    ("Antibiyotiklerin yem katkısı olarak kullanımı organikte...", "Yasaktır", ["Serbesttir", "Kanatlıda serbesttir", "Önerilir"],
     "Büyüme veya üretimi artırıcı maddeler kullanılmaz."),
    ("Organik yemin üretiminde hangisi kullanılmaz?", "Kimyasal gübre ve pestisit", ["Hayvan gübresi", "Kompost", "Ekim nöbeti"],
     "Ders notu."),
    ("Rasyonda kullanılan katkılar kimin kontrolünde eklenmelidir?", "Veteriner hekim ve ziraat mühendisi", ["Yem satıcısı",
     "Kasap", "Muhasebeci"], "Kalıntı analizleri de kayda geçer."),
    ("Hayvanlar öncelikle hangi yemle beslenir?", "Kendi işletmesinde üretilen organik yem", ["Fabrika yemi", "İthal konvansiyonel yem",
     "Kadavra unu"], "Mümkün değilse kurallara uyan diğer işletmelerden."),
    ("Doğal kaynaklı vitaminlerin organik rasyonda kullanımı...", "İzinlidir", ["Yasaktır", "Yalnız kanatlıda izinlidir",
     "Yalnız hasta hayvanda izinlidir"], "Ders notu."),
    ("Sütten kesilen genç ruminantlar nasıl beslenmelidir?", "Gereksinimini karşılayan organik kaba ve yoğun yemle",
     ["Yalnızca suyla", "Yalnızca süt tozuyla", "Yalnızca kesif yemle"], "Ders notu."),
    ("Geçiş dönemi yemi (AB kuralına göre) rasyonun ortalama en çok ne kadarı olabilir?", "%30 (kendi çiftliğindense %100)",
     ["%60", "%5", "%90"], "Notta '%30–60' yazıyor; kural %30, kendi geçiş arazisinden %100."),
    ("Melas organik rasyonda...", "Kullanılabilir", ["Yasaktır", "Yalnız domuzda kullanılabilir", "Yalnız ihracatta kullanılabilir"],
     "Ders notu."),
    ("Genç memeliler organikte tercihen nasıl beslenmelidir?", "Doğal yolla, ana sütüyle", ["Süt ikamesiyle", "Erken sütten keserek",
     "Zorla besleyerek"], "Ders notu."),
]

S_GECIS = [
    ("Organikte büyükbaş et üretimi için geçiş süresi nedir?", "12 ay", ["6 ay", "10 hafta", "24 ay"], "Ders notu."),
    ("Küçükbaş ve domuz eti için geçiş süresi nedir?", "6 ay", ["12 ay", "6 hafta", "3 ay"], "Ders notu."),
    ("Süt üretimi için yetiştirilen hayvanlarda geçiş süresi nedir?", "6 ay", ["12 ay", "10 hafta", "3 yıl"], "Ders notu."),
    ("Etlik kanatlıda geçiş süresi nedir?", "10 hafta", ["6 hafta", "6 ay", "3 gün"], "3 günlükten büyük olmamak kaydıyla."),
    ("Yumurta tavuğunda geçiş süresi nedir?", "6 hafta", ["10 hafta", "6 ay", "12 ay"], "Ders notu."),
    ("Organik süt işletmesinden et için ayrılan hayvanda geçiş süresi nedir?", "Yaşam süresinin 3/4'ü", ["12 ay", "Yaşam süresinin yarısı",
     "6 hafta"], "Ders notu."),
    ("Geçiş süresindeki hayvansal ürün nasıl satılır?", "Organik olarak satılamaz", ["Organik olarak satılır",
     "Yarı fiyatına organik satılır", "Yalnız ihraç edilir"], "Ders notu."),
    ("Arazi geçişinde '24 ay' neyi anlatır? (AB kuralı)", "Yem bitkisi tarlası ve çayırın geçiş süresi", ["Tavuk kümesinin süresi",
     "Kesim yaşını", "Süt sağım süresini"], "Ürünü organik yem sayılmadan önce."),
    ("Domuz ve kanatlının kullandığı mera ve açık alanlar için AB'deki geçiş süresi nedir?", "12 ay (koşulla 6 aya inebilir)",
     ["24 ay", "3 yıl", "10 hafta"], "Notta '24; 12; 6 ay' olarak özetlenmiş."),
    ("ABD organik kuralında arazinin yasaklı madde almamış olması gereken süre nedir?", "Son 3 yıl", ["Son 6 ay", "Son 10 yıl", "Son 1 ay"],
     "NOP."),
    ("Geçiş süresine neden gerek vardır?", "Önceki konvansiyonel girdilerin etkisinin ve kalıntısının ortadan kalkması için",
     ["Fiyatı artırmak için", "Hayvanı büyütmek için", "Kayıt tutmamak için"], "Organik bütünlük."),
    ("Yılda 3'ten fazla kimyasal ilaç kürü alan hayvan için ne olur?", "Yeniden geçiş sürecine alınır", ["Hemen kesilir",
     "Hiçbir şey olmaz", "Yalnız sütü atılır"], "Sağlık bölümüyle bağlantılı."),
    ("Etlik civcivin geçiş süresinin 10 hafta olması için hangi koşul gerekir?", "Civcivin 3 günlükten küçükken alınması",
     ["Civcivin erkek olması", "Kümesin ısıtılması", "Civcivin aşılanması"], "Ders notu."),
    ("Kuzu ve oğlak hangi koşulla konvansiyonel işletmeden alınabilir?", "60 günden büyük olmamalı", ["6 aylıktan küçük olmalı",
     "3 günlükten küçük olmalı", "1 yaşından büyük olmalı"], "Ders notu."),
    ("Buzağı konvansiyonel işletmeden alınırken kaç aylıktan küçük olmalıdır?", "6", ["3", "12", "18"], "Ders notu."),
    ("Yaşam süresi 24 ay olan, süt sürüsünden ayrılan bir hayvanın geçiş süresi nedir?", "18 ay", ["12 ay", "24 ay", "6 ay"],
     "3/4 × 24 = 18."),
    ("Yaşam süresi 40 ay olan, süt sürüsünden ayrılan bir hayvanın geçiş süresi nedir?", "30 ay", ["20 ay", "40 ay", "12 ay"],
     "3/4 × 40 = 30."),
    ("Geçiş süreleri sıralamasında en uzun olan hangisidir?", "Büyükbaş eti (12 ay)", ["Süt (6 ay)", "Etlik kanatlı (10 hafta)",
     "Yumurta (6 hafta)"], "12 ay en uzun."),
    ("Geçiş süreleri sıralamasında en kısa olan hangisidir?", "Yumurta tavuğu (6 hafta)", ["Etlik kanatlı (10 hafta)",
     "Süt (6 ay)", "Küçükbaş eti (6 ay)"], "6 hafta en kısa."),
    ("Domuz eti için geçiş süresi hangisiyle aynıdır?", "Küçükbaş eti", ["Büyükbaş eti", "Etlik kanatlı", "Yumurta"], "İkisi de 6 ay."),
    ("Bir sürü ilk kez kurulurken yeterli organik hayvan yoksa ne yapılabilir?", "Kurallara uyulmak şartıyla konvansiyonel hayvan kullanılabilir",
     ["Sürü kurulamaz", "Yalnız ithal hayvan alınır", "Klonlanmış hayvan alınır"], "Ders notu."),
    ("Etlik piliçler geldikleri çiftlikten ayrılırken en çok kaç günlük olabilir?", "3", ["7", "10", "21"], "Ders notu."),
    ("Süt sığırı için geçiş süresi hangisiyle aynıdır?", "Küçükbaş eti", ["Büyükbaş eti", "Etlik kanatlı", "Yumurta tavuğu"],
     "İkisi de 6 ay."),
    ("Buzağılar ve taylar organik işletmeye geldiklerinde ne zamandan itibaren organik kurallara tabi olur?", "Sütten kesilir kesilmez",
     ["Doğumdan bir yıl sonra", "Kesimde", "Hiçbir zaman"], "Ders notu."),
    ("Geçiş süresi dolmamış bir hayvanın etiketinde hangisi yazamaz?", "Organik", ["Doğum tarihi", "Irk", "İşletme adı"],
     "Geçiş ürünleri organik pazarlanamaz."),
    ("Arazi geçişinde '6 ay' hangi durumda geçerli olabilir? (AB)", "Yakın zamanda yasaklı madde kullanılmadığı belgelenirse, domuz-kanatlı alanlarında",
     ["Her durumda", "Yem bitkisi tarlasında her zaman", "Hiçbir zaman"], "12 ay → 6 ay indirimi."),
    ("Koyun eti için geçiş süresi kaç haftaya yakındır?", "≈26 hafta", ["10 hafta", "52 hafta", "6 hafta"], "6 ay ≈ 26 hafta."),
    ("Sığır eti için geçiş süresi kaç haftaya yakındır?", "≈52 hafta", ["26 hafta", "10 hafta", "6 hafta"], "12 ay ≈ 52 hafta."),
]

S_SAGLIK = [
    ("Organik hayvan sağlığında öncelik nedir?", "Hastalığı önlemek (koruyucu tedbir)", ["Antibiyotikle tedavi",
     "Hormon kullanmak", "Hasta hayvanı satmak"], "Koruyucu tedbirler ve koruyucu hekimlik."),
    ("Hasta hayvanda organikte önce hangi tedaviler tercih edilir?", "Fitoterapi ve homeopati gibi alternatif yöntemler",
     ["Geniş spektrumlu antibiyotik", "Hormon", "Tedavi etmemek"], "Kalıntı bırakmayan yöntemler."),
    ("Alternatif tedavi yetersiz kalırsa ne yapılır?", "Yetkili kuruluşun izniyle kontrollü kimyasal ilaç, kayıt altında",
     ["Hayvan tedavisiz bırakılır", "Hormon verilir", "Hayvan konvansiyonel sürüye satılır"], "Hayvan acı çekmemelidir."),
    ("Bir yılda kaçtan fazla kimyasal ilaç kürü alan hayvanın ürünü organik satılamaz?", "3", ["1", "5", "10"],
     "Verimli ömrü 1 yıldan kısaysa 1."),
    ("Verimli ömrü bir yıldan kısa hayvanlarda kür sınırı nedir?", "1'den fazla kür alırsa organik satılamaz", ["3'ten fazla",
     "5'ten fazla", "Sınır yoktur"], "Ders notu."),
    ("Kür sınırına hangisi sayılmaz?", "Aşı uygulamaları", ["Antibiyotik kürü", "Kimyasal sentezlenmiş ilaç", "Sentetik ağrı kesici"],
     "Aşı, parazit tedavisi ve zorunlu programlar sayılmaz."),
    ("Organikte ilaç bekleme süresi nasıl belirlenir?", "Yasal sürenin iki katı, en az 48 saat", ["Yasal sürenin yarısı",
     "Hiç beklenmez", "Her zaman 7 gün"], "AB kuralıyla uyumlu."),
    ("Yasal bekleme süresi 3 gün olan ilaçta organik bekleme süresi nedir?", "6 gün", ["3 gün", "2 gün", "12 gün"], "2 × 3 = 6 gün."),
    ("Yasal bekleme süresi 12 saat olan ilaçta organik bekleme süresi nedir?", "48 saat", ["24 saat", "12 saat", "6 saat"],
     "2 × 12 = 24 < 48 → en az 48 saat."),
    ("Hangisi organikte rutin olarak yapılmaz?", "Boynuz çıkarma", ["Tırnak bakımı", "Aşılama", "Yapağı kırkımı"], "Bedene müdahale yasakları."),
    ("Koyunlarda kuyruğu elastik bantla boğma organikte...", "Yapılmaz", ["Önerilir", "Zorunludur", "Kuzularda serbesttir"],
     "Ders notu."),
    ("Domuz yavrularında diş kesme organikte...", "Yapılmaz", ["Zorunludur", "Önerilir", "Doğumda yapılır"], "Ders notu."),
    ("Kızgınlığı uyarmak için hormon kullanımı organikte...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnız koyunda serbesttir"],
     "Ders notu."),
    ("Koruyucu amaçla antibiyotik kullanımı organikte...", "Yasaktır", ["Serbesttir", "Önerilir", "Yalnızca buzağıda serbesttir"],
     "Önleyici kullanım yok."),
    ("Barınak hijyeni neden önemlidir?", "Çapraz enfeksiyon ve hastalık taşıyıcıları önlemek için", ["Ürün rengini değiştirmek için",
     "Hayvanı büyütmek için", "Hiç önemli değildir"], "Ders notu."),
    ("Barınakta düzenli uzaklaştırılması gerekenler hangileridir?", "İdrar, gübre, artık ve saçılmış yem", ["Yalnızca saman",
     "Yalnızca su", "Hiçbiri"], "Ders notu."),
    ("Organikte tedaviler neden kayda geçirilir?", "Kür sayısı, bekleme süresi ve denetim için", ["Satış fiyatı için", "Vergi için",
     "Gerekmez"], "Kayıt şart."),
    ("Kür sınırı aşılan hayvana ne olur?", "Yeniden geçiş sürecine alınır", ["Ödüllendirilir", "Hemen kesilir", "Hiçbir şey olmaz"],
     "Ders notu."),
    ("Homeopatinin hayvanlardaki etkisiyle ilgili bilimsel kanıt için en doğru ifade hangisidir?", "Plasebodan üstün etkisi gösterilememiştir",
     ["Antibiyotikten güçlüdür", "Tüm hastalıkları tedavi eder", "Hiç araştırılmamıştır"], "Mevzuat öncelik verse de kanıt zayıftır."),
    ("Organik hayvancılıkta hasta hayvanın tedavisi neden geciktirilmemelidir?", "Hayvan acı çekmemelidir", ["Ürün fiyatı düşmesin diye",
     "Kayıt tutmamak için", "Geciktirilmesi önerilir"], "Primum non nocere."),
    ("İbik ve gaga kesme organikte...", "Rutin olarak yapılmaz", ["Zorunludur", "Her tavukta yapılır", "Horozda zorunludur"],
     "Ders notu."),
    ("Büyüme ya da verimi uyarıcı maddeler organikte...", "Kullanılmaz", ["Serbesttir", "Yalnız sütte serbesttir", "Önerilir"],
     "Antibiyotik, koksidiyostat vb."),
    ("Bir inek bir yılda 2 antibiyotik kürü ve 3 aşı aldı. Sütü organik satılabilir mi?", "Evet, bekleme süresi dolunca",
     ["Hayır, 5 tedavi aldı", "Hayır, aşı yasak", "Hiçbir zaman"], "Aşı sayılmaz: 2 ≤ 3."),
    ("Bir etlik piliç sürüsü 2 kez antibiyotik kürü aldı. Eti organik satılabilir mi?", "Hayır, ömrü 1 yıldan kısa, sınır 1",
     ["Evet", "Evet, 3'ten az olduğu için", "Evet, aşı sayılırsa"], "Verimli ömrü kısa hayvanlarda sınır 1."),
    ("Organikte aşı uygulaması...", "Veteriner hekim önerisiyle yapılabilir", ["Yasaktır", "Yalnız kesimden önce yapılır",
     "Kür sayısına eklenir"], "Hijyenik tedbirlerden."),
    ("İstisnai olarak bir bedene müdahale işlemine izin verilirse hangi şart aranır?", "Kuruluş izni, uygun yaş ve anestezi/ağrı kesici",
     ["Hiçbir şart yok", "Yalnız bakıcı onayı", "Yalnız gece yapılması"], "Acıdan kaçınmak kesin şarttır."),
    ("Zorunlu hastalık eradikasyon programındaki ilaç uygulaması kür sayısına...", "Eklenmez", ["Eklenir", "İki kür sayılır",
     "Üç kür sayılır"], "Ders notu."),
    ("Yasal bekleme süresi 10 gün olan ilaçta organik bekleme süresi nedir?", "20 gün", ["10 gün", "48 saat", "5 gün"], "2 × 10."),
    ("Organikte fitoterapi nedir?", "Bitkisel preparatlarla tedavi", ["Hormonla tedavi", "Işıkla tedavi", "Ameliyat"], "Alternatif tedavi."),
    ("Hayvan sağlığının korunmasında organikte hangisi yer almaz?", "Rutin antibiyotikli yem", ["Aşı", "Dezenfeksiyon", "Uygun ırk seçimi"],
     "Koruyucu antibiyotik yok."),
]

S_TASIMA = [
    ("Organik hayvanların nakli sırasında sakinleştirici kullanılır mı?", "Hayır", ["Evet, her zaman", "Yalnızca uzun yolda",
     "Yalnızca sığırda"], "Ders notu."),
    ("Kara taşımacılığında kaç saatte bir mola verilmelidir?", "8 saatte bir", ["2 saatte bir", "24 saatte bir", "Mola gerekmez"],
     "Yemleme, sulama, dinlenme."),
    ("12 saatlik bir yolculukta en az kaç mola gerekir?", "1", ["0", "2", "3"], "8. saatte bir mola."),
    ("20 saatlik bir yolculukta en az kaç mola gerekir?", "2", ["1", "3", "0"], "8. ve 16. saatlerde."),
    ("Organik ve konvansiyonel hayvanların kesimi nasıl yapılmalıdır?", "Ayrı kesimhanede ya da aynı yerde farklı zamanda",
     ["Aynı anda, aynı hatta", "Konvansiyonel önce, karışık", "Fark etmez"], "Ders notu."),
    ("Taşıma hangi ilkeye göre planlanır?", "En az stres ve en kısa süre", ["En çok hayvan, en ucuz araç", "En uzun mola",
     "Gece ve sakinleştiriciyle"], "Hayvan etiği."),
    ("Organik tarımda kayıt tutmanın önemi nedir?", "Çok önemlidir; denetim ve izlenebilirlik için", ["Önemsizdir", "Yalnız vergide gerekir",
     "Yalnız büyük işletmede gerekir"], "Sertifikalı, kontrollü sistem."),
    ("98/58/EC'ye göre ölüm ve tedavi kayıtları kaç yıl saklanır?", "3 yıl", ["1 yıl", "10 yıl", "6 ay"], "AB direktifi."),
    ("Davranış notuna göre piliçler kesimde neden elektrikle bayıltılmalıdır?", "Çırpınmayla kemik kırılması ve göğüs ezilmesini önlemek için",
     ["Eti renklendirmek için", "Hızlı soğutmak için", "Tüyü yumuşatmak için"], "Kesim kayıpları."),
    ("Piliçlerin yakalanması ve nakli sırasında berelenme oranı ne zaman artar?", "Sıcak havada ve ağır hayvanlarda",
     ["Soğuk havada ve hafif hayvanlarda", "Hiç artmaz", "Yalnızca gece"], "%3 ve üzeri."),
    ("Organik ürün olduğunu gösteren tek güvence hangisidir?", "Sertifika", ["'Köy' yazısı", "'Doğal' yazısı", "'Özgür' yazısı"],
     "Ders notu."),
    ("Organik hayvancılığa karar verirken sorulacak sorulardan biri hangisidir?", "Yeterli yem ya da yan ürün var mı?",
     ["Komşum ne yapıyor?", "En ucuz ilaç hangisi?", "Kafes nereden alınır?"], "Karar verme slaytları."),
    ("Karar verirken 'Gübreyi uygun şekilde kullanabilir miyim?' sorusu neden önemlidir?", "Kapalı döngü ve 170 kg N sınırı için",
     ["Gübre satmak yasak olduğu için", "Önemsizdir", "Ambalaj için"], "Döngü."),
    ("Karar verirken pazar sorusu neyi sorgular?", "Ürünlerimi satın alacak birileri var mı", ["Hayvan ırkını", "Ahır rengini",
     "Kesim yöntemini"], "Ders notu."),
    ("Organik hayvan kesiminde hangisi istenir?", "Hayvana stres yaratmayan davranış ve uygun yöntem", ["Hızlı ve sert muamele",
     "Sakinleştirici", "Konvansiyonellerle karışık kesim"], "Ders notu."),
    ("Kayıtta hangisi yer almalıdır?", "Tedaviler, ilaçlar ve bekleme süreleri", ["Bakıcının hobileri", "Komşunun hayvan sayısı",
     "Hava durumu tahmini"], "Sağlık kayıtları."),
    ("Kayıtlarda yem için hangi bilgi tutulur?", "Kaynağı, miktarı ve organik belgesi", ["Yalnızca rengi", "Yalnızca fiyatı",
     "Hiçbiri"], "İzlenebilirlik."),
    ("Konvansiyonelden alınan hayvanlar için hangi kayıt gerekir?", "Nereden ve kaç yaşında alındığı", ["Yalnızca adı",
     "Yalnızca rengi", "Hiçbiri"], "Yaş sınırlarını kanıtlamak için."),
    ("4 saatlik bir yolculukta mola gerekir mi?", "Hayır", ["Evet, 2", "Evet, 1", "Evet, 4"], "8 saatten kısa."),
    ("Organik tarımın üç temel niteliği nedir?", "Sertifikalı, kontrollü, kurallı", ["Ucuz, hızlı, kolay", "Kapalı, karanlık, sıkışık",
     "Serbest, belgesiz, denetimsiz"], "Ders notu."),
    ("Hayvan nakli neden kısa tutulmalıdır?", "Stres, yaralanma ve kayıpları azaltmak için", ["Yakıt fiyatı için", "Etin rengi için",
     "Gerek yoktur"], "Hayvan etiği."),
    ("Karar verirken 'Hayvanlar mahsullerimi nasıl etkiler?' sorusu neyi gösterir?", "Bitkisel ve hayvansal üretimin bütünleşmesini",
     ["Hayvanların bitkiden ayrı olduğunu", "Mahsulün önemsiz olduğunu", "Gübrenin satılacağını"], "Döngü düşüncesi."),
    ("Karar verirken iş gücü sorusu neden önemlidir?", "Organik sistem daha çok emek ve bakım ister", ["İş gücüne gerek yoktur",
     "Makineler her şeyi yapar", "Yalnız kesimde gerekir"], "Ad libitum, mera, kayıt, alternatif tedavi."),
    ("'Fiyat bu çabaya değer mi?' sorusu neyi tartar?", "Ek maliyet ile ek gelir dengesini", ["Hayvan rengini", "Irk adını",
     "Mevsimi"], "Ekonomik karar."),
    ("Organik ve konvansiyonel hayvanlar aynı kesimhanede kesilecekse ne yapılır?", "Farklı zamanlarda kesilir", ["Aynı anda kesilir",
     "Karıştırılır", "Kesilemez"], "Ders notu."),
    ("28 saatlik bir yolculukta en az kaç mola gerekir?", "3", ["2", "4", "1"], "8, 16, 24. saatler."),
    ("Hangi etiket sertifikasız bir üründe organik anlamı taşımaz?", "Kafessiz", ["Organik logosu ve sertifika numarası",
     "Kontrol kuruluşunun kodu", "Sertifika belgesi"], "Doğal, kafessiz, köy, özgür, gezen."),
    ("Taşıma sırasındaki molalarda ne yapılır?", "Yemleme, sulama ve dinlendirme", ["Sakinleştirici verilir", "Hayvanlar karıştırılır",
     "Hiçbir şey yapılmaz"], "Ders notu."),
]

S_REFAH = [
    ("1960–70'lerde hayvan refahı nasıl tanımlanıyordu?", "Stres yoksa refah iyi, stres varsa zayıf", ["Hayvanların duyguları vardır",
     "Ruhsal sağlık önemlidir", "Hiç tanımlanmamıştı"], "Bugün duygular ve ruhsal sağlık da katıldı."),
    ("Bugünkü refah anlayışına göre hangisi doğrudur?", "Hayvanların duyguları vardır; ruhsal sağlık da önemlidir",
     ["Yalnız stres önemlidir", "Yalnız verim önemlidir", "Refah ölçülemez"], "Ders notu."),
    ("Hangisi iyi refahın göstergesidir?", "Doğal davranışlarını tam gösterebilmesi", ["Anormal davranışların artması",
     "Bağışıklığın zayıflaması", "Yaşam süresinin kısalması"], "Ders notu."),
    ("Hangisi zayıf refahın göstergesidir?", "Anormal davranışların artması", ["Çevresiyle uyum", "Duygularını ifade etmesi",
     "Ağrısız uyum"], "Ders notu."),
    ("Brambell Komitesi hangi yıl hayvan özgürlüklerini sıraladı?", "1965", ["1993", "1979", "2008"], "İngiltere."),
    ("Brambell listesinin odağı nedir?", "Hareket özgürlüğü (dönme, kalkma, yatma, gerinme)", ["Yem miktarı", "Ürün fiyatı",
     "Kesim yöntemi"], "İlk liste hareketle ilgilidir."),
    ("Beş özgürlükten biri hangisidir?", "Korku ve stresten uzak olma", ["En yüksek verimi verme", "Kafeste yaşama",
     "Zorla beslenme"], "FAWC."),
    ("Beş özgürlük ilk kez hangi yıl açıklandı?", "1979", ["1965", "1993", "2010"], "FAWC 1979; 1993'te son biçim. Notta 1993."),
    ("'Normal davranışı gösterme özgürlüğü' için ne sağlanmalıdır?", "Yeterli alan, uygun araç ve aynı türden arkadaşlar",
     ["Bireysel kafes", "Sürekli karanlık", "Bağlama"], "Ders notu."),
    ("Suluğun bozulup hayvanların susuz kalması hangi özgürlüğü çiğner?", "Açlık ve susuzluktan özgürlük", ["Korku ve stresten",
     "Rahatsızlıktan", "Normal davranış"], "Birinci özgürlük."),
    ("Topallayan ineğin tedavi edilmemesi hangi özgürlüğü çiğner?", "Acı, yaralanma ve hastalıktan özgürlük", ["Açlıktan",
     "Normal davranış", "Rahatsızlıktan"], "Üçüncü özgürlük."),
    ("Kafeste kanat çırpamayan tavuk hangi özgürlükten yoksundur?", "Normal davranışı gösterme", ["Açlıktan", "Acıdan",
     "Susuzluktan"], "Dördüncü özgürlük."),
    ("Bakıcının hayvanlara vurması hangi özgürlüğü çiğner?", "Korku ve stresten özgürlük", ["Açlıktan", "Rahatsızlıktan",
     "Normal davranış"], "Beşinci özgürlük."),
    ("Islak, çamurlu zeminde yatacak kuru yer olmaması hangi özgürlüğü çiğner?", "Rahatsızlıktan özgürlük", ["Açlıktan",
     "Korkudan", "Normal davranış"], "İkinci özgürlük."),
    ("98/58/EC'ye göre çiftlik hayvanları en az ne sıklıkla kontrol edilmelidir?", "Günde 1 kez", ["Haftada 1 kez", "Ayda 1 kez",
     "Yılda 1 kez"], "Bütün çiftlik hayvanları."),
    ("Barınaktaki buzağılar günde en az kaç kez kontrol edilmelidir?", "2", ["1", "4", "Haftada 1"], "Dışarıdakiler en az 1."),
    ("AB kuralına göre buzağılar günde en az kaç kez yemlenmelidir?", "2", ["1", "4", "6"], "Buzağı direktifi."),
    ("Buzağılar için yapay aydınlatma süresi en az neye denk olmalıdır?", "09.00–17.00 arası doğal ışık süresine", ["24 saate",
     "2 saate", "Gece yarısına kadar"], "Sürekli karanlıkta tutulmazlar."),
    ("AB buzağı kurallarına göre buzağılar...", "Bağlanmamalıdır", ["Sürekli bağlı tutulmalıdır", "Karanlıkta tutulmalıdır",
     "Tek öğün yemlenmelidir"], "Ders notu."),
    ("Mekanik havalandırma kullanılan buzağı ahırında ne bulunmalıdır?", "Arıza alarm sistemi", ["Sakinleştirici", "UV lamba",
     "Kafes"], "Ders notu."),
    ("Etlik piliçlerin refahını düzenleyen AB direktifi hangisidir?", "2007/43/EC", ["1999/74/EC", "2008/119/EC", "2008/120/EC"],
     "Ders notu."),
    ("Yumurta tavuklarını düzenleyen ve artık yürürlükte olmayan direktif hangisidir?", "88/166/EEC", ["1999/74/EC", "2007/43/EC",
     "98/58/EC"], "Yerini 1999/74/EC aldı."),
    ("Domuz refahını düzenleyen güncel AB direktifi hangisidir?", "2008/120/EC", ["2008/119/EC", "2007/43/EC", "1999/74/EC"], "Ders notu."),
    ("Çiftlik hayvanlarının korunmasına ilişkin Avrupa Sözleşmesi hangi yıl kabul edildi?", "1976", ["1965", "1998", "2008"],
     "Avrupa Konseyi."),
    ("Entansif sistemde gaga kesimi gibi uygulamaların gerekçesi neydi?", "Hijyen, ölüm oranı ve yem tüketimi", ["Hayvan refahı",
     "Doğal davranış", "Organik sertifika"], "Ama refahı düşürdü."),
    ("Refah sorunlarının çoğu neyle ilgilidir?", "Çevreyle", ["Irk adıyla", "Bakıcının yaşıyla", "Ürün fiyatıyla"], "Ders notu."),
    ("Sığır ve koyunun uzun süre çamurlu, ıslak zeminde tutulması neye yol açar?", "Ayak sorunlarına", ["Yapağı kalitesinin artmasına",
     "Süt yağının artmasına", "Hiçbir şeye"], "Yönetim hatası."),
    ("Zayıf refahta bağışıklık sistemi nasıl etkilenir?", "Yetersiz kalır", ["Güçlenir", "Değişmez", "Kaybolmaz"], "Ders notu."),
    ("98/58/EC'ye göre hayvan bakımı kim tarafından yapılmalıdır?", "Bilgili personel", ["Herhangi biri", "Yalnız veteriner",
     "Yalnız çiftlik sahibi"], "Ders notu."),
    ("Her buzağı doğumdan sonra ne zaman kolostrum almalıdır?", "En kısa sürede", ["Bir hafta sonra", "Sütten kesimde",
     "Hiç almamalı"], "Buzağı direktifi."),
]

S_ETHOLOJI = [
    ("Etholoji nedir?", "Hayvan davranışını biyolojik olarak inceleyen bilim", ["Hayvan beslemesi", "Hayvan ıslahı", "Hayvan anatomisi"],
     "Tinbergen'in tanımı."),
    ("Etholojiye önceleri ne ad verilirdi?", "Karakter bilimi", ["Davranış ekonomisi", "Hayvan fiziği", "Zootekni"], "Ders notu."),
    ("Etholoji hangi yıl Nobel ödülüyle bilim dalı olarak tescillendi?", "1973", ["1972", "1965", "1859"],
     "Notta 1972 yazıyor; doğrusu 1973."),
    ("1973 Nobel ödülünü alan etholog üçlü hangisidir?", "Lorenz, Tinbergen, von Frisch", ["Darwin, Mendel, Pavlov",
     "Brambell, Harrison, Webster", "Watson, Crick, Wilkins"], "Fizyoloji veya Tıp."),
    ("Türlerin Kökeni kitabının yazarı kimdir?", "Charles Darwin", ["Konrad Lorenz", "Karl von Frisch", "Niko Tinbergen"],
     "Etholojiye büyük katkı."),
    ("Doğuştan gelen, istemsiz ve otomatik yanıta ne denir?", "Refleks", ["Şartlı refleks", "Öğrenme", "Yer değiştirme aktivitesi"],
     "Ders notu."),
    ("Sağım makinesinin sesini duyunca süt indirmeye başlayan inek hangi davranışı gösterir?", "Şartlı refleks", ["İçgüdü",
     "Refleks", "Flehmen"], "Deneyimle öğrenilmiş."),
    ("Aynı türün bireylerinde aynı biçimde görülen, kalıtsal iç eğilime ne denir?", "İçgüdü", ["Öğrenme", "Güdü", "Şartlı refleks"],
     "Ders notu."),
    ("Davranışı başlatan, yönünü ve sürekliliğini belirleyen içsel güç nedir?", "Güdü", ["Refleks", "Hormon", "Feromon"], "Ders notu."),
    ("İki zıt güdü arasında kalan hayvanın ilgisiz bir davranış göstermesine ne denir?", "Yer değiştirme aktivitesi",
     ["Şartlı refleks", "Gagalama düzeni", "Flehmen"], "Displacement."),
    ("Ana-yavru tanımasında, emme ve yalamada hangi duyu öne çıkar?", "Dokunma", ["Tat alma", "Görme", "İşitme"], "Ders notu."),
    ("Feromonlar hangi duyu ile algılanır?", "Koklama", ["Görme", "İşitme", "Dokunma"], "Ders notu."),
    ("Fotoperiyot hangi duyu ile ilişkilidir?", "Görme", ["Tat", "Koku", "Dokunma"], "Işık süresi ve çiftleşme düzeni."),
    ("Seçici otlama ve yem tercihinde hangi duyu önemlidir?", "Tat alma", ["İşitme", "Görme", "Dokunma"], "Ders notu."),
    ("Dış ortamdan gelen uyarıları algılayan alıcılara ne denir?", "Eksteroseptör", ["İnteroseptör", "Aktivatör", "Hormon"],
     "Duyu organlarında."),
    ("Kas, tendon ve iç organlardaki alıcılara ne denir?", "İnteroseptör", ["Eksteroseptör", "Feromon", "Korteks"], "Ders notu."),
    ("Beynin tabanında yer alan ve hipofizi yöneten bölüm hangisidir?", "Hipotalamus", ["Serebral korteks", "Epifiz", "Tiroid"],
     "Ders notu."),
    ("Görme, işitme ve koku merkezleri beynin hangi bölümündedir?", "Serebral korteks", ["Hipotalamus", "Omurilik", "Hipofiz"],
     "Ders notu."),
    ("Süt indirmeyi (salıverme) sağlayan hormon hangisidir?", "Oksitosin", ["Prolaktin", "Testosteron", "Melatonin"],
     "Notta prolaktin yazıyor; doğrusu oksitosin."),
    ("Prolaktinin temel görevi nedir?", "Süt sentezi ve analık davranışı", ["Süt indirme", "Kızgınlık", "Kaç ya da savaş"],
     "Ön hipofiz hormonu."),
    ("Dişide kızgınlık davranışını oluşturan hormon hangisidir?", "Östrojen", ["Oksitosin", "Adrenalin", "T4"],
     "Düzeyi en yüksekken kızgınlık."),
    ("Tehlike karşısında kaçma ya da saldırma davranışını hangi hormon artırır?", "Adrenalin", ["Prolaktin", "Östrojen", "Melatonin"],
     "Adrenal medulla."),
    ("Gün uzunluğuna göre salgılanıp mevsimsel üremeyi düzenleyen hormon hangisidir?", "Melatonin", ["Oksitosin", "Testosteron",
     "ADH"], "Epifiz."),
    ("Testosteron düzeyi belli bir eşiğin üzerine çıkarsa cinsel davranış nasıl değişir?", "Değişmez", ["İki katına çıkar",
     "Tamamen durur", "Dişi davranışına döner"], "Belli düzey yeterlidir."),
    ("Ön hipofizden salgılanan ve üreme davranışında etkili hormonlar hangileridir?", "FSH ve LH", ["Oksitosin ve ADH",
     "T3 ve T4", "Adrenalin ve noradrenalin"], "Ders notu."),
    ("Hayvan davranışını bilmesi gerekenler arasında hangisi yer alır?", "Ekipman tasarımcıları", ["Yalnız veteriner hekimler",
     "Yalnız kasaplar", "Hiç kimse"], "Ders notu listesi."),
    ("Davranış bilgisinin faydalarından biri hangisidir?", "Kavga ve yaralanma riskini azaltmak", ["Hormon kullanmayı artırmak",
     "Alanı daraltmak", "Kaydı azaltmak"], "Ders notu."),
    ("Yoğun hayvancılığın kritik noktası nedir?", "Hayvanın fizyolojik ve davranışsal uyum sağlayabilmesi", ["Ürün fiyatı",
     "Bakıcı sayısı", "Ahır rengi"], "Ders notu."),
    ("Kısa gün üreyeni koyunda günler kısalınca artan melatonin ne yapar?", "Üreme mevsimini başlatır", ["Üremeyi durdurur",
     "Süt indirir", "Kaç ya da savaş tepkisi"], "Atta etkisi terstir."),
    ("Emme uyarısı hipotalamus aracılığıyla hangi hormonu artırarak süt indirir?", "Oksitosin", ["Testosteron", "T4", "Melatonin"],
     "Uyarı → hipotalamus → oksitosin."),
    ("Hayvanların kendisini yetiştiren insanla ilişkisi için notta ne denir?", "Birbirlerini etkilemişlerdir", ["Hiç etkileşmemişlerdir",
     "Yalnız insan etkilenmiştir", "Yalnız hayvan etkilenmiştir"], "Ders notu."),
]

S_CEVRE = [
    ("Barınak içi çevre hangilerini doğrudan etkiler?", "Refah, sağlık ve verimi", ["Yalnızca ürün fiyatını", "Yalnızca rengini",
     "Hiçbirini"], "Ders notu."),
    ("Dar yaşam alanı neye yol açabilir?", "Oburluk ve aşırı yağlanma", ["Hızlı kas gelişimi", "Daha çok egzersiz", "Hiçbir şeye"],
     "Ders notu."),
    ("Küçük hayvanlarda yüzey/ağırlık oranı nasıldır?", "Büyüktür; termoregülasyona daha çok enerji harcanır", ["Küçüktür",
     "Büyük hayvanla aynıdır", "Ölçülemez"], "Ders notu."),
    ("Büyük hayvanlarda termoregülasyon için harcanan enerji nasıldır?", "Daha azdır", ["Daha fazladır", "Sıfırdır", "Sonsuzdur"],
     "Yüzey/ağırlık oranı küçük."),
    ("Mikroorganizmaların üremesini sınırlamak için uygun bağıl nem nedir?", "%50–60", ["%10–20", "%80–90", "%95–100"], "Ders notu."),
    ("Bağıl nem yüksek olursa ne olur?", "Amonyak artar, yem ve altlık küflenir", ["Toz artar", "Solunum yolu kurur", "Hiçbir şey olmaz"],
     "Ders notu."),
    ("Bağıl nem düşük olursa ne olur?", "Toz artar, solunum yolları tahriş olur", ["Amonyak artar", "Altlık küflenir", "Boğulma olur"],
     "Ders notu."),
    ("Birçok laboratuvar hayvanı ısıyı nasıl atar?", "Solunum hızını artırarak", ["Terleyerek", "Kıl dökerek", "Uyuyarak"],
     "Terleme yeteneği yok."),
    ("Hayvan barınaklarında işitmeye fiziksel zarar veren gürültü düzeyi nedir?", "95 dB ve üstü", ["40 dB", "60 dB", "20 dB"],
     "Ders notu."),
    ("Sese duyarlı ve az duyarlı türler için ne önerilir?", "Aynı binada tutulmamaları", ["Aynı odada tutulmaları",
     "Gürültüye alıştırılmaları", "Kulaklarının kapatılması"], "Ders notu."),
    ("Barınak aydınlatmasında doğru ışık kaynağı hangisidir?", "Floresan ya da LED", ["UV lamba", "Kızılötesi lazer", "Mum"],
     "Notta 'UV' yazıyor; bu yanlış. UV dezenfeksiyon içindir."),
    ("UV lambaların hayvan barınağındaki doğru kullanımı nedir?", "Dezenfeksiyon", ["Genel aydınlatma", "Isıtma", "Sulama"],
     "Uzun süre UV göz ve deriye zararlıdır."),
    ("Havalandırmanın görevlerinden biri hangisidir?", "Zehirli gaz, koku, toz ve etkenleri uzaklaştırmak", ["Yem vermek",
     "Hayvanları saymak", "Gürültü üretmek"], "Ders notu."),
    ("Havalandırma miktarını belirleyen etkenlerden biri hangisidir?", "Hayvan türü ve sayısı", ["Bakıcının adı", "Yem markası",
     "Haftanın günü"], "Ayrıca ısı yükü, yalıtım, hacim."),
    ("Hayvan-hayvan etkileşiminin faydası nedir?", "Sosyal davranışların gelişmesi", ["Daha çok yaralanma", "Yem kapma",
     "Stresin artması"], "Toplanma, oyun."),
    ("Hayvan-hayvan etkileşiminin zararı nedir?", "Güçlülerin zayıfların yemine saldırması", ["Sosyal gelişim", "Oyun",
     "Dostluk"], "Ders notu."),
    ("Hayvanlar ne zaman birlikte yaşamaya başlarsa birbirlerine daha dostça davranır?", "Ne kadar erken başlarlarsa",
     ["Ne kadar geç başlarlarsa", "Hiç fark etmez", "Yalnız yetişkinken"], "Ders notu."),
    ("Doğumdan beri kendisiyle ilgilenen bakıcıya karşı sıcakkanlı hayvan nasıl davranır?", "Tanır ve saldırmaz",
     ["Saldırır", "Kaçar", "Tanımaz"], "Yabancılara saldırgan olabilir."),
    ("Yavruların erken dönemde elle tutulmasının etkisi nedir?", "Ergin dönem fizyolojisi ve davranışını önemli ölçüde etkiler",
     ["Hiç etkisi yoktur", "Yalnız rengini değiştirir", "Yalnız boyunu etkiler"], "Ders notu."),
    ("Barınak aydınlatmasında neye dikkat edilir?", "Süre, şiddet, renk ve tüm hayvanların eşit ışık alması", ["Yalnız lamba fiyatı",
     "Yalnız lamba sayısı", "Hiçbir şey"], "Ders notu."),
    ("Işık hayvanda hangi işlevi düzenler?", "Üreme ve günlük ritim (hormonal mekanizma)", ["Yalnız yem rengi",
     "Yalnız su sıcaklığı", "Hiçbiri"], "Ders notu."),
    ("Barınak sıcaklığı ayarlanırken neye dikkat edilir?", "Beden sıcaklığı ve vücut iriliği", ["Yalnız mevsim adı", "Bakıcının tercihi",
     "Yem fiyatı"], "Ders notu."),
    ("Hayvanın tüm metabolik işlevlerini sürdürebildiği sıcaklığa ne denir?", "Beden sıcaklığı", ["Oda sıcaklığı",
     "Çiy noktası", "Kaynama noktası"], "Ders notu."),
    ("Barınak içi sıcaklığı düşürmek için ne önerilir?", "İyi havalandırma ve ortamda su bulundurmak", ["Pencereleri kapatmak",
     "Yoğunluğu artırmak", "Işığı artırmak"], "Ders notu."),
    ("Personel odaları ve gürültülü işler hayvanlara göre nerede olmalıdır?", "Uzakta", ["Hemen yanında", "Aynı odada",
     "Fark etmez"], "Ders notu."),
    ("Barınağı etkileyen fiziksel faktörlerden biri hangisidir?", "Nem", ["Pazar fiyatı", "Irk adı", "Kesim yeri"], "8 faktör."),
    ("Havalandırma ile ilgili hangisi doğrudur?", "Sıcaklık ve nemi çok değiştirmemelidir", ["Sıcaklığı hızla düşürmelidir",
     "Nemi %95'e çıkarmalıdır", "Gerekli değildir"], "Ders notu."),
    ("Kötü muamele ve uyumsuz bakıcılar neyi bozar?", "Hayvan davranışı ve deney (üretim) sonuçlarını", ["Yalnız ahır rengini",
     "Hiçbir şeyi", "Yalnız yem fiyatını"], "Ders notu."),
    ("Barınak tanımında hangisi yer alır?", "Hayvanı düşman ve hastalık etkenlerinden korur", ["Hayvanı satışa hazırlar",
     "Hayvanı kafeste tutar", "Yemi saklar"], "Ders notu."),
]

S_TUR = [
    ("Sığırların günlük otlama mesafesi yaklaşık ne kadardır?", "4 km", ["40 km", "0,4 km", "15 km"], "Ders notu."),
    ("Sığırlar günde kaç yoğun otlama dönemi gösterir?", "4", ["1", "2", "8"], "Sabah erken, öğle, öğleden sonra, gün batımı."),
    ("Sığırlar yemi ağzına nasıl alır?", "Dilini kepçe gibi kullanarak", ["Dudakla koparıp", "Dişle keserek", "Tırnakla eşeleyerek"],
     "Ders notu."),
    ("Sığırlarda günlük geviş süresi ne kadardır?", "4–9 saat", ["30 dakika", "15–20 saat", "1 saat"], "Otlama süresinin %75'i kadar."),
    ("Geviş getirme/otlama oranı hangi aralıktadır?", "0,5–1", ["2–3", "0,01–0,1", "5–10"], "Ders notu."),
    ("Buzağı doğumdan ne kadar sonra emmeye başlar?", "2–5 saat", ["2–5 gün", "Hemen 5 dakika", "1 hafta"], "Ders notu."),
    ("Büyük buzağıların birbirini emmesi neyin göstergesidir?", "Besin maddesi yetersizliği", ["Aşırı beslenme", "İyi refah", "Kızgınlık"],
     "Ders notu."),
    ("Boğalara yılda kaç aşım yaptırılır?", "50–80", ["5–8", "500–800", "1–2"], "Ders notu."),
    ("Sperma üretim merkezlerinde boğadan ne sıklıkla sperma alınır?", "Haftada bir", ["Günde üç", "Yılda bir", "Ayda bir"], "Ders notu."),
    ("Sığırda gebelik olasılığı en yüksek tohumlama zamanı nedir?", "Kızgınlık başlangıcından ≈12 saat sonra", ["Kızgınlıktan 3 gün önce",
     "Doğumdan hemen sonra", "Kızgınlık bittikten 2 gün sonra"], "Ders notu."),
    ("Kızgınlıkta olduğu hâlde belirti göstermeyen inek için ne denir?", "Sessiz kızgınlık", ["Flehmen", "Gurkluk", "Polidipsi"],
     "Ders notu."),
    ("Yeni oluşturulan besi grubunda sosyal düzen çoğunlukla ne kadar sürede oluşur?", "2 saat", ["2 ay", "2 hafta", "2 yıl"], "Ders notu."),
    ("Koyunun otu dipten koparabilmesini sağlayan özellik nedir?", "Yarık üst dudak", ["Uzun dil", "Üst kesici dişler", "Boynuzlar"],
     "Ders notu."),
    ("Koyunların günlük otlama mesafesi ne kadardır?", "3–10 km", ["0,3 km", "40–60 km", "1 km"], "Irk ve meraya göre."),
    ("Koyunlar günde yaklaşık kaç saat geviş getirir?", "8 saat", ["1 saat", "20 saat", "3 saat"], "8 dönemde."),
    ("Kuzey yarımkürede koyunların çiftleşme mevsimi hangisidir?", "Sonbahar", ["İlkbahar", "Yaz", "Kış ortası"], "Ders notu."),
    ("Koyunda kızgınlık süresi ne kadardır?", "20–30 saat", ["2–3 saat", "5–7 gün", "2 hafta"], "Ders notu."),
    ("Koç başına kaç koyun hesaplanır?", "20–30", ["2–3", "100–150", "5"], "Ders notu."),
    ("50–60 koyunluk gruba kaç koç önerilir?", "3", ["1", "2", "6"], "2 koç olursa üstün olan astı engellerken kendisi de çiftleşemez."),
    ("Ana koyun kuzusunu başlangıçta neyle tanır?", "Kokusundan", ["Renginden", "Sesinden", "Boyundan"],
     "Sonra görme ve işitme devreye girer."),
    ("Zayıf, ilgi görmeyen kuzu elden süt içirildikten sonra en geç ne zaman anasına verilmelidir?", "8 saat içinde", ["8 gün içinde",
     "Sütten kesimde", "Hiç verilmemeli"], "Ders notu."),
    ("Koyun sürüsünde lider kimdir?", "Yaşlı koyunlar", ["En genç kuzular", "Koç her zaman", "Çoban köpeği"], "Ders notu."),
    ("Keçiler otlamanın yaklaşık ne kadarını yüksekten yapar?", "%65–70", ["%5", "%30", "%100"], "Ders notu."),
    ("Tehdit karşısında keçi ve koyun nasıl davranır?", "Keçi döner ve pozisyon alır, koyun kaçar", ["İkisi de kaçar",
     "İkisi de saldırır", "Koyun döner, keçi kaçar"], "Ders notu."),
    ("Keçilerde doğum ne kadar sürer?", "½–4 saat", ["1–2 gün", "5 dakika", "1 hafta"], "Ders notu."),
    ("İki tekenin yeteceği keçi grubuna neden üç teke katılır?", "Alfa teke diğerini engellerken kendisi de çiftleşemez",
     ["Tekeler yalnız yaşayamaz", "Yönetmelik böyle ister", "Keçiler tekeyi reddeder"], "Ders notu."),
    ("Erkeğin dişinin idrarını kokladıktan sonra üst dudağını kıvırmasına ne denir?", "Flehmen", ["Gurkluk", "Ruminasyon",
     "Sessiz kızgınlık"], "Tekede belirgin."),
    ("Ağılda barındırılan keçiler ruminasyonun ne kadarını gece yapar?", "%75", ["%10", "%25", "%100"], "Ders notu."),
    ("Horozlarda çiftleşme davranışı kaç haftalıkta başlar?", "12–16 hafta", ["2–4 hafta", "40–50 hafta", "1 hafta"], "Dişilerde en erken 18."),
    ("Tavuğun kuluçkaya yatma isteğine ne denir?", "Gurkluk", ["Flehmen", "Polidipsi", "Kanibalizm"], "Ders notu."),
    ("Doğal kuluçkada tavuğun altına cüssesine göre kaç yumurta konur?", "10–15", ["2–3", "30–40", "1"], "Ders notu."),
    ("Tavukta kuluçka süresi kaç gündür?", "21", ["14", "28", "30"], "Çıkım 21. günde en yüksek (notta 20 yazar)."),
    ("Tavuklar kaç farklı sesle iletişim kurar?", "22", ["2", "12", "50"], "Civcivler 12."),
    ("Tavuklarda üstünlük sıralamasına ne ad verilir?", "Gagalama düzeni", ["Lineer hiyerarşi", "Anaerkil düzen", "Flehmen"], "Ders notu."),
    ("Yumurta tavuğunda günlük aydınlatma en çok kaç saat olmalıdır?", "17", ["24", "10", "8"], "Ders notu."),
    ("28 saatlik aydınlatma döngüsünde haftada kaç döngü olur?", "6", ["7", "4", "28"], "168 ÷ 28 = 6."),
    ("28 saatlik aydınlatma döngüsünün yumurtaya etkisi nedir?", "Sayı biraz azalır, büyüklük artar", ["Sayı artar, büyüklük azalır",
     "Hiç etkisi yoktur", "Yumurtlama durur"], "Ders notu."),
    ("Folluk girişi tercihen hangi şekilde olmalıdır?", "Üçgen", ["Kare", "Yuvarlak", "Altıgen"], "Ders notu."),
    ("Etlik piliçler yemliğe en çok ne kadar uzaklıkta olmalıdır?", "2 m", ["20 m", "10 m", "50 cm altı olmamalı"], "Ders notu."),
    ("Kümes tabanındaki altlık derinliği folluk dışına yumurtlamayı önlemek için en çok ne kadar olmalıdır?", "7–8 cm",
     ["30 cm", "50 cm", "1 m"], "Ders notu."),
]

S_BOZUKLUK = [
    ("Kuyruk ısırma en çok hangi türde görülür?", "Domuz", ["Sığır", "Tavuk", "Keçi"], "Ders notu."),
    ("Kanibalizm (yamyamlık) en çok hangi türde görülür?", "Tavuk", ["Koyun", "Sığır", "At"], "Ders notu."),
    ("Dil oynatma hangi türde görülen bir davranış bozukluğudur?", "Sığır", ["Tavuk", "Domuz", "Koyun"], "Ders notu."),
    ("Yapağı ısırma hangi türde görülür?", "Koyun", ["Domuz", "Tavuk", "Sığır"], "Ders notu."),
    ("Kloak gagalama daha çok hangi dönemde görülür?", "Yumurtlamaya başlamak üzere olan piliçlerde", ["Civcivlikte",
     "Kesim öncesi horozlarda", "Kuluçkada"], "Hormon değişimi."),
    ("Kloak gagalamaya karşı önerilen önlem hangisidir?", "Kümeste ışık şiddetini düşürmek", ["Işığı artırmak",
     "Yoğunluğu artırmak", "Suyu kesmek"], "Ders notu."),
    ("Polidipsi nedir?", "Aşırı su içme", ["Aşırı yem yeme", "Yumurta yeme", "Tüy yolma"], "Kafes tavukçuluğunda."),
    ("Polidipsiyi önlemek için ne önerilir?", "Yemliği sık karıştırıp dikkati yeme çekmek", ["Suyu tamamen kesmek",
     "Işığı 24 saat açmak", "Gaga kesmek"], "Ders notu."),
    ("Yumurta yemeyi başlatan etkenlerden biri hangisidir?", "Besin eksikliği ya da yetersiz grid", ["Fazla alan", "Loş folluk",
     "Yumurtaların hemen toplanması"], "Ders notu."),
    ("Yumurta yemeyi önlemek için folluklar nasıl olmalıdır?", "Loş", ["Çok parlak", "Kapısız", "Kümesin ortasında ve aydınlık"],
     "Ders notu."),
    ("Organikte yumurta yemeye karşı 'gaga kesimi' önerilebilir mi?", "Hayır, rutin olarak yasaktır", ["Evet, zorunludur",
     "Evet, tüm sürüye", "Evet, civcivlikte"], "Not konvansiyonel yaklaşımı yansıtır."),
    ("Anormal davranışlar neyin göstergesidir?", "Refahın bozulduğunun", ["İyi refahın", "Yüksek verimin", "Doğal davranışın"],
     "Ders notu."),
    ("Domuzlarda kuyruk ısırmanın organik çözümü hangisidir?", "Yeterli alan, saman ve uğraşı materyali", ["Kuyruk kesmek",
     "Diş kesmek", "Karanlıkta tutmak"], "Nedeni ortadan kaldırmak."),
    ("Dil oynatmanın olası nedeni hangisidir?", "Kaba yemin az, yeme süresinin kısa olması", ["Fazla kaba yem", "Geniş mera",
     "Ad libitum yemleme"], "Ders notu."),
    ("Tavuklarda kanibalizmi artıran etkenlerden biri hangisidir?", "Kalabalık ve aşırı ışık", ["Geniş alan", "Loş ışık",
     "Bol altlık"], "Ders notu."),
    ("Konvansiyonel tavukçulukta gaga kesimi hangi yaşta yapılır? (notta)", "5–7 günlük civcivde", ["20 haftalıkta",
     "Kesimden önce", "Kuluçkada"], "Gaganın 1/3'ü; organikte rutin değil."),
    ("Organik bakışta davranış bozukluğuna yaklaşım nedir?", "Nedenini ortadan kaldırmak", ["Belirtiyi kesip atmak",
     "Görmezden gelmek", "İlaçla bastırmak"], "Ders notu."),
    ("Yumurta yeme sürüde nasıl yayılır?", "Hızla", ["Hiç yayılmaz", "Çok yavaş", "Yalnız horozlara"], "Ders notu."),
    ("Kırık yumurtalar ve artıkları ne yapılmalıdır?", "Yok edilmelidir", ["Folluğa bırakılmalıdır", "Tavuklara verilmelidir",
     "Kümeste saklanmalıdır"], "Ders notu."),
    ("Gagasına yumurta sarısı bulaşmış tavuk için ne yapılır?", "Şüpheli olarak ayıklanır", ["Ödüllendirilir", "Folluğa konur",
     "Gagası boyanır"], "Ders notu."),
    ("Büyük buzağılarda birbirinin kulak ve göbeğini emme neye işaret eder?", "Besin yetersizliği ve karşılanmamış emme isteği",
     ["İyi refah", "Aşırı beslenme", "Kızgınlık"], "Ders notu."),
    ("Kafeste uğraşı yokluğu tavuklarda hangi bozukluğa yol açabilir?", "Polidipsi", ["Gurkluk", "Flehmen", "Sessiz kızgınlık"],
     "Nipelle oynama."),
    ("Yapağı ısırmanın olası nedeni nedir?", "Kaba yem eksikliği ve sıkışıklık", ["Fazla mera", "Yalnızlık", "Soğuk su"], "Ders notu."),
    ("Kuyruk kesmek kuyruk ısırma sorununu ne yapar?", "Gizler ama nedenini çözmez", ["Tamamen çözer", "Refahı artırır",
     "Organikte zorunludur"], "Organik bakış."),
    ("Sağlam kabuklu yumurta için uygun besleme hangi bozukluğu önlemeye yardım eder?", "Yumurta yeme", ["Dil oynatma",
     "Kuyruk ısırma", "Yapağı ısırma"], "Ders notu."),
    ("Folluk dışına yumurtlanan yumurtalar ne zaman toplanmalıdır?", "Hemen", ["Hafta sonunda", "Hiç", "Kesimde"], "Ders notu."),
    ("Entansif sistemlerde anormal davranışlar neden gelişir?", "Davranış ihtiyaçları karşılanmadığı için", ["Alan çok geniş olduğu için",
     "Mera olduğu için", "Hayvanlar organik olduğu için"], "Ders notu."),
    ("Organik sistemlerde kanibalizmi önlemek için hangisi önerilir?", "Loş ışık, altlık, açık alan ve yeterli protein",
     ["Gaga kesimi", "Kafes", "Sürekli ışık"], "Neden odaklı."),
    ("Etlik piliçlerde davranış sorunları neye yol açabilir?", "Büyümenin yavaşlaması ve ölüm oranının artması", ["Daha iyi yem değerlendirme",
     "Daha hızlı büyüme", "Hiçbir şeye"], "Ders notu."),
    ("Kloak gagalama hangi organın gagalanmasıdır?", "Kloak (dışkı ve yumurta çıkış açıklığı)", ["İbik", "Gaga", "Ayak"], "Ders notu."),
]


# ---------------------------------------------------------------------------
def gen_neden(r):
    return _tamamla(r, [], _ek(r, S_NEDEN))


def gen_tanim(r):
    sabit = []
    urun, dogru = _sec_bir(r, ORGANIK_MI)
    sabit.append(_secim(r, f"“{urun}” organik diye satılabilir mi?", "Evet" if dogru == "Organik" else "Hayır",
                        ["Hayır" if dogru == "Organik" else "Evet", "Yalnız köyde", "Yalnız ihracatta"],
                        ["Organik: sertifikalı, kurallara uygun üretim. Etiketteki 'doğal, köy, gezen' yeterli değil."]))
    return _tamamla(r, sabit, _ek(r, S_TANIM))


def gen_kaynak(r):
    sabit = []
    tur = _sec_bir(r, list(ALIM_YAS))
    birim, sinir, kural = ALIM_YAS[tur]
    yas = int(r.integers(1, sinir * 2 + 2))
    uygun = yas < sinir if tur == "Buzağı / tay" else yas <= sinir
    sabit.append(_secim(r, f"{yas} {'aylık' if birim == 'ay' else 'günlük'} bir {tur.split(' / ')[0].lower()} konvansiyonel işletmeden organik işletmeye alınabilir mi?",
                        "Evet" if uygun else "Hayır", ["Hayır" if uygun else "Evet", "Yalnız kesim için", "Yalnız kışın"],
                        [f"Kural: {kural}."]))
    return _tamamla(r, sabit, _ek(r, S_KAYNAK))


def gen_barinma(r):
    sabit = []
    tur = _sec_bir(r, ["Süt ineği", "Koyun / keçi", "Besi domuzu, 110 kg'a kadar", "Sığır, 200 kg'a kadar"])
    ic_m, dis_m = YOGUNLUK[tur]
    ic = int(r.integers(4, 40)) * 10
    n = math.floor(ic / ic_m + 1e-9)
    sabit.append(soru_sayi(f"{ic} m² kapalı alanda en çok kaç {tur.lower()} barındırılabilir? (hayvan başına {_tr(ic_m)} m²)", n,
                           [_md(f"{ic} ÷ {_tr(ic_m)} = {_tr(ic / ic_m)} → aşağı yuvarla: **{n}**")],
                           [math.ceil(ic / ic_m), ic * ic_m, n + 2], ondalik=0))
    at = _sec_bir(r, ["Süt ineği", "Koyun", "Yumurta tavuğu", "Besi domuzu"])
    ha = int(r.integers(2, 30))
    m = math.floor(AZOT_ESDEGER[at] * ha + 1e-9)
    sabit.append(soru_sayi(f"170 kg N/ha sınırına hektar başına {_tr(AZOT_ESDEGER[at])} {at.lower()} karşılık geliyorsa, {ha} ha "
                           f"alanda en çok kaç {at.lower()} barındırılır?", m,
                           [_md(f"{_tr(AZOT_ESDEGER[at])} × {ha} = {_tr(AZOT_ESDEGER[at] * ha)} → **{m}**")],
                           [m * 2, ha, math.ceil(m / 2)], ondalik=0))
    return _tamamla(r, sabit, _ek(r, S_BARINMA))


def gen_besleme(r):
    sabit = []
    madde, d = _sec_bir(r, IZIN_YASAK)
    sabit.append(_secim(r, f"Organik hayvancılıkta “{madde}”...", "İzinli" if d == "İzinli" else "Yasak",
                        ["Yasak" if d == "İzinli" else "İzinli", "Yalnız kışın izinli", "Yalnız ihracatta izinli"],
                        [f"{madde}: **{d}**."]))
    yt = _sec_bir(r, list(SUT_SURE))
    sabit.append(_secim(r, f"{yt} için yavruların sütle beslenmesi gereken asgari süre kaç gündür?",
                        f"{SUT_SURE[yt]} gün", [f"{v} gün" for v in (90, 45, 40, 60, 30) if v != SUT_SURE[yt]],
                        [f"Büyükbaş-tay 90, küçükbaş 45, domuz 40 gün."]))
    return _tamamla(r, sabit, _ek(r, S_BESLEME))


def gen_gecis(r):
    sabit = []
    omur = int(r.integers(3, 20)) * 4
    sabit.append(soru_sayi(f"Organik süt işletmesinden et için ayrılan, toplam yaşam süresi {omur} ay olan bir hayvanın geçiş süresi kaç aydır?",
                           omur * 0.75, [_md(f"3/4 × {omur} = **{_tr(omur * 0.75)} ay**")], [omur / 2, omur, 12], ondalik=1))
    tur = _sec_bir(r, list(GECIS_TUR))
    birim, sure = GECIS_TUR[tur]
    ay = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    if birim == "ay":
        b = int(r.integers(0, 12))
        dogru = ay[(b + sure) % 12]
        yanlis = [ay[(b + k) % 12] for k in (sure // 2, sure + 3, sure + 1)]
        sabit.append(_secim(r, f"{tur} için organik yönetim {ay[b]} ayının 1'inde başladı. Ürün en erken hangi ayın 1'inde organik satılabilir?",
                            dogru, yanlis, [f"Geçiş süresi {sure} ay: {ay[b]} + {sure} ay = **{dogru}**."]))
    else:
        sabit.append(soru_sayi(f"{tur}: geçiş süresi kaç gündür?", sure * 7, [_md(f"{sure} hafta × 7 = **{sure * 7} gün**")],
                               [sure * 30, sure, sure * 10], ondalik=0))
    return _tamamla(r, sabit, _ek(r, S_GECIS))


def gen_saglik(r):
    sabit = []
    yasal = int(r.integers(1, 15))
    birim = _sec_bir(r, ["gün", "saat"])
    saat = yasal * (24 if birim == "gün" else 1)
    org = max(2 * saat, 48)
    sabit.append(soru_sayi(f"Yasal bekleme süresi {yasal} {birim} olan bir ilaç için organik bekleme süresi kaç saattir?", org,
                           [_md(f"2 × {saat} saat = {2 * saat} saat; en az 48 saat → **{org} saat**")],
                           [saat, 2 * saat if 2 * saat != org else saat + 24, 48 if org != 48 else 96], ondalik=0))
    kur = int(r.integers(0, 6))
    asi = int(r.integers(0, 5))
    kisa = bool(r.integers(0, 2))
    sinir = 1 if kisa else 3
    hay = "etlik piliç sürüsü" if kisa else "süt ineği"
    ok = kur <= sinir
    sabit.append(_secim(r, f"Bir {hay} son 12 ayda {kur} kimyasal ilaç kürü ve {asi} aşı aldı. Ürünü (bekleme süresi dolunca) organik satılabilir mi?",
                        "Evet" if ok else "Hayır, yeniden geçiş gerekir", ["Hayır, yeniden geçiş gerekir" if ok else "Evet",
                                                                         "Yalnızca aşıları sayarsak", "Hiçbir zaman satılamaz"],
                        [f"Aşı sayılmaz. Sınır {'1 (verimli ömrü < 1 yıl)' if kisa else '3'}; {kur} {'≤' if ok else '>'} {sinir}."]))
    return _tamamla(r, sabit, _ek(r, S_SAGLIK))


def gen_tasima(r):
    sabit = []
    sure = int(r.integers(3, 40))
    mola = max(0, math.ceil(sure / 8) - 1)
    sabit.append(soru_sayi(f"{sure} saatlik bir hayvan naklinde en az kaç mola verilmelidir? (8 saatte bir)", mola,
                           [_md(f"⌈{sure} ÷ 8⌉ − 1 = **{mola}**")], [mola + 1, math.floor(sure / 8) + 1 if math.floor(sure / 8) + 1 != mola else mola + 2,
                                                                   max(0, mola - 1) if mola else 2], ondalik=0))
    return _tamamla(r, sabit, _ek(r, S_TASIMA))


def gen_refah(r):
    sabit = []
    durum, k = _sec_bir(r, OZGURLUK_DURUM)
    adlar = [o[0] for o in OZGURLUKLER]
    sabit.append(_secim(r, f"“{durum}” Bu durumda hangi özgürlük çiğneniyor?", adlar[k], _diger(r, adlar, adlar[k]),
                        [f"**{adlar[k]} özgürlük(ü)**: {OZGURLUKLER[k][1]}."]))
    return _tamamla(r, sabit, _ek(r, S_REFAH))


def gen_etholoji(r):
    return _tamamla(r, [], _ek(r, S_ETHOLOJI))


def gen_cevre(r):
    sabit = []
    nem = int(r.integers(2, 10)) * 10 + int(r.integers(0, 2)) * 5
    d = "Uygun" if 50 <= nem <= 60 else ("Yüksek: amonyak ve küf artar" if nem > 60 else "Düşük: toz ve solunum tahrişi artar")
    sabit.append(_secim(r, f"Barınakta bağıl nem %{nem} ölçüldü. Değerlendirmeniz?", d,
                        ["Uygun", "Yüksek: amonyak ve küf artar", "Düşük: toz ve solunum tahrişi artar", "Nemin önemi yoktur"],
                        ["Uygun aralık %50–60."]))
    return _tamamla(r, sabit, _ek(r, S_CEVRE))


def gen_tur(r):
    sabit = []
    sa = int(r.integers(0, 24))
    h = (sa + 12) % 24
    sabit.append(_secim(r, f"İnekte kızgınlık saat {sa:02d}:00'de başladı. Tohumlama için en uygun saat yaklaşık kaçtır?", f"{h:02d}:00",
                        [f"{(sa + k) % 24:02d}:00" for k in (2, 24 - 6, 6)], [f"Başlangıç + 12 saat = **{h:02d}:00**."]))
    n = int(r.integers(3, 30)) * 10
    sabit.append(_secim(r, f"{n} koyunluk bir sürü için kaç koç gerekir? (koç başına 20–30 koyun)",
                        f"{math.ceil(n / 30)}–{math.ceil(n / 20)}",
                        [f"{math.ceil(n / 60)}–{math.ceil(n / 50)}", f"{math.ceil(n / 10)}–{math.ceil(n / 5)}", "1"],
                        [f"{n} ÷ 30 = {_tr(n / 30)} → {math.ceil(n / 30)}; {n} ÷ 20 = {_tr(n / 20)} → {math.ceil(n / 20)}."]))
    ot = int(r.integers(10, 25)) / 2
    sabit.append(soru_sayi(f"Günlük otlama süresi {_tr(ot)} saat olan bir sığırın geviş süresi yaklaşık kaç saattir? (otlamanın %75'i)",
                           0.75 * ot, [_md(f"0,75 × {_tr(ot)} = **{_tr(0.75 * ot)} saat**")], [ot, 0.5 * ot, 1.5 * ot], ondalik=2))
    return _tamamla(r, sabit, _ek(r, S_TUR))


def gen_bozukluk(r):
    sabit = []
    a, t, n, o = _sec_bir(r, ANORMAL)
    sabit.append(_secim(r, f"“{a}” en çok hangi türde görülür?", t, _diger(r, ["Sığır", "Koyun", "Domuz", "Tavuk"], t),
                        [f"{a}: {t}. Olası neden: {n}."]))
    a2, t2, n2, o2 = _sec_bir(r, ANORMAL)
    sabit.append(_secim(r, f"“{a2}” için uygun önleme hangisidir?", o2, _diger(r, [x[3] for x in ANORMAL], o2),
                        [f"Neden: {n2}. Önleme: {o2}."]))
    return _tamamla(r, sabit, _ek(r, S_BOZUKLUK))


def gen_tekrar(r):
    ureticiler = [gen_neden, gen_tanim, gen_kaynak, gen_barinma, gen_besleme, gen_gecis, gen_saglik, gen_tasima,
                  gen_refah, gen_etholoji, gen_cevre, gen_tur, gen_bozukluk]
    secilen = [ureticiler[int(i)] for i in r.permutation(len(ureticiler))[:SORU_SAYISI]]
    return [u(r)[0] for u in secilen]


# ===========================================================================
# Gezinme
# ===========================================================================
SAYFALAR = [
    st.Page(sayfa_giris, title="Giriş", icon="🏠", url_path="giris", default=True),
    st.Page(sayfa_neden, title="1 · Neden organik?", url_path="neden-organik"),
    st.Page(sayfa_tanim, title="2 · Tanım, ilkeler ve mevzuat", url_path="tanim-mevzuat"),
    st.Page(sayfa_kaynak, title="3 · Hayvan kaynağı ve üreme", url_path="hayvan-kaynagi"),
    st.Page(sayfa_barinma, title="4 · Barınma ve açık alan", url_path="barinma"),
    st.Page(sayfa_besleme, title="5 · Besleme", url_path="besleme"),
    st.Page(sayfa_gecis, title="6 · Geçiş süreleri", url_path="gecis-sureleri"),
    st.Page(sayfa_saglik, title="7 · Hayvan sağlığı ve tedavi", url_path="saglik-tedavi"),
    st.Page(sayfa_tasima, title="8 · Taşıma, kesim, kayıt, karar", url_path="tasima-kesim-kayit"),
    st.Page(sayfa_refah, title="9 · Hayvan refahı", url_path="hayvan-refahi"),
    st.Page(sayfa_etholoji, title="10 · Etholoji ve davranışın temelleri", url_path="etholoji"),
    st.Page(sayfa_cevre, title="11 · Barınak çevresi", url_path="barinak-cevresi"),
    st.Page(sayfa_tur, title="12 · Türlere göre davranış", url_path="turlere-gore-davranis"),
    st.Page(sayfa_bozukluk, title="13 · Davranış bozuklukları", url_path="davranis-bozukluklari"),
    st.Page(sayfa_tekrar, title="14 · Genel tekrar", url_path="genel-tekrar"),
]
gezinme = st.navigation(SAYFALAR)

with st.sidebar:
    tohum = st.number_input("Rastgele tohum (0 = rastgele)", 0, 999999, 0,
                            help="Sınıfta herkes aynı sayıyı girerse aynı soruları görür.")
    if st.session_state.get("tohum") != tohum:
        st.session_state.tohum = tohum
        st.session_state.rng = (np.random.default_rng(tohum) if tohum
                                else np.random.default_rng())
    st.divider()
    st.caption(TELIF)

basliklar = [p.title for p in SAYFALAR]
simdiki = basliklar.index(gezinme.title) if gezinme.title in basliklar else 0
secilen = st.selectbox("📚 Bölüm", basliklar, index=simdiki)
if secilen != gezinme.title:
    st.switch_page(SAYFALAR[basliklar.index(secilen)])

gezinme.run()

st.divider()
c1, _, c3 = st.columns([1, 0.2, 1])
if simdiki > 0:
    c1.page_link(SAYFALAR[simdiki - 1], label=f"◀ {basliklar[simdiki - 1]}")
if simdiki < len(SAYFALAR) - 1:
    c3.page_link(SAYFALAR[simdiki + 1], label=f"{basliklar[simdiki + 1]} ▶")

st.markdown(f'<div style="text-align:center;color:gray;font-size:0.85rem;'
            f'margin-top:24px">{TELIF}</div>', unsafe_allow_html=True)
