from string import Template
from PIL import Image, UnidentifiedImageError
import numpy as np

templateString = Template(
"""#ifndef $MACRO_GUARD
#define $MACRO_GUARD

#include $ICON_HEADER_PATH
    
const Icon STATIC_SECTION $ARRAY_NAME = {$ICON_WIDTH, $ICON_HEIGHT, (const uint8_t[]){$ICON_DATA}};
    
#endif"""
) 

def LoadImage(fileName):
    try:
        iconImage = Image.open(fileName)
    except (FileNotFoundError, UnidentifiedImageError):
        print("error opening image file")
        return None

    return iconImage

def ChangeColorDepth(iconIm):
    if iconIm != None:
        return iconIm.quantize(4)

    return None
    
def StringifyArray(grayscaleArrayFlat):
    returnString = ""
    for i in grayscaleArrayFlat:
        returnString += str(hex(i) + ", ")

    return returnString[:-2]

def ImageToArray(fileName, outputFileName, headerPath, arrayName):
    grayscaleImage = ChangeColorDepth(LoadImage(fileName=fileName))
    grayscaleImageArray = np.asarray_chkfinite(grayscaleImage)
    grayscaleImageArrayFlat = grayscaleImageArray.flatten()
    grayscaleImageArrayFlatString = StringifyArray(grayscaleImageArrayFlat)

    outputString = templateString.substitute(
        MACRO_GUARD=outputFileName.upper() + "_H",
        ICON_HEADER_PATH=headerPath,
        ARRAY_NAME=arrayName,
        ICON_WIDTH=grayscaleImage.size[0],
        ICON_HEIGHT=grayscaleImage.size[1],
        ICON_DATA=grayscaleImageArrayFlatString
    )

    print(outputString)

if __name__ == "__main__":
    ImageToArray("test.jpg", "diamond", "../../UI/Widgets/Icon.h", "diamond")
    
