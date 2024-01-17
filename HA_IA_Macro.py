import os

from ij import IJ, WindowManager
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
#remove the first member of the files list
files.pop(0)
for file in files:
    IJ.run("Bio-Formats Importer", "open=[" + input + file + "]" + DEFAULT_OPTIONS)

    # Get the original file name without extension
    originalFileName = os.path.basename(file)
    originalFileNameWithoutExtension = os.path.splitext(originalFileName)[0]
    originalFilePath = input + originalFileName
    
    # #######DAPI Count 
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
        IJ.runMacro('setResult("Image File", {0}, "{1}")'.format(i, blueChannelName))
    
    # Open the Image as a Composite
    IJ.run("Bio-Formats Importer", "open=[" + input + file + "]" + COMPOSITE_OPTIONS)

    # Create a composite image with the GFAP ROI overlay on all three channels
    IJ.selectWindow(originalFileName)
    imp = IJ.getImage()
    rm = RoiManager.getInstance()
    IJ.run("Colors...", "channels=1 slices")
    rm.runCommand(imp, "Show All")
    IJ.run("Make Composite")

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
    IJ.runMacro("""roiManager("Add")""")
    rm.runCommand("Save", output + originalFileNameWithoutExtension + "-DAPI_RoiSet.zip")

    # Save the non-duplicated image as TIFF with the overlay
    IJ.selectWindow(blueChannelName)
    IJ.saveAs(imp, "Tiff", output + originalFileName)

    IJ.run("Set Measurements...", "area mean standard min max perimeter shape limit redirect=[duplicate_C1-" + originalFileName + "] decimal=2")
    IJ.run("Analyze Particles...", "size=10.00-Infinity circularity=0.50-1.00 show=Outlines display summarize overlay composite add")
    IJ.run("Measure")

    # Save the results to a different CSV file
    IJ.selectWindow("Results")
    for i in indexes:
        IJ.runMacro('setResult("Image File", {0}, "duplicate_C1" + "{1}" + "")'.format(i, originalFileName))

    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-DAPI_Duplicate_Image_Results.csv")
    IJ.run("Clear Results")

    #reset the ROI manager
    rm.reset()

    # Duplicating GFAP Channels for Downstream Analysis
    # Select the GFAP channel (assuming it's the green channel)
    IJ.selectWindow(greenChannelName)
    
    # Specify the name for the duplicated image
    duplicateTitle = "duplicate_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle)
    
    # Select the GFAP channel (assuming it's the green channel)
    IJ.selectWindow(greenChannelName)
    
    # Create a Second Duplicate
    duplicateTitle2 = "duplicate_2_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle2)
    
    # Select the GFAP channel (assuming it's the green channel)
    IJ.selectWindow(greenChannelName)
    
    # Create a Second Duplicate
    duplicateTitle3 = "duplicate_3_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle3)
    
    # Create a Second Duplicate
    duplicateTitle4 = "duplicate_4_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle4)
    
    # Create a Second Duplicate
    duplicateTitle5 = "duplicate_5_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle5)
    
    # Create a Second Duplicate
    duplicateTitle6 = "duplicate_6_" + greenChannelName
    
    # Duplicate the green channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitle6)

    ######### Mean Flourescence Intensity (MFI) for Green Channel
			
    # Select the first duplicate
    IJ.selectWindow(duplicateTitle)
    # Increase brightness/contrast of the non-duplicated image with normalization
    IJ.run("Enhance Contrast...", "saturated=1 normalize")
    
    # Preprocess the image with Gaussian Blur
    IJ.run("Gaussian Blur...", "sigma=2")
    
    # Remove the backgroung using Rolling Ball Subtraction 
    IJ.run("Subtract Background...", "rolling=50")
    
    # Threshold and Convert to Mask
    IJ.setAutoThreshold(imp, "Default dark no-reset")
    IJ.runMacro("""setOption("BlackBackground", true)""")
    IJ.run("Convert to Mask")
    
    IJ.run("Set Measurements...", "area mean standard min max limit redirect=[duplicate_2_C2-" + originalFileName + "] decimal=2")
    IJ.run("Measure")
    
    # Save Summary data from results
    IJ.selectWindow("Results")
    # change Image File to be the name of the file in all rows
    IJ.runMacro('setResult("Image File", {0}, "duplicate_2_C2-" + "{1}" + "")'.format(0, originalFileName))
    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension +"-GFAP_MFI_Results.csv")
    #Clear the results Table
    IJ.run("Clear Results")

    ######### Mean Flourescence Intensity (MFI) for Red Channel 
			
    # Select the Vimentin channel (assuming it's the red channel)
    IJ.selectWindow(redChannelName)
    # Specify the name for the duplicated image
    duplicateTitleRed = "duplicate_" + redChannelName
    # Duplicate the red channel with the specified title
    IJ.run("Duplicate...", "title=" + duplicateTitleRed)
    
    # Select the original (non-duplicated) version
    IJ.selectWindow(redChannelName)
    
    # Increase brightness/contrast of the non-duplicated image with normalization
    IJ.run("Enhance Contrast...", "saturated=1 normalize")

    # Preprocess the image with Gaussian Blur
    IJ.run("Gaussian Blur...", "sigma=2")
    
    # Remove the backgroung using Rolling Ball Subtraction 
    IJ.run("Subtract Background...", "rolling=50")
    
    # Threshold and Convert to Mask
    IJ.setAutoThreshold(imp, "Default dark no-reset")
    IJ.runMacro("""setOption("BlackBackground", true)""")
    IJ.run("Convert to Mask")
    
    IJ.run("Set Measurements...", "area mean standard min max limit redirect=[duplicate_C3-" + originalFileName + "] decimal=2")
    IJ.run("Measure")
    
    # Save Summary data from results
    IJ.selectWindow("Results")

    # change Image File to be the name of the file in all rows
    IJ.runMacro('setResult("Image File", {0}, "duplicate_C3-" + "{1}" + "")'.format(0, originalFileName))

    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-Vimentin_MFI_Results.csv")
    
    #Clear the results Table
    IJ.run("Clear Results")

    ######### Cell Area Measurements - GFAP 
			
    # Select the second duplicate of the green channel
    IJ.selectWindow(duplicateTitle3)
    imp = IJ.getImage()

    # Increase brightness/contrast of the non-duplicated image
    IJ.run("Enhance Contrast...", "saturated=0 normalize")
                
    # Preprocess the image with Gaussian Blur
    IJ.run("Gaussian Blur...", "sigma=8")
    
    # Remove the background using Rolling Ball Subtraction 
    IJ.run("Subtract Background...", "rolling=52")
    IJ.run("Bandpass Filter...", "filter_large=85 filter_small=20 suppress=None tolerance=5 autoscale saturate")
    IJ.run("Despeckle")
    IJ.run("Maximum...", "radius=3")
    IJ.run("Remove Outliers...", "radius=2 threshold=50 which=Bright")
    
    # Preprocess the image with Gaussian Blur
    IJ.run("Gaussian Blur...", "sigma=1")
    
    # Threshold and Convert to Mask
    # minThresholdValue = 150
    IJ.setAutoThreshold(imp, "MaxEntropy dark no-reset")
    # IJ.setThreshold(minThresholdValue, 255)
    IJ.runMacro("""setOption("BlackBackground", true)""")

    IJ.run("Convert to Mask")
    IJ.run("Despeckle")
    IJ.run("Close-")
    IJ.run("Dilate")
    IJ.run("Watershed")
    # Post-processing
    IJ.run("Fill Holes")
    IJ.run("Close-")
    
    IJ.run("Set Measurements...", "area mean standard min perimeter shape integrated skewness limit redirect=[None] decimal=2")
    IJ.run("Analyze Particles...", "size=60.00-Infinity circularity=0.00-1.00 show=Outlines display summarize overlay add composite")
    IJ.run("Measure")
    
    # Get the number of ROIs in the ROI Manager
    rm = RoiManager.getInstance()
    nROIs = rm.getCount()
    print(nROIs)
    indexes = range(0, nROIs+1)
    print(indexes)
    
    # Fill the array with ROI indices
    # Add image name to results table
    IJ.selectWindow("Results")
    # change Image File to be the name of the file in all rows    
    for i in indexes:
        IJ.runMacro('setResult("Image File", {0}, "{1}")'.format(i, greenChannelName))
    
    # Save the results to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-GFAP_Cell_Count_Results.csv")
    
    # Save Summary data from results
    IJ.selectWindow("Summary")
    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-GFAP_Count_Summary.csv")
    # Clear the results Table
    IJ.run("Clear Results")
    
    # Save ROIs
    rm.setSelectedIndexes(indexes)
    IJ.runMacro("""roiManager("Add")""")
    rm.runCommand("Save", output + originalFileNameWithoutExtension + "-GFAP_RoiSet.zip")

    # Save the non-duplicated original image as TIFF with the overlay
    IJ.selectWindow(duplicateTitle3)
    IJ.saveAs("Tiff", output + originalFileNameWithoutExtension + "-greenChannel_with_ROI.tif")
    
    IJ.run("Set Measurements...", "area mean standard min max perimeter shape limit redirect=[duplicate_4_C2-" + originalFileName + "] decimal=2")
    IJ.run("Analyze Particles...", "size=60.00-Infinity circularity=0.00-1.00 show=Outlines display summarize overlay add composite")
    IJ.run("Measure")

    # Save the results to a different CSV file (replace with your desired file path)
    IJ.selectWindow("Results")
    # change Image File to be the name of the file in all rows
    for i in indexes:
        IJ.runMacro('setResult("Image File", {0}, "duplicate_4_C2-" + "{1}"+ "")'.format(i, originalFileName))
    
    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-GFAP_Duplicate_Image_Results.csv")

    #Clear the results Table
    IJ.run("Clear Results")
    
    # Create a composite image with the GFAP ROI overlay on all three channels
    IJ.run("Bio-Formats Importer", "open=[" + input + file + "]" + COMPOSITE_OPTIONS)
    
    IJ.selectWindow(originalFileName)
    imp = IJ.getImage()
    rm = RoiManager.getInstance()
    IJ.run("Colors...", "channels=1 slices")
    rm.runCommand(imp, "Show All")
    IJ.run("Make Composite")

    # Save the composite image as TIFF with the overlay
    IJ.saveAs("Tiff", output + originalFileNameWithoutExtension + "-GFAP_Composite_Image_With_ROI.tif")
    # Clear the ROI Manager
    rm.reset()

    ######### Cell Branching Measurements - GFAP 
    
    # Select the fifth duplicate of the green channel
    IJ.selectWindow(duplicateTitle5)
                
    IJ.run("Bandpass Filter...", "filter_large=85 filter_small=8 suppress=None tolerance=5 autoscale saturate")
    
    IJ.run("Despeckle")
    IJ.run("Sharpen")
    IJ.run("Grays")
    IJ.run("Unsharp Mask...", "radius=35 mask=0.75")
    IJ.run("Despeckle")
    IJ.run("Remove Outliers...", "radius=2 threshold=50 which=Bright")
    
    IJ.setAutoThreshold(imp, "MaxEntropy dark no-reset")
    IJ.runMacro("""setOption("BlackBackground", true)""")

    IJ.run("Convert to Mask")
    IJ.run("Despeckle")
    IJ.run("Close-")
    IJ.run("Remove Outliers...", "radius=3 threshold=50 which=Bright")
    
    IJ.run("Skeletonize")
    IJ.run("Analyze Skeleton (2D/3D)", "prune=none show display")
    
    IJ.selectWindow("Results")
    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-GFAP_Skeleton_Results.csv")
    
    IJ.selectWindow("Branch information")
    # Save the Summary to a CSV file (replace with your desired file path)
    IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-GFAP_Skeleton_Branch_Info.csv")
    
    # Save the images
    IJ.selectWindow("Tagged skeleton")
    IJ.saveAs("Tiff", output + originalFileNameWithoutExtension + "-Tagged_Skeletons.tif")
    
    IJ.selectWindow(duplicateTitle6)
    IJ.run("8-bit")
    skelestring = " c2=" + originalFileNameWithoutExtension + "-Tagged_Skeletons.tif create"
    IJ.run("Merge Channels...", "c1=duplicate_6_C2-" + originalFileName + skelestring)
    IJ.saveAs("Tiff", output + originalFileNameWithoutExtension + "-GFAP_Tagged_Skeletons_Overlay.tif")
    
    # Clear the results Table
    IJ.run("Clear Results")

    # Clear All Windows 
    # Images
    IJ.run("Close All")
    # Tables
    window_list = WindowManager.getNonImageWindows()
    # print(window_list[1].title)
    for window in window_list:
        IJ.selectWindow(window.title)
        IJ.run("Close")
