# Operations Guide

## Table of Contents

- [Debug release pipeline](#debug-release-pipeline)
- [Retrigger release pipeline](#retrigger-release-pipeline)
- [Check frontend logs](#check-frontend-logs)
- [Check backend logs](#check-backend-logs)
- [Check Postgres logs](#check-postgres-logs)
- [Check Opensearch logs](#check-opensearch-logs)
- [Check metrics](#check-metrics)
- [Debug indexing and clear dead-letter queue for indexing](#debug-indexing-and-clear-dead-letter-queue-for-indexing)
- [Log into running container](#log-into-running-container)
- [Trigger index creation](#trigger-index-creation)
- [Trigger batch upgrade](#trigger-batch-upgrade)
- [Trigger reindexing](#trigger-reindexing)
- [Flip a feature flag](#flip-a-feature-flag)
- [Add new feature flag](#add-new-feature-flag)
- [Connect to Postgres with psql](#connect-to-postgres-with-psql)
- [Connect to Opensearch](#connect-to-opensearch)
- [Restore database snapshot to lower environments](#restore-database-snapshot-to-lower-environments)
- [Swap Opensearch](#swap-opensearch)
- [Swap Postgres](#swap-postgres)

---

## Debug release pipeline

1. Find failed pipeline in CodePipeline console.
2. Identify failed step.
3. Check logs for build steps, or details in CloudFormation `Events` tab for deployment steps:

<p align="center">
  <img src="./images/howto/debug-release-pipeline_1.png" alt="Debug release pipeline 1" width="500">
</p>

---

## Retrigger release pipeline

1. Find pipeline in CodePipeline console:

<p align="center">
  <img src="./images/howto/retrigger-release-pipeline_1.png" alt="Retrigger release pipeline 1" width="500">
</p>

2. Click on `Release Change` button:

<p align="center">
  <img src="./images/howto/retrigger-release-pipeline_2.png" alt="Retrigger release pipeline 2" width="500">
</p>

---

## Check frontend logs

1. Find cluster in ECS console:

<p align="center">
  <img src="./images/howto/check-frontend-logs_1.png" alt="Check frontend logs 1" width="500">
</p>

2. Click on `Frontend` service:

<p align="center">
  <img src="./images/howto/check-frontend-logs_2.png" alt="Check frontend logs 2" width="500">
</p>

3. Click on `Logs` tab and `View in CloudWatch` button (select `ApplicationContainerLogGroup`):

<p align="center">
  <img src="./images/howto/check-frontend-logs_3.png" alt="Check frontend logs 3" width="500">
</p>

4. Add custom time range to narrow down logs:

<p align="center">
  <img src="./images/howto/check-frontend-logs_4.png" alt="Check frontend logs 4" width="500">
</p>

---

## Check backend logs

1. Follow [Check frontend logs](#check-frontend-logs) for backend cluster and `Backend` service.

---

## Check Postgres logs

1. Find database in RDS console:

<p align="center">
  <img src="./images/howto/check-postgres-logs_1.png" alt="Check postgres logs 1" width="500">
</p>

2. Click on `Monitor` tab to view metrics like CPU utilization:

<p align="center">
  <img src="./images/howto/check-postgres-logs_2.png" alt="Check postgres logs 2" width="500">
</p>

3. Click on `Logs` tab to and select log to `View`:

<p align="center">
  <img src="./images/howto/check-postgres-logs_3.png" alt="Check postgres logs 3" width="500">
</p>

4. Examine logs:

<p align="center">
  <img src="./images/howto/check-postgres-logs_4.png" alt="Check postgres logs 4" width="500">
</p>

---

## Check Opensearch logs

1. Find Opensearch cluster in Opensearch console (see #2 for checking tags if name is obscure):

<p align="center">
  <img src="./images/howto/check-opensearch-logs_1.png" alt="Check opensearch logs 1" width="500">
</p>

2. Click on `Tags` tab to ensure cluster corresponds to correct environment:

<p align="center">
  <img src="./images/howto/check-opensearch-logs_2.png" alt="Check opensearch logs 2" width="500">
</p>

3. Click on `Cluster health` and `Instance health` tabs to check metrics:

<p align="center">
  <img src="./images/howto/check-opensearch-logs_3.png" alt="Check opensearch logs 3" width="500">
</p>

4. Click on `Logs` tab to view logs:

<p align="center">
  <img src="./images/howto/check-opensearch-logs_4.png" alt="Check opensearch logs 4" width="500">
</p>
---

## Check metrics

- See monitoring section of [Check Postgres logs](#check-postgres-logs) for Postgres metrics
- See monitoring section of [Check Opensearch logs](#check-opensearch-logs) for Opensearch metrics

For ECS Fargate:

1. Find cluster in ECS console.
2. Click on service name.
3. Look at `Health and metrics` tab for CPU and memory utilization.

---

## Debug indexing and clear dead-letter queue for indexing

1. Find dead letter queue with messages in SQS console:

<p align="center">
  <img src="./images/howto/dead-letter-queue_1.png" alt="Debug dead letter queue 1" width="500">
</p>

2. Click on `Send and receive messages` button:

<p align="center">
  <img src="./images/howto/dead-letter-queue_2.png" alt="Debug dead letter queue 2" width="500">
</p>

3. Click on `Poll for messages` button:

<p align="center">
  <img src="./images/howto/dead-letter-queue_3.png" alt="Debug dead letter queue 3" width="500">
</p>

4. Open up the message to get the UUID of the object that failed to index:

<p align="center">
  <img src="./images/howto/dead-letter-queue_4.png" alt="Debug dead letter queue 4" width="500">
</p>

5. After cause has been investigated and fixed, click on `Start DLQ redrive` and `DLQ redrive` to send the messages back to primary queue for indexing.

<p align="center">
  <img src="./images/howto/dead-letter-queue_5.png" alt="Debug dead letter queue 5" width="500">
</p>

6. Monitor DLQ to make sure objects index correctly and messages don't reappear.

---

## Log into running container

1. Find cluster in ECS console:

<p align="center">
  <img src="./images/howto/connect-to-running-container_1.png" alt="Connect to running container 1" width="500">
</p>

2. Click on desired service:

<p align="center">
  <img src="./images/howto/connect-to-running-container_2.png" alt="Connect to running container 2" width="500">
</p>

3. Find task ID:

<p align="center">
  <img src="./images/howto/connect-to-running-container_3.png" alt="Connect to running container 3" width="500">
</p>

4. Find container name (if task has multiple containers):

<p align="center">
  <img src="./images/howto/connect-to-running-container_4.png" alt="Connect to running container 4" width="500">
</p>

5. Run command in terminal, filling in cluster, task, container name, and profile:

```bash
aws ecs execute-command \
    --command "/bin/bash" \
    --interactive \
    --cluster igvfd-dev-DeployDevelopment-BackendStack-EcsDefaultClusterMnL3mNNYNDemoVpc278C9613-7BVzDrMc52Ln \
    --task 26f42c00797144ec89393019c15c3d2b \
    --container pyramid \
    --profile igvf-dev
```

---

## Trigger index creation

Steps to trigger index creation.

---

## Trigger batch upgrade

Steps to trigger a batch upgrade.

---

## Trigger reindexing

Steps to trigger reindexing.

---

## Flip a feature flag

1. Find application in AppConfig console:

<p align="center">
  <img src="./images/howto/flip-feature-flag_1.png" alt="Flip feature flag 1" width="500">
</p>

2. Click on configuration profile:

<p align="center">
  <img src="./images/howto/flip-feature-flag_2.png" alt="Flip feature flag 2" width="500">
</p>

3. Toggle desired flag.

<p align="center">
  <img src="./images/howto/flip-feature-flag_3.png" alt="Flip feature flag 3" width="500">
</p>

4. Click `Save new version` button and `Start deployment` button.

5. Select deployment method and deploy.

6. Check `{backend_url}/feature-flags` endpoint on backend application.

---

## Add new feature flag

1. Add a new feature flag key and value (True/False) to https://github.com/IGVF-DACC/igvfd/blob/dev/cdk/infrastructure/config.py for a specific environment:

<p align="center">
  <img src="./images/howto/add-new-feature-flag_1.png" alt="Add new feature flag 1" width="500">
</p>

2. Make sure all flags in the config are set to desired state for next flag deployment (adding or changing any flag in the config will cause a new deployment of the flags, overwritting any flags toggled in the console).

3. Commit code and push.

---

## Connect to Postgres with psql

1. Log into running backend application container using [Log into running container](#log-into-running-container).

2. Install `psql` with `# apt-get update && apt-get install postgresql-client`.

3. Create database url with `# export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}`.

4. Connect to database with `# psql $SQLALCHEMY_URL`.

---

## Connect to Opensearch

1. Log into running backend application container using [Log into running container](#log-into-running-container).

2. Query with cURL or Python client: `# curl -XGET ${OPENSEARCH_URL}/_cat/indices`.

---

## Restore database snapshot to lower environments

Steps to restore a database snapshot to lower environments.

---

## Swap Opensearch

Instructions for swapping Opensearch.

---

## Swap Postgres

Instructions for swapping Postgres.

---
