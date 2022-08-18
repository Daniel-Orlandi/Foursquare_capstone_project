import pandas
from main.utils.data_logger import Logger
from main.core.data_handler import DataHandler
from main.core.classifier import Recommender
from main.core.make_map import FoliumMap

def make_recommendation(restaurant:pandas.DataFrame, classification_db:str="RESTAURANT_SP_CAP_5_50", best_k:int=4)->None:  
  try:
    # Initializing
    data_handler = DataHandler()
    map_handler = FoliumMap()
    data_handler = DataHandler()
    my_classifier = Recommender()
    my_logger = Logger(logger_name=__name__).get_logger()
    #Connecting to db
    my_logger.info(f'Connecting to {classification_db}')
    engine = data_handler.db_connect(db_url = "mysql+pymysql://root:secret@db:3306/my_db")
    my_logger.info(f'Connected')
    # Getting data from DB
    my_logger.info(f'loading db data.')
    data_frame = data_handler.get_data_from_db(query=f"SELECT * FROM {classification_db}", con=engine)
    my_logger.info(f'Loaded.')
    # Setting Training DF
    my_logger.info(f'Setting training df.')
    data_frame.dropna(inplace=True)
    data_frame.drop_duplicates(['place_id'], keep='last', inplace=True)
    data_frame.reset_index(drop=True, inplace=True)    
    train_data_frame=data_frame[['price_level', 'rating', 'user_ratings_total', 'lat', 'lon']]
    my_logger.info(f'Df Set.')
    #Training step
    my_logger.info(f'Training.')
    my_classifier.preprocess(train_data_frame, standarize=True)
    my_classifier.train(n_clusters=best_k, init = "k-means++", n_init=12)    
    
    result = []
    for idx, row in train_data_frame.iterrows():
      result.append([idx,my_classifier.predict_over_a_dataset(row)[0]])

    data_frame['id'] = data_frame.index
    result_series = pandas.DataFrame(result)
    result_series.rename(columns={0:'id',1:'cluster'}, inplace=True)
    final_df = pandas.merge(data_frame, result_series)
    my_logger.info(f'Done.')

    #Recommendationg step
    my_logger.info(f'Recomending')
    cluster = my_classifier.predict_over_a_dataset(restaurant)
    best_5_rest = final_df[(final_df['cluster']==cluster[0])].sort_values('rating').iloc[:4]
    locations_df = best_5_rest[['name', 'lat', 'lon']]
    marker_locations_df = locations_df.copy()
    marker_locations_df['marker_color'] = locations_df['name'].apply(lambda x: 'green')
    
    map_handler.bulk_add_location_to_map(location_dataframe=locations_df, zoom_start=5, circle_color='#000000', marker_color='#d35400')
    map_handler.add_marker_cluster(marker_locations_df)
    
    my_logger.info('Success.')    
  
  except Exception as general_error:
    my_logger.error(f'Error:\n {general_error}')
    raise general_error
  
  else:
    return map_handler.show_map()


