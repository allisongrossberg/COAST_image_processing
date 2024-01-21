from ij import IJ
from loci.plugins import BF
from ij.io import FileInfo

import os

file = "/Users/allisongrossberg/Desktop/Confocal_Images_for_Analysis_Duplicated/COAST_HA_9_17_23_TLR_Exp_1/COAST_HA_YCH_Untr._2_15.oir"

# Open the file
IJ.run("Bio-Formats Importer", "open=[" + file + "]")

originalFileName = os.path.basename(file)
originalFileNameWithoutExtension = os.path.splitext(originalFileName)[0]
#extract metadata
IJ.selectWindow(originalFileName)
imp = IJ.getImage()
print(imp.getDimensions())

file_info = imp.getOriginalFileInfo()
print(file_info)
