import cv2, pandas  # Biblioteca para procesamiento de imágenes y video y manejo de datos tabulares
import time  # Biblioteca para manejar tiempos y pausas
from datetime import datetime  # Para manejar fechas y horas

# Inicializamos la variable para almacenar el primer cuadro (frame) de referencia
first_frame = None

# Lista para almacenar el estado de detección en los cuadros consecutivos
status_list = [None, None]

# Lista para almacenar los tiempos de inicio y fin de detección de movimiento
times = []

# Creamos un DataFrame para almacenar los tiempos de inicio y fin de detección de movimiento
df = pandas.DataFrame(columns=['Start', 'End'])

# Capturamos el video desde la cámara (índice 0 indica la cámara predeterminada)
video = cv2.VideoCapture(0)

# Bucle infinito para procesar cada cuadro del video
while True:
    # Leemos un cuadro del video
    check, frame = video.read()

    # Inicializamos el estado en 0 (no se detecta movimiento)
    status = 0

    # Convertimos el cuadro a escala de grises para simplificar el procesamiento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicamos un desenfoque gaussiano para reducir el ruido y mejorar la detección de movimiento
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si es el primer cuadro, lo almacenamos como referencia y continuamos con el siguiente cuadro
    if first_frame is None:
        first_frame = gray
        continue

    # Calculamos la diferencia absoluta entre el cuadro actual y el cuadro de referencia
    delta_frame = cv2.absdiff(first_frame, gray)

    # Aplicamos un umbral para destacar las áreas con diferencias significativas
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos la imagen para rellenar los huecos y mejorar la detección de contornos
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Encontramos los contornos en la imagen umbralizada
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iteramos sobre cada contorno detectado
    for contour in cnts:
        # Ignoramos los contornos pequeños (menos de 20,000 píxeles de área)
        if cv2.contourArea(contour) < 20000:
            continue

        # Si encontramos un contorno significativo, actualizamos el estado a 1
        status = 1

        # Obtenemos las coordenadas del rectángulo delimitador del contorno
        (x, y, w, h) = cv2.boundingRect(contour)

        # Dibujamos un rectángulo alrededor del área detectada en el cuadro original
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Añadimos el estado actual a la lista de estados
    status_list.append(status)

    # Si el estado cambia de 0 a 1, registramos el tiempo de inicio del movimiento
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    # Si el estado cambia de 1 a 0, registramos el tiempo de fin del movimiento
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    # Mostramos las diferentes etapas del procesamiento en ventanas separadas
    cv2.imshow("Gray Frame", gray)  # Cuadro en escala de grises
    cv2.imshow("Delta Frame", delta_frame)  # Diferencia entre cuadros
    cv2.imshow("Threshold Frame", thresh_frame)  # Imagen umbralizada
    cv2.imshow("Color Frame", frame)  # Cuadro original con rectángulos dibujados

    # Esperamos una tecla por 1 milisegundo
    key = cv2.waitKey(1)

    # Si se presiona la tecla 'q', salimos del bucle
    if key == ord('q'):
        # Si el estado es 1 (movimiento detectado), registramos el tiempo de fin antes de salir
        if status == 1:
            times.append(datetime.now())
        break

# Imprimimos la lista de estados y los tiempos registrados
print(status_list)
print(times)

# Iteramos sobre los tiempos registrados para crear el DataFrame
for i in range(0, len(times), 2):
    df.loc[len(df)] = {'Start': times[i], 'End': times[i + 1]}

# Guardamos el DataFrame en un archivo CSV
df.to_csv("Times.csv")

# Liberamos la captura de video y cerramos todas las ventanas
video.release()
cv2.destroyAllWindows()
