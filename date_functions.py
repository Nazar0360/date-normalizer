from datetime import datetime, timedelta
def check_date(year, month, *args, **kwargs):
    if year < 1 or year > 9999:
        raise ValueError("Year must be between 1 and 9999")
    elif month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    elif type(year) == float or type(month) == float:
        raise TypeError("Year and month must be integers")
def normalize_date(year, month, day, hour=0, minute=0, second=0):
    check_date(year, month)
    
    seconds = second + (minute * 60) + (hour * 3600) + (day * 86400)
    date = datetime(year, month, 1) + timedelta(days=-1, seconds=seconds)
    return date.year, date.month, date.day, date.hour, date.minute, date.second

def date2str(year, month, day, hour=0, minute=0, second=0, date_format="%Y.%m.%d %H:%M:%S"):
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime(date_format)

def str2float(date_string, default=0.0):
    return float(date_string) if date_string and date_string not in "+-." else default

def str2int(date_string, default=0):
    return int(date_string) if date_string and date_string not in "+-" else default
def str2date(string, date_format="%Y.%m.%d %H:%M:%S"):
    year, month, day, hour, minute, second = [""] * 6

    i = 0
    j = 0
    mode = None
    while i < len(string):
        if mode is not None:
            if (string[i] != date_format[j]) if j < len(date_format) else True:
                if mode == "year":
                    year += string[i]
                elif mode == "month":
                    month += string[i]
                elif mode == "day":
                    day += string[i]
                elif mode == "hour":
                    hour += string[i]
                elif mode == "minute":
                    minute += string[i]
                elif mode == "second":
                    second += string[i]
                i += 1
                continue
            else:
                mode = None
                i += 1
                j += 1

        if date_format[j] == "%":
            if date_format[j + 1] == "Y":
                mode = "year"
                j += 2
                continue
            elif date_format[j + 1] == "m":
                mode = "month"
                j += 2
                continue
            elif date_format[j + 1] == "d":
                mode = "day"
                j += 2
                continue
            elif date_format[j + 1] == "H":
                mode = "hour"
                j += 2
                continue
            elif date_format[j + 1] == "M":
                mode = "minute"
                j += 2
                continue
            elif date_format[j + 1] == "S":
                mode = "second"
                j += 2
                continue
        
        if string[i] != date_format[j]:
            print(string[i], date_format[j])
            raise ValueError("Invalid date format")
        i += 1
        j += 1
    
    return abs(str2int(year)), abs(str2int(month)), str2float(day), str2float(hour), str2float(minute), str2float(second)
