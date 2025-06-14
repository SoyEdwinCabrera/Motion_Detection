from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter

# Verificar el contenido del DataFrame
print("Contenido del DataFrame:")
print(df)

# Validar que las columnas 'Start' y 'End' existen y no están vacías
if 'Start' in df.columns and 'End' in df.columns and not df.empty:
    # Crear el gráfico
    p = figure(title="Motion Graph", x_axis_label='Time (seconds)', height=400, width=1000, x_axis_type="datetime")
    
    p.yaxis.minor_tick_line_color = None  # Ocultar las líneas menores del eje Y
    p.yaxis[0].ticker.desired_num_ticks = 1  # Configurar el número de ticks en el eje Y
    
    # Configurar el formateador de etiquetas para mostrar solo segundos
    p.xaxis.formatter = DatetimeTickFormatter(seconds="%Ss")
    
    # Dibujar las barras
    p.quad(left=df['Start'], right=df['End'], bottom=0, top=1, color='green')

    # Generar el archivo HTML y mostrar el gráfico
    output_file("Graph.html")
    show(p)
else:
    print("El DataFrame no contiene datos válidos en las columnas 'Start' y 'End'.")
