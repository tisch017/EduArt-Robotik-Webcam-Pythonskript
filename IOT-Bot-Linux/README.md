# **Python-Skript zur direkten Ausführung auf dem Linux des IOTBot**

Dieses Python-Skript ist zur **direkten Ausführung auf dem Debian Linux des IOTBot** vorgesehen.

---

## Voraussetzungen

Um das Skript auszuführen, müssen folgende Pakete installiert sein:

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-numpy
sudo apt install python3-websockets
sudo apt install python3-opencv
sudo apt install python3-multiprocessing
```

---

## Starten des Skripts

```bash
python3 script-camera-linux.py
```

> 💡 **Hinweis:** Ggf. muss die Kamera-ID angepasst werden, falls mehrere Kameras verbunden sind.
