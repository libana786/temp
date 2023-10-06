from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from .models import Payment

def Query_model_by_duration(model, duration):
    today = timezone.now()

    if duration == 'day':
        # Query for objects created within the current day
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today.replace(hour=23, minute=59, second=59, microsecond=999)
    elif duration == 'week':
 # Find the first day (usually Monday) of the current week
        first_day_of_week = today - timedelta(days=today.weekday())
        # Calculate the end of the week (Sunday)
        end_date = first_day_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999)
        start_date = first_day_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    elif duration == 'month':
        # Query for objects created within the current month
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = today.replace(month=today.month % 12 + 1)
        end_date = next_month - timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999)
    else:
        raise ValueError("Invalid duration. Use 'day', 'week', or 'month'.")

    # Use the provided model and date range to query objects
    filtered_objects = model.objects.filter(
        Q(Date_created__gte=start_date) & Q(Date_created__lte=end_date)
    )

    return filtered_objects

# A = Query_model_by_duration(Payment,'week')
# if A:
#     print("yess................")
#     print(A)
# else:
#     print("nooooooo")