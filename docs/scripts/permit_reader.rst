What It Is:
===========

The permit_reader is a script whose primary job is to generate a pandas dataframe out of the full dataset (with some elimination of weird results). This is primarily a toy to show that we can generate a pandas dataframe on loading and then perform data analysis and pivoting on it.


How It Works:
=============

::
   python scripts/permit_reader.py all_out.csv --analysis_key ISSUEDATE

Here:
* all_out.csv is the file that it is going to process
* analysis_key is the pivot key (ISSUEDATE). It will calculate the mean and standard deviation of all individual entries in that column.
