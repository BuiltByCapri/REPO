import pandas as pd

# Load the data
df = pd.read_csv('timecard_sample_data.csv')

# Convert time columns
df['actual_clock_in'] = pd.to_datetime(df['actual_clock_in'], format='%H:%M', errors='coerce')
df['actual_clock_out'] = pd.to_datetime(df['actual_clock_out'], format='%H:%M', errors='coerce')
df['scheduled_start'] = pd.to_datetime(df['scheduled_start'], format='%H:%M', errors='coerce')

anomalies = []

for _, row in df.iterrows():
    # Missing clock in
    if pd.isna(row['actual_clock_in']):
        anomalies.append({**row, 'anomaly_type': 'Missing Clock In'})
    
    # Missing clock out
    elif pd.isna(row['actual_clock_out']):
        anomalies.append({**row, 'anomaly_type': 'Missing Clock Out'})
    
    # Late arrival (more than 15 minutes)
    elif (row['actual_clock_in'] - row['scheduled_start']).total_seconds() / 60 > 15:
        anomalies.append({**row, 'anomaly_type': 'Late Arrival'})
    
    # Unauthorized overtime (over 8.5 hours)
    elif row['total_hours_worked'] != '' and float(row['total_hours_worked']) > 8.5:
        anomalies.append({**row, 'anomaly_type': 'Unauthorized Overtime'})
    
    # Early departure (less than 7 hours)
    elif row['total_hours_worked'] != '' and float(row['total_hours_worked']) < 7.0:
        anomalies.append({**row, 'anomaly_type': 'Early Departure'})

anomaly_df = pd.DataFrame(anomalies)
print(f"Total anomalies detected: {len(anomaly_df)}")
print(anomaly_df[['employee_name', 'date', 'anomaly_type']])

anomaly_df.to_csv('anomaly_report.csv', index=False)
print("\nReport saved to anomaly_report.csv")