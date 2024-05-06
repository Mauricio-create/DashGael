import folium
from folium.plugins import HeatMap

class MapGenerator: 
    def __init__(self, data, geoJson_path, class_css = ""): 
        self.data = data 
        self.json = geoJson_path
        self.css_class = class_css

    def gereate_map(self): 
        map_center = [19.43926, -99.1332]
        map = folium.Map(location = map_center, zoom_start=10)
        folium.GeoJson(open(self.json).read(), name="geojson").add_to(map)

        heat_data = [[row['coordenada_x'], row['coordenada_y']] for index, row in self.data.iterrows()]
        HeatMap(heat_data).add_to(map)
        html_str = map._repr_html_()
        return html_str
    

