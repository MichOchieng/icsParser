from os import times
import sys
import re
from datetime import datetime

class Event:
    # Will be used to encapsulate event data from the parser class
    def __init__(self,name,startTime,endTime,rawDate):
        self.name         = name
        self.startTime    = startTime
        self.endTime      = endTime
        self.rawDate      = rawDate # Used to clean the event list

class Parser:
    fileName = ""

    # Constants used for identifying calendar event attributes
    EVENT_BLOCK_START  = "BEGIN:VEVENT"
    EVENT_BLOCK_END    = "END:VEVENT"

    EVENT_START_TIME   = ["DTSTART;","DTSTART:"]
    EVENT_END_TIME     = ["DTEND;","DTEND:"]

    EVENT_SUMMARY      = "SUMMARY:"

    EVENT_DESC_END     = ["LAST-MODIFIED:","LOCATION:","SEQUENCE:","STATUS:","SUMMARY:"]
    EVENT_DATA_REMAINS = "\\n\\nî¡¸\\n\\n\\nOrganiser: News Blocks"
    
    # Will hold event objects before they are sent to a file
    EVENT_LIST         = []
    CLEAN_EVENT_LIST   = []

    PARSED_FILENAME = "PARSED" + sys.argv[1]

    def parseTime(self,dateTime):
        # Could be implemented with datetime
        # parsedYear  = dateTime[:4] + '-' + dateTime[4:4]
        # parsedMonth = dateTime[4:6] + '-'
        # parsedDay   = dateTime[6:8] + ' '
        parsedTime  = dateTime[8:10] + ':' + dateTime[10:12] + ':' + dateTime[12:14]
        return parsedTime

    def parseFile(self):
        self.fileName = sys.argv[1]
        # Takes in file as a command line argument
        try: 
            with open(self.fileName,"r",encoding='utf-8',errors='ignore') as file:
                lines = file.readlines()
        except OSError:
            print("Could not open file " + self.fileName + ".")
            sys.exit()

        eventFound  = False

        # Temporary values used to create event objects at the end of for loop
        tempStartTime = ''
        tempEndTime   = ''
        tempSum       = ''
        tempRawTime   = ''
        for line in lines:
            # Find an Event
            if(line.replace('\n','') == self.EVENT_BLOCK_START): # Removing new line char at the end of each line
                eventFound = True
                continue

            # Get event start time
            if(any(identifier in line for identifier in self.EVENT_START_TIME) and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                tempStartTime = self.parseTime(time)
                continue

            # Get event end time
            if(any(identifier in line for identifier in self.EVENT_END_TIME) and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                # This grabs the numerical YYYY/MM/DD value as a str and saves it as an integer to be used later for cleaning the eventList
                tempRawTime = int(time[0:8:])
                tempEndTime = self.parseTime(time)
                continue

            # Get event summary/name
            if(self.EVENT_SUMMARY in line and eventFound):
                readingDesc = False
                # tempSum = re.sub('[^a-zA-Z ]','',(line.replace(self.EVENT_SUMMARY,''))) will only display alphabetical characters and spaces
                tempSum = (line.replace(self.EVENT_SUMMARY,'')).replace('\n','')
                continue 

            if(self.EVENT_BLOCK_END in line and eventFound):
                eventFound = False
                # Create event object
                temp = Event(tempSum,tempStartTime,tempEndTime,tempRawTime)
                # Push event to list
                self.EVENT_LIST.append(temp)
                continue   
    # This will remove events older than a given datetime value
    def cleanList(self):
        # Loop through EVENT_LIST
            # If an event has a start datetime older than the current datetime
                # Remove the event

        # Gets the current datetime then removes non-numeric values and saves the result as an integer value
        currentDateTime = int(
                                re.sub(
                                        '[^0-9]','',datetime.today().strftime('%Y-%m-%d')
                                    )
                            )
        for i,evnt in enumerate(self.EVENT_LIST):
            if(currentDateTime <= evnt.rawDate):
                self.CLEAN_EVENT_LIST.append(evnt)

    # This will print the encapsulated events to a new file
    def printEvents(self):
        # Remove old events
        self.cleanList()
        try:
            with open('PARSED' + self.fileName,'w',encoding='utf-8',errors='ignore') as file:
                sys.stdout = file
                for i,evnt in enumerate(self.CLEAN_EVENT_LIST):
                    print("~~EVENT " + str(i+1))
                    print(evnt.name)  
                    print(evnt.startTime)
                    print(evnt.endTime) 
                    print(evnt.rawDate)
                    print("\n")    
        except OSError:
            print("Something went wrong writing to parse file!")
p = Parser()
p.parseFile()
p.printEvents()