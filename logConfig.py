import logging
import json

def myLogger () -> logging.Logger : 
    logger = logging.getLogger("kinglog")

    ### Handlers

    f_handler = logging.FileHandler("kingdomRoyale.log")
    f_handler.setLevel(logging.DEBUG)

    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    f_handler.setFormatter(f_format)

    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def jsonLogger(serial):
    logger = myLogger()
    pyObject = json.loads(serial)

    for i in pyObject['listPlayers']:
        try:        
            del i['privateTextChannel']
            del i['member']
        except:
            pass
            
    for i in pyObject['listDeadPlayers']:
        try:        
            del i['privateTextChannel']
            del i['member']
        except:
            pass
    for i in pyObject['pastPlayers']:
        try:        
            del i['privateTextChannel']
            del i['member']
        except:
            pass
    logger.debug(json.dumps(pyObject, indent=4))
