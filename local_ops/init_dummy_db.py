import pandas as pd
import os
from datetime import datetime, timedelta
import random

# Configuration
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 12, 31)
TEAMS = ['A', 'B', 'C'] # 3 Groups
SHIFTS = ['Day', 'Swing', 'Night'] # 3 Shifts
EMPLOYEES_PER_TEAM = 5
OUTPUT_FILE = 'Shift_Schedule_DB.xlsx'

def generate_dates(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def main():
    print("Generating Dummy Shift Schedule DB...")

    data = []
    
    # Simple 3-Shift Rotation Logic (Just for dummy data)
    # A Team: Day -> Swing -> Night ...
    # This is a simplified pattern for demonstration. 
    # Real 3-shift 2-rotation (4조3교대 or 3조2교대) might be more complex, 
    # but here we ensure data exists for testing.
    
    dates = list(generate_dates(START_DATE, END_DATE))
    
    # Generate Employee List
    employees = []
    for team in TEAMS:
        for i in range(1, EMPLOYEES_PER_TEAM + 1):
            employees.append({
                'id': f"EMP_{team}_{i:02d}",
                'name': f"User_{team}_{i:02d}",
                'team': team
            })

    # Create Schedule Data
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        
        # Rotation Logic (Cycle every 3 days for simplicity in dummy)
        # Day 0: A=Day, B=Swing, C=Night 
        # Day 1: A=Night, B=Day, C=Swing ... 
        
        day_idx = (date - START_DATE).days
        shift_cycle = day_idx % 3
        
        team_shifts = {}
        if shift_cycle == 0:
            team_shifts = {'A': 'Day', 'B': 'Swing', 'C': 'Night'}
        elif shift_cycle == 1:
            team_shifts = {'A': 'Night', 'B': 'Day', 'C': 'Swing'}
        else:
            team_shifts = {'A': 'Swing', 'B': 'Night', 'C': 'Day'}

        for emp in employees:
            shift = team_shifts[emp['team']]
            
            # Randomly add some "Overtime" or "Leave" (Vacation)
            # internal_type: 'Regular', 'Overtime', 'Leave'
            # Note: In a real scenario, this comes from the cloud (Supabase)
            
            rand_val = random.random()
            work_type = 'Regular'
            if rand_val > 0.95:
                work_type = 'Leave'
                shift = 'OFF'
            elif rand_val > 0.90:
                work_type = 'Overtime' # e.g. Extended shift

            data.append({
                'date': date_str,
                'emp_id': emp['id'],
                'emp_name': emp['name'],
                'team': emp['team'],
                'shift': shift,
                'work_type': work_type,
                'synced_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Initial creation time
            })

    df = pd.DataFrame(data)
    
    # Save to Excel
    file_path = os.path.join(os.getcwd(), OUTPUT_FILE)
    df.to_excel(file_path, index=False)
    print(f"Successfully created {file_path} with {len(df)} rows.")

if __name__ == "__main__":
    main()
