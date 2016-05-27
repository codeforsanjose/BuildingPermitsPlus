# About the BuildingPermitsPlus Project

The goal of this project is to analyze historical data from building permit records to determine anything notable (such as bottle-necks etc.), and to design and develop a web interface for the application process. For further details, visit https://codeforsanjose.slack.com/messages/buildingpermitsplus/.

Current Data Sets:

  http://www.sjpermits.org/permits/ftproot/SanJose/permitdataMonths/PD_00_Layout.txt
  
  http://www.sjpermits.org/permits/general/getreports.asp?rt=py
  
## Languages

Python

## Administration

Team Lead: Matthew Norman
Team Lead: Joseph

For information or inquiries: Joseph - JcoEighty6@gmail.com

## Project Status

First round of data processing complete. Waiting for visulaization.

## Data:

 * raw_data: This directory holds the raw_data from recent years in PD_*_ISSUE and PD_*_FINAL state.
 * PD_*_ISSUE contains information on permits grouped by issue year.
 * PD_*_FINAL contains information on permits grouped by year of completion.

## raw_data/all_permits.csv
 * This holds the entire dataset from 1900 to 2014.
 * It includes all fields, although many are blank in earlier entries.
 * It adds the following three fields: INTERVAL, latitude, and longitude
 * INTERVAL is the time between ISSUE_DATE and FINAL_DATE
 * latitude and longitude are the coordinates, and are present when a valid APN is available.
 
## Further Investigation:
 * Where are people building and how has that changed over time.?
 * What type of properties are being modified?
 * How long do permits take to complete and does that vary by geography?
 * Does the geography of permits correspond to any other geographic distribution?
 * How does a high volume of permits affect the area? Given twenty years of permit data, can we track trends in construction and compare it to trends in income, density, transit use, school performance, or other data from any other geographic dataset?
 * Anything else interesting in the data.


## Contributing

As posted in the meet-up notification:

Come up with insights to help make the permitting process more readily understandable and transparent to residents and businesses. The end result might be a customer facing product that shows how long each permit takes and what the expectation should be. So, we're also interested in prototypes for a dashboard that tracks the timeline for every step in the permitting process (request, acceptance, plan reviews, inspections and approval) for a particular type of business, such as restaurant, retail, office, medical/dental clinic, and so on.

Have anything to add? Fork this repository and open a pull request.
