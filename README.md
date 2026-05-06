Bumblebee: 80. Yıl Fuarı Demo Sprinti (6 - 11 Mayıs)
Hedef: 11 Mayıs'taki fuar için ziyaretçilerin interaktif olarak deneyimleyebileceği, RViz ve Gazebo tabanlı "GTA Tarzı" otonom araç simülasyonu hazırlamak.Konsept: Ziyaretçiler aracı klavye (WASD) ile sürebilecek (Manuel Mod). İstediğimiz an sistemi "Otomatik Mod"a alıp aracın engelleri aşarak parkuru kendi başına tamamlamasını (şov kısmını) göstereceğiz.

Görev Dağılımı ve Check-list
1. Altyapı ve Simülasyon (Sıla)

[ ] Gazebo Ortamı: İçerisinde şeritler, dubalar (engel) ve levhalar olan hafif bir fuar parkuru tasarlanması.

[ ] Araç Dinamikleri: Aracın Gazebo'ya aktarılması, LiDAR, Odometri ve /camera/image_raw sensörlerinin aktif edilmesi.

[ ] Manuel Kontrol: teleop_twist_keyboard (WASD) entegrasyonu ile aracın klavyeden sürülebilmesi.

[ ] RViz Arayüzü: Ziyaretçilere görsel şov sunmak için sadece gerekli verileri (Kamera, YOLO kutuları, Planlama çizgisi) gösteren temiz bir .rviz konfigürasyonu.

[ ] Docker & Git: Tüm ortamın tek bir komutla (bringup.launch.py) çalışacak şekilde Dockerize edilip repoya pushlanması.

2. Karar Verme ve Sistem Geçişi (Umut)

[ ] State Machine (Durum Makinesi): Manuel Mod (WASD) ile Otomatik Mod (Otonom Sürüş) arasında sorunsuz geçişi sağlayacak ROS2 servisi/düğümü.

[ ] Kill-Switch (Acil Durdurma): Ziyaretçi aracı duvara sürerse anında müdahale edebileceğimiz, tüm komutları kesip aracı kilitleyen acil fren butonu/komutu.

3. Yol Planlama (Murat)

[ ] Demo Rotası: GeoJSON bağımlılığı olmadan, Gazebo parkuru üzerinde aracın sürekli dönebileceği "hard-coded" veya basit bir hedef listesi (waypoints) oluşturulması.

[ ] TEB/A Entegrasyonu:* Rotanın dinamik ve statik engellere (dubalara) çarpmadan akıcı bir şekilde planlanması.

4. Algı ve Şerit Takibi (Beril & Betül)

[ ] YOLO Entegrasyonu (Beril): Gazebo'daki /camera/image_raw topiğinden alınan görüntülerdeki dubaların ve levhaların tespit edilip RViz ekranına (Bounding Box ile) yansıtılması.

[ ] Şerit Takibi (Betül): IPM ve Sliding Window algoritmalarının simülasyon kamerasına bağlanarak parkur şeritlerinin tespit edilmesi ve görselleştirilmesi.

5. Kontrol ve Akıcılık (Meryem)

[ ] Simülasyon Optimizasyonu: PID ve Stanley Controller parametrelerinin Gazebo'daki aracın fiziksel dinamiklerine (ağırlık, tork) göre ayarlanması.

[ ] Akıcı Sürüş: Araç otomatik moda geçtiğinde planlanan rotaya sert savrulmalar yapmadan, pürüzsüz bir şekilde oturmasının sağlanması.
