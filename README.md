# Graphed-and-Organized
This program has been written as a form of foundation, using the materials collected from the previous repository, in preparation for future projects.
The program begins by importing the data collected from an hourly calling of the webscrape function, which is a csv listing gas prices(in gwei) for every hour of the day(UTD).
I currently do not require any feature of datetime aside from the hour, or any gas cost other than 'average,' so the program starts by cleaning the data into two columns 'hours' and 'cost,' that respectively carry the 'hour' the data was collected and the average 'cost' of gas at that given hour.

A quick bar graph was built from this data that will be edited, and used to its full potential in future programs.
After this was done I believed it necessary to have a more easily readable csv file for possible displays, so I created an empty dataframe and transposed the Data into it.
