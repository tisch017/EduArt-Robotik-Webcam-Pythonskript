# 🚨 **ACHTUNG: Unvollständige Implementierung** 🚨

> Dieses Setup wurde **nicht vollständig finalisiert**, da die Projektzeit abgelaufen ist.  
> Der aktuelle Stand erlaubt es, einen Docker-Container zu erstellen.  
> **Eine Verbindung zu Node-RED konnte jedoch nicht erfolgreich hergestellt werden.**  
> Der Grund für dieses Problem ist **unklar** und konnte im Rahmen des Projekts nicht weiter untersucht werden.

---

# Docker-Container erstellen

## Verzeichnis auf dem IOTBot anlegen

```bash
mkdir camera-docker
cd camera-docker
```

Kopiere die `Dockerfile`, `docker-compose.yml` und das Python-Skript `script-camera-docker.py` in dieses Verzeichnis. (Siehe USB-Mounten)

---

## Docker-Image erstellen

### Online

```bash
docker build -t camera-docker-image .
```

### Offline

Alternativ kann das Image auch von einem anderen Gerät kopiert werden.

---

## Container starten

Zum Starten des Containers verwenden wir **Docker Compose**. Die Konfiguration befindet sich in der Datei `docker-compose.yml`. Diese muss ggf. angepasst werden, z. B. um die richtige Webcam auszuwählen.

### Docker starten

```bash
docker-compose up -d
```

### Docker stoppen

```bash
docker-compose down
```
