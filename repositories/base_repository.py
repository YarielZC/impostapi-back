from pymongo.asynchronous.database import AsyncDatabase

class BaseRepository:
  def __init__(self, db: AsyncDatabase, collection: str) -> None:
    self.db = db
    self.collection = collection

  def _map_doc(self, dic: dict) -> dict:
    try:
      dic['id'] = str(dic.pop('_id'))
    except KeyError:
      print(f'El documento {dic} no tenia campo _id')
      dic['id'] = ''

    return dic
  
  
