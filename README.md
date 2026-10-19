# Timecard Anomaly Detector

A Python tool that scans employee timecard data for common problems and writes them to a report for review.

## Business Problem

Organizations rely on accurate timecards for payroll, compliance, and workforce planning. Missing punches, late arrivals, unauthorized overtime, and early departures cause payroll errors and compliance risk, and finding them by hand is slow. This project automates that first pass so reviewers only look at the records that need attention.

## What It Detects

| Anomaly | Rule |
|---|---|
| Missing Clock In | `actual_clock_in` is empty |
| Missing Clock Out | `actual_clock_out` is empty |
| Late Arrival | Clock-in more than 15 minutes after `scheduled_start` |
| Unauthorized Overtime | `total_hours_worked` over 8.5 |
| Early Departure | `total_hours_worked` under 7.0 |

Rules are checked in the order above, and each record gets at most one flag (the first rule it matches).

## Sample Results

Running against the included sample data (210 records of fictional employees) produces 30 anomalies:

| Anomaly | Count |
|---|---|
| Late Arrival | 13 |
| Early Departure | 12 |
| Missing Clock Out | 3 |
| Missing Clock In | 2 |

## Repository Files

- [detector.py](detector.py): reads the timecard CSV and writes `anomaly_report.csv`
- [timecard_sample_data.csv](timecard_sample_data.csv): fictional sample data with seeded anomalies
- [requirements.txt](requirements.txt): Python dependencies
- [Dockerfile](Dockerfile): container image for the detector
- [.github/workflows/run_detector.yml](.github/workflows/run_detector.yml): GitHub Actions workflow that runs the detector on every push to `main` and uploads the report as a build artifact
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md): guide for deploying to Google Cloud

## Tech Stack

- **Language:** Python 3.11
- **Library:** pandas
- **Container:** Docker
- **CI:** GitHub Actions

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python detector.py
```

The report is written to `anomaly_report.csv` in the repository root.

## Run with Docker

```bash
docker build -t timecard-anomaly-detector:local .
docker run --rm -v "$PWD":/app timecard-anomaly-detector:local
```

The container runs the detector once and exits; `anomaly_report.csv` appears in your working directory.

## Cloud Deployment (Planned Architecture)

This repo runs as a single local script. [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) describes a Google Cloud version:

CSV uploaded to Cloud Storage → Cloud Run processes the file → anomalies stored in BigQuery → dashboards in Looker Studio

## Future Work

- Allow multiple flags per record (e.g. a late arrival that also runs into overtime)
- Add overtime cases to the sample data
- Accept the input file path as a command-line argument
- Add unit tests for each detection rule
