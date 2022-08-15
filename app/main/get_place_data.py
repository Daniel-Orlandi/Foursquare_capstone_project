import os
import numpy
from dotenv import load_dotenv

from main.core.geodata import GeoLocData
from main.core.http_engine import Request

async def run(query:str, request_identification:str, resolution, timeout=1) -> dict:
    try:
        load_dotenv("conf/.env")
        api_key = os.getenv("GOOGLE_API_KEY")
        my_location = GeoLocData(api_key=api_key)        
        b_box, centroid = await my_location.get_geolocation_from_text(query=query,
                                                                      request_identification=request_identification,
                                                                      timeout=timeout)
        # data_dict =  my_location.get_all_pages(lat=centroid['lat'], lon=centroid['lng'], type='restaurant', request_identification='SJC')
        lon,lat = my_location.build_search_grid(upper_right=[b_box['northeast']['lat'], b_box['northeast']['lng']],
                                                lower_left=[b_box['southwest']['lat'], b_box['southwest']['lng']],
                                                resolution=resolution)

        positions = positions = numpy.vstack([lat.ravel(),lon.ravel()])
        positions_dict = {}
        indexer = 1
        for position in numpy.nditer(positions, flags=['external_loop'], order='F'):
            positions_dict[f'result_{indexer}'] = position
            indexer += 1
    
    except Exception as error:
        raise error

    else:
        return positions_dict
