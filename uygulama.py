import time
import streamlit as st
import pandas as pd
from groq import Groq

# --- HAFIZA YÖNETİMİ (Session State) ---
if "gecmis_aramalar" not in st.session_state:
    st.session_state.gecmis_aramalar = []
    
# Raporun anahtar değiştiğinde kaybolmaması için yeni bellekler ekliyoruz
if "aktif_rapor_hikaye" not in st.session_state:
    st.session_state.aktif_rapor_hikaye = None
if "aktif_rapor_analitik" not in st.session_state:
    st.session_state.aktif_rapor_analitik = None
if "analiz_yapildi" not in st.session_state:
    st.session_state.analiz_yapildi = False

# Sayfa Ayarları
st.set_page_config(page_title="Idea Co-Pilot", page_icon="🚀", layout="wide")

# Modern Tasarım CSS
st.markdown("""
    <style>
    .ana-baslik {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #1E90FF, #FF1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .alt-baslik {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        font-weight: 400;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    .stApp {
        background-color: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)

# Sol Menü (Sidebar)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2083/2083213.png", width=50)
st.sidebar.header("⚙️ Sistem Ayarları")
api_key = st.sidebar.text_input("Groq API Anahtarı:", type="password")

st.sidebar.markdown("---")
st.sidebar.header("📂 Geçmiş Analizler")
if len(st.session_state.gecmis_aramalar) == 0:
    st.sidebar.info("Henüz analiz edilmiş bir fikir yok.")
else:
    for i, analiz in enumerate(reversed(st.session_state.gecmis_aramalar)): 
        with st.sidebar.expander(f"💡 Fikir {len(st.session_state.gecmis_aramalar) - i}: {analiz['fikir'][:25]}..."):
            st.write(analiz['rapor'][:150] + "...")

# Ana Ekran
st.markdown('<div class="ana-baslik">Idea Co-Pilot</div>', unsafe_allow_html=True)
st.markdown('<div class="alt-baslik">Girişimin yazılması, pazarlanması, teknoloji ve yatırım verileriyle analiz edilmesi.</div>', unsafe_allow_html=True)
st.markdown("---")

# Fikir Giriş Alanı
kullanici_fikri = st.text_area("Girişim Fikrinizi Detaylıca Anlatın:", height=150, placeholder="Örneğin: Yapay zeka ile kişiselleştirilmiş diyet listeleri hazırlayan mobil uygulama...")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analiz_butonu = st.button("🚀 Fikri Doğrula ve Analizi Başlat", use_container_width=True)

# 1. AŞAMA: YAPAY ZEKA SORGUSU (Sadece Butona Basılınca Çalışır)
if analiz_butonu:
    if not api_key:
        st.warning("⚠️ Lütfen analizi başlatmadan önce sol menüden Groq API Anahtarınızı girin.")
    elif not kullanici_fikri:
        st.warning("⚠️ Lütfen analiz etmek için bir fikir girin!")
    else:
        try:
            df = pd.read_csv("startuplar.csv")
            ornek_veriler = df.head(10).to_string()
            
            with st.status("Idea Co-Pilot Ajanları Devrede...", expanded=True) as status:
                st.write("🕵️ Yönlendirici Ajan: Fikir analiz ediliyor...")
                time.sleep(1)
                st.write("🌐 Veri Ajanı: YC hafıza havuzu belleğe alındı...")
                st.write("🧠 Sentezleyici Ajan: Meta Llama 3.3 modeli fikirleri çarpıştırıyor...")
                
                client = Groq(api_key=api_key)
                
                sistem_mesaji = f"""
                Sen Silikon Vadisi'nin en iyi melek yatırımcısı ve hikaye anlatıcısısın. 
                Kullanıcının fikrini şu YC veritabanı örneklerine bakarak analiz et: {ornek_veriler}
                
                Lütfen cevabını tam olarak aşağıdaki gibi İKİ BÖLÜM halinde ver:
                
                --- BÖLÜM 1: HİKAYE ---
                (Buraya fikrin vizyonunu, pazardaki yerini ve geleceğini anlatan, ilham verici, akıcı ve 3 paragraflık bir yönetici özeti yaz.)
                
                --- BÖLÜM 2: ANALİTİK ---
                ### 🚧 Risk ve Fırsat Tablosu
                | Kriter | Değerlendirme | Risk Seviyesi (Düşük/Orta/Yüksek) |
                | :--- | :--- | :--- |
                | Özgünlük | ... | ... |
                | Uygulanabilirlik | ... | ... |
                | İş Modeli | ... | ... |
                
                ### 🔄 Aksiyon Planı (Pivot Önerileri)
                * **Ekle:** ...
                * **Çıkar:** ...
                * **Odaklan:** ...
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": sistem_mesaji},
                        {"role": "user", "content": kullanici_fikri}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                yapay_zeka_cevabi = chat_completion.choices[0].message.content
                status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)

            # Cevabı bölümlere ayırma
            if "--- BÖLÜM 2: ANALİTİK ---" in yapay_zeka_cevabi:
                bolumler = yapay_zeka_cevabi.split("--- BÖLÜM 2: ANALİTİK ---")
                hikaye_kismi = bolumler[0].replace("--- BÖLÜM 1: HİKAYE ---", "").strip()
                analitik_kisim = bolumler[1].strip()
            else:
                hikaye_kismi = "Hikaye oluşturulamadı."
                analitik_kisim = yapay_zeka_cevabi

            # VERİLERİ KALICI BELLEĞE (SESSION STATE) KAYDETME (Sihir burada)
            st.session_state.aktif_rapor_hikaye = hikaye_kismi
            st.session_state.aktif_rapor_analitik = analitik_kisim
            st.session_state.analiz_yapildi = True
            
            # Geçmişe Ekleme
            st.session_state.gecmis_aramalar.append({"fikir": kullanici_fikri, "rapor": yapay_zeka_cevabi})
            
        except Exception as e:
            st.error(f"⚠️ Bir hata oluştu: {e}")

