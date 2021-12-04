// ----------- Main Contents -----------

// Constants
    var file = File('~/Documents/icsParser/scripts/example.txt');
    file.open('r');

// File creation and document setup
    if(!app.homeScreenVisible){
        // Overwrite
        app.activeDocument.close(SaveOptions.DONOTSAVECHANGES); // Temporary, closes previous document window on load
    }
    var myDoc    = app.documents.add();
    //for (var index = 0; index < 4; index++) {
        //alert(file.readln());
    //}
    myDoc.layers[0].name = "Background Layer";

// Render Schedule elements
    drawGridLines(36,10,576,10,24,20,0);
    drawGridLines(36,10,36,740,6,72,1);

    // Save
    myDoc.exportFile(File('~/Documents/scripts/schedule.png'),ExportType.PNG24);


// ----------- Functions -----------

    function drawGridLines(initialX,initialY,initialX2,initialY2,maxLine,offset,axis){
        // Variables
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

    function drawTextContainer(){
        var doc           = app.activeDocument;
        var rectangle     = doc.pathItems.add();
        rectangle.stroked = true;
        // Draws a rectangle by connecting the points bellow
        rectangle.setEntirePath(
            [
                [
                    71.69,719  // Bottom left corner
                ],
                [
                    540.31,719 // Bottom right corner
                ],
                [
                    540.31,73  // Top left corner
                ],
                [
                    71.69,73   // Top right corner
                ],
                [
                    71.69,719  // Bottom left corner
                ]
            ]
        )
    }

    function addText(text,eventNum){
        var doc       = app.activeDocument;
        var txtFrame  = doc.textFrames.add();
        var txtRange  = txtFrame.textRange;
        // Input file contents
        txtFrame.contents = text; // DONT FORGET 's' AT THE END OF CONTENTS!!!
        txtFrame.name    = "scheduleEvent" + eventNum;
        txtRange.size    = 14; // Should scale to # of events
        txtFrame.position = [ // Should be scalable
            (75.69),
            (724)
        ]
        
    }
