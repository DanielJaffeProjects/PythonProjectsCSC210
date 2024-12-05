##############
# Daniel Jaffe
# Date Made 11/23/24
# Compresses an image's pixel data using the Lempel-Ziv algorithm and outputs the compressed binary message.
##############

# Imports
from PIL import Image
import math

# performs Lempel-Ziv Algorithm
class lempelZivAlgorithm:
    def __init__(self,binaryStr):
        self.binaryStr = binaryStr
        self.uniqueSubstring = None
        self.convertedSubstring = None
        self.encodedMessage = None
        self.RGB =None

    # converts the bit string into a dictionary of different substrings
    # had to change this up to make faster by using sets
    def getUniqueSubstring(self):
        substringsArray = []
        seenSet = set()
        substring = ""
        i = 0
        length = len(self.binaryStr)
        while i <length:
            substring += self.binaryStr[i]
            if substring not in seenSet:
                substringsArray.append(substring)
                seenSet.add(substring)
                substring = ""
            i+=1
        # if the substring still has stuff in it add it to the substring array
        if substring != "":
            substringsArray.append(substring)
        self.uniqueSubstring = substringsArray


    # encodes substrings by taking there prefix and converting to their indices in the unique list
    def getConvertedSubstring(self):
        newArray = []

        for num in self.uniqueSubstring:
            # appends every thing but last character
            newArray.append(num[:-1])
        convertedSubstringArray = []
        # used chatgpt to make this more efficient
        # Create a dictionary mapping prefixes to their indices
        prefix_to_index = {}
        for i in range (0, len(newArray)):
            prefix = newArray[i]
            if prefix == "":
                continue
            if prefix not in prefix_to_index:
                prefix_to_index[prefix] = str(len(prefix_to_index) + 1)

        for num in newArray:
            # Append an empty string if the prefix is empty
            if num == "":
                convertedSubstringArray.append("")
            else:
                #look up what index num is
                convertedSubstringArray.append(prefix_to_index[num])

        for i in range (0,len(convertedSubstringArray)):
            lastNumber = (self.uniqueSubstring[i])[-1]
            convertedSubstringArray[i]+=lastNumber
        self.convertedSubstring = convertedSubstringArray

    # takes the prefix of the converted substring and puts it in binary form
    def getEncodedMessage(self):
        encodedArray = []
        biggestNumber = 0
        for i in range(0,len(self.convertedSubstring)-1):
            num = ((self.convertedSubstring[i])[:-1])
            # if number is nothing make number 0
            if num == "":
                num = 0
            # otherwise just convert the number into an integer
            else:
                num = int(num)
            if num > biggestNumber:
                biggestNumber = num
        # find how many bits the biggest number can be converted to
        bits = math.ceil(math.log2(biggestNumber+1))

        for i in range(0,len(self.convertedSubstring)):
            # if the length is 1 then append the number
            if (len(self.convertedSubstring[i]) == 1):
                encodedArray.append(self.convertedSubstring[i])
            else:
                # the last character in the substring is removed
                number = self.convertedSubstring[i][:-1]
                # convert number to binary
                bitStr = (bin(int(number))[2:])
                # if bitstr does have the same bits as the biggest number add zeros to the front
                if len(bitStr) < bits:
                    difference = bits - len(bitStr)
                    bitStr = ("0" * difference) + bitStr
                encodedArray.append(bitStr)
                # adds the last number to string in the encoded array
                encodedArray[i] += self.convertedSubstring[i][-1]
        self.encodedMessage = "".join(encodedArray)

    def splitEncodedIntoEights(self):
        arrayEncodedMessageEight = []
        i = 0
        while i < len(self.encodedMessage):
            arrayEncodedMessageEight.append(self.encodedMessage[i:(i+8)])
            i+=8
        return(arrayEncodedMessageEight)
    # converts binary into pixels of group 3
    def convertBinaryToPixels(self):
        newPixels = []
        i = 2
        newEncodedMessage = self.splitEncodedIntoEights()
        # sections all the bits into groups of 8 and converts to integer
        while (i < len(newEncodedMessage)):
            newPixels.append(int(newEncodedMessage[i],2))
            i+=1
        newRGB = []
        groupOfThree = []
        j = 0
        # combine number into groups of 3
        while(j< (len(newPixels))):
            groupOfThree.append((int(newPixels[j])))
            if len(groupOfThree)== 3:
                # chatgpt showed me how to convert a array to a tuple
                newRGB.append(tuple(groupOfThree))
                groupOfThree = []
            j+=1
        if groupOfThree:
            newRGB.append(groupOfThree)
        self.newRGB =  newRGB

    # outputs the table and the results
    def tableOutput(self):
        self.getUniqueSubstring()
        self.getConvertedSubstring()
        self.getEncodedMessage()
        self.convertBinaryToPixels()
        print("Unique Substrings")
        print(self.uniqueSubstring)
        print("Converted Substrings")
        print(self.convertedSubstring)
        print("Encoded Message")
        print(self.encodedMessage)

        print("We started with " + "".join(self.binaryStr) + " with a length of "+ str(len(self.binaryStr)))
        print("The final encoded message is " + (self.encodedMessage) +" with a length of " + str(len(self.encodedMessage)))
        # the smaller the number here the more compress it is
        print("The difference between the final and initial lengths is " + str((len(self.encodedMessage))-len(self.binaryStr)))
        return (self.newRGB)

# converts pixels to binary and returns all concatenated together
def convertPixelsValueToBinary(pixelsValue):
    i = 0
    pixelsInBinary = ""
    while i < len(pixelsValue):
        pixelValue = pixelsValue[i]
        binaryVal = bin(pixelValue)
        binaryVal = binaryVal[2:]
        # make sure binary value is at least 8 for each of the values
        if len(binaryVal) < 8:
            difference = 8 - len(binaryVal)
            binaryVal = ("0" * difference) + binaryVal
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
# used https://www.thecoderscamp.com/how-to-read-bmp-file-in-python/ to find how to open an image file
file = "small.bmp"
image = Image.open(file)
pixels = image.load()

endingWidth, endingHeight = image.size


entireImageConvertToBinary =convertRGBToBits(pixels,endingWidth,endingHeight)

algorithm =lempelZivAlgorithm(entireImageConvertToBinary)
finaltuple=algorithm.tableOutput()

# used chatgpt to turn my bits back into a image
# Function to convert RGB tuples back into an image
def tuplesToImage(rgb_tuples, width, height):
    # Create a new blank image
    global file
    image = Image.open(file)
    new_pixels = image.load()
    index = 0
    x = 0
    y = 0
    while index < len(rgb_tuples):
        new_pixels[y, x] = rgb_tuples[index]

        index += 1
        y += 1
        if y == width:
            x += 1
            y = 0
        if x == height:
            break

    return image

reconstructedImage = tuplesToImage(finaltuple, endingWidth, endingHeight)
reconstructedImage.save("modified.bmp")
reconstructedImage.show()

