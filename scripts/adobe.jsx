// ----------- Main Contents -----------

// Constants
    const myFile = "example.txt";

// File creation and document setup
    if(!app.homeScreenVisible){
        // Overwrite
        app.activeDocument.close(SaveOptions.DONOTSAVECHANGES); // Temporary, closes previous document window on load
    }
    var myDoc    = app.documents.add();
    var text     = "test";
    myDoc.layers[0].name = "Background Layer";
    
// Render Schedule elements
  
    // Add text
    addText(text);

    // Save
    myDoc.exportFile(File('~/Documents/scripts/schedule.png'),ExportType.PNG24);


// ----------- Functions -----------

    function addText(text){
        var doc       = app.activeDocument;
        var txtFrame  = doc.textFrames.add();
        var txtRange  = txtFrame.textRange;
        // Input file contents
        txtFrame.contents = text; // DONT FORGET 's' AT THE END OF CONTENTS!!!
        txtFrame.name    = "My Text";
        txtRange.size    = 36;
        txtFrame.position = [
            ((doc.width * 0.5) - (txtFrame.width * 0.5)),
            ((doc.height * 0.5) + (txtFrame.width * 0.5))
        ]
        
    }
