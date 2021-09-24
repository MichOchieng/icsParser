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
    
    EVENT_BLOCK_START  = "BEGIN:VEVENT"
    EVENT_BLOCK_END    = "END:VEVENT"

    EVENT_START_TIME   = "DTSTART;"
    EVENT_END_TIME     = "DTEND;"

    EVENT_DESCRIPTION  = "DESCRIPTION:"
    EVENT_SUMMARY      = "SUMMARY:"

    EVENT_DESC_END     = ["LAST-MODIFIED:","LOCATION:","SEQUENCE:","STATUS:","SUMMARY:"]
    EVENT_DATA_REMAINS = "\\n\\nî¡¸\\n\\n\\nOrganiser: News Blocks"
    
    # Will hold event objects before they are sent to a file
    EVENT_LIST = []

    PARSED_FILENAME = "PARSED" + sys.argv[1]

    def parseDateTime(self,dateTime):
        # Could be implemented with datetime
        parsedYear  = dateTime[:4] + '-' + dateTime[4:4]
        parsedMonth = dateTime[4:6] + '-'
        parsedDay   = dateTime[6:8] + ' '
        parsedTime  = dateTime[8:10] + ':' + dateTime[10:12] + ':' + dateTime[12:14]
        return parsedYear + parsedMonth + parsedDay + parsedTime

    def parseFile(self):
        # Takes in file as a command line argument
        with open(sys.argv[1],"r") as file:
            lines = file.readlines()

        eventFound  = False
        readingDesc = False # Allows the full description to be parsed if it spans multiple lines

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
                tempStartTime = self.parseDateTime(time)
                continue

            # Get event end time
            if(self.EVENT_END_TIME in line and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                tempEndTime = self.parseDateTime(time)
                continue

            # Get event description
            if(self.EVENT_DESCRIPTION in line and eventFound):
                readingDesc = True
                desc = line.replace(self.EVENT_DESCRIPTION,'')
                tempDesc = desc.replace('\\n','')
                continue
            
            # Stops unwanted event attributes after the description from being saved to event object
            if(readingDesc and eventFound and not any(identifier in line for identifier in self.EVENT_DESC_END )):
                tempDesc += line.replace('\n','')

            # Get event summary
            if(self.EVENT_SUMMARY in line and eventFound):
                readingDesc = False
                # tempSum = re.sub('[^a-zA-Z ]','',(line.replace(self.EVENT_SUMMARY,''))) will only display alphabetical characters and spaces
                tempSum = (line.replace(self.EVENT_SUMMARY,'')).replace('\n','')
                continue 

            if(self.EVENT_BLOCK_END in line and eventFound):
                eventFound = False
                # Create event object
                temp = Event(tempSum,tempDesc.replace(self.EVENT_DATA_REMAINS,''),tempStartTime,tempEndTime)
                # Push event to list
                self.EVENT_LIST.append(temp)
                continue   
    # This will print the encapsulated events to a new file
    def printEvents(self):
        with open('PARSED'+sys.argv[1],'w') as file:
            sys.stdout = file
            for evnt in self.EVENT_LIST:
                print("---------")
                print(evnt.name)  
                print(evnt.description)
                print(evnt.startTime)
                print(evnt.endTime)        
p = Parser()
p.parseFile()
p.printEvents()