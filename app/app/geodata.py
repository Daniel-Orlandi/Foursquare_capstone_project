import numpy
import math
from app.core.http_engine import Request

class GeoLocData:
  def __init__(self, api_key:str) -> None:
    self.api_key = api_key
   
  async def get_geolocation_from_text(self, query:str, request_identification:str='test')->dict:
    data_getter=Request()
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={self.api_key}"
    await data_getter.async_request(key=request_identification, url=url)
    b_box = data_getter.get_data_dict()
    centroid = b_box[request_identification]['data']['results'][0]['geometry']['location']
    b_box = b_box[request_identification]['data']['results'][0]['geometry']['viewport']
    return b_box, centroid

  async def get_geolocation_data_from_coord(
                                            self,                                           
                                            lat:str,
                                            lon:str,
                                            type:str,
                                            radius=50000,
                                            pagetoken=None,
                                            request_identification:str='test')->dict:

    data_getter=Request()
    if pagetoken:
      url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?\
                  &location={lat}%2C{lon}&radius={radius}&type={type}&key={self.api_key}"
      
    else:
      url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?\
                  &location={lat}%2C{lon}&radius={radius}&type={type}&pagetoken={pagetoken}&key={self.api_key}"
                                                 
    await data_getter.async_request(key=request_identification, url=url)
    place_data = data_getter.get_data_dict()    
    return place_data

  @staticmethod
  def build_search_grid(upper_right:list, lower_left:list, resolution:int=10):  
    x_axis_step =(abs(lower_left[1]) - abs(upper_right[1]))/resolution
    y_axis_step =(abs(lower_left[0]) - abs(upper_right[0]))/resolution  
    x_axis = numpy.arange(lower_left[1], upper_right[1], x_axis_step)  
    y_axis = numpy.arange(lower_left[0], upper_right[0], y_axis_step)      
    x_axis, y_axis = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis

  
