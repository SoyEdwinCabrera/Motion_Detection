# 📖 Manual de Creación del Proyecto: Detector de Movimiento

¡Bienvenido al manual de creación del proyecto! Este detector de movimiento utiliza Python y OpenCV para identificar cambios en una escena capturada por una cámara. Aquí aprenderás cómo configurar, ejecutar y entender el funcionamiento del proyecto. 🚀

---

## 🛠️ **Requisitos Previos**

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

1. **Python 3.7 o superior** 🐍
2. Las siguientes bibliotecas:
   - `opencv-python` 📸
   - `pandas` 📊

Puedes instalarlas ejecutando el siguiente comando en tu terminal:
```bash
pip install opencv-python pandas
```

---

## 📂 **Estructura del Proyecto**

El proyecto consta de un único archivo principal:
- `motion_detector.py`: Contiene todo el código necesario para capturar video, procesar imágenes y registrar los tiempos de detección de movimiento.

---

## 🚀 **Cómo Ejecutar el Proyecto**

1. **Clona el repositorio** o copia el archivo `motion_detector.py` en tu máquina local.
2. Abre una terminal en el directorio donde se encuentra el archivo.
3. Ejecuta el siguiente comando:
   ```bash
   python motion_detector.py
   ```
4. El programa comenzará a capturar video desde tu cámara predeterminada. 🎥

---

## 🖥️ **Funcionamiento del Programa**

### **1. Captura de Video**
El programa utiliza la cámara predeterminada de tu computadora para capturar cuadros en tiempo real. Asegúrate de que tu cámara esté conectada y funcionando correctamente. 📸

### **2. Procesamiento de Imágenes**
Cada cuadro capturado pasa por los siguientes pasos:
- **Conversión a escala de grises**: Simplifica el procesamiento eliminando la información de color.
- **Desenfoque Gaussiano**: Reduce el ruido en la imagen para mejorar la detección de movimiento.
- **Diferencia entre cuadros**: Compara el cuadro actual con un cuadro de referencia para identificar cambios.
- **Umbral y dilatación**: Destaca las áreas con movimiento y rellena huecos en las regiones detectadas.

### **3. Detección de Movimiento**
El programa identifica contornos en las áreas con movimiento y dibuja rectángulos alrededor de ellos. Solo se consideran contornos con un área significativa (mayor a 20,000 píxeles). 🟩

### **4. Registro de Tiempos**
Cada vez que se detecta movimiento, el programa registra:
- **Inicio del movimiento**: Cuando el estado cambia de "sin movimiento" a "movimiento detectado".
- **Fin del movimiento**: Cuando el estado cambia de "movimiento detectado" a "sin movimiento".

Estos tiempos se almacenan en un archivo CSV llamado `Times.csv`. 📊

---

## ⌨️ **Controles**

- **Tecla `q`**: Presiónala para salir del programa. Si hay movimiento detectado al momento de salir, se registrará el tiempo de fin automáticamente. 🛑

---

## 📊 **Salida del Programa**

Al finalizar la ejecución, el programa generará un archivo `Times.csv` con los tiempos de inicio y fin de cada detección de movimiento. Este archivo puede ser abierto con cualquier editor de texto o software de hojas de cálculo como Excel. 📄

Ejemplo de contenido del archivo:
```
Start,End
2023-10-01 14:23:45,2023-10-01 14:23:50
2023-10-01 14:24:10,2023-10-01 14:24:15
```

---

## 🛠️ **Personalización**

Si deseas ajustar el comportamiento del programa, puedes modificar los siguientes parámetros en el código:
1. **Área mínima de contornos**:
   - Ubicado en la línea:
     ```py
     if cv2.contourArea(contour) < 20000:
     ```
   - Cambia `20000` por un valor más bajo o más alto según el tamaño de los objetos que deseas detectar.

2. **Umbral de diferencia**:
   - Ubicado en la línea:
     ```py
     thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
     ```
   - Cambia `50` por un valor más alto para ignorar diferencias menores o más bajo para detectar cambios más pequeños.

---

## 🐞 **Solución de Problemas**

### **1. La cámara no funciona**
- Asegúrate de que tu cámara esté conectada y no esté siendo utilizada por otro programa.

### **2. Detecciones falsas**
- Ajusta el área mínima de contornos o el umbral de diferencia como se indica en la sección de personalización.

### **3. El archivo CSV no se genera**
- Verifica que el programa tenga permisos para escribir en el directorio donde se ejecuta.