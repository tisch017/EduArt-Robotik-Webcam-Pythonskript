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

---

# Autostart mit Boot einstellen

Um das Skript automatisch beim Systemstart auszuführen, kannst du einen **Systemd-Service** erstellen:

### 1. Service-Datei erstellen

```bash
sudo nano /etc/systemd/system/camera-script.service
```

### 2. Inhalt der Datei einfügen

```ini
[Unit]
Description=Camera Script Autostart
After=network.target

[Service]
ExecStart=/usr/bin/python3 /pfad/zum/script-camera-linux.py
WorkingDirectory=/pfad/zum/verzeichnis
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi  # oder ein anderer Benutzername

[Install]
WantedBy=multi-user.target
```

> 🔧 Ersetze `/pfad/zum/script-camera-linux.py` und `User=pi` durch die tatsächlichen Pfade und den richtigen Benutzernamen.

### 3. Service aktivieren und starten

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable camera-script.service
sudo systemctl start camera-script.service
```

### 4. Status prüfen

```bash
sudo systemctl status camera-script.service
```
