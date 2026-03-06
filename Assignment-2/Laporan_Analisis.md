# Analisis Tugas Pemrosesan Citra Dasar

## 1. Perbandingan Grayscale Metode Rata-rata dan Luminance
* **Metode Rata-rata** `(R + G + B)/3`: Memberikan bobot matematis yang sama pada ketiga warna dasar. Metode ini cenderung menyebabkan beberapa detail citra terlihat terlalu gelap atau terlalu terang sehingga mengurangi variabilitas tekstur, akibat warna biru yang secara visual terlihat gelap diberi bobot sama dengan hijau dan merah.
* **Metode Luminance** `(0.299R + 0.587G + 0.114B)`: Diformulasikan berdasarkan studi biologis terhadap penglihatan manusia. Mata manusia secara alami jauh lebih sensitif terhadap warna terang kehijauan dibandingkan warna biru gelap. Metode ini menghasilkan reproduksi citra abu-abu (grayscale) yang terlihat jauh lebih natural karena merepresentasikan kecerahan spesifik sejalan dengan persepsi manusia.

## 2. Efek Brightness Terhadap Citra
Operasi penyesuaian kecerahan (brightness adjustment) dilakukan melalui penambahan konstanta $b$ ke setiap intensitas piksel citra: $f(x,y)' = f(x,y) + b$.
* Jika nilai $b$ **positif**, nilai spektrum piksel akan bertambah sehingga citra menjadi **lebih terang**. Namun, bila intensitas mencapai nilai maksimum (255 untuk citra 8-bit), piksel tersebut akan terpotong (clipping) menjadi warna putih pekat, yang mana bisa menghilangkan tekstur objek jika $b$ terlalu besar (overexposure).
* Jika nilai $b$ **negatif**, nilai warna turun sehingga citra terlihat **secara keseluruhan lebih gelap**. Transisi piksel yang nilainya jatuh di bawah nilai 0 di-clip menjadi 0 (hitam total), juga dapat menghilangkan detail pada area bayangan (underexposure).

## 3. Pengaruh Filtering Terhadap Noise
Filter yang diimplementasikan (Mean Filter atau Low-pass Filter dengan mask kernel berukuran 3x3 bernilai 1/9) berfungsi untuk meratakan intensitas sebuah piksel dengan rata-rata piksel tetangganya.
Operasi ini **sangat efektif untuk mereduksi noise**, khususnya *Gaussian noise* atau *grain* pada citra, dengan cara menyebarkan ekstremitas piksel bernoise di sekitarnya. 
Efek samping visual utamanya adalah hilangnya detail frekuensi tinggi pada citra. Bagian ujung atau batas tajam (edges) suatu bentuk akan menjadi berbayang atau **terlihat blur**.

## 4. Fungsi Operasi AND Dalam Pemrosesan Citra
Operasi Boolean AND digunakan untuk operasi **Image Masking** (pemotongan berlapis).
Dalam implementasi standar, di mana operasi dilakukan piksel demi piksel antara citra asal warna dan sebuah citra mask / biner hitam-putih, fitur matematika gerbang logika AND berarti $1 \land x = x$ dan $0 \land x = 0$.
Akibatnya:
* Area citra yang tumpang tindih dengan area "Putih (1 / 255)" pada layer mask akan **dipertahankan seutuhnya**.
* Area citra yang tumpang tindih dengan area "Hitam (0 / 0)" pada layer mask akan dihapus atau **diubah menjadi warna hitam gulita (0)**.
Hal ini sangat berguna untuk proses menyeleksi sebuah ROI (Region of Interest) spesifik dalam suatu frame demi mengabaikan elemen latar belakang.

## 5. Pengaruh Nilai α Pada Image Blending
Operasi blending memadukan dua buah citra dengan formula linear: $Blended = img1 \cdot \alpha + img2 \cdot (1 - \alpha)$.
Nilai $\alpha$ (Alpha) di mana $0 \leq \alpha \leq 1$, menentukan bobot transparansi antara masing-masing saluran gambar masuk.
* Jika $\alpha = 1$, Citra Pertama (`img1`) akan terlihat utuh (100% solid) tanpa jejak sama sekali dari Citra Kedua, karena nilainya dikalikan 0.
* Jika $\alpha = 0$, Citra Kedua (`img2`) yang menjadi solid sepenuhnya tanpa jejak dari `img1`.
* Nilai menengah, sebagai contoh $\alpha = 0.5$, akan membuat tampilan di mana kedua citra adalah bayangan tembus pandang satu sama lain dengan proporsi keterlihatan yang seimbang (50% : 50%). Konsep dasar ini adalah core dari efek "Opacity / Transparency" pada layer-layer aplikasi *Photoshop / GIMP*.
