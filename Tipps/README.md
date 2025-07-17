# Linux-Spickzettel

## 1. DHCP / Routing einrichten

### Verbindung testen

```bash
ping -c 4 8.8.8.8
```

Beispielausgabe:

```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=22.6 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=22.4 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=22.7 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=117 time=22.3 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3003ms
rtt min/avg/max/mdev = 22.359/22.525/22.720/0.166 ms
```

### DHCP-Client neu starten (falls Ping fehlschlägt)

```bash
sudo dhclient eno1
```

### Standardroute manuell setzen (falls immer noch kein Erfolg)

```bash
sudo ip route del default
sudo ip route add default via 192.168.1.1 dev eno1 metric 100
```

Prüfen mit:

```bash
ping -c 4 8.8.8.8
```

_Hinweis:_ statt 8.8.8.8 auch google.com probiren

### Netzwerkschnittstellen anzeigen

```bash
ip addr
```

Beispielausgabe (gekürzt):

```text
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP qlen 1000
    inet 192.168.1.42/24 brd 192.168.1.255 scope global dynamic eno1
       valid_lft 86390sec preferred_lft 86390sec
```

_Hinweis:_ `eno1` ist das Interface zum internen Netzwerk – ggf. anpassen.

---

## 2. Webcam testen

### USB-Geräte listen

```bash
lsusb
```

Beispielausgabe:

```text
Bus 002 Device 003: ID 046d:0825 Logitech, Inc. Webcam C270
Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
```

### v4l-utils installieren

```bash
sudo apt install v4l-utils
```

### Verfügbare Video-Devices anzeigen

```bash
v4l2-ctl --list-devices
```

Beispielausgabe:

```text
HD Webcam C270 (usb-0000:00:14.0-1.6):
	/dev/video0
	/dev/video1
```

---

## 3. Dateien von USB-Sticks einbinden

```bash
lsblk                         # Blockgeräte anzeigen
sudo mkdir -p /mnt/usb        # Mount-Punkt anlegen
sudo mount /dev/sdb1 /mnt/usb # Stick einhängen (Beispielgerät)
cd /mnt/usb && ls             # Inhalt prüfen
sudo umount /mnt/usb          # Stick aushängen
```

Beispielausgaben:

`lsblk`

```text
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 238.5G  0 disk
└─sda1   8:1    0 238.5G  0 part /
sdb      8:16   1  28.9G  0 disk
└─sdb1   8:17   1  28.9G  0 part
```

`ls` innerhalb von `/mnt/usb`

```text
backup/
documents/
pictures/
```

---

## 4. Docker

### Laufende Container anzeigen

```bash
docker ps
```

Beispielausgabe:

```text
CONTAINER ID   IMAGE                  COMMAND             CREATED        STATUS        PORTS                    NAMES
f34a1c93b4e7   nodered/node-red:3.1   "npm --no-update-…"  2 hours ago    Up 2 hours    0.0.0.0:1880->1880/tcp   docker-eduart-node-red-1
```

### Interaktive Shell öffnen

```bash
docker exec -it <CONTAINER_NAME> /bin/bash
# Beispiel:
docker exec -it docker-eduart-node-red-1 /bin/bash
```

_Achtung:_ `docker attach` kann den Container abstürzen lassen.

---

## 5. Grundlegende Shell-Tipps

| Shortcut / Befehl              | Funktion                     |
| ------------------------------ | ---------------------------- |
| `sudo <Befehl>`                | Befehl als root ausführen    |
| `cd /pfad/zum/verzeichnis`     | Verzeichnis wechseln         |
| `ls`                           | Dateien/Ordner auflisten     |
| Tab                            | Auto-Vervollständigung       |
| ↑ / ↓                          | Befehls-Historie durchsuchen |
| Strg + C                       | Aktuellen Prozess abbrechen  |
| Strg + D oder `exit`           | Shell verlassen              |
| Rechtsklick / Strg + Shift + V | Einfügen ins Terminal        |
