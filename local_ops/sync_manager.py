import pandas as pd
import shutil
import os
from datetime import datetime, timedelta

# Configuration
LOCAL_DB_PATH = 'Shift_Schedule_DB.xlsx'
BACKUP_DIR = '_backup'
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def create_backup(file_path):
    """
    [Safety Guardrail] Mandatory Backup
    Creates a timestamped copy of the master DB before any write operation.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"Shift_Schedule_DB_{timestamp}.xlsx"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"[Backup] Created: {backup_path}")
        return True
    except Exception as e:
        print(f"[Error] Backup failed: {e}")
        return False

def fetch_changes_from_cloud():
    """
    [One-Way Traffic]
    Simulate fetching data from Supabase.
    In real implementation, this would use supabase-py client.
    """
    print("[Sync] Pulling data from Supabase (External Layer)...")
    
    # Mock Data: Simulating a change request from the web for a FUTURE date
    # Example: User_A_01 changes shift to 'Night' on a future date
    future_date = (TODAY + timedelta(days=2)).strftime('%Y-%m-%d')
    
    mock_changes = [
        {
            'date': future_date, 
            'emp_id': 'EMP_A_01', 
            'emp_name': 'User_A_01', 
            'team': 'A', 
            'shift': 'Night', 
            'work_type': 'Regular',
            'synced_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    return mock_changes

def calculate_weekly_hours(df):
    """
    [Compliance] 52-Hour Work Week Check
    Simple logic: Group by Week+User and sum hours.
    Assumptions:
    - Day/Swing/Night = 8 hours
    - Overtime = +4 hours (Total 12)
    - Off/Leave = 0 hours
    """
    print("[Analysis] Running 52-Hour Compliance Check...")
    
    # Helper to clean valid shifts
    def get_hours(row):
        base = 0
        if row['shift'] in ['Day', 'Swing', 'Night']:
            base = 8
        
        if row['work_type'] == 'Overtime':
            base += 4
        elif row['work_type'] == 'Leave' or row['shift'] == 'OFF':
            base = 0
            
        return base

    df['work_hours'] = df.apply(get_hours, axis=1)
    
    # Convert date to datetime
    df['date_dt'] = pd.to_datetime(df['date'])
    # ISO Calendar week
    df['week_number'] = df['date_dt'].dt.isocalendar().week
    
    # Group by Employee and Week
    report = df.groupby(['emp_name', 'week_number'])['work_hours'].sum().reset_index()
    
    # Check for violations
    violations = report[report['work_hours'] > 52]
    
    if not violations.empty:
        print("⚠️  [WARNING] 52-Hour Policy Violations Found:")
        print(violations)
    else:
        print("✅  [Pass] All schedules comply with 52-hour policy.")
        
    return report

def sync_logic():
    # 1. Load Local SSOT
    if not os.path.exists(LOCAL_DB_PATH):
        print(f"[Error] Master DB not found: {LOCAL_DB_PATH}")
        return

    try:
        df = pd.read_excel(LOCAL_DB_PATH)
        print(f"[Load] Local DB loaded ({len(df)} records).")
    except Exception as e:
        print(f"[Error] Failed to load Excel: {e}")
        return

    # 2. Fetch New Data (One-Way Pull)
    changes = fetch_changes_from_cloud()
    if not changes:
        print("[Sync] No new changes from cloud.")
        return

    # 3. Create Backup (Mandatory)
    if not create_backup(LOCAL_DB_PATH):
        print("[Abort] Cannot proceed without backup.")
        return

    # 4. Apply Changes (Upsert Strategy)
    updated_count = 0
    skipped_count = 0
    
    for change in changes:
        target_date = change['date']
        target_date_dt = datetime.strptime(target_date, '%Y-%m-%d')
        
        # Security: Do not overwrite past data
        if target_date_dt < TODAY:
            print(f"[Skip] Attempt to modify past date: {target_date}")
            skipped_count += 1
            continue

        # Logic: Find matching row (Date + Emp_ID)
        mask = (df['date'] == target_date) & (df['emp_id'] == change['emp_id'])
        
        if df[mask].empty:
            # New Insert
            new_row = pd.DataFrame([change])
            df = pd.concat([df, new_row], ignore_index=True)
            updated_count += 1
        else:
            # Update (Upsert)
            idx = df[mask].index[0]
            for key, val in change.items():
                df.at[idx, key] = val
            updated_count += 1

    # 5. Save Report & File
    if updated_count > 0:
        df.to_excel(LOCAL_DB_PATH, index=False)
        print(f"[Success] Synced {updated_count} records. (Skipped: {skipped_count})")
        
        # 6. Run Compliance Check after update
        calculate_weekly_hours(df)
        
    else:
        print("[Sync] No valid updates applied.")

if __name__ == "__main__":
    sync_logic()
