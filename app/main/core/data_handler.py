import pandas
import sqlalchemy

class DataHandler:

  @staticmethod
  def dict_list_to_dataframe(data_dict_list:list, **kwargs)->list:
    df_list=[]
    for key, each_data_dict in data_dict_list.items():
      df_list.append(pandas.DataFrame.from_dict(each_data_dict, **kwargs))
    return pandas.DataFrame.from_dict(df_list)
  
  @staticmethod
  def concat_dataframe_list(df_list:list)->pandas.DataFrame:
    return pandas.concat(df_list)

  @staticmethod
  def db_connect(db_url:str):
    try:
      engine = sqlalchemy.create_engine(db_url)    
      metadata = sqlalchemy.MetaData(bind=engine)
      metadata.reflect(only=['test_table'])
      test_table=metadata.tables['test_table']    
      print(f"Connected:\n {test_table}")
      return engine

    except Exception as ex:
            print('Connection could not be made due to the following error: \n', ex)
