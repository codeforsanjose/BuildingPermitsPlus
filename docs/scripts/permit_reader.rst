What It Is:
===========

The permit_reader is a script whose primary job is to generate a pandas dataframe out of the full dataset (with some elimination of weird results). This is primarily a toy to show that we can generate a pandas dataframe on loading and then perform data analysis and pivoting on it.


How It Works:
=============

::

   python scripts/permit_reader.py raw_data/PD_*_ISSUE.txt --analysis_key SUBCODE --secondary_key=PERMITFLAG --output_format csv --output_file out.csv

Here:

* raw_data/PD_*_ISSUE.txt are the files that it is going to process
* analysis_key is the pivot key (SUBCODE). It will calculate the mean and standard deviation of all individual entries in that column.
* secondary_key is a second key that is also pivoted on. With a secondary key you get another value in the output that calculates the number of standard deviations that the mean of the subgroup is from the main group (the difference between the mean if you include everything with the same analysis_key compared with the mean of the subgroup with the analysis_key and the secondary_key)
* output_format is the format in which you want the output. Currently supports csv, json, and print (which is just stdout).
* output_file is an optional argument that it will write out to in either csv or json. This is not used by the print output_format.
