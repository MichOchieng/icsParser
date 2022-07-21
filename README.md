# ICS File Parser
This program finds all google calendar (ics) files in the working directory, parses the files and prints the output into the CFUR playlist schedule in adobe illustrator.

## Classes
### Event
This class is used to encapsulate parsed events.
### Parser
This class handles parsing incoming text files and printing the parsed data to an output file.
#### &nbsp;&nbsp;&nbsp;&nbsp;Functions
- parseFile
    * This function handles parsing data from an incoming text file in multiple steps.
    1. Lines from the text file are read and stored in the lines variable.
    2. The lines variable is then used in a for loop to scan for specific event attribute identifiers.
    3. Once an identifier is found the data from that line will cleaned and saved into a temporary varible for future use.
    4. At the end of an event block the temporary variables are used to create an Event object that is then push to a list of Events.
- getRruleDay
    * This function is used in the parseFile function and determines what day an event will regularly reoccur on then returns that day in the form of a string.
- cleanList
    * This function is used to create a new 'clean' event list that excludes past events that have been saved to the event list that's used to hold all events saved from the parseFile function.
- getDate
    * This function uses the current days datetime to get the date of the most recent sunday in the current week.
- convertDay
    * Used to find what day of the week Daily events start on by converting a datetime to one of the
- printEvents
    * This Function will create a new file and print Events from the earleir mentioned Event list to said file.
- getFiles
    * This will find all the files in the current directory (in this case the icsParser directory) with the .ics file extension
- stripGenre
    * Strips genre tags (anything inside and including brackets) from all of the event titles 

## Example 
### Creating a parse file for adobe illustrator
```console
my@comp: python3 icsParser.py
```
- Example of output parse file
```console
-----EVENT 113
Throwback Funk & Soul
19
20220120
BYDAY=TH
-1
-----EVENT 114
Folk Traditions
10
20210909
BYDAY=TH
20220120
-----EVENT 115
Folk Traditions (Roots)
10
20220120
BYDAY=TH
-1
```
### Generating schedule from parse file
*   In illustrator goto the 'file' tab, select 'scripts' then 'other scritps' and select the adobe.jsx file. This will run the script and generate a version of the schedule below.

![output](public/timeTable.jpg)
*   A PNG of the schedule will be saved in the scripts folder.

## Notes
- The files to be parsed must be in the same directory as the python file otherwise they wont be found.
- More detail on the functions can be found in the comments.
- Should be ran using python 3.x

## Fixes/Additions
- ~~Text alignment in cells~~
- ~~Varying text size depending on length of the string~~
- ~~Increasing text range stroke width to increase visability~~
- ~~Automatically get ics file names from the working directory instead of entering manually~~
- ~~Exporting to PDF once schedule is created~~

