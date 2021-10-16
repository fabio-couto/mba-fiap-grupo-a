#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import time
import random
from json import dumps
from collections import OrderedDict
from kafka import KafkaProducer


# In[ ]:


def create_jmsg(timestamp, medida, machineID, value):
    msg = OrderedDict()         # ordered dictionary
    if(timestamp != ""):
        msg["timestamp"] = timestamp
    if(medida != ""):
        msg["medida"] = medida
    if(machineID != ""):
        msg["machineID"] = machineID
    if(value != ""):
        msg["value"] = value    
    return dumps(msg)


# In[ ]:


def generate_producer_kafka(domain_kafka):
    producer = KafkaProducer(bootstrap_servers=[domain_kafka], value_serializer=lambda v: str(v).encode('utf-8'))
    return producer


# In[ ]:


def main():

    dict_medidas = {'volt':[97, 255],
                    'rotate':[138, 695],
                    'pressure':[51, 185],
                    'vibration':[14, 76]
                   }
    
    #Gerar producer do kafka
    producer = generate_producer_kafka('localhost:9092')
    producer_name_topic = 'iot-telemetry'

    while (True):

        now = datetime.datetime.now()
        unixtime = time.mktime(now.timetuple())

        for medida, medida_valores in dict_medidas.items():
            for maquina in range(1, 101):  

                # Gerar valor randomico para cada variável
                medida_valor = random.sample(range(medida_valores[0], medida_valores[1]), k=1)[0]            
                msg = create_jmsg(unixtime, medida, maquina, medida_valor)

                # print test
                print(msg)

                #kafka producer
                producer.send(producer_name_topic, msg)

        time.sleep(5)


# In[ ]:


if __name__ == "__main__":
    main()

