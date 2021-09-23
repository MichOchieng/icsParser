import sys
import re

class Event:
    # Will be used to encapsulate event data from the parser class
    def __init__(self,name,description,startTime,endTime):
        self.name        = name
        self.description = description
        self.startTime   = startTime
        self.endTime     = endTime

class Parser:
    # Constants used for identifying calendar event attributes
    
    EVENT_BLOCK_START = "BEGIN:VEVENT"
    EVENT_BLOCK_END   = "END:VEVENT"

    EVENT_START_TIME  = "DTSTART;"
    EVENT_END_TIME    = "DTEND;"

    EVENT_DESCRIPTION = "DESCRIPTION:"
    EVENT_SUMMARY     = "SUMMARY:"
    
    # Will hold event objects before they are sent to a file
    EVENT_LIST = []

    PARSED_FILENAME = "PARSED" + sys.argv[1]


    def parseFile(self):
        # Takes in file as a command line argument
        with open(sys.argv[1],"r") as file:
            lines = file.readlines()
        # Parse file data into event objects
        eventFound = False

        # Temporary values used to create event objects at the end of for loop
        tempStartTime = ''
        tempEndTime   = ''
        tempDesc      = ''
        tempSum       = ''
        for line in lines:
            # Find an Event
            if(line.replace('\n','') == self.EVENT_BLOCK_START): # Removing new line char at the end of each line
                eventFound = True
                continue
            # Get event start time
            if(self.EVENT_START_TIME in line and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                print(time)
                continue
            # Get event end time
            if(self.EVENT_END_TIME in line and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                print(time)
                continue
            # Get event description
            if(self.EVENT_DESCRIPTION in line and eventFound):
                print(line)
                continue
            # Get event summary
            if(self.EVENT_SUMMARY in line and eventFound):
                # Push event to list
                print(line)
                continue 
            if(self.EVENT_BLOCK_END in line and eventFound):
                eventFound = False
                # Push event to list
                print(line)
                continue 

p = Parser()
p.parseFile()