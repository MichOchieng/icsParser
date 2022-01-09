// ----------- Main Contents -----------

// Constants
    var parseFile = File('~/Documents/icsParser/scripts/example.txt');
    parseFile.open('r');

// Open calendar file
    var filePath = "~/Documents/cfur/adobeScripts/icsParser/scripts/timeTableTest.ai"; // Replace with correct path on your machine
    var file = File(filePath);
    file.open('r');
    app.open(file);

// Add text to calendar file
    fillSchedule();

// Save PNG of Schedule
    //myDoc.exportFile(File('testSchedule.png'),ExportType.PNG24);


// ----------- Functions -----------
    // Currently only adds boilerplate text
    function fillSchedule(){
        for (var i = 0; i < 7; i++) {  // Row

            for (var j = 0; j < 24; j++) {   // Column
                var doc = app.activeDocument; // Targets the opened file as the working document
                var txtFrame = doc.textFrames.add();
                var txtRange = txtFrame.textRange;
        
                var posX     = 127;
                var posY     = -156; // Negative because Y values are flipped in illustrator
                var offSetY  = 14.2;
                var offsetX  = 63;
        
                txtFrame.contents = "text"; // DONT FORGET 's' AT THE END OF CONTENTS!!!
                txtRange.size    = 8;
                txtFrame.position = [
                    (posX + (i*offsetX)), // Offsets used to place in the correct row
                    (posY - (j*offSetY))  // Subtracting from posY due to flipped values
                ];   
                // Center align text in frame
                // Must go after setting position otherwise wont work
                txtRange.justification = Justification.CENTER;
            }
        }
    }

    function parseFile(){
    
    }

    function convertDay(day){
    // This will take in the rrule 'BYDAY' value and return an index that will be used
    // in the schedule matrix
        switch(day){
            case "BYDAY=MO":
                return 0
            case "BYDAY=TU":
                return 1
            case "BYDAY=WE":
                return 2
            case "BYDAY=TH":
                return 3
            case "BYDAY=FR":
                return 4
            case "BYDAY=SA":
                return 5
            case "BYDAY=SU":
                return 6
            default:
                alert("Something went wrong coverting dates into indexes.")
        }
    }

    function drawGridLines(initialX,initialY,initialX2,initialY2,maxLine,offset,axis){
        // Params
            // initial(X,Y): Starting coordinate position for the first line in the loop
            // maxLine: The maximum numberof lines being generated
            // offset: Determines how the lines are spaced
            // axis: A value of 0 will result in the x axis being generated while 1 generates the y

        var doc = app.activeDocument;

        // Draws grid lines from the given start location
        for (var index = 0; index < maxLine; index++) {
            var line     = doc.pathItems.add();
            line.stroked = true;
            if (axis == 0) {
                line.name    = 'xLine' + index;
                // Creates a single line with the given coordinates 
                line.setEntirePath(
                    [
                        [
                            initialX,(initialY + offset)
                        ],
                        [
                            initialX2,(initialY2 + offset)
                        ]
                    ]
                )
                offset+=30;
            }
            else if (axis == 1) {
                line.name    = 'yLine' + index;
                // Creates a single line with the given coordinates
                line.setEntirePath(
                    [
                        [
                            (initialX + offset),initialY
                        ],
                        [
                            (initialX2 + offset),initialY2
                        ]
                    ]
                )
                offset+=81;
            }else{
                alert("Incorrect input for axis variable in drawGridLines function!")
            }
        }
    }

    function addTimes(initialX,initialY,offset){
        for (var index = 0; index < 25; index++) {
            addText(initialX,initialY + offset);
            offset+=30;
        }
    }
    
    function addText(posX,posY){
        var doc       = app.activeDocument;
        var txtFrame  = doc.textFrames.add();
        var txtRange  = txtFrame.textRange;
        // Input file contents
        txtFrame.contents = "text"; // DONT FORGET 's' AT THE END OF CONTENTS!!!
        txtRange.size    = 14;
        txtFrame.position = [
            posX,
            posY
        ]
    }
