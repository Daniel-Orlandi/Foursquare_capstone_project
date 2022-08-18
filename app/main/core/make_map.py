import folium
import pandas
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon

class FoliumMap:
    def __init__(self, initial_location_coord:list = None,
                       zoom_start:int=10,
                       **kwargs) -> folium.Map:

        self.zoom_start = zoom_start        
        self.Map = folium.Map(location=initial_location_coord, zoom_start = zoom_start, **kwargs)
    
    def check_map(self, initial_location_coord, **kwargs):
        if(self.Map.get_bounds()[0] == [None,None]):
            self.Map = folium.Map(location=initial_location_coord, **kwargs)

    def show_map(self):
        return self.Map
    
    def add_mouse_position(self):
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        )

        mouse_position.add_to(self.Map)
        
    
    def add_circle(self,location_name:str, location_coord:list, color:str ='#d35400') -> None:        
        circle = folium.Circle(location_coord, radius=1000, color=color, fill=True).add_child(folium.Popup(f'{location_name}.'))
        circle.add_to(self.Map)


    def add_marker(self,location_name:str, location_coord:list, color:str = '#d35400') -> folium.Marker:
        marker = folium.Marker( location_coord,
                                        # Create an icon as a text label
                                        icon=DivIcon(
                                            icon_size=(20,20),
                                            icon_anchor=(0,0),
                                            html=f'<div style="font-size: 12; color:{color};"><b>{location_name}</b></div>',
                                            )
                                        )
        marker.add_to(self.Map)

    def add_distance_marker(self):
        distance_marker = folium.Marker(
           coordinate,
           icon=DivIcon(
               icon_size=(20,20),
               icon_anchor=(0,0),
               html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
               )
           )

    def add_poly_line(self):
        folium.PolyLine(locations=coordinates, weight=1).add_to(self.Map)

    def add_marker_cluster(self, location_dataframe:pandas.DataFrame, color:str = 'white')->None:                
        marker_cluster = MarkerCluster().add_to(self.Map)     
        for _, row in location_dataframe.iterrows():             
            location_coord = row[[1, 2]].to_list()                        
            folium.Marker(location_coord, popup=row[0] ,icon=folium.Icon(color=color, icon_color=row[3])).add_to(marker_cluster)
           

        

    def bulk_add_location_to_map(self, location_dataframe:pandas.DataFrame, circle_color='#d35400', marker_color='#d35400', **kwargs) -> None:
        try:
            if(not location_dataframe.empty):
                initial_location_coord = location_dataframe.iloc[0][[1,2]].to_list()
                self.check_map(initial_location_coord, **kwargs)

                for _, row in location_dataframe.iterrows():
                    location_coord = row[[1, 2]].to_list()
                    location_name =  row[0]                         
                    self.add_circle(location_name,location_coord,color=circle_color)
                    self.add_marker(location_name,location_coord,color=marker_color)                
            
            else:
                raise Exception('location_dict is empty!')

        except Exception as exeption:
            raise(exeption)
