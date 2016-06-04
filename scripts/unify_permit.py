import csv

full_dataset = []
fieldnames = None
with open('permit_out.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if fieldnames is None:
            fieldnames = row.keys()
        full_dataset.append(row)

fieldnames.extend(['latitude', 'longitude'])
with open('out.csv', 'r') as csvfile:
    latlng_dict = {}
    reader = csv.DictReader(csvfile)
    for row in reader:
        latlng_dict[row['APN']] = row

for row in full_dataset:
    apn = row.get('APN')
    if apn == '':
        # Nothing to do here.
        continue
    if apn in latlng_dict:
        row.update(latlng_dict[apn])
    else:
        row['latitude'] = None
        row['longitude'] = None

with open('all_permit.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile,
                            fieldnames=fieldnames)
    writer.writeheader()
    for row in full_dataset:
        writer.writerow(row)
