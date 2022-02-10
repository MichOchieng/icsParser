// ----------- Main Contents -----------
    
    var scheduleArray = initializeArray(7,24);
    var currentDir    = new File($.fileName);

    // Open calendar file
    var filePath = (currentDir.path + "/timeTable.ai"); // Replace with correct path on your machine
    var file     = File(filePath);

    // Export options
    var exprt       = new ExportOptionsPNG24();
    var type        = ExportType.PNG24;
    var schedulePNG = new File(currentDir.path + "/newSchedule");
    exprt.antiAliasing = true;
    exprt.transparency = false;
    exprt.saveAsHTML   = true;

    file.open('r');
    app.open(file);

    // Add text to calendar file
    fillEventArray();
    fillSchedule();

    // Save PNG of Schedule
    app.activeDocument.exportFile(schedulePNG,type,exprt);


// ----------- Functions -----------

    // Currently only adds boilerplate text
    function fillSchedule(){
        // Text: Sz - 4.2, stroke - 0.25
        var doc = app.activeDocument; // Targets the opened file as the working document
        for (var i = 0; i < 7; i++) {  // Colun
            for (var j = 0; j < 24; j++) {   // Row
                var txtFrame = doc.textFrames.add();
                var txtRange = txtFrame.textRange;

                var posX     = 100;
                var posY     = -156; // Negative because Y values are flipped in illustrator
                var offSetY  = 14.2;
                var offsetX  = 63;
                
                var eventName;

                var black = new RGBColor();
                black.red   = 0;
                black.green = 0;
                black.blue  = 0;

                // Need to check for null and undefined values otherwise error 1238 will be thrown
                if (scheduleArray[i][j] != null) {
                    if(j == 8){ // Bandaid fix for talking radical radio replacing BBC world service
                        eventName = "BBC World Service";
                    }
                    else{
                        eventName = scheduleArray[i][j];
                    }
                } 
                else{
                    eventName = ""
                }
        
                txtFrame.contents = stripGenre(eventName);
                // If the eventName string is longer than 20 characters decrease the strings size to 3.5pts otherwise keep at 6pts
                txtRange.size         = fontSizing(txtFrame.contents.length);
                txtRange.strokeColor  = black;
                txtRange.strokeWeight = 0.2;
                txtRange.textFont     = textFonts[278] // Sets all event names to futura bold font
                
                // Change text positioning to fix offset in thursday and saturday rows
                if (i == 4) {
                    txtFrame.position = [
                        (posX + ((i * 1.01) * offsetX)), // Offsets used to place in the correct row
                        (posY - (j * offSetY))           // Subtracting from posY due to flipped values
                    ];   
                }
                else if (i == 6) {
                    txtFrame.position = [
                        (posX + ((i * 0.99) * offsetX)), // Offsets used to place in the correct row
                        (posY - (j * offSetY))           // Subtracting from posY due to flipped values
                    ];  
                }
                else {
                    txtFrame.position = [
                        (posX + (i * offsetX)), // Offsets used to place in the correct row
                        (posY - (j * offSetY))  // Subtracting from posY due to flipped values
                    ];    
                }
            }
        }
    }

    function initializeArray(width,height){
        var arr = new Array(width);
        for (var index = 0; index < width; index++) {
            arr[index] = new Array(height);
        }
        return arr;
    }

    function fillEventArray(){
        var currentDir    = new File($.fileName);
        var parseFilePath = (currentDir.path + "/parseFile.txt");
        // Open up incoming file
        try {
            var file = File(parseFilePath);
            file.open('r');
            var fileContents = file.read();
            fileContents = fileContents.split("\n"); // Makes indexing a lot easier by creating substrings
        } catch (error) {
            alert("An error occured reading input file.");
            print(error);
        }

        // Loop through file and add events to an array
        //  Pull the startTime, rruleDay and rawDate from each event
        //  The startTime corresponds to the row in the schedule
        //  The rruleDay corresponds to the column in the schedule

        // File structure
        //  0  - Event Indicator
        //  1  - Event Name
        //  2  - Event Start time
        //  3  - Events date
        //  4  - Event day
        //  5  - Recurrance identifier (-1: Weekly, -2: Daily)

        var tempName;
        var tempStartTime;
        var tempDay;

        for (var index = 0; index < fileContents.length; index++) {
            // Check for Event name (index % 5 = 1)
            if (index % 6 == 1){
                tempName = fileContents[index]
            }

            // Check for Event startTime (index % 5 = 2)
            if (index % 6 == 2) {
                tempStartTime = fileContents[index]
            }

            // Check for Event Day (index % 5 = 4)
            if (index % 6 == 4) {
                tempDay = convertDay(fileContents[index])
            }
            if (index % 6 == 5) {
                // Add Name to correct positon in array
                if (fileContents[index] == -2) {
                    // For daily events add in a loop
                    for (var i = 0; i < 7; i++) {
                        scheduleArray[i][tempStartTime] = tempName;
                    }
                }
                // Regular events
                else{
                    scheduleArray[tempDay][tempStartTime] = tempName;
                }
            }
        }
    }

    function convertDay(day){
    // This will take in the rrule 'BYDAY' value and return an index that will be used
    // in the schedule matrix
        switch(day){
            case "BYDAY=MO":
                return 1
            case "BYDAY=TU":
                return 2
            case "BYDAY=WE":
                return 3
            case "BYDAY=TH":
                return 4
            case "BYDAY=FR":
                return 5
            case "BYDAY=SA":
                return 6
            case "BYDAY=SU":
                return 0
            default:
                alert("Something went wrong coverting dates into indexes.")
        }
    }

    function stripGenre(string){
        var newString = string.replace(/\(.*?)/,'')
        return newString
    }

    function fontSizing(length){
        switch (true) {
            case (length <= 20) :
                return 6
            case (length > 20 && length <= 30):
                return 4.2
            case (length > 30):
                return 3.5
            default:
                alert("Something went wrong sizing text font!")
                return 0
        }
    }