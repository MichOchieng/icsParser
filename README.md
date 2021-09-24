# Google Calendar Parser
This is a relatively simple program that will parse Google Calendar text files through a command line interface

## Classes
### Event
This class will encapsulate parsed events
### Parser
This class handles parsing incoming text files and printing the parsed data to an output file
#### &nbsp;&nbsp;&nbsp;&nbsp;Functions
- parseDateTime
    * This function takes in a datetime string in the form of yyyy-mm-dd-hh-mm-ss and breaks up the string making it easily readable
- parseFile
    * This function handles parsing data from an incoming text file in multiple steps
    1. Lines from the text file are read and stored in the lines variable
    2. The lines variable is then used in a for loop to scan for specific event attribute identifiers
    3. Once an identifier is found the data from that line will cleaned and saved into a temporary varible for future use
    4. At the end of an event block the temporary variables are used to create an Event object that is then push to a list of Events
- printEvents
    * This Function will create a new file and print Events from the earleir mentioned Event list to said file

## Example 
```console
my@comp: python icsParser.py <fileToBeParsed>.txt
```

## Notes
- The file to be parsed must be in the same directory as this python file