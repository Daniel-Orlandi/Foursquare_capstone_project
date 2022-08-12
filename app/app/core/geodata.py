import time
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


  async def get_geolocation_data_from_coord(self,                                           
                                            lat:str=None,
                                            lon:str=None,
                                            type:str=None,
                                            radius=50000,
                                            pagetoken=None,
                                            request_identification:str='test')->dict:

    data_getter=Request()
    if pagetoken:            
      url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?\
                  &pagetoken={pagetoken}&key={self.api_key}"
      
    else:
      url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?\
                  &location={lat}%2C{lon}&radius={radius}&type={type}&key={self.api_key}"
                                                 
    await data_getter.async_request(key=request_identification, url=url)
    place_data = data_getter.get_data_dict()

    if place_data [request_identification]['data']['status'] == 'INVALID_REQUEST':     
      for attempt in range(2):
        time.sleep(1)
        print('retrying')
        await data_getter.async_request(key=request_identification, url=url)    
    return place_data


  async def get_all_pages_geolocation_data_from_coord(self,
                                                      lat:str=None,
                                                      lon:str=None,
                                                      type:str=None,
                                                      radius=50000,
                                                      pagetoken=None,
                                                      request_identification:str='test')->dict:
    
    if pagetoken:
      place_data[pagetoken]=await self.get_geolocation_data_from_coord(request_identification=request_identification,
                                                                       pagetoken=pagetoken)

    else:
      place_data = await self.get_geolocation_data_from_coord(lat=lat,
                                                              lon=lon,
                                                              type=type,
                                                              radius=radius,
                                                              request_identification=request_identification,
                                                              pagetoken=pagetoken)

    if 'next_page_token' in place_data[request_identification]['data']:                 
      pagetoken = place_data[request_identification]['data']['next_page_token']      
      place_data[pagetoken] = await self.get_all_pages(request_identification=request_identification,
                                            pagetoken=pagetoken)
    return place_data


  @staticmethod
  def build_search_grid(upper_right:list, lower_left:list, resolution:int=10):  
    x_axis_step =(abs(lower_left[1]) - abs(upper_right[1]))/resolution
    y_axis_step =(abs(lower_left[0]) - abs(upper_right[0]))/resolution  
    x_axis = numpy.arange(lower_left[1], upper_right[1], x_axis_step)  
    y_axis = numpy.arange(lower_left[0], upper_right[0], y_axis_step)      
    x_axis, y_axis = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis

  
