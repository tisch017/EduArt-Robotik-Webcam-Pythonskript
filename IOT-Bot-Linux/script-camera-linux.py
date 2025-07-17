# Importanweisungen von Paketen:
import cv2
import numpy as np
import websockets
import json
import asyncio
from multiprocessing import Process, Manager
import base64

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
                        "area": distance_dict.get('area', 0),
                        "image": distance_dict.get('image64', 0)
                    }
                    await websocket.send(json.dumps(response))
                # Prüfe ob es eine Anfrage für die Farbbereiche und Fläche sind    
                if request.get('request') == 'set_params':
                    # Neue HSV-Grenzen und Flächen-Schwellenwert übernehmen
                    distance_dict['h_min']     = request.get('h_min', distance_dict.get('h_min'))
                    distance_dict['s_min']     = request.get('s_min', distance_dict.get('s_min'))
                    distance_dict['v_min']     = request.get('v_min', distance_dict.get('v_min'))
                    distance_dict['h_max']     = request.get('h_max', distance_dict.get('h_max'))
                    distance_dict['s_max']     = request.get('s_max', distance_dict.get('s_max'))
                    distance_dict['v_max']     = request.get('v_max', distance_dict.get('v_max'))
                    distance_dict['area_thres']= request.get('area_thres', distance_dict.get('area_thres'))
                    await websocket.send(json.dumps({"status":"parameters_updated"}))   
            except json.JSONDecodeError:
                print("Ungültiges JSON Format empfangen")
                
    except websockets.exceptions.ConnectionClosed:
        print("Websocket Verbindung geschlossen")

# Websocket Server starten
async def start_websocket_server(distance_dict):
    server = await websockets.serve(lambda ws, path: handle_websocket(ws, distance_dict), "localhost", 3000)
    print("Websocket Server läuft auf ws://localhost:3000")
    await server.wait_closed()

def detect_color(distance_dict):

    # Webcam initialisieren
    cap = cv2.VideoCapture(0)
    
    # Trackbars für HSV-Bereiche erstellen
    def nothing(x):
        pass

    while True:

        # Parameter bei Bedarf aus distance_dict aktualisieren
        required = {'h_min','s_min','v_min','h_max','s_max','v_max','area_thres'} # Prüfe ob alle Werte vorhanden
        if required.issubset(distance_dict.keys()):
            lower      = np.array([distance_dict['h_min'], distance_dict['s_min'], distance_dict['v_min']])
            upper      = np.array([distance_dict['h_max'], distance_dict['s_max'], distance_dict['v_max']])
            area_thres = distance_dict['area_thres']

        # Lese Bild von Kamerastream cap aus
        ret, frame = cap.read()
        if not ret:
            break
            
        # Konvertiere das Bild von BGR zu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Erstelle Maske für den definierten Farbbereich
        mask = cv2.inRange(hsv, lower, upper)

        # Finde alle Konturen
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Erstelle Ausgabebild
        result = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        if contours:
            # Finde die größte Kontur
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Berechne die Fläche
            area = cv2.contourArea(largest_contour)
            
            # Nur weitermachen wenn die Fläche groß genug ist
            if area > area_thres:  # Schwellwert anpassbar
                # Rechteck um die Kontur
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Zeichne das Rechteck
                cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Berechne den Mittelpunkt
                center_x = x + w//2
                center_y = y + h//2
                
                # Zeichne den Mittelpunkt
                cv2.circle(result, (center_x, center_y), 5, (255, 0, 0), -1)
                
                # Zeige die Koordinaten an
                text = f"Center: ({center_x}, {center_y})"
                cv2.putText(result, text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Zeige die Fläche an
                area_text = f"Area: {int(area)}"
                cv2.putText(result, area_text, (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Berechne vertikale Bildmitte:
                height, width = result.shape[:2]
                vertical_center = width / 2
                distance_to_center = center_x - vertical_center

                # Speichere den Distanz-Wert und die Fläche im Dictionary
                distance_dict['distance_value'] = distance_to_center
                distance_dict['area'] = area

                # Zeige Abstand zur Bildmitte als Text an:
                distance_text = f"Distance to center: {distance_to_center}px"
                cv2.putText(result, distance_text, (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            else:
                # Wenn keine ausreichend große Kontur gefunden wird
                distance_dict['distance_value'] = None
                distance_dict['area'] = 0

                # Info auf Resultbild ausgeben
                height, width = result.shape[:2]
                cv2.putText(result, "No object detected", (height-30, width-200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
        else:
            # Wenn keine Konturen vorhanden sind
            distance_dict['distance_value'] = None
            distance_dict['area'] = 0

            # Info auf Resultbild ausgeben
            height, width = result.shape[:2]
            cv2.putText(result, "No object detected", (height-30, width-200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Zeige Farbebereiche auf Ausgabebild
        lower_color_text = f"Untere Farbgrenze: {int(lower[0])};{int(lower[1])};{int(lower[2])}"
        cv2.putText(result, lower_color_text, (10, height-60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        upper_color_text = f"Obere Farbgrenze: {int(upper[0])};{int(upper[1])};{int(upper[2])}"
        cv2.putText(result, upper_color_text, (10, height-30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Wandle Resultbild in JPG um
        success, buffer = cv2.imencode('.jpg', result)
        if not success or buffer is None:
            # Kodierung fehlgeschlagen: optional vorheriges Bild behalten oder Platzhalter setzen
            print("Fehler: Bild konnte nicht in JPEG konvertiert werden")
        else:
            distance_dict['image64'] = base64.b64encode(buffer.tobytes()).decode('utf-8')

        # Zeige Originalframe, Maske und Ergebnis
        # cv2.imshow('Original', frame)
        # cv2.imshow('result', result)
        
        # Beenden mit 'q'
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Programm starten
if __name__ == '__main__':

    manager = Manager()
    distance_dict = manager.dict()

    # Werte auf Farberkennung Rot initial setzen
    distance_dict['h_min']     = 112
    distance_dict['s_min']     = 173
    distance_dict['v_min']     = 134
    distance_dict['h_max']     = 179
    distance_dict['s_max']     = 255
    distance_dict['v_max']     = 255
    distance_dict['area_thres']= 500

    # Starte den WebSocket-Server im Event Loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_task = loop.create_task(start_websocket_server(distance_dict))

    # Starte den Farberkennungsprozess
    process = Process(target=detect_color, args=(distance_dict,))
    process.start()

    # Warte auf Beendigung des WebSocket-Servers
    try:
        loop.run_until_complete(server_task)
    finally:
        process.join()
