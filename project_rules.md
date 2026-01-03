# Project Rules & Safety Guardrails

This project strictly adheres to the following safety protocols to protect data integrity and separate security domains.

## 1. No Deletion Policy
- **Strictly Prohibited:** Usage of destructive commands such as `rm`, `delete`, `os.remove`, `shutil.rmtree` etc.
- **Goal:** Prevent accidental loss of master data or source code.
- **Action:** If a file needs to be "removed", archive it to a `_archive` folder or rename it with a `_deprecated` suffix instead.

## 2. Mandatory Backup (Time-Lock Safety)
- **Requirement:** Before ANY write operation to the local Master Data (`Shift_Schedule_DB.xlsx`), a backup MUST be created.
- **Format:** `_backup/Shift_Schedule_DB_YYYYMMDD_HHMMSS.xlsx`
- **Implementation:** The `sync_manager.py` script must handle this automatically.

## 3. One-Way Traffic (Security)
- **Direction:** External (Cloud/Web) -> Internal (Local PC) Only.
- **Constraint:** The local synchronization script (`sync_manager.py`) is allowed to **PULL** data from Supabase.
- **Prohibited:** It is strictly prohibited to PUSH local Excel data back to the external web database. The Local PC is the Secure Source of Truth (SSOT).
