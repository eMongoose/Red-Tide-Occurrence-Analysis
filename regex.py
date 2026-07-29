import re

date_re = re.compile(r"^(\S+)-(\d+)-(\d+)-(\d+)-0$")
temp_re = re.compile(r'(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z')

def dateConverterHelper(date):
    match = date_re.match(date)
    if match:
        month = match.group(2)
        day = match.group(3) 
        year = match.group(4)
        return f'{year}-{month}-{day}'
    else:
        return None


def tempDateParser(date):
    match = temp_re.match(date)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return f'{year}-{month}-{day}'
    else:
        return None

def tempTimeParser(time):
    match = temp_re.match(time)
    if match:
        hour = match.group(4)
        minute = match.group(5)
        second = match.group(6)
        return f'{hour}:{minute}:{second}'
    else:
        return None
    
