import random
import time
import datetime
import uuid
from faker.providers import BaseProvider


class IoTProvider(BaseProvider):

    def produce_msg(
        self,
        FakerInstance,
    ):
        temperature = FakerInstance.random.uniform(18.0, 30.0)
        humidity = FakerInstance.random.uniform(30.0, 70.0)
        timestamp = datetime.datetime.utcnow().isoformat()
        sensor_uuid = FakerInstance.uuid4()

        # Create the event data dictionary

        # message composition
        event = {
            "sensor_uuid": sensor_uuid,
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity
        }
        key = {"sensor_uuid": sensor_uuid}

        return event, key