# 2. AŞAMA: EKRANDA GÖSTERİM (Butona basılmasa bile hafızadan okunur)
if st.session_state.analiz_yapildi:
    st.markdown("---")
    st.markdown("### 📊 Analiz Sonucu")
    
    # Görünüm Anahtarı
    hikaye_modu = st.toggle("📖 Görünümü Değiştir: Hikayeleştirilmiş Yönetici Özeti")

    if hikaye_modu:
        # HİKAYE MODU (Bellekten okunuyor)
        st.success("✨ **Yönetici Özeti Modu Aktif:** Büyük resmi ve vizyonu okuyorsunuz.")
        st.markdown(f"*{st.session_state.aktif_rapor_hikaye}*")
    else:
        # ANALİTİK MOD (Bellekten okunuyor)
        tab1, tab2, tab3 = st.tabs(["🗄️ 1. Hafıza Havuzu", "📈 2. Görsel Metrikler", "🛠️ 3. Yapay Zeka Stratejisi"])
        
        with tab1:
            try:
                df = pd.read_csv("startuplar.csv")
                st.dataframe(df.head(5))
            except:
                st.warning("startuplar.csv dosyası okunamadı.")

        with tab2:
            st.markdown("#### 📏 Ürün-Pazar Uyumu Tahmini Metrikleri")
            grafik_verisi = pd.DataFrame({
                "Kriterler": ["Pazar Boşluğu", "Teknik Yapılabilirlik", "İş Modeli Gücü"],
                "Puan (100)": [75, 85, 40]
            })
            st.bar_chart(grafik_verisi.set_index("Kriterler"), color="#1E90FF")
            st.progress(60, text="Tahmini MVP Geliştirme Kolaylığı: %60")

        with tab3:
            st.write(st.session_state.aktif_rapor_analitik)