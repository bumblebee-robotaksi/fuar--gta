Bumblebee: 80. Yıl Fuarı Demo Sprinti (6 - 11 Mayıs)
Hedef: 11 Mayıs'taki fuar için ziyaretçilerin interaktif olarak deneyimleyebileceği, RViz ve Gazebo tabanlı "GTA Tarzı" otonom araç simülasyonu hazırlamak.Konsept: Ziyaretçiler aracı klavye (WASD) ile sürebilecek (Manuel Mod). İstediğimiz an sistemi "Otomatik Mod"a alıp aracın engelleri aşarak parkuru kendi başına tamamlamasını (şov kısmını) göstereceğiz.


Before you run, one command on your host:
```bash
xhost +local:docker
```
This lets the Docker container open Gazebo/RViz windows on your screen.
You need this every time before running.

Then to run:
```bash
# With NVIDIA GPU
docker compose --profile gpu up

# Without GPU
docker compose --profile cpu up
```
