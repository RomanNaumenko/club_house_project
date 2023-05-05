from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime


def calendar_specific(request, year=datetime.now().year, month=datetime.now().strftime("%B")):

    month = month.capitalize()
    time = datetime.now().strftime('%I:%M %p')
    month_number = int(list(calendar.month_name).index(month))
    cal = HTMLCalendar().formatmonth(year, month_number)
    context = {"year": year, "month": month, "month_number": month_number, "cal": cal, "time": time}
    return render(request, 'calendar/calendar.html', context)
