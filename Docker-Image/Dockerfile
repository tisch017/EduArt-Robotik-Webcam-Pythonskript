# Verwende ein grundlegendes Python-Basisimage
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopiere das aktuelle Verzeichnis (mit Ihrem Skript) in das Arbeitsverzeichnis
COPY . /app

# Installiere die erforderlichen Python-Pakete
RUN pip install opencv-python-headless numpy websockets

# Setze die Standard-Startkommando
CMD ["python", "script-camera-docker.py"]