##############
# Daniel Jaffe
# Date Made 11/23/24
# todo what does this program do
##############

# Imports
from PIL import Image


# TODO
# performs Lempel-Ziv Algorithm
class lempelZivAlgorithm:
    def __init__(self,binaryStr):
        self.binaryStr = binaryStr


    def tableOfContents(self):
        tableOfContents = []
        tableOfContents.append(self.getUniqueSubstring())
        tableOfContents.append(self.getConvertedSubstring())
        return(tableOfContents)


    # converts the bit string into a unique array of different substrings
    def getUniqueSubstring(self):
        arraySubstrings = []
        substring = ""
        for i in range(0,len(self.binaryStr)):
            substring += self.binaryStr[i]
            if substring not in arraySubstrings:
                arraySubstrings.append(substring)
                substring = ""
        return (arraySubstrings)

    #TODO
    def getConvertedSubstring(self):
        newArray = []
        uniqueSubstring = self.getUniqueSubstring()
        for num in uniqueSubstring:
            # appends every thing but last character
            newArray.append(num[:-1])
        convertedSubstringArray = []
        # go throught all numbers in the new array
        for num in newArray:
            #if nothing in string append to converted substring
            if num == "":
                convertedSubstringArray.append("")
            # otherwise go through the unique substring to find the number that is in new array
            else:
                if num in uniqueSubstring:
                    found = False
                    i = 0
                    while found == False:
                        # if the number is found append index + 1 new Converted Substring array
                        if num == uniqueSubstring[i]:
                            convertedSubstringArray.append(str(i+1))
                            found = True
                        i +=1
        # go through the entire converted substring Array
        # then append the last number in the unique substring to the end of the converted substring
        for i in range (0,len(convertedSubstringArray)):
            lastNumber = (uniqueSubstring[i])[-1]
            convertedSubstringArray[i]+=lastNumber
        return (convertedSubstringArray)

    #TODO
    def encodedMessage(self):
        pass

    #TODO
    def tableOutput(self):
        print("Unique Substrings")
        print(self.tableOfContents()[0])
        print("Converted Substrings")
        print(self.tableOfContents()[1])

# converts pixels to binary and returns all concatenated together
def convertPixelsValueToBinary(pixelsValue):
    i = 0
    pixelsInBinary = ""
    while i < len(pixelsValue):
        pixelValue = pixelsValue[i]
        binaryVal = bin(pixelValue)
        binaryVal = binaryVal[2:]
        pixelsInBinary += binaryVal
        i += 1
    return pixelsInBinary

# this takes all pixels and converts from RGB numbers to bits
def convertRGBToBits(pixels,endingWidth,endingHeight):
    pixelsInBinary = "10"
    currentHeight = 0
    # loop through the entire picture
    while currentHeight < endingHeight:
        currentWidth = 0
        while currentWidth < endingWidth:
            pixelsValue = pixels[currentWidth, currentHeight]
            # convert pixels to binary and concatenate all value to the string
            pixelsInBinary += convertPixelsValueToBinary(pixelsValue)
            currentWidth += 1
        currentHeight += 1
    return pixelsInBinary
# Main
# used https://www.thecoderscamp.com/how-to-read-bmp-file-in-python/ to find how to open a image file
image = Image.open("3x4.bmp")
pixels = image.load()

endingWidth, endingHeight = image.size
print(endingWidth, endingHeight)
entireImageConvertToBinary =convertRGBToBits(pixels,endingWidth,endingHeight)

algorithm =lempelZivAlgorithm(entireImageConvertToBinary)
print(algorithm.tableOutput())
