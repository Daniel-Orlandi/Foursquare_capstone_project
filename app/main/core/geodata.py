import time
import numpy
import asyncio
from itertools import chain

from main.core.http_engine import Request
from main.utils.data_logger import Logger

class GeoLocData:
  def __init__(self, api_key:str) -> None:
    self.logger = Logger(logger_name=__name__).get_logger()
    self.api_key = api_key
    self.text_search_main_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    self.geocode_main_url = "https://maps.googleapis.com/maps/api/geocode/json?"
  

  async def get_geolocation_data(self, data_getter:Request , request_dict:dict, timeout:int=1)->Request:
    try:
      data_getter.set_data_dict(data_dict = request_dict)
      await data_getter.get(method='async', timeout=timeout)

      #Simple retry strategy for invalid requests.
      req_id = list(request_dict.keys())[0]      
      if data_getter.get_data_dict()[req_id]['status'] == 'INVALID_REQUEST':     
        self.logger.warning('GOT A INVALID_REQUEST!')
        data_getter.set_data_dict(request_dict)          
        for attempt in range(2): 
          time.sleep(2) #just in case so info can be generated at google servers.                 
          self.logger.warning(f'retrying:\n{data_getter.get_data_dict()}')
          await data_getter.get(method='async', timeout=timeout)
    
    except Exception as general_error:
      self.logger.error(f"Error:\n{general_error}")

    else:
     return data_getter
  

  async def get_all_pages_geolocation_data_from_coord(self, data_getter:Request, request_dict:dict, timeout:int=1)->Request:    
    data_getter = await self.get_geolocation_data(data_getter, request_dict, timeout)
    temp_data_dict = data_getter.get_data_dict()        
    req_id = list(temp_data_dict.keys())[0]
    
    if 'next_page_token' in temp_data_dict[req_id]:
      '''
      This recursive step is only triggered if next_page_toke is present in response.
      '''
      self.logger.info('Getting next page data.')
      # Necessary so next_page_token can be generated at google servers.
      time.sleep(2)      
      pagetoken = temp_data_dict[req_id]['next_page_token']
      # recursion_data_dict will be of format pagetoken: url+pagetoken
      recursion_data_dict = self.build_query_dict(pagetoken=pagetoken, req_id=pagetoken)
      # Recursive call      
      data_getter = await self.get_all_pages_geolocation_data_from_coord(data_getter, recursion_data_dict, timeout)
      recursion_data_dict = data_getter.get_data_dict()
      # Get request_dict from get_all_pages_geolocation_data_from_coord
      # Merge those dicts and stores them in data_getter object.
      temp_data_dict = dict(chain(temp_data_dict.items(), recursion_data_dict.items()))
      data_getter.set_data_dict(temp_data_dict)
    self.logger.info('Success.')
    return data_getter  


  async def bulk_get_all_data_from_coord(self, request_dict:dict, timeout=10) -> list:
    task_list = []
    for _, request_value in request_dict.items():
        temp_data_getter = Request()
        self.logger.info(f"getting_data from:{request_value}")        
        result = await self.get_all_pages_geolocation_data_from_coord(data_getter=temp_data_getter,request_dict=request_value, timeout=timeout)
        task_list.append(result)     
    self.logger.info('Sucess!')   
    return task_list


  def build_query_dict(self,
                      query:str=None, 
                      lat:str=None,
                      lon:str=None,
                      type:str=None,
                      radius:int=50000,
                      pagetoken:str=None,
                      req_id:str='test')->dict:

      if query:
        url = self.geocode_main_url+f"address={query}&key={self.api_key}"

      elif (lat and lon):
        url = self.text_search_main_url+f"&location={lat}%2C{lon}&radius={radius}&type={type}&key={self.api_key}"
      
      elif(pagetoken):
        url =self.text_search_main_url+f"&pagetoken={pagetoken}&key={self.api_key}"
      
      else:
        raise Error("You should provide either [lat, lon], query or pagetoken ")
      
      return {req_id:url}


  @staticmethod
  def get_bounding_box(data_dict:dict)->list:
    centroid = data_dict['results'][0]['geometry']['location']
    b_box = data_dict['results'][0]['geometry']['viewport']
    return [b_box, centroid]


  @staticmethod
  def build_search_grid(upper_right:list, lower_left:list, resolution:int=10):  
    x_axis_step =(abs(lower_left[1]) - abs(upper_right[1]))/resolution
    y_axis_step =(abs(lower_left[0]) - abs(upper_right[0]))/resolution  
    x_axis = numpy.arange(lower_left[1], upper_right[1], x_axis_step)  
    y_axis = numpy.arange(lower_left[0], upper_right[0], y_axis_step)      
    x_axis, y_axis = numpy.meshgrid(x_axis, y_axis, sparse=True)
    return x_axis, y_axis 
