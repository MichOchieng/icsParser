// Create new file
if(!app.homeScreenVisible){
    // Overwrite
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES); // Temporary, closes previous document window on load
}
const myFile = "example.txt";
var myDoc    = app.documents.add();
var text     = "testing"


myDoc.layers[0].name = "Background Layer";

// Draw triangle
triangle();

// Add text
addText(text);

// Save
myDoc.exportFile(File('~/Documents/scripts/schedule.png'),ExportType.PNG24);

function triangle() {
    var doc      = app.activeDocument;
    var triangle = doc.pathItems.add();
    triangle.stroked = true; // visable
    triangle.setEntirePath(
        [
            [doc.width/2,25],
            [25,doc.height-25],
            [doc.width-25,doc.height-25],
            [doc.width/2,25]
        ]
    );
}

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
