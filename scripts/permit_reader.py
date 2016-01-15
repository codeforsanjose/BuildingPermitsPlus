import sys
import csv
import json
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
@click.option('--secondary_key', default=None, help='Secondary pivot key')
@click.option('--output_format', default='print',
              help='Way to output final data')
@click.option('--output_file', default='output.out',
              help='File to write output to. Does not effect print.')
def run(input_file, analysis_key, secondary_key, output_format,
        output_file):
                    
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
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
        if secondary_key is not None:
            group_by = [analysis_key, secondary_key]
            keyname = '{}:{}'.format(analysis_key, secondary_key)
        else:
            group_by = analysis_key
            keyname = analysis_key
        interval_dataseries = df.groupby(group_by).INTERVAL
        means = interval_dataseries.mean().to_dict()
        stddevs = interval_dataseries.std().to_dict()
        counts = interval_dataseries.count().to_dict()
        output_data = [{'keyname': keyname, 'key': key,
                        'mean time (days)': mean,
                        'stddev (days)': stddevs.get(key, None),
                        'number of entries': counts.get(key, None)}
                       for key, mean in means.items()]
        if len(output_data) == 0:
            # No data
            print('No data at end!')
            sys.exit(0)
        if output_format == 'print':
            for row in output_data:
                print(row)
        elif output_format == 'json':
            with open(output_file, 'w') as f:
                json.dump(output_data, f)
        elif output_format == 'csv':
            with open(output_file, 'w') as csvfile:
                fieldnames = output_data[0].keys()
                writer = csv.DictWriter(csvfile,
                                        fieldnames=fieldnames)
                writer.writeheader()
                for row in output_data:
                    writer.writerow(row)
                


if __name__=='__main__':
    run()
