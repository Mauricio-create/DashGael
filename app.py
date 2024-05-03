from flask import Flask, render_template
from markupsafe import Markup
from modules.DB import DatabaseHandler
from modules.Graph import GraphGenerator
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_CONFIG = {
    'user':  'root',
    'password': 'R00t',
    'host': 'localhost',
    'database': 'hechos_transito',
    'raise_on_warnings': True
}


db = DatabaseHandler(DATABASE_CONFIG)
graph = GraphGenerator(db)
app = Flask(__name__)



@app.route('/')
def dashboard():
    plt_html = graph.generate_plot("SELECT Tipo_evento as Tipo_E, COUNT(iD_Evento) as N_Evento FROM evento GROUP BY Tipo_evento", plot_type='bar', x_axis='Tipo_E', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    return render_template('index.html', plot_html = safe_html)

@app.route('/eventos')
def eventos():
    plt_html = graph.generate_plot("SELECT Tipo_evento as Tipo_E, COUNT(iD_Evento) as N_Evento FROM evento GROUP BY Tipo_evento", plot_type='bar', x_axis='Tipo_E', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    return render_template('index.html', plot_html = safe_html)

@app.route('/vehiculos')
def vehiculos():
    plt_html = graph.generate_plot("SELECT Tipo_vehiculo as Tipo_V, COUNT(ID_Evento) as N_Evento FROM vehiculo GROUP BY Tipo_vehiculo", plot_type='bar', x_axis='Tipo_V', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    return render_template('vehiculos/vehiculos.html', plot_html = safe_html)

@app.route('/lugares')
def lugares():
    plt_html = graph.generate_plot("Select * from calle", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "barTipo", xName = "Tipo", yName = "Evento", Titulo = "Tipo vs Evento", rotation = 90)
    safe_html = Markup(plt_html)
    plt_html1 = graph.generate_plot("Select * from colonias", plot_type='pairplot', x_axis='Tipo_V', y_axis='N_Evento', className = "barCol", xName = "Tipo", yName = "Evento", Titulo = "Colonias", rotation = 90)
    safe_html1 = Markup(plt_html1)
    return render_template('lugares/lugares.html', plot_html = safe_html, plot_html1 = safe_html1)

if __name__ == '__main__':
    app.run(debug=True)
