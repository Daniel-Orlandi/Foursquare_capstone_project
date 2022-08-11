import os
import sys
import pathlib
from logging.handlers import TimedRotatingFileHandler
import logging.config

class Logger:
    """ 
    Logger class 
    ...

    Attributes
    ----------
    logger_name:str
        logger choosen name.

    filename: str = None
        if not none, log file name, where the logs will be saved.
        else, filename will be log_file.log at project root.

    log_format: str = None
        if not none, change log formating.
        else, use standart log formating : 2020-12-23 14:23:05
    Methods
    -------
    get_logger(self):
        get logger.

    """

    def __init__(self, logger_name:str, filename:str = None, log_format: str = None, config_file_path:str = None):
        self.logger_name = logger_name        
        self.logger = None        
        
        if (isinstance(filename, str)):
            self.filename = filename

        else:
            self.filename = "data/logs/log_file.log"
            if(pathlib.Path(self.filename).exists() == False):
                path = os.path.dirname(self.filename)
                path = pathlib.Path(path)
                path.mkdir(parents=True, exist_ok=True) 
                open(f"{self.filename}","x")           

        if (isinstance(log_format, str)):
            self.log_format = logging.Formatter(log_format)

        if(isinstance(config_file_path, str)):       
            logging.config.fileConfig(config_file_path)

        self.logger = logging.getLogger(self.logger_name)

    def get_logger(self):    
        return self.logger
    

        
