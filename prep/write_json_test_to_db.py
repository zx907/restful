from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prep.jsparse import get_json_obj_list
from sqlalchemy_model import Itemids, Properties, Coordinate
from datetime import datetime

engine = create_engine('postgresql://user:123456@localhost/test')
Session = sessionmaker(bind=engine)

json_obj_list = get_json_obj_list()

for json_obj in json_obj_list:

    try:
        session = Session()

        _timestamp = datetime(int(json_obj['properties']['year']),
                              int(json_obj['properties']['month']),
                              int(json_obj['properties']['day']),
                              int(json_obj['properties']['hour']),
                              int(json_obj['properties']['minute']),
                              int(json_obj['properties']['second']))

        properties = Properties(_text=json_obj['properties']['text'],
                                userID=json_obj['properties']['userID'],
                                userName=json_obj['properties']['userName'],
                                _timestamp=_timestamp,
                                source=json_obj['properties']['source'],
                                sentiment=json_obj['properties']['sentiment'],
                                sentiStrings=json_obj['properties']['sentiStrings'],
                                labelledSentiment=json_obj['properties']['labelledSentiment'],
                                crowder=json_obj['properties']['crowder'])


        coordinate = Coordinate(latitude=float(json_obj['coordinate']['coordinates'][0]),
                                longtitude=float(json_obj['coordinate']['coordinates'][1]))

        item = Itemids(_id=json_obj['_id'], properties=properties, coordinates=coordinate)

        session.add(item)
        session.add(properties)
        session.add(coordinate)
        session.commit()
        print("succeed")
    except Exception as e:
        session.rollback()
        print(e)
        print('failed')
    finally:
        session.close()
        print('Done')

