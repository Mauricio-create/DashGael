from flask import Flask, render_template
from markupsafe import Markup
from modules.DB import DatabaseHandler
from modules.Graph import GraphGenerator
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
    return render_template('index.html', plot_html = safe_html, plot_html1= safe1_html, plot_html2=safe2_html, plot_html3=safe3_html, plot_html4 = safe4_html, plot_html5 = safe5_html)

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
    return render_template('index.html', plot_html = safe_html, plot_html1= safe1_html, plot_html2=safe2_html, plot_html3=safe3_html, plot_html4 = safe4_html, plot_html5 = safe5_html)

@app.route('/vehiculos')
def vehiculos():
    plt_html = graph.generate_plot("SELECT * FROM tablename", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    return render_template('vehiculos/vehiculos.html', plot_html = safe_html)

@app.route('/lugares')
def lugares():
    plt_html = graph.generate_plot("SELECT * FROM tablename", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    plt_html1 = graph.generate_plot("SELECT * FROM tablename", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "barCol", xName = "Tipo", yName = "Evento", Titulo = "Colonias", rotation = 90)
    safe_html1 = Markup(plt_html1)
    return render_template('lugares/lugares.html', plot_html = safe_html, plot_html1 = safe_html1)

if __name__ == '__main__':
    app.run(debug=True)

# Toda esta clase es donde se hacen la consultas y se pasan al graficador