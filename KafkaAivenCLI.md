# Starting your Apache Kafka Service with Aiven.io

Aiven provides a command-line interface (CLI) tool that allows you to manage and deploy cloud services, including Apache Kafka, from the command line. This guide will walk you through the steps to create a Kafka service using the Aiven CLI.

## Prerequisites

- Aiven CLI installed (Refer to the [Aiven documentation](https://docs.aiven.io/docs/tools/cli) for installation instructions)
- A valid Aiven account

## Steps to Create a Kafka Service
If you don't have a Apache Kafka Cluster available, you can easily start one in [Aiven.io console](https://console.aiven.io/signup?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post).

Once created your account you can start your Apache Kafka service with [Aiven.io's cli](https://github.com/aiven/aiven-client)

1. Copy the file conf/env.conf.sample` to `conf/env.conf`

2. Edit the `conf/env.conf file filling the following placeholders:
```bash
PROJECT_NAME="myproject-0709"
KAFKA_SERVICE_NAME="kafka-19c70d7e"
TOPIC="sensor_metrics"
PARTITIONS=2
REPLICATION=2
NR_MESSAGES=200
MAX_TIME=0
USERNAME="farhanekarim@gmail.com"
TOKEN="g0aOsWS3xSd1TmSabwKTd1NWrQXB8B496iT+jHWnQh27tQ96XPald9xhQy49pvGdNz7p+7stOtDUoCcvXL5Uwl4NAg8CdGo0zgDqTgfk3HLXQ24P4v0tHmosFdoMbSEcAJfXBc4Qc31iaEklv4eV2N0Il2/TGHgpJwjrHbNwKYAyRHTH7HltdVGQ5o/bpUzlfB19xtZLTQIMi6pW4vML3pBzufZFQI/3qlg364Rg7yjCuzFp+ZbGgY10j/vg5uhBKp2a0v4nKJLbzEz9+o7mmO/vl/CXb/RhMiwQhd3rTr8kyisHIepYj768IyaPp2ShdNxh/kw+FgB6Et+ON3xsgIScetXd1+8zrC6rNc+zY0b3UycoWw=="
PRIVATELINK="NO"
SECURITY="SSL"
CLOUD_REGION="azure-france-central"
AIVEN_PLAN_NAME="business-4"
DESTINATION_FOLDER_NAME="/Users/karimfarhane/PycharmProjects/AivenAssignement/kafkaCerts/SensorIoT/"
```

Parameters:
* `PROJECT_NAME`: the name of the project created during sing-up
* `KAFKA_SERVICE_NAME`: the name you want to give to the Apache Kafka instance
* `CLOUD_REGION`: the name of the Cloud region where the instance will be created. The list of cloud regions can be found
 with
```bash
avn cloud list
```
* `AIVEN_PLAN_NAME`: name of Aiven's plan to use, which will drive the resources available, the list of plans can be found with
```bash
avn service plans --project <PROJECT_NAME> -t kafka --cloud <CLOUD_PROVIDER>
```
* `DESTINATION_FOLDER_NAME`: local folder where Apache Kafka certificates will be stored (used to login)

* `USERNAME`: the email address used as username to log in to Aiven services
* `TOKEN`: the access token can be generated the aiven console or with aiven client as follow:
```bash
avn user access-token create                            \
--description "Token used by Fake data generator"       \
--max-age-seconds 3600                                  \
--json | jq -r '.[].full_token'
```


3. You can create the Apache Kafka service with

```bash
avn service create  \
  -t kafka $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME \
  --cloud  $CLOUD_REGION \
  -p $AIVEN_PLAN_NAME \
  -c kafka_rest=true \
  -c kafka.auto_create_topics_enable=true \
  -c schema_registry=false
```

---

4. You can download the required SSL certificates in the `<DESTINATION_FOLDER_NAME>` with

```bash
avn service user-creds-download $KAFKA_SERVICE_NAME \
   --project $PROJECT_NAME    \
   -d $DESTINATION_FOLDER_NAME \
   --username avnadmin
```

5. And retrieve the Apache Kafka Service URI with

```bash
avn service get $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME \
  --format '{service_uri}'
```

The Apache Kafka Service URI is in the form `hostname:port` and provides the `hostname` and `port` needed to execute the code.
You can wait for the newly created Apache Kafka instance to be ready with

```bash
avn service wait $KAFKA_SERVICE_NAME --project $PROJECT_NAME
````

## Conclusion

By following these steps, you can create a Kafka service using the Aiven CLI. The CLI provides a convenient way to automate the deployment and management of your Kafka clusters, making it easier to integrate Aiven services into your scripts and workflows.

Once your Kafka service is up and running, you can start leveraging its capabilities for building scalable and real-time data streaming applications.

Happy Kafka-ing with Aiven CLI!

---