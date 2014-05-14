from datetime import date

def format_date(template, d=None):
    if d is None:
        d = date.today()
    template_vars = {
        'year': d.year,
        'month': d.month,
        'monthname': ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[d.month-1],
        'day': d.day,
        'weekday': d.weekday(),
        'weekdayname': ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')[d.weekday()],
    }
    return template.format(**template_vars)

print(format_date('{monthname} {day}, {year}, {weekdayname}'))
