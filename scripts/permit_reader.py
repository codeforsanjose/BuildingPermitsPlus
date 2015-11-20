import sys
import csv
import click
import datetime
import calendar
import operator
import pandas as pd
from collections import defaultdict

MONTHS = {v.lower(): k for k, v in enumerate(calendar.month_abbr)}
MASTER_KEY = 'SUBCODE'
FIELDNAMES = ['TRACT', 'APN', 'ISSUEDATE', 'FINALDATE', 'LOT',
              'FOLDERNUMBER', 'OWNERNAME', 'CONTRACTOR', 'APPLICANT',
              'JOBLOCATION', 'PERMITAPPROVALS', 'SUBCODE', 'SUBDESC',
              'WORKCODE', 'WORKDESC', 'CENSUSCODE', 'PERMITVALUATION',
              'REROOFVALUATION', 'SQFT', 'DWELLUNITS', 'FOLDERRSN',
              'SWIMMINGPOOL', 'SEWER', 'ENTERPRISE', 'PERMITFLAG']

def date_parse(input):
    """
    Take a string and turn it into a date
    Clumsy, replace with strftime

    day - month -year
    """
    if '/' in input:
        dt = datetime.datetime.strptime(input.lower(), '%m/%d/%Y')
    else:
        dt = datetime.datetime.strptime(input.lower(), '%d-%b-%y')
    return dt

@click.command()
@click.argument('input_file')
@click.option('--analysis_key', default='SUBCODE', help='Key to pivot on')
def run(input_file, analysis_key):
                    
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', fieldnames=FIELDNAMES)
        output = defaultdict(list)
        full_dataset = []
        for row in reader:
            try:
                current_entry = {}
                for k,v in row.items():
                    if isinstance(v, str):
                        v = v.lstrip().rstrip()
                    current_entry[k] = v
                start_dt = date_parse(row['ISSUEDATE'])
                stop_dt = date_parse(row['FINALDATE'])
                interval = (stop_dt - start_dt).days
                current_entry['INTERVAL'] = interval
                full_dataset.append(current_entry)
            except Exception as ex:
                continue

        df = pd.DataFrame(full_dataset)
        means = df.groupby(analysis_key).INTERVAL.mean().to_dict()
        stddevs = df.groupby(analysis_key).INTERVAL.std().to_dict()
        for k, v in means.items():
            msg = 'Key {} value: {},  mean time (days): {},  stddev (days): {}'
            msg = msg.format(analysis_key, k, v, stddevs.get(k, 'NULL'))
            print(msg)
                


if __name__=='__main__':
    run()
