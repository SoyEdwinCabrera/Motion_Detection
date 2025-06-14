from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool, ColumnDataSource

# Verificar el contenido del DataFrame
print("Contenido del DataFrame:")
print(df)

# Asegurarse de que las columnas 'Start' y 'End' son de tipo datetime
df["Start-string"]= df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End-string"]= df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Importar las librerías necesarias
cds = ColumnDataSource(df)
    # Crear el gráfico
p = figure(title="Motion Graph", x_axis_label='datetime', height=400, width=1000, x_axis_type="datetime")

p.yaxis.minor_tick_line_color = None  # Ocultar las líneas menores del eje Y
p.yaxis[0].ticker.desired_num_ticks = 1  # Configurar el número de ticks en el eje Y

# Configurar el hover tool para mostrar los tiempos de inicio y fin
#Agregar la herramienta HoverTool configurando qué información mostrar
hover = HoverTool(tooltips=[
    ("Start", "@Start{%F %T}"),
    ("End", "@End{%F %T}")
],
formatters={
    '@Start': 'datetime',  # Formatea la columna Start como datetime
    '@End'  : 'datetime',  # Formatea la columna End como datetime
},
mode='vline')  # Puedes ajustar el modo de la herramienta según tus necesidades
   
p.add_tools(hover)

# Configurar el formateador de etiquetas para mostrar solo segundos
p.xaxis.formatter = DatetimeTickFormatter(seconds="%Ss")

# Dibujar las barras
p.quad(left="Start", right="End", bottom=0, top=1, color='green', source =cds)

# Generar el archivo HTML y mostrar el gráfico
output_file("Graph.html")
show(p)
