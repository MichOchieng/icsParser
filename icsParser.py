import sys

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
            content = file.read()
        # Parse file data into event objects

        # Create new file with parsed data
        print(content)


