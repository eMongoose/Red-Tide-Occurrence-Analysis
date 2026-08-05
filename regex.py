import re

hab_occurrence_re = re.compile(r"^(\S+)-(\d+)-(\d+)-(\d+)-0$")
temp_re = re.compile(r'(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z')
o_fldc_pm_re = re.compile(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')

def hab_occurrencesStationParser(string):
    '''
    Parse the station name from the hab_occurrences 
    '''
    match = hab_occurrence_re.match(string)
    if match:
        station = match.group(1)
        return f'{station}'
    else:
        return None
    

def hab_occurrencesDateParser(string):
    '''
    Parse the date from the hab_occurrences
    '''
    match = hab_occurrence_re.match(string)
    if match:
        month = match.group(2)
        day = match.group(3) 
        year = match.group(4)
        return f'{year}-{month}-{day}'
    else:
        return None


def tempDateParser(date):
    '''
    Parse date from temp 
    '''
    match = temp_re.match(date)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return f'{year}-{month}-{day}'
    else:
        return None

def tempTimeParser(time):
    '''
    Parse time from temp
    '''
    match = temp_re.match(time)
    if match:
        hour = match.group(4)
        minute = match.group(5)
        second = match.group(6)
        return f'{hour}:{minute}:{second}'
    else:
        return None
    

def o_fldc_pmDateParser(object):
    '''
    Parse date from o_fldc_pm
    '''
    match = o_fldc_pm_re.match(object)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return f'{year}-{month}-{day}'
    else:
        return None 