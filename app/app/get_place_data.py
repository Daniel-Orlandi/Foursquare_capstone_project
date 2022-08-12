from core.geodata import GeoLocData

with open('data/api_key.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

my_location = GeoLocData(api_key=json_data['google_api_key'])
b_box, centroid = my_location.get_geolocation_from_text(query='São Paulo', request_identification='SP')
data_dict =  my_location.get_all_pages(lat=centroid['lat'], lon=centroid['lng'], type='restaurant', request_identification='SJC')
