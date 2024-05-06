from flask import Flask, render_template, request
from markupsafe import Markup
import pandas as pd
from modules.DB import DatabaseHandler
from modules.Graph import GraphGenerator
from modules.MapGenerator import MapGenerator
import os

DATABASE_CONFIG = {
    'user':  'root',
    'password': '',
    'host': 'localhost',
    'database': 'Accidentes',
    'raise_on_warnings': True
}


db = DatabaseHandler(DATABASE_CONFIG)
graph = GraphGenerator(db)
app = Flask(__name__)


def map_alcaldias(): 
    path = "data/alcaldias.json"
    query = "SELECT alcaldia, coordenada_x, coordenada_y from tablename"
    data = db.query_db(query, None)
    alcaldias_data = pd.DataFrame(data)
    alcaldias_data.dropna(subset=['alcaldia','coordenada_x', 'coordenada_y'], inplace = True)
    # Convertir las columnas a numéricas y rellenar los valores faltantes con cero
    alcaldias_data['coordenada_x'] = pd.to_numeric(alcaldias_data["coordenada_x"], errors='coerce').fillna(0)
    alcaldias_data['coordenada_y'] = pd.to_numeric(alcaldias_data["coordenada_y"], errors='coerce').fillna(0)
    mapGenerator = MapGenerator(alcaldias_data,path)
    return mapGenerator.gereate_map()


def map_colonias(): 
    path = "data/catlogo-de-colonias.json"
    query = "SELECT colonia, coordenada_x, coordenada_y from tablename"
    data = db.query_db(query, None)
    alcaldias_data = pd.DataFrame(data)
    alcaldias_data.dropna(subset=['colonia','coordenada_x', 'coordenada_y'], inplace = True)
    alcaldias_data['coordenada_x'] = pd.to_numeric(alcaldias_data["coordenada_x"], errors='coerce').fillna(0)
    alcaldias_data['coordenada_y'] = pd.to_numeric(alcaldias_data["coordenada_y"], errors='coerce').fillna(0)
    mapGenerator = MapGenerator(alcaldias_data,path)
    return mapGenerator.gereate_map()


def shut_down_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("No se pudo apagar el servidor")
    func()


@app.route('/')
def dashboard():
    plt_html = graph.generate_plot("SELECT condicion, COUNT(no_folio) as No_Accidentes FROM tablename GROUP BY 1", plot_type='bar', x_axis='condicion', y_axis='No_Accidentes', className = "accidentes", xName = "Tipo de condición", yName = "Número de accidentes", Titulo = "Accidentes por condición", rotation = 90)
    safe_html = Markup(plt_html)
    plt1_html = graph.generate_plot("SELECT tipo_de_evento, condicion, COUNT(no_folio) as No_Accidentes FROM tablename GROUP BY 1,2", plot_type='bar', x_axis='tipo_de_evento', y_axis='No_Accidentes', className = "evento", xName = "Tipo de evento", yName = "Número de accidentes", Titulo = "Condición por evento", rotation = 90, hue="condicion")
    safe1_html = Markup(plt1_html)
    plt2_html = graph.generate_plot("SELECT year(fecha_evento) as Fecha, COUNT(no_folio) as NUM FROM tableName GROUP BY 1 ORDER BY 1", plot_type='line_plot', x_axis='Fecha', y_axis='NUM', className = "fechas", xName = "Fecha", yName = "Número de accidentes", Titulo = "Accidentes por año", rotation = 90)
    safe2_html = Markup(plt2_html)
    plt3_html = graph.generate_plot("SELECT genero, COUNT(no_folio) as NUM_G FROM tableName GROUP BY 1", plot_type='pie', x_axis='genero', y_axis='NUM_G', className = "genero", xName = " ", yName = " ", Titulo = "Género", rotation = 90)
    safe3_html = Markup(plt3_html)
    plt4_html = graph.generate_plot("SELECT dia, count(no_folio) as cuenta from tablename group by 1", plot_type='line_plot', x_axis='dia', y_axis='cuenta', className = "dias", xName = "Día", yName = "Accidentes", Titulo = "Accidentes por dia", rotation = 90)
    safe4_html = Markup(plt4_html)
    plt5_html = graph.generate_plot("SELECT count(no_folio) as numero from tablename", plot_type='card', x_axis='dia', y_axis='cuenta', className = "cardtotal", xName = "Día", yName = "Accidentes", Titulo = "Numero de accidentes", rotation = 90)
    safe5_html = Markup(plt5_html)
    plt6_html = graph.generate_plot("SELECT * FROM tablename", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "ageDistribution", xName = "Tipo", yName = "Evento", Titulo = "Distribucion de edad", rotation = 90)
    safe6_html = Markup(plt6_html)
    return render_template('index.html', plot_html = safe_html, plot_html1= safe1_html, plot_html2=safe2_html, plot_html3=safe3_html, plot_html4 = safe4_html, plot_html5 = safe5_html, plot_html_age = safe6_html)

