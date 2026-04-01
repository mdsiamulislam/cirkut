from django.core.management import call_command
from django.http import HttpResponse

def backup_database(request):
    try:
        call_command('dbbackup')
        print("Database backup successful!")
        return HttpResponse("Database backup successful!")
    except Exception as e:
        print(f"Database backup failed: {e}")
        return HttpResponse(f"Database backup failed: {e}")