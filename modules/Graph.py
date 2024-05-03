import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Configurar el backend a 'Agg'
from io import BytesIO
import base64
import pandas as pd

#Tipos de gráfico 
#   bar: necesita "x" y "y"
#   scatter_plot: necesita "x" y "y"
#   join_plot: necesita "x" y "y"
#   line_plot: necesita "x" y "y"
#   heatmap: necesita solo un df con columnas numericas
#   pairplot: solo necesita un df

class GraphGenerator:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def generate_plot(self, query, args=None, plot_type='bar', x_axis='x', y_axis='y', className="", xName = "x_label", yName = "y_label", Titulo = "Titulo", rotation = 0, hue=None):
        data = self.db_handler.query_db(query, args) #Se obtiene el resultado de la query que paso de app.py
        if data:
            df = pd.DataFrame(data) # Se transforma el resultado de un quety a un elemento de pandas
            plt.figure(figsize=(10, 6))
            if plot_type == 'bar':
                sns.barplot(data=df, x=x_axis, y=y_axis, hue=hue)
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)  
            if plot_type == "scatter_plot": 
                sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue)
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation) 
            if plot_type == "join_plot": 
                sns.jointplot(data=df, x=x_axis, y=y_axis, hue=hue)
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)  
            if plot_type == "line_plot": 
                df[x_axis] = df[x_axis].astype(str)
                sns.lineplot(x=df[x_axis], y=df[y_axis])
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)  
            if plot_type == "heatmap": 
                sns.heatmap(df)
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)

            if plot_type == "pairplot": 
                sns.pairplot(df)
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)

            if plot_type == "pie":
                plt.pie(df[y_axis], labels=df[x_axis])
                plt.title(Titulo)  
                plt.xlabel(xName)  
                plt.ylabel(yName)  
                plt.xticks(rotation=rotation)

            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            return f'<img src="data:image/png;base64,{image_base64}" class = "{className}"/>'
        else: 
            print("No hay datos")
            
        return "<div>No data available.</div>"

#