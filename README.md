# Mini-Budget Projesi

**Yazar:** Yiğit Bilge (251478059)
**Mevcut Versiyon:** V2

Bu proje, kişisel harcamalarınızı ve bütçenizi komut satırı (terminal) üzerinden yönetmenizi sağlayan bir Python uygulamasıdır.

---

## 🚀 [V2] - Mevcut Sürüm Değişiklikleri

### V2 Görev Listesi (Tasks)
1. **Timestamp:** Harcamalara otomatik tarih ve saat eklenmesi.
2. **Total Command:** Tüm harcamaların toplamını veren fonksiyonun geliştirilmesi.
3. **Error Handling:** Veri dosyası henüz oluşturulmamışken yapılan sorgularda çökmenin engellenmesi.

### V1 -> V2 Değişiklik Özeti
* **Otomatik Tarih:** Artık her işlem eklendiğinde sistem saatini (`datetime` modülü ile) otomatik kaydeder.
* **Bakiyeyi Toplama:** `total` komutu eklendi. `while` döngüsü kullanılarak dosyadan okunan miktarlar matematiksel olarak toplanır ve net bakiye gösterilir.
* **Güvenlik ve Stabilite:** Dosya bulunamadığında veya hatalı/harf içeren bir veri girildiğinde programın çökmesi engellendi (Try-Except ve Path check kullanıldı).

---

## 🕰️ [V1] - Sürüm Geçmişi

### V1 Görev Listesi
1. `list` komutunu `while` döngüsü kullanarak implemente et.
2. `ledger.dat` dosyası boşsa "No transactions found." uyarısı ver.
3. Çıktı formatını güzelleştir: `|` karakterlerini ` - ` ile değiştir (replace).

### V0 -> V1 Değişiklik Özeti
V0 sürümünde uygulamanın sadece temel iskeleti (`init`) ve dosyaya veri yazma işlemi (`add`) aktifti. Ancak verileri okuyup kullanıcıya gösterme özelliği yoktu. 

V1 aşamasında uygulamaya `while` döngüsü entegre edildi. Artık `list` komutu çağrıldığında sistem `.minibudget/ledger.dat` dosyasını açıyor, içerideki kayıtları döngü yardımıyla satır satır okuyor ve ekrana yazdırıyor. Formatlama yaparken henüz listeler (`[]`) öğrenilmediği için `replace()` metodu kullanılarak dik çizgiler (`|`) okunabilir tirelere çevrildi. Dosya boşsa kullanıcıya SPEC'te belirtildiği gibi uyarı verilmesi sağlandı.