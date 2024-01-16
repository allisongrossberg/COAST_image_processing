import os

from ij import IJ, Macro
from ij.plugin.frame import RoiManager  



# IJ.log("Hello, ImageJ!")
# Set input and output folders
input = "/Users/allisongrossberg/Desktop/Test_Input_Folder/"
output = "/Users/allisongrossberg/Desktop/Test_Output_Folder/"
# Get list of files
all_files = os.listdir(input)
files = [file for file in all_files if file.endswith(".oir")]

DEFAULT_OPTIONS = "open=[Bio-Formats] color_mode=Default view=Hyperstack"
COMPOSITE_OPTIONS = "open=[Bio-Formats] color_mode=Composite view=Hyperstack"

for file in files:
    IJ.run("Bio-Formats Importer", "open=[" + input + file + "]" + DEFAULT_OPTIONS)

    # Get the original file name without extension
    originalFileName = os.path.basename(file)
    originalFileNameWithoutExtension = os.path.splitext(originalFileName)[0]
    originalFilePath = input + originalFileName
    
    # DAPI Count 
    IJ.run("Set Scale...", "distance=1 known=0.311 unit=micron global")

    # Split Channels
    IJ.selectWindow(originalFileName)
    IJ.run("Split Channels")

    # Specify the names for each channel
    blueChannelName = "C1-" + originalFileName
    greenChannelName = "C2-" + originalFileName
    redChannelName = "C3-" + originalFileName

    # Select the DAPI channel (blue channel)
    IJ.selectWindow(blueChannelName)

    # Duplicate and specify the name for the duplicated image
    duplicateTitle = "duplicate_" + blueChannelName

    # Duplicate the blue channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle)

    # Select the original (non-duplicated) version
    IJ.selectWindow(blueChannelName)
    imp = IJ.getImage()
    
    # Preprocess the image with Gaussian Blur
    IJ.run("Gaussian Blur...", "sigma=2")
    IJ.run("Gamma...", "value=0.5")
    IJ.run("Max...", "value=1500")

    IJ.setAutoThreshold(imp, "Default dark no-reset")
    IJ.runMacro("""setOption("BlackBackground", true)""")
    IJ.run("Convert to Mask")
    IJ.run("Watershed")

    # Initial Measurements
    IJ.run("Set Measurements...", "area mean standard min max perimeter shape limit redirect=[None] decimal=2")
    IJ.run("Analyze Particles...", "size=10.00-Infinity circularity=0.50-1.00 show=Outlines display summarize overlay composite add")
    IJ.run("Measure")

    # Get the number of ROIs in the ROI manager
    rm = RoiManager.getInstance()
    nROIs = rm.getCount()
    indexes = range(0, nROIs+1)
    # Add image name to results table
    IJ.selectWindow("Results")
    for i in indexes:
        IJ.runMacro('setResult("Image File", {0}, "{1}");'.format(i, blueChannelName))
    
    # Open the Image as a Composite
    IJ.run("Bio-Formats Importer", "open=[" + input + file + "]" + COMPOSITE_OPTIONS)

    # Create a composite image with the GFAP ROI overlay on all three channels
    IJ.selectWindow(originalFileName)
    imp = IJ.getImage()
    rm = RoiManager.getInstance()
    IJ.run("Colors...", "channels=1 slices")
    rm.runCommand(imp, "Show All")
    IJ.run("Make Composite");

    # Save the composite image as TIFF with the overlay
    IJ.saveAs(imp, "Tiff", output + originalFileName)

    # Save the results to a csv file
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-DAPI_Count_Results.csv")

    # Save summary data from results
    IJ.selectWindow("Summary")
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-DAPI_Count_Summary.csv")

    # Clear the Results Table
    IJ.run("Clear Results")

    # Save ROIs
    rm.setSelectedIndexes(indexes)
    rm.runCommand(imp, "Add")
    rm.runCommand("Save", output + originalFileNameWithoutExtension + "-DAPI_RoiSet.zip")

    # Save the non-duplicated image as TIFF with the overlay
    IJ.selectWindow(blueChannelName)
    imp = IJ.getImage()
    rm = RoiManager.getInstance()
    rm.runCommand(imp, "Show All")
    IJ.run("Colors...", "channels=1 slices")
    IJ.run("Make Composite")
    IJ.saveAs(imp, "Tiff", output + originalFileName)

    IJ.run("Set Measurements...", "area mean standard min max perimeter shape limit redirect=[duplicate_C1-" + originalFileName + "] decimal=2");
    IJ.run("Analyze Particles...", "size=10.00-Infinity circularity=0.50-1.00 show=Outlines display summarize overlay composite add");
    IJ.run("Measure");

    # Save the results to a different CSV file
    IJ.selectWindow("Results")
    for i in indexes:
        IJ.runMacro('setResult("Image File", {0}, "duplicate_C1" + "{1}" + "");'.format(i, originalFileName))

    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-DAPI_Duplicate_Image_Results.csv")
    IJ.run("Clear Results")

    #reset the ROI manager
    rm.reset()

    

    print("Done!")
    exit(1)

