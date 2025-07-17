## Verwendung des Skripts `script-camera-GUI.py`

Das Skript `script-camera-GUI.py` dient zum **Testen und Einstellen** der Webcam sowie der **Objekterkennung**. Es bietet eine grafische Benutzeroberfläche (GUI) und ist daher **nur auf einem PC mit grafischer Oberfläche** lauffähig – **nicht auf dem IOTBot** und auch **nicht dafür vorgesehen**.

### Beispielaufruf in der Eingabeaufforderung (CMD):

```bash
python "Pfad\zum\script-camera-GUI.py" 112 173 134 179 255 255 500 1
```

### Parameterbeschreibung:

- `h_min`: Untere Farbgrenze im HSV-Farbraum (H = Farbwert)
- `s_min`: Untere Farbgrenze im HSV-Farbraum (S = Sättigung)
- `v_min`: Untere Farbgrenze im HSV-Farbraum (V = Helligkeit)
- `h_max`: Obere Farbgrenze im HSV-Farbraum (H = Farbwert, max. 179)
- `s_max`: Obere Farbgrenze im HSV-Farbraum (S = Sättigung, max. 255)
- `v_max`: Obere Farbgrenze im HSV-Farbraum (V = Helligkeit, max. 255)
- `area`: Mindestfläche, die als Objekt erkannt werden soll
- `camera_id`: ID der verwendeten Kamera (interne Kamera meist `0`, externe Kamera `1` oder höher)

> ⚠️ Hinweis: Dieses Tool ist ausschließlich für Test- und Kalibrierungszwecke gedacht.

---

## Benötigte Python-Pakete

Das Skript benötigt folgende Python-Module:

```python
import cv2
import numpy as np
import sys
import websockets
import json
import asyncio
from multiprocessing import Process, Manager
```

### Installation unter Debian/Linux

Die benötigten Pakete können unter Debian-basierten Systemen wie folgt installiert werden:

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-numpy
sudo apt install python3-websockets
sudo apt install python3-opencv
sudo apt install python3-multiprocessing
```

> 💡 Stelle sicher, dass du `python3` verwendest, da einige Distributionen noch `python` mit Python 2 verknüpfen.
