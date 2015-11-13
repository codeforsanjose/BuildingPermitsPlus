import sys
import csv
import click
import datetime
import calendar
import operator
from collections import defaultdict

MONTHS = {v.lower(): k for k, v in enumerate(calendar.month_abbr)}
MASTER_KEY = 'SUBCODE'

def average(values):
    if len(values) < 1:
        return 0
    return sum(values)/len(values)

def date_parse(input):
    """
    Take a string and turn it into a date
    Clumsy, replace with strftime

    day - month -year
    """
    if '/' in input:
        dt = datetime.datetime.strptime(input.lower(), '%d/%m/%y')
    else:
        dt = datetime.datetime.strptime(input.lower(), '%d-%b-%y')
    return dt


@click.command()
@click.argument('input_file')
@click.option('--analysis_key', default='SUBCODE', help='Key to pivot on')
def run(input_file, analysis_key):
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        output = defaultdict(list)
        averages = {}
        for row in reader:
            start_dt = date_parse(row['ISSUEDATE'])
            stop_dt = date_parse(row['FINALDATE'])
            interval = (stop_dt - start_dt).days
            key = row[analysis_key].lstrip()
            output[key].append(interval)
        for key, value in output.items():
            averages[key] = average(value)

        sorted_averages = sorted(averages.items(),
                                 key=operator.itemgetter(1))

        with open('data.out', 'w') as csvfile:
            fieldnames = [analysis_key, 'Interval_Average']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k, average_interval in sorted_averages:
                writer.writerow({analysis_key: k,
                                 'Interval_Average': average_interval})
            

if __name__=='__main__':
    run()
