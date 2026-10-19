**GCP Deployment Guide — Timecard Anomaly Detector**

This guide outlines steps to deploy the Timecard Anomaly Detector to Google Cloud using Cloud Run, Cloud Storage, BigQuery, and Looker Studio.

Prerequisites
- A Google Cloud project with billing enabled
- gcloud CLI installed and authenticated (`gcloud auth login`)
- Docker installed locally (or use Cloud Build)
- Project IAM permissions to create Cloud Run services, Cloud Storage buckets, and BigQuery datasets

1. Build and push container image (Cloud Build)

- Option A — Cloud Build (recommended):

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/timecard-anomaly-detector:latest
```

- Option B — Docker (local):

```bash
docker build -t gcr.io/PROJECT_ID/timecard-anomaly-detector:latest .
docker push gcr.io/PROJECT_ID/timecard-anomaly-detector:latest
```

2. Deploy to Cloud Run

```bash
gcloud run deploy timecard-anomaly-detector \
  --image gcr.io/PROJECT_ID/timecard-anomaly-detector:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

3. Create Cloud Storage bucket for CSV uploads

```bash
gsutil mb -l us-central1 gs://PROJECT_ID-timecards
```

4. Configure Cloud Run to process uploaded files

- Option A: Use a Cloud Function or Cloud Run service triggered by Eventarc on `google.cloud.storage.object.v1.finalized` to POST the file URL to the Cloud Run service.
- Option B: Use a small Cloud Run HTTP endpoint and configure a Cloud Storage notification via Pub/Sub + Eventarc.

5. Persist results to BigQuery

- Create dataset and table
```bash
bq --location=US mk -d PROJECT_ID:timecard_anomalies
bq mk --table PROJECT_ID:timecard_anomalies.anomalies schema.json
```
- In your Cloud Run service, after processing, insert rows into BigQuery via the Python client library (`google-cloud-bigquery`).

6. Visualize in Looker Studio

- Create a new report in Looker Studio and connect it to your BigQuery `timecard_anomalies.anomalies` table.

Security & Costs
- Use least-privilege service accounts for Cloud Run and Eventarc.
- Monitor costs: Cloud Run, BigQuery storage/queries, and Cloud Build incur charges.

Notes
- For demo purposes you can run the container locally and POST a CSV to the `/` or `/process` endpoint (implement as needed).
- Consider automating build/deploy via Cloud Build triggers or GitHub Actions workflows.
