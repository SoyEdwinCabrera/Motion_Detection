import cv2  # Biblioteca para procesamiento de imágenes y video
import time  # Biblioteca para manejar tiempos y pausas

# Inicializamos la variable para almacenar el primer cuadro (frame) de referencia
first_frame = None

# Capturamos el video desde la cámara (índice 0 indica la cámara predeterminada)
video = cv2.VideoCapture(0)

# Bucle infinito para procesar cada cuadro del video
while True:
    # Leemos un cuadro del video
    check, frame = video.read()

    # Convertimos el cuadro a escala de grises para simplificar el procesamiento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Aplicamos un desenfoque gaussiano para reducir el ruido y mejorar la detección de movimiento
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si es el primer cuadro, lo almacenamos como referencia y continuamos con el siguiente cuadro
    if first_frame is None:
        first_frame = gray
        continue
        
    # Calculamos la diferencia absoluta entre el cuadro actual y el primer cuadro
    delta_frame = cv2.absdiff(first_frame, gray)
    # Aplicamos un umbral para destacar las áreas con diferencias significativas
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # Dilatamos la imagen para rellenar los huecos y mejorar la detección de contornos
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Encontramos los contornos en la imagen umbralizada
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iteramos sobre cada contorno detectado
    for contour in cnts:
        # Ignoramos los contornos pequeños (menos de 1000 píxeles de área)
        if cv2.contourArea(contour) < 1000:
            continue
        # Obtenemos las coordenadas del rectángulo delimitador del contorno
        (x, y, w, h) = cv2.boundingRect(contour)
        # Dibujamos un rectángulo alrededor del área detectada en el cuadro original
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Mostramos las diferentes etapas del procesamiento en ventanas separadas
    cv2.imshow("Gray Frame", gray)  # Cuadro en escala de grises
    cv2.imshow("Delta Frame", delta_frame)  # Diferencia entre cuadros
    cv2.imshow("Threshold Frame", thresh_frame)  # Imagen umbralizada
    cv2.imshow("Color Frame", frame)  # Cuadro original con rectángulos dibujados

    # Esperamos una tecla por 1 milisegundo
    key = cv2.waitKey(1)

    # Si se presiona la tecla 'q', salimos del bucle
    if key == ord('q'):
        break

# Liberamos la captura de video y cerramos todas las ventanas
video.release()
cv2.destroyAllWindows()
