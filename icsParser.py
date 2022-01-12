import sys
import re
import shutil
import os
from datetime import datetime

class Event:
    # Will be used to encapsulate event data from the parser class
    def __init__(self,name,startTime,endTime,rawDate,rruleDay,rruleFreq,rruleEnd):
        self.name         = name
        self.startTime    = startTime
        self.endTime      = endTime
        # Used to clean the event list
        self.rawDate      = rawDate
        # Variables for recurrance rules
        self.rruleEnd     = rruleEnd
        self.rruleFreq    = rruleFreq
        self.rruleDay     = rruleDay

class Parser:
    fileName = ""

    # Constants used for identifying calendar event attributes
    EVENT_BLOCK_START  = "BEGIN:VEVENT"
    EVENT_BLOCK_END    = "END:VEVENT"

    EVENT_START_TIME   = ["DTSTART;","DTSTART:"]
    EVENT_END_TIME     = ["DTEND;","DTEND:"]

    EVENT_SUMMARY      = "SUMMARY:"

    RRULE              = "RRULE:"
    RRULE_DAYS         = ["BYDAY=MO","BYDAY=TU","BYDAY=WE","BYDAY=TH","BYDAY=FR","BYDAY=SA","BYDAY=SU",]

    EVENT_DESC_END     = ["LAST-MODIFIED:","LOCATION:","SEQUENCE:","STATUS:","SUMMARY:"]
    EVENT_DATA_REMAINS = "\\n\\nî¡¸\\n\\n\\nOrganiser: News Blocks"
    
    # Will hold event objects before they are sent to a file
    EVENT_LIST         = []
    CLEAN_EVENT_LIST   = []

    PARSED_FILENAME = "PARSED" + sys.argv[1]

    # This will do most of the heavy lifting of stripping important data from the input file
    # and creating event objects
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
        tempFreq      = ''
        tempRREND     = ''

        for line in lines:
            # Find an Event
            if(line.replace('\n','') == self.EVENT_BLOCK_START): # Removing new line char at the end of each line
                eventFound = True
                continue

            # Get event start time
            if(any(identifier in line for identifier in self.EVENT_START_TIME) and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                tempStartTime = time[8:10]
                continue

            # Get event end time
            if(any(identifier in line for identifier in self.EVENT_END_TIME) and eventFound):
                # Strip date/time from string
                time = re.sub('[^0-9]','',line)
                # This grabs the numerical YYYY/MM/DD value as a str and saves it as an integer to be used later for cleaning the eventList
                tempRawTime = int(time[0:8:])
                tempEndTime = time[8:10]
                continue

            # Get info on Recurance Rules
            if((self.RRULE in line) and eventFound):
                # Get the day of the event
                tempRRDAY = self.getRruleDay(line)
                # Get frequency
                if("FREQ=WEEKLY" in line):
                    tempFreq  = "WEEKLY"
                    # Get datetime and convert into an int of the event
                    if(any(identifier in line for identifier in self.RRULE_DAYS)):
                        temp = re.sub('[^0-9]','',line)[0:8:]
                        # Fixes int casting issue
                        if(temp != ''):
                            tempRREND = int(temp)
                        else:
                            tempRREND = temp
                elif("FREQ=DAILY" in line):
                    tempFreq  = "DAILY"
                    # Get datetime and convert into an int of the event
                    if(any(identifier in line for identifier in self.RRULE_DAYS)):
                        temp = re.sub('[^0-9]','',line)[0:8:]
                        # Fixes int casting issue
                        if(temp != ''):
                            tempRREND = int(temp)
                        else:
                            tempRREND = temp
                    continue

            # Get event summary/name
            if(self.EVENT_SUMMARY in line and eventFound):
                readingDesc = False # ! Might not need this anymore !
                # tempSum = re.sub('[^a-zA-Z ]','',(line.replace(self.EVENT_SUMMARY,''))) will only display alphabetical characters and spaces
                tempSum = (line.replace(self.EVENT_SUMMARY,'')).replace('\n','')
                continue 

            if(self.EVENT_BLOCK_END in line and eventFound):
                eventFound = False
                # Create event object
                temp = Event(tempSum,tempStartTime,tempEndTime,tempRawTime,tempRRDAY,tempFreq,tempRREND)
                # Push event to list
                self.EVENT_LIST.append(temp)
                continue   

    def getRruleDay(self,line):
        # Not Ideal
        if re.search(r'\b' + "BYDAY=MO" + r'\b',line):
            return "BYDAY=MO"
        elif re.search(r'\b' + "BYDAY=TU" + r'\b',line):
            return "BYDAY=TU"
        elif re.search(r'\b' + "BYDAY=WE"+ r'\b',line):
            return "BYDAY=WE"
        elif re.search(r'\b' + "BYDAY=TH"+ r'\b',line):
            return "BYDAY=TH"
        elif re.search(r'\b' + "BYDAY=FR"+ r'\b',line):
            return "BYDAY=FR"
        elif re.search(r'\b' + "BYDAY=SA"+ r'\b',line):
            return "BYDAY=SA"
        elif re.search(r'\b' + "BYDAY=SU"+ r'\b',line):
            return "BYDAY=SU"
    
    # This will create a new event list with only newer events
    def cleanList(self):
        # Loop through EVENT_LIST
            # If an event has a start datetime older than the current datetime
                # Check to see if it's a reccuring event that was created earlier than today
                    # Check to see if there is a stopping date
                        # If there is and it's not older than today
                            # Add to new event list 
                        # If there is and it's older than today
                            # Don't add to the new list 
            # Otherwise just add to the new event list

        # Gets the current datetime then removes non-numeric values and saves the result as an integer value
        currentDateTime = datetime.today()
        currentDateInt  = int(
                                re.sub(
                                        '[^0-9]','',datetime.today().strftime('%Y-%m-%d')
                                    )
                            ) + self.getDate(currentDateTime)

        for i,evnt in enumerate(self.EVENT_LIST):
            # 20211201 is used for debugging should be the currentDateTime var
            if(currentDateInt <= evnt.rawDate):
                self.CLEAN_EVENT_LIST.append(evnt)
            # If the event is 'older' than todays date
            elif(currentDateInt > evnt.rawDate):
                # Check to see if the stopping date exists and is older than today as well
                if(evnt.rruleEnd != '' and (20211201 <= evnt.rruleEnd)):
                    self.CLEAN_EVENT_LIST.append(evnt)

    # Takes in the current datetime and finds how far that day is from the previous sunday
    def getDate(self,datetime):
        # Sunday = 6    Monday = 0
        # Schedule week starts on sunday
        # Depending on the current day a value is returned to subtract
        # from the current datetime to get sundays datetime of the current week
        if(datetime.weekday() == 6):
            return 0
        elif(datetime.weekday() == 0):
            return -1
        elif(datetime.weekday() == 1):
            return -2
        elif(datetime.weekday() == 2):
            return -3
        elif(datetime.weekday() == 3):
            return -4
        elif(datetime.weekday() == 4):
            return -5
        elif(datetime.weekday() == 5):
            return -6

    # This will print the encapsulated events to a new file
    def printEvents(self):
        # Remove old events
        self.cleanList()
        try:
            with open('parseFile.txt','w',encoding='utf-8',errors='ignore') as file:
                sys.stdout = file
                for i,evnt in enumerate(self.CLEAN_EVENT_LIST):
                    print("-----EVENT " + str(i+1))
                    print(evnt.name)  
                    print(evnt.startTime)
                    print(evnt.rawDate)
                    print(evnt.rruleDay)
                # Moves new parse file to the scripts folder
                shutil.move("./parseFile.txt","./scripts/parseFile.txt")
        except OSError:
            print("Something went wrong writing to parse file!")
p = Parser()
p.parseFile()
p.printEvents()