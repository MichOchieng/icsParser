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
    // Add text
    drawTextContainer();
    addText("test","1");

    // Save
    myDoc.exportFile(File('~/Documents/scripts/schedule.png'),ExportType.PNG24);


// ----------- Functions -----------

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
