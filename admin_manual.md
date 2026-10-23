# DEÜ Kitap Satış - Yönetim Paneli Kullanım Kılavuzu

Bu kılavuz, **DEÜ Kitap Satış** platformunun yönetim (Admin) panelini kullanacak yöneticiler için hazırlanmıştır. Sistemin genel işleyişi, envanter yönetimi, sipariş takibi, elden teslimat doğrulaması, kullanıcı yönetimi, destek mesajları ve detaylı raporlama işlemleri adım adım açıklanmıştır.

---

## İÇİNDEKİLER
1. [Yönetim Paneline Giriş](#1-yonetim-paneline-giris)
2. [Genel Bakış (Dashboard) Paneli](#2-genel-bakis-dashboard-paneli)
3. [Kitap Yönetimi (Envanter)](#3-kitap-yonetimi-envanter)
   - [Yeni Kitap Ekleme](#yeni-kitap-ekleme)
   - [Filtreleme ve Arama](#filtreleme-ve-arama)
   - [Toplu İşlemler ve Fiyat Güncelleme](#toplu-islemler-ve-fiyat-guncelleme)
   - [Kitap Düzenleme ve Silme](#kitap-duzenleme-ve-silme)
4. [Sipariş Yönetimi](#4-siparis-yonetimi)
   - [Elden Teslimat Doğrulama (Barkod/Kod Doğrulama)](#elden-teslimat-dogrulama-barkodkod-dogrulama)
   - [Sipariş Durumunu Güncelleme](#siparis-durumunu-guncelleme)
   - [Sipariş Detayları ve Ödeme Özeti](#siparis-detaylari-ve-odeme-ozeti)
5. [Kullanıcı Yönetimi](#5-kullanici-yonetimi)
   - [Kullanıcı İnceleme ve Sipariş Geçmişi](#kullanici-inceleme-ve-siparis-gecmisi)
   - [Kullanıcı Yetkilendirme ve Engelleme/Silme](#kullanici-yetkilendirme-ve-engellemesilme)
6. [İletişim Mesajları (Destek Talepleri)](#6-iletisim-mesajlari-destek-talepleri)
   - [Mesaj Okuma ve Yanıtlama](#mesaj-okuma-ve-yanitlama)
7. [Güvenlik ve Şifre Değiştirme (2FA)](#7-guvenlik-ve-sifre-degistirme-2fa)
8. [Detaylı Raporlama ve Dışa Aktarma](#8-detayli-raporlama-ve-disa-aktarma)
   - [Excel (XLSX) Olarak İndirme](#excel-xlsx-olarak-indirme)
   - [PDF Olarak İndirme](#pdf-olarak-indirme)

---

## 1. YÖNETİM PANELİNE GİRİŞ
Yönetim paneline erişebilmek için yetkili bir yönetici (Admin) hesabı ile sisteme giriş yapılması gerekmektedir:
1. Ana sayfada bulunan **Giriş Yap** seçeneğiyle yönetici e-posta ve şifrenizi girin.
2. Başarılı giriş sonrasında, üst menüde veya kullanıcı profil alanında beliren **Yönetim Paneli** butonuna tıklayın.
3. Yönetici yetkiniz doğrulanarak sol tarafta kontrol menüsü, sağ tarafta ise ilgili içerik alanı açılacaktır.

---

## 2. GENEL BAKIŞ (DASHBOARD) PANELİ
Yönetim paneline giriş yaptığınızda sizi karşılayan ilk ekrandır. Bu ekran, mağazanın genel durumunu anlık olarak analiz etmenizi sağlar.

![Dashboard Paneli](manual_assets/dashboard_mockup.png)

### Göstergeler ve Kartlar:
*   **💰 Toplam Gelir**: Tamamlanmış (kargolanan veya elden teslim edilen) siparişlerden elde edilen toplam ciroyu gösterir. Sağ üstündeki grafik simgesi (📈/📉), bir önceki aya göre gelirdeki yüzdelik değişimi ifade eder.
*   **🛒 Toplam Sipariş**: Sistemdeki tüm siparişlerin (aktif, iptal edilen, iade edilen dahil) sayısını gösterir. Siparişlerin altında yer alan kırmızı uyarılar kaç adet iptal veya iade sipariş olduğunu listeler.
*   **📚 Satılan Kitap**: Müşterilere başarıyla teslim edilmiş veya kargolanmış kitapların toplam adet bilgisidir.
*   **👥 Yeni Üye**: İçinde bulunulan ay içerisinde sisteme kaydolan yeni kullanıcı sayısıdır.

### Grafikler ve Analiz Tabloları:
*   **Aylık Satış Analizi**: Son aylarda kargolanmış ve elden teslim edilmiş siparişlerin aylık gelir grafiğidir. Barların üzerine gelerek o aya ait tam tutarı görebilirsiniz.
*   **Son Gelen Siparişler**: Mağazaya düşen en son 5 siparişin numarasını, tarihini ve toplam tutarını listeler.
*   **En Çok Satan Kitaplar**: Bu ay en çok satılan 4 kitabı, yazarını, birim fiyatını ve toplam satış miktarını gösterir.
*   **Kategori Gelirleri**: Satış yapılan kategorilerin toplam gelir içerisindeki dağılımını renkli ilerleme çubukları ile yüzdesel olarak gösterir.
*   **Detaylı Rapor Butonu**: Sağ üst köşede yer alan buton ile gelişmiş filtreleme ve dışa aktarma (Excel/PDF) ekranına geçiş yapabilirsiniz.

---

## 3. KİTAP YÖNETİMİ (ENVANTER)
Sistemdeki kitapların eklenmesi, stok takibi, fiyatlandırılması ve listelenmesi işlemleri bu sekmeden yapılır.

![Kitap Yönetimi](manual_assets/books_mockup.png)

### Yeni Kitap Ekleme:
1. Kitap listesi ekranının sağ üst köşesindeki **+ Yeni Kitap Ekle** butonuna tıklayın.
2. Açılan formda aşağıdaki bilgileri eksiksiz doldurun:
    *   **Kitap Adı**: Kitabın tam adı (örn: *Veri Yapıları ve Algoritmalar*).
    *   **Yazar(lar)**: Kitabın yazarı. Birden fazla yazar varsa aralarına virgül koyarak yazın.
    *   **Açıklama**: Kitap içeriği, kimler için uygun olduğu gibi detaylı tanıtım yazısı.
    *   **Kategori**: İlgili mühendislik veya bilim dalını seçin (örn: *Bilgisayar Mühendisliği*, *Elektrik Elektronik Mühendisliği* vb.).
    *   **Yayınevi**: Kitabı basan yayınevinin adı.
    *   **ISBN No**: Kitabın arkasında yer alan 13 haneli barkod numarasıdır. Sayılar girildikçe sistem tarafından otomatik olarak uluslararası standart formatta (örn: `978-605-...`) biçimlendirilir.
    *   **Fiyat (₺)**: Kitabın KDV dahil satış fiyatını kuruş detayına kadar girin.
    *   **Stok Adedi**: Depodaki mevcut kitap sayısı.
    *   **Min Stok**: Kritik stok uyarısı için sınır değerdir (Varsayılan: 25). Stok bu seviyenin altına düştüğünde sistem otomatik olarak uyarı verir.
    *   **Kitap Görseli**: Kapak seç butonuna tıklayarak bilgisayarınızdan kitabın kapak resmini seçip yükleyin. Görsel yüklendiğinde anında önizleme gösterilir. İstenirse "Görseli Kaldır" butonu ile kaldırılabilir.
    *   **Durum ve Görünürlük**: 
        *   *Satışa Açık*: Kapatılırsa kitap sitede pasif duruma geçer, müşteriler ürünü göremez ve sepete ekleyemez.
        *   *Öne Çıkarılan*: Açılırsa kitap ana sayfadaki "Öne Çıkan Kitaplar" vitrininde sergilenir.
3. Formun sağ üst köşesindeki **💾 Kaydet** butonuna basarak kitabı yayına alın.

### Filtreleme ve Arama:
*   **Kitap İsmi Ara**: Arama kutusuna yazılan kelimelere göre kitap listesi anlık olarak filtrelenir.
*   **⚠️ Kritik Stok**: Bu butona tıkladığınızda yalnızca stoğu yönetici tarafından belirlenen "Min Stok" değerinin altına düşmüş kitaplar listelenir. Böylece hızlıca sipariş vermeniz gereken kitapları tespit edebilirsiniz. Butonun sağ üstündeki kırmızı daire güncel kritik kitap adetini gösterir.
*   **🚫 Pasifteki Kitaplar**: Yayından kaldırılmış, satışı durdurulmuş kitapları hızlıca listelemek için kullanılır.

### Toplu İşlemler ve Fiyat Güncelleme:
*   **Tümünü Satışa Aç / Kapat**: Tek tek uğraşmak yerine depodaki tüm kitapları tek tıkla toplu olarak yayına alabilir veya pasifleştirebilirsiniz.
*   **Toplu Fiyat Arttır**: Enflasyon veya maliyet artışı durumlarında, kutucuğa yüzdelik bir oran girip (örn: `15` girerek %15 artış) **Toplu Fiyat Arttır** butonuna bastığınızda, sistemdeki tüm kitapların fiyatı girilen oranda otomatik olarak arttırılır.

### Kitap Düzenleme ve Silme:
*   Düzenlemek istediğiniz kitabın satırındaki sarı **✏️ (Düzenle)** simgesine tıklayarak formu açabilir ve güncellemelerinizi yapabilirsiniz.
*   Bir kitabı tamamen silmek (veya pasife almak) için kırmızı **🗑️ (Sil)** simgesine tıklayın, açılan onay penceresinde işlemi onaylayın.

---

## 4. SİPARİŞ YÖNETİMİ
Müşterilerin oluşturduğu siparişlerin hazırlandığı, kargolandığı veya elden teslim edildiği kontrol merkezidir.

![Sipariş Yönetimi](manual_assets/orders_mockup.png)

### Elden Teslimat Doğrulama (Barkod/Kod Doğrulama):
Öğrenciler veya alıcılar siparişlerini kargo yerine dekanlıktan/şahsen teslim almayı seçebilirler. Bu durumda kullanıcılara **DK-FXXXXX** formatında benzersiz bir "Teslimat Kodu" tanımlanır.
1. Alıcı dekanlığa gelip teslimat kodunu ibraz ettiğinde, sipariş listesinin üstünde yer alan mavi **Elden Teslimat Doğrulama** alanındaki kutuya bu kodu yazın.
2. **Bul & Doğrula** butonuna basın (veya Enter'a basın).
3. Sistem siparişi anında bulur, detay ekranını açar ve ekranda yeşil renkli **✅ KOD DOĞRULANDI** rozeti gösterir.
4. Bu sayede siparişin doğruluğundan emin olarak kitapları alıcıya elden teslim edebilirsiniz.

### Sipariş Durumunu Güncelleme:
Sipariş detay sayfasında bulunan "Sipariş Durumu Güncelle" alanından siparişin aşamalarını yönetebilirsiniz. Siparişin türüne göre durum seçenekleri dinamiktir:
*   **Kargolu Siparişler İçin**:
    *   *Hazırlanıyor*: Sipariş paketlenme aşamasındadır.
    *   *Kargoya Verildi*: Paket kargoya teslim edildiğinde seçilir.
    *   *İptal Edildi*: İlk 10 dakika veya sipariş gönderilmeden önce iptal edilirse seçilir.
    *   *İade Edildi*: 14 günlük yasal süreçte iade alınan siparişler için seçilir.
*   **Elden Teslimat Siparişleri İçin**:
    *   *Hazırlanıyor*: Kitaplar raftan alınıp hazırlanıyor.
    *   *Elden Teslim Edildi*: Alıcı kodu doğrulanıp kitapları elden aldığında seçilir.
    *   *İptal Edildi / İade Edildi*: İptal veya iade durumları için seçilir.

*Not: Durumu değiştirdikten sonra beliren **Değişiklikleri Kaydet** butonuna tıklamayı unutmayın.*

### Sipariş Detayları ve Ödeme Özeti:
*   Müşterinin adı, adresi, telefon numarası ve sipariş ettiği kitapların adet/fiyat dökümü detay sayfasında listelenir.
*   Ödeme özeti alanında ürünlerin toplam tutarı gösterilir.

---

## 5. KULLANICI YÖNETİMİ
Sisteme kayıtlı olan öğrencilerin, personellerin ve yöneticilerin hesaplarını denetlemek için kullanılır.

### Kullanıcı İnceleme ve Sipariş Geçmişi:
1. Kullanıcı listesinden arama çubuğunu veya sıralama seçeneklerini kullanarak aradığınız kullanıcıyı bulun.
2. Satırdaki **👁️ (İncele)** simgesine tıklayın.
3. Açılan detay sayfasında kullanıcının adı soyadı, e-posta adresi, telefon numarası, kayıt tarihi ve şimdiye kadar verdiği tüm siparişlerin geçmiş tablosu listelenir. Siparişlerin hangi tarihte yapıldığı, tutarları ve durumları buradan görülebilir.

### Kullanıcı Yetkilendirme ve Engelleme/Silme:
*   Kullanıcıların yetkisi tablodaki "Yetki" sütununda (örn: *Admin* veya *Kullanıcı*) gösterilir.
*   Kullanıcıyı tamamen silmek için satırdaki kırmızı **🗑️ (Sil)** butonuna basarak onay verin.
*   *Önemli Güvenlik Kuralı: Sistem kurucusu/ana yönetici (ID: #1) güvenlik sebebiyle silinemez veya pasifleştirilemez.*

---

## 6. İLETİŞİM MESAJLARI (DESTEK TALEPLERİ)
Ziyaretçilerin ve müşterilerin "İletişim" sayfasından gönderdiği soru, şikayet ve destek taleplerinin yönetildiği alandır.

### Mesaj Okuma ve Yanıtlama:
1. Sol menüdeki **İletişim Mesajları** sekmesinin yanında kırmızı renkte okunmamış mesaj sayısı gösterilir.
2. Mesaj listesinde okunmamış mesajların solunda mavi bildirim ışığı yanıp söner ve satır arka planı belirgin bir renkle gösterilir.
3. Mesajı okumak için **Oku & Yanıtla** veya **Görüntüle** butonuna tıklayın.
4. Açılan pencerede (modal) gönderenin bilgileri, gönderim tarihi, mesajın konusu ve detaylı içeriği yer alır.
5. **Yanıtınız** kutusuna cevabınızı yazın ve **Cevabı Gönder** butonuna tıklayın. Mesaj yanıtlandığında durumu otomatik olarak "Yanıtlandı" (yeşil rozet) olarak güncellenir.

---

## 7. GÜVENLİK VE ŞİFRE DEĞİŞTİRME (2FA)
Yönetici hesabınızın şifresini güvenli bir şekilde değiştirmek için kullanılan sayfadır.

### Şifre Güncelleme Süreci (2FA E-posta Doğrulama):
Siber güvenlik önlemleri gereği şifrenizi değiştirmek için iki aşamalı doğrulama uygulanır:
1. **Şifre Değiştir** sekmesine girin.
2. *Mevcut Şifre*, *Yeni Şifre* ve *Yeni Şifre (Tekrar)* alanlarını doldurun.
3. **Şifreyi Güncelle** butonuna tıklayın.
4. Sistem, hesabınıza kayıtlı e-posta adresinize anında **6 haneli geçici bir doğrulama kodu** gönderir ve ekranda kod giriş alanını açar.
5. E-postanıza gelen 6 haneli kodu kopyalayıp ekrandaki alana girin.
6. **Doğrula ve Şifreyi Değiştir** butonuna tıklayarak işlemi tamamlayın. Kod doğruysa şifreniz başarıyla güncellenir.

---

## 8. DETAYLI RAPORLAMA VE DIŞA AKTARMA
Finansal denetimler, satış analizleri ve yönetim kurulu sunumları için gelişmiş filtreleme ve raporlama ekranıdır.

![Raporlama Ekranı](manual_assets/reports_mockup.png)

### Gelişmiş Filtreleme Seçenekleri:
*   **Tarih Aralığı**: Başlangıç ve Bitiş tarihlerini seçerek belirli dönemlerin satışlarını filtreleyin.
*   **Sipariş Durumu**: Yalnızca iadeleri, hazırlananları veya tamamlanmış olanları seçebilirsiniz.
*   **Kitap / Sipariş No**: Sipariş numarasına veya satılan kitabın ismine göre filtreleme yapın.

### Rapor Çıktısı Alma (Dışa Aktarma):

#### Excel (XLSX) Olarak İndirme:
*   Filtrelemelerinizi yaptıktan sonra yeşil **📊 Excel İndir** butonuna tıklayın.
*   Sistem, tüm verileri otomatik olarak işler ve Excel dosyası (`Siparis_Raporu.xlsx`) olarak indirir.
*   **Tasarım Özellikleri**: Excel tablosunda sütun genişlikleri otomatik ayarlanmış olup başlık satırı sarı dolgu ile belirginleştirilmiştir. Hücreler ince gri çizgilerle sınırlandırılmış, fiyatlar para birimi formatında (`₺#,##0.00`) biçimlendirilmiştir. Dosyada ayrıca kategorilere göre satış adetlerini gösteren bir **Kategori İstatistikleri** sayfası da bulunur.

#### PDF Olarak İndirme:
*   Kırmızı **📄 PDF İndir** butonuna tıklayarak raporu PDF olarak indirin.
*   **Tasarım Özellikleri**: PDF dosyası landscape (yatay A4) formatında, kurumsal mavi (`#4318ff`) başlık şeridiyle oluşturulur. Tabloda çizgili satır tasarımı kullanılır, fiyatlar sağa hizalıdır. Türkçe karakterlerin (ş, ı, ğ, ç, ö, ü) PDF standart fontlarında bozulmaması için otomatik karakter normalizasyonu (temizleme) uygulanmaktadır. Sayfanın en altında otomatik sayfa numaralandırması yer alır.

---
*Kılavuz Sonu - Herhangi bir teknik sorunda sistem yöneticisiyle iletişime geçiniz.*
