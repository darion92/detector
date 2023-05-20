import json
import uuid
from pykafka import KafkaClient
from person import Person
from threading import Thread, current_thread


class KafkaProducer:
    client = None
    topic = None
    producer = None
    def __init__(self):
        self.client = KafkaClient(hosts="172.17.0.1:9092", use_greenlets=True)
        self.topic = self.client.topics["person-track"]
        self.producer = self.topic.get_sync_producer() 

    
    def send(self, person):
        print("sending person "+str(person.number))
        data={
           'person_id': str(uuid.uuid1()),
           'person_timestamp':person.timestamp,
           'person_number' :person.number 
           }
        m=json.dumps(data).encode('utf-8')
        try:
            ts = str(person.timestamp).encode('utf-8')
            print(ts)
            self.producer.produce(m)
            print("produced !")
        except Exception as e:
            print(e)
            pass # for at least once delivery you will need to catch network errors and retry.
