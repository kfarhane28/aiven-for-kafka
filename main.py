from faker import Faker
import json
from kafka import KafkaProducer
import time
import sys
import random
import argparse
from iotproducer import IoTProvider


# Creating a Faker instance and seeding to have the
# same results every time we execute the script
fake = Faker()
Faker.seed(1234)


# function produce_msgs starts producing messages with Faker
def produce_msgs(
    security_protocol="SSL",
    sasl_mechanism="SCRAM-SHA-256",
    cert_folderName="~/kafkaCerts/SensorIoT/",
    username="",
    password="",
    hostname="kafka-19c70d7e-myproject-0709.aivencloud.com",
    port="26430",
    topic_name="sensor_metrics",
    nbr_messages=-1,
    max_waiting_time_in_sec=5,
):
    if security_protocol.upper() == "PLAINTEXT":
        producer = KafkaProducer(
            bootstrap_servers=hostname + ":" + port,
            security_protocol="PLAINTEXT",
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
            key_serializer=lambda v: json.dumps(v).encode("ascii"),
        )
    elif security_protocol.upper() == "SSL":
        producer = KafkaProducer(
            bootstrap_servers=hostname + ":" + port,
            security_protocol="SSL",
            ssl_cafile=cert_folderName + "/ca.pem",
            ssl_certfile=cert_folderName + "/service.cert",
            ssl_keyfile=cert_folderName + "/service.key",
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
            key_serializer=lambda v: json.dumps(v).encode("ascii"),
        )
    elif security_protocol.upper() == "SASL_SSL":
        producer = KafkaProducer(
            bootstrap_servers=hostname + ":" + port,
            security_protocol="SASL_SSL",
            sasl_mechanism=sasl_mechanism,
            ssl_cafile=cert_folderName + "/ca.pem" if cert_folderName else None,
            sasl_plain_username=username,
            sasl_plain_password=password,
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
            key_serializer=lambda v: json.dumps(v).encode("ascii"),
        )
    else:
        sys.exit("This security protocol is not supported!")

    if nbr_messages <= 0:
        nbr_messages = float("inf")
    i = 0


    fake.add_provider(IoTProvider)

    while i < nbr_messages:
        message, key = fake.produce_msg(
                fake,
        )

        print("Sending: {}".format(message))
        # sending the message to Kafka
        producer.send(topic_name, key=key, value=message)
        # Sleeping time
        sleep_time = (
            random.randint(0, int(max_waiting_time_in_sec * 10000)) / 10000
        )
        print("Sleeping for..." + str(sleep_time) + "s")
        time.sleep(sleep_time)

        # Force flushing of all messages
        if (i % 100) == 0:
            producer.flush()
        i = i + 1
    producer.flush()


# calling the main produce_msgs function: parameters are:
#   * nbr_messages: number of messages to produce
#   * max_waiting_time_in_sec: maximum waiting time in sec between messages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--security-protocol",
        help="""Security protocol for Kafka
                (PLAINTEXT, SSL, SASL_SSL)""",
        required=True,
    )
    parser.add_argument(
        "--sasl-mechanism",
        help="""SASL mechanism for Kafka
                (PLAIN, GSSAPI, OAUTHBEARER, SCRAM-SHA-256, SCRAM-SHA-512)""",
        required=False,
    )
    parser.add_argument(
        "--cert-folder",
        help="""Path to folder containing required Kafka certificates.
                Required --security-protocol equal SSL or SASL_SSL""",
        required=False,
    )
    parser.add_argument(
        "--username",
        help="Username. Required if security-protocol is SASL_SSL",
        required=False,
    )
    parser.add_argument(
        "--password",
        help="Password. Required if security-protocol is SASL_SSL",
        required=False,
    )
    parser.add_argument(
        "--host",
        help="Kafka Host (obtained from Aiven console)",
        required=True,
    )
    parser.add_argument(
        "--port",
        help="Kafka Port (obtained from Aiven console)",
        required=True,
    )
    parser.add_argument("--topic-name", help="Topic Name", required=True)
    parser.add_argument(
        "--nbr-messages",
        help="Number of messages to produce (0 for unlimited)",
        required=True,
    )
    parser.add_argument(
        "--max-waiting-time",
        help="Max waiting time between messages (0 for none)",
        required=True,
    )

    args = parser.parse_args()
    p_security_protocol = args.security_protocol
    p_cert_folder = args.cert_folder
    p_username = args.username
    p_password = args.password
    p_sasl_mechanism = args.sasl_mechanism
    p_hostname = args.host
    p_port = args.port
    p_topic_name = args.topic_name
    produce_msgs(security_protocol=p_security_protocol, sasl_mechanism=p_sasl_mechanism, cert_folderName=p_cert_folder,
                 username=p_username, password=p_password, hostname=p_hostname, port=p_port, topic_name=p_topic_name,
                 nbr_messages=int(args.nbr_messages), max_waiting_time_in_sec=float(args.max_waiting_time))
    print(args.nbr_messages)


if __name__ == "__main__":
    main()