import sys
import csv
import json
import math
import click
import sqlite3
import datetime
import calendar
import operator
import pandas as pd
from collections import defaultdict

MONTHS = {v.lower(): k for k, v in enumerate(calendar.month_abbr)}
MASTER_KEY = 'SUBCODE'
FIELDNAMES = {'TRACT': str, 'APN': str, 'ISSUEDATE': str,
              'FINALDATE': str, 'LOT': str,
              'FOLDERNUMBER': str, 'OWNERNAME': str,
              'CONTRACTOR': str, 'APPLICANT': str,
              'JOBLOCATION': str, 'PERMITAPPROVALS': str,
              'SUBCODE': int, 'SUBDESC': str,
              'WORKCODE': int, 'WORKDESC': str,
              'CENSUSCODE': str, 'PERMITVALUATION': float,
              'REROOFVALUATION': float, 'SQFT': float,
              'DWELLUNITS': int, 'FOLDERRSN': int,
              'SWIMMINGPOOL': str, 'SEWER': str,
              'ENTERPRISE': str, 'PERMITFLAG': str}
STDDEV_SIGNIFICANCE = 2.0

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
@click.argument('input_files', nargs=-1)
@click.option('--analysis_key', default='SUBCODE', help='Key to pivot on')
@click.option('--secondary_key', default=None, help='Secondary pivot key')
@click.option('--output_format', default='print',
              help='Way to output final data')
@click.option('--output_file', default='output.out',
              help='File to write output to. Does not effect print.')
def run(input_files, analysis_key, secondary_key, output_format,
        output_file):

    full_dataset = []
    for input_file in input_files:
        fds = run_file(input_file=input_file, analysis_key=analysis_key,
                       secondary_key=secondary_key,
                       output_format=output_format,
                       output_file=output_file)
        full_dataset.extend(fds)

    full_dataframe = pd.DataFrame(full_dataset)
    primary_dataseries = full_dataframe.groupby(analysis_key).INTERVAL
    interval_dataseries = primary_dataseries
    keyname = analysis_key
    primary_means = None
    primary_stddevs = None

    if secondary_key is not None:
        group_by = [analysis_key, secondary_key]
        keyname = '{}:{}'.format(analysis_key, secondary_key)
        interval_dataseries = full_dataframe.groupby(group_by).INTERVAL
        primary_means = primary_dataseries.mean().to_dict()
        primary_stddevs = primary_dataseries.std().to_dict()
    
    means = interval_dataseries.mean().to_dict()
    stddevs = interval_dataseries.std().to_dict()
    counts = interval_dataseries.count().to_dict()
        
    output_data = []
    for key, mean in means.items():
        stddev_deviation = 'N/A'
        if secondary_key is not None:
            try:
                prim_key = key[0]
                stddev = float(primary_stddevs.get(prim_key, 0.0))
                primary_mean = float(primary_means.get(prim_key, 0.0))
                distance = math.fabs(primary_mean - mean)
                stddev_deviation = distance/stddev
                if stddev_deviation > STDDEV_SIGNIFICANCE:
                    print('KEY {} DEVIATED BY {}'.format(key,
                                                         stddev_deviation))
            except ValueError:
                # Do nothing, because something was NaN
                pass
            except ZeroDivisionError:
                # Do nothing, because stddev was 0
                pass
        output_data.append(
            {'keyname': keyname, 'key': key,
             'mean time (days)': mean,
             'stddev (days)': stddevs.get(key, None),
             'number of entries': counts.get(key, None),
             'deviation from category mean': stddev_deviation
         }
        )

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
    elif output_format == 'sqlite':
        conn = sqlite3.connect(output_file)
        full_dataframe.to_sql(name='permit', con=conn, flavor='sqlite',
                              if_exists='replace')


def run_file(input_file, analysis_key, secondary_key, output_format,
             output_file):
    """
    Run under one file.
    """
                    
    with open(input_file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        output = defaultdict(list)
        full_dataset = []
        for row in reader:
            try:
                current_entry = {}
                for k,v in row.items():
                    if isinstance(v, str):
                        v = v.lstrip().rstrip()
                    validate_func = FIELDNAMES[k]
                    try:
                        if v != '':
                            validate_func(v)
                    except ValueError:
                        print('INVALID KEY, VALUE: ', k, v)
                        raise
                    current_entry[k] = v
                start_dt = date_parse(row['ISSUEDATE'])
                stop_dt = date_parse(row['FINALDATE'])
                interval = (stop_dt - start_dt).days
                if interval < 0:
                    print('TIME INTERVAL LESS THAN 0')
                    continue
                current_entry['INTERVAL'] = interval
                full_dataset.append(current_entry)
            except Exception as ex:
                continue

        return full_dataset


if __name__=='__main__':
    run()
