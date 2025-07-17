# Importanweisungen von Paketen:
import cv2
import numpy as np
import sys
import websockets
import json
import asyncio
from multiprocessing import Process, Manager

# Websocket Handler Funktion
async def handle_websocket(websocket, distance_dict):
    try:
        while True:
            # Warte auf Anfrage von Node-RED
            message = await websocket.recv()
            
            try:
                request = json.loads(message)
                # Prüfe ob es eine Anfrage für den Distanz-Wert ist
                if request.get('request') == 'get_distance':
                    # Sende den aktuellen Distanz-Wert
                    response = {
                        "distance_to_center": distance_dict.get('distance_value', None),
                        "area": distance_dict.get('area', 0)
                    }
                    await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                print("Ungültiges JSON Format empfangen")
                
    except websockets.exceptions.ConnectionClosed:
        print("Websocket Verbindung geschlossen")

# Websocket Server starten
async def start_websocket_server(distance_dict):
    server = await websockets.serve(lambda ws, path: handle_websocket(ws, distance_dict), "localhost", 8081)
    print("Websocket Server läuft auf ws://localhost:8081")
    await server.wait_closed()

def detect_color(lower: np.ndarray, upper: np.ndarray, area_thres, camera_id, distance_dict):
    # Webcam initialisieren
    cap = cv2.VideoCapture(camera_id)
    
    # Fenster für Trackbars erstellen
    # cv2.namedWindow('Color Detection')
    
    # Trackbars für HSV-Bereiche erstellen
    def nothing(x):
        pass
    
    # Erstelle 6 Trackbars für untere und obere HSV-Grenzen
    # cv2.createTrackbar('H_min', 'Color Detection', 0, 179, nothing)
    #cv2.createTrackbar('H_max', 'Color Detection', 179, 179, nothing)
    #cv2.createTrackbar('S_min', 'Color Detection', 0, 255, nothing)
    #cv2.createTrackbar('S_max', 'Color Detection', 255, 255, nothing)
    #cv2.createTrackbar('V_min', 'Color Detection', 0, 255, nothing)
    #cv2.createTrackbar('V_max', 'Color Detection', 255, 255, nothing)
    #cv2.createTrackbar('Min Area', 'Color Detection', 200, 2000, nothing)

    while True:
        # Lese Bild von Kamerastream cap aus
        ret, frame = cap.read()
        if not ret:
            break
            
        # Konvertiere das Bild von BGR zu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Lese aktuelle Trackbar-Positionen
        # h_min = cv2.getTrackbarPos('H_min', 'Color Detection')
        # h_max = cv2.getTrackbarPos('H_max', 'Color Detection')
        # s_min = cv2.getTrackbarPos('S_min', 'Color Detection')
        # s_max = cv2.getTrackbarPos('S_max', 'Color Detection')
        # v_min = cv2.getTrackbarPos('V_min', 'Color Detection')
        # v_max = cv2.getTrackbarPos('V_max', 'Color Detection')
        # area_val = cv2.getTrackbarPos('Min Area', 'Color Detection')
        
        # Definiere HSV-Bereich für die Farberkennung
        # lower_color = np.array([h_min, s_min, v_min])
        # upper_color = np.array([h_max, s_max, v_max])
        # lower_color = lower
        # upper_color = upper

        # Erstelle Maske für den definierten Farbbereich
        mask = cv2.inRange(hsv, lower, upper)
        
        # Rauschreduzierung
        # kernel = np.ones((5,5), np.uint8)
        # mask = cv2.erode(mask, kernel, iterations=1)
        # mask = cv2.dilate(mask, kernel, iterations=1)

        # Finde alle Konturen
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Finde die größte Kontur
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Berechne die Fläche
            area = cv2.contourArea(largest_contour)
            
            # Nur weitermachen wenn die Fläche groß genug ist
            if area > area_thres:  # Schwellwert anpassbar
                # Rechteck um die Kontur
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Berechne den Mittelpunkt
                center_x = x + w//2
                height, width = frame.shape[:2]
                vertical_center = width / 2
                distance_to_center = center_x - vertical_center

                # Speichere den Distanz-Wert und die Fläche im Dictionary
                distance_dict['distance_value'] = distance_to_center
                distance_dict['area'] = area
            else:
                # Wenn keine ausreichend große Kontur gefunden wird
                distance_dict['distance_value'] = None
                distance_dict['area'] = 0
        else:
            # Wenn keine Konturen vorhanden sind
            distance_dict['distance_value'] = None
            distance_dict['area'] = 0

        # Zeige Originalframe, Maske und Ergebnis
        cv2.imshow('Original', frame)
        cv2.imshow('result', mask)
        
        # Beenden mit 'q'
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Programm starten
if __name__ == '__main__':

    # Überprüfe die Anzahl der Argumente
    if len(sys.argv) < 9:
        print("Verwendung: python script.py h_min s_min v_min h_max s_max v_max area camera_id")
        print("Beispiel: python script.py 1 0 100 100 179 255 255 500")
        sys.exit(1)
    
    try:
        # Untere HSV-Grenze
        h_min = int(sys.argv[1])
        s_min = int(sys.argv[2])
        v_min = int(sys.argv[3])
        
        # Obere HSV-Grenze
        h_max = int(sys.argv[4])
        s_max = int(sys.argv[5])
        v_max = int(sys.argv[6])

        # Schwellwert Fläche
        area_thres = int(sys.argv[7])
        # Kamera Modus
        camera_id = int(sys.argv[8])

    except ValueError:
        print("Error: Alle Argumente müssen Zahlen sein!")
        sys.exit(1)
    except IndexError:
        print("Error: Nicht genügend Argumente!")
        sys.exit(1)

    arr_lower = np.array([h_min, s_min, v_min]) # Standard: 112 173 134
    arr_upper = np.array([h_max, s_max, v_max]) # Standard: 179 255 255

    manager = Manager()
    distance_dict = manager.dict()

    # Starte den WebSocket-Server im Event Loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_task = loop.create_task(start_websocket_server(distance_dict))

    # Starte den Farberkennungsprozess
    process = Process(target=detect_color, args=(arr_lower, arr_upper, area_thres, camera_id, distance_dict))
    process.start()

    # Warte auf Beendigung des WebSocket-Servers
    try:
        loop.run_until_complete(server_task)
    finally:
        process.join()