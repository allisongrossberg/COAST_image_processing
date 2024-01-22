######## NFKB Analysis #######
    if nfkb_staining == True:
        nfkbChannelName = "C4-" + originalFileName

        # Save the non-duplicated image as TIFF with the overlay
        IJ.selectWindow(nfkbChannelName)
        print("1")
        IJ.run("Set Measurements...", "mean standard min max limit redirect=[C4-" + originalFileName + "] decimal=2")
        IJ.run("Analyze Particles...", "size=10.00-Infinity circularity=0.50-1.00 show=Outlines display summarize overlay composite add")
        IJ.run("Measure")
        print("2")

        # Save the results to a different CSV file
        IJ.selectWindow("Results")
        for i in indexes:
            IJ.runMacro('setResult("Image File", {0}, "C4-" + "{1}" + "")'.format(i, originalFileName))
        print("3")
        IJ.saveAs("Results", output + originalFileNameWithoutExtension + "-NFkB_Results.csv")
        IJ.run("Clear Results")
        print("4")
        IJ.selectWindow(originalFileName)
        imp = IJ.getImage()
        print("5")
        rm = RoiManager.getInstance()
        IJ.run("Colors...", "channels=1 slices")
        rm.runCommand(imp, "Show All")
        print("6")
        IJ.run("Make Composite")
        print("7")
        IJ.saveAs("Tiff", output + originalFileNameWithoutExtension + "-NFkB_Composite_Image_With_ROI.tif")