@app.route('/eventos')
def eventos():
    plt_html = graph.generate_plot("SELECT condicion, COUNT(no_folio) as No_Accidentes FROM tablename GROUP BY 1", plot_type='bar', x_axis='condicion', y_axis='No_Accidentes', className = "accidentes", xName = "Tipo de condición", yName = "Número de accidentes", Titulo = "Accidentes por condición", rotation = 90)
    safe_html = Markup(plt_html)
    plt1_html = graph.generate_plot("SELECT tipo_de_evento, condicion, COUNT(no_folio) as No_Accidentes FROM tablename GROUP BY 1,2", plot_type='bar', x_axis='tipo_de_evento', y_axis='No_Accidentes', className = "evento", xName = "Tipo de evento", yName = "Número de accidentes", Titulo = "Condición por evento", rotation = 90, hue="condicion")
    safe1_html = Markup(plt1_html)
    plt2_html = graph.generate_plot("SELECT year(fecha_evento) as Fecha, COUNT(no_folio) as NUM FROM tableName GROUP BY 1 ORDER BY 1", plot_type='line_plot', x_axis='Fecha', y_axis='NUM', className = "fechas", xName = "Fecha", yName = "Número de accidentes", Titulo = "Accidentes por año", rotation = 90)
    safe2_html = Markup(plt2_html)
    plt3_html = graph.generate_plot("SELECT genero, COUNT(no_folio) as NUM_G FROM tableName GROUP BY 1", plot_type='pie', x_axis='genero', y_axis='NUM_G', className = "genero", xName = " ", yName = " ", Titulo = "Género", rotation = 90)
    safe3_html = Markup(plt3_html)
    plt4_html = graph.generate_plot("SELECT dia, count(no_folio) as cuenta from tablename group by 1", plot_type='line_plot', x_axis='dia', y_axis='cuenta', className = "dias", xName = "Día", yName = "Accidentes", Titulo = "Accidentes por dia", rotation = 90)
    safe4_html = Markup(plt4_html)
    plt5_html = graph.generate_plot("SELECT count(no_folio) as numero from tablename", plot_type='card', x_axis='dia', y_axis='cuenta', className = "cardtotal", xName = "Día", yName = "Accidentes", Titulo = "Numero de accidentes", rotation = 90)
    safe5_html = Markup(plt5_html)
    plt6_html = graph.generate_plot("SELECT * FROM tablename", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "ageDistribution", xName = "Tipo", yName = "Evento", Titulo = "Distribucion de edad", rotation = 90)
    safe6_html = Markup(plt6_html)
    return render_template('index.html', plot_html = safe_html, plot_html1= safe1_html, plot_html2=safe2_html, plot_html3=safe3_html, plot_html4 = safe4_html, plot_html5 = safe5_html, plot_html_age = safe6_html)

