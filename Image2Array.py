from string import Template
from more_itertools import grouper
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import cairosvg
import numpy as np
import argparse
from Template import templateString

def LoadImage(fileName):
    try:
        outBytes = fileName
        if fileName.find(".svg") != -1:
            outBytes = BytesIO()
            cairosvg.svg2png(url=fileName, write_to=outBytes)

        iconImage = Image.open(outBytes)
    except (FileNotFoundError, UnidentifiedImageError):
        print("error opening image file")
        raise SystemExit
        return None

    return iconImage

def ChangeColorDepth(iconIm):
    if iconIm != None:
        return iconIm.quantize(4)

    return None
    
def SquashBits(grayscaleArrayFlat):
    squashedArray = []
    for bitLeftMost, bitLeftMiddle, bitRightMiddle, bitRightMost in grouper(4, grayscaleArrayFlat, 0):
        squashedArray.append(bitLeftMost << 6 | bitLeftMiddle << 4 | bitRightMiddle << 2 | bitRightMost)

    return np.array(squashedArray)

def StringifyArray(grayscaleArrayFlat):
    returnString = ""
    for i in grayscaleArrayFlat:
        returnString += str(hex(i) + ", ")

    return returnString[:-2]

def Image2Array(fileName, outputFileName="ImageHeader", headerPath="../../UI/Widgets/Icon.h", arrayName="ImageArray", templateString=templateString):
    grayscaleImage = ChangeColorDepth(LoadImage(fileName=fileName))
    grayscaleImageArray = np.asarray_chkfinite(grayscaleImage)
    grayscaleImageArrayFlat = SquashBits(grayscaleImageArray.flatten())
    grayscaleImageArrayFlatString = StringifyArray(grayscaleImageArrayFlat)

    outputString = templateString.substitute(
        MACRO_GUARD=''.join(filter(str.isalpha, outputFileName.upper())) + "_H",
        ICON_HEADER_PATH=headerPath,
        ARRAY_NAME=arrayName,
        ICON_WIDTH=grayscaleImage.size[0],
        ICON_HEIGHT=grayscaleImage.size[1],
        ICON_DATA=grayscaleImageArrayFlatString
    )

    with open(outputFileName + ".h", "w+") as fileHandle:
        fileHandle.write(outputString)
        fileHandle.close()

if __name__ == "__main__":
    argParse = argparse.ArgumentParser(description='Convert image files to C header files')
    argParse.add_argument("-i", "--input", required=True, help="Specify the path of input image", type=str)
    argParse.add_argument("-o", "--output", default="ImageHeader", help="Specify the name of output .h file (don't write .h to the end)", type=str)
    argParse.add_argument("--header", default="../../UI/Widgets/Icon.h", help="Path of include header for icon struct", type=str)
    argParse.add_argument("--array_name", default="ImageArray", help="Specify the name of output array in header file", type=str)
    argsParsed = argParse.parse_args()

    Image2Array(argsParsed.input , argsParsed.output, argsParsed.header, argsParsed.array_name)
    
