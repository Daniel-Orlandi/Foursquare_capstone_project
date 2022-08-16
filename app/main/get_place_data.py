from asyncio.log import logger
import os
import numpy
from dotenv import load_dotenv
from itertools import chain

from main.core.geodata import GeoLocData
from main.core.http_engine import Request
from main.utils.data_logger import Logger

async def run(query:str, req_id:str,type:str, resolution=5, timeout=1) -> list[Request]:
    try:
        logger = Logger(logger_name=__name__).get_logger()

        logger.info('Loading API Key.')
        load_dotenv("conf/.env")
        api_key = os.getenv("GOOGLE_API_KEY")

        my_location = GeoLocData(api_key=api_key)
        my_data_getter = Request()

        logger.info('Requesting location lat/lon and centroid.')
        request_dict = my_location.build_query_dict(query=query, req_id=req_id)   
        results = await my_location.get_geolocation_data(my_data_getter, request_dict, timeout=timeout)   
        positions = my_location.get_bounding_box(results.get_data_dict()[req_id])
        b_box = positions[0]
        centroid = positions[1]
        logger.info(f'boundin_box:{b_box}, centroid:{centroid}')

        logger.info(f'Setting search grid.')        
        lon,lat = my_location.build_search_grid(upper_right=[b_box['northeast']['lat'], b_box['northeast']['lng']],
                                                lower_left=[b_box['southwest']['lat'], b_box['southwest']['lng']],
                                                resolution=resolution)
        
        positions = positions = numpy.vstack([lat.ravel(),lon.ravel()])

        logger.info(f'Positions to be requested:\n {positions}')
        positions_dict = {}
        indexer = 1
        for position in numpy.nditer(positions, flags=['external_loop'], order='F'):
            temp_data_dict = {}
            temp_data_dict[f"req_{indexer}"] = my_location.build_query_dict(lat=position[0], lon=position[1], type=type, req_id=indexer)
            positions_dict= dict(chain(positions_dict.items(), temp_data_dict.items()))            
            indexer += 1
        logger.info(f'Final request dict:\n {positions_dict}')
        logger.info(f'Starting bulk request')
        results = await my_location.bulk_get_all_data_from_coord(data_getter=my_data_getter, request_dict=positions_dict, timeout=timeout)
        results = [result.get_data_dict() for result in results]
        logger.info(f'Success.')

    except Exception as general_error:
        logger.error(f"Error:\n{general_error}")
        raise general_error

    else:
        return results