@app.route('/vehiculos')
def vehiculos():
    plt_html = graph.generate_plot("SELECT Implicado, count(no_folio) as numero from tablename group by 1", plot_type='pie', x_axis='Implicado', y_axis='numero', className = "tipoImplicado", xName = "", yName = "", Titulo = "Implicados", rotation = 90)
    safe_html = Markup(plt_html)
    plt1_html = graph.generate_plot("SELECT Vehiculo, count(no_folio) as numero from tablename group by 1", plot_type='pie', x_axis='Vehiculo', y_axis='numero', className = "tipoVehiculo", xName = "", yName = "", Titulo = "Vehiculos implicados", rotation = 90)
    safe1_html = Markup(plt1_html)
    plt2_html = graph.generate_plot("SELECT marca_vehiculo, count(no_folio) as numero from tablename group by 1 order by 2 desc limit 10", plot_type='bar', x_axis='marca_vehiculo', y_axis='numero', className = "marcaVehiculo", xName = "Marca", yName = "Accidentes", Titulo = "Top 10 marcas de vehiculos", rotation = 90)
    safe2_html = Markup(plt2_html)
    plt3_html = graph.generate_plot("SELECT vehiculo, implicado, count(no_folio) as numero from tablename group by 1, 2 order by 2 desc", plot_type='heatmap', x_axis='vehiculo', y_axis='implicado', className = "mapaCalor", xName = "Implicado", yName = "Vehiculo", Titulo = "Implicado vs vehiculo(miles)", rotation = 90)
    safe3_html = Markup(plt3_html)
    return render_template('vehiculos/vehiculos.html', plot_html = safe_html, plot_html_vehiculo = safe1_html, plot_html_marca = safe2_html, plot_joinPlot = safe3_html)

@app.route('/lugares')
def lugares():
    plt_html = graph.generate_plot("SELECT interseccion_semaforizada, count(no_folio) as numero FROM tablename group by 1", plot_type='pie', x_axis='interseccion_semaforizada', y_axis='numero', className = "semaforizada", xName = "", yName = "", Titulo = "Intersecciones semaforizadas", rotation = 90)
    safe_html = Markup(plt_html)
    plt1_html = graph.generate_plot(" SELECT colonia, count(no_folio) as numero from tablename group by 1 order by 2 desc limit 10;", plot_type='bar', x_axis='colonia', y_axis='numero', className = "colonias", xName = "Colonias", yName = "Accidentes", Titulo = "Top 10 colonias con más accidentes", rotation = 90)
    safe1_html = Markup(plt1_html)
    plt2_html = graph.generate_plot(" SELECT alcaldia, count(no_folio) as numero from tablename group by 1 order by 2 desc limit 10;", plot_type='bar', x_axis='alcaldia', y_axis='numero', className = "alcaldias", xName = "Alcaldias", yName = "Accidentes", Titulo = "Top 10 alcaldias con más accidentes", rotation = 90)
    safe2_html = Markup(plt2_html)
    plt3_html = graph.generate_plot(" Select tipo_de_interseccion, count(no_folio) as numero from tablename group by 1 order by 2", plot_type='pie', x_axis='tipo_de_interseccion', y_axis='numero', className = "tipo_interseccion", xName = "", yName = "", Titulo = "Tipo de interseccion", rotation = 90)
    safe3_html = Markup(plt3_html)
    plt4_html = map_alcaldias()
    safe4_html = Markup(plt4_html)
    plt5_html = map_colonias()
    safe5_html = Markup(plt5_html)
    return render_template('lugares/lugares.html', plot_html = safe_html, plot_html_colonias = safe1_html, plot_html_alcaldias = safe2_html, plot_html_tipo_iterseccion = safe3_html, plot_html_map_alcaldias = safe4_html, plot_html_map_colonias = safe5_html)

@app.route('/salir')
def salir(): 
    db.close()
    shut_down_server()
    return "Servidor apagado", 200

if __name__ == '__main__':
    app.run(debug=True)

# Toda esta clase es donde se hacen la consultas y se pasan al graficador