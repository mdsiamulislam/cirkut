from django.core.management import call_command

def backup_database():
    try:
        call_command('dbbackup')
        print("Database backup successful!")
    except Exception as e:
        print(f"Database backup failed: {e}")