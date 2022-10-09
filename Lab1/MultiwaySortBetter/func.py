import time
import array
import os
import psutil

def splitFile(infileName, filesCount, numsPerFile):
    """splits the file into that amount of equal files"""
    startTime = time.time()
    infile = open(infileName, 'rb')
    
    for i in range(filesCount - 1):
        currFile = open(f"b{i}.bin", 'wb')
        buffer = infile.read(4*numsPerFile)
        currFile.write(buffer)
        currFile.close()
    
    currFile = open(f"b{filesCount - 1}.bin", 'wb')
    buffer = infile.read()
    currFile.write(buffer)
    currFile.close()
    infile.close()

    endTime = time.time()
    print(f"File split in {endTime - startTime} seconds.")

def sortFile(currFileName, numsPerFile, fileInd, rest = 0):
    """sorts whatever is in the file"""
    startTime = time.time()
    currFile = open(currFileName, 'rb')

    unsortedArr = array.array('L')
    unsortedArr.fromfile(currFile, numsPerFile + rest)
    sortStartTime = time.time()
    li = unsortedArr.tolist()
    li.sort()
    arr = array.array('L')
    arr.fromlist(li)
    sortEndTime = time.time()
    print(f"Sorting done in {sortEndTime - sortStartTime} seconds.")

    currFile = open(currFileName, 'wb')
    arr.tofile(currFile)
    currFile.close()

    endTime = time.time()
    print(f"Contents of file {fileInd} updated in {endTime - startTime} seconds.")

def mergeFiles(filesCount, totalSize):
    infileArr = []

    outfile = open(f"sorted.bin", 'wb')

    waitingNumbers = []
    for i in range(filesCount):
        infileArr.append(open(f"b{i}.bin", 'rb'))
        waitingNumbers.append(infileArr[i].read(4))

    for loop in range(totalSize // 4):
        min = waitingNumbers[0]
        minInd = 0
        for i in range(1, filesCount):
            if waitingNumbers[i] <= min: 
                min = waitingNumbers[i]
                minInd = i

        if min == b'\xff\xff\xff\xff':
            for i in range(len(infileArr)):
                infileArr[i].close()
            filled = os.stat('sorted.bin').st_size
            leftToFill = totalSize - filled
            outfile.write(b'\xff'*leftToFill)
            outfile.close()
            break

        else:
            outfile.write(min)
            waitingNumbers[minInd] = infileArr[minInd].read(4)
            if not waitingNumbers[minInd]:
                waitingNumbers[minInd] = b'\xff\xff\xff\xff'

def clearGarbage(filesCount):
    for i in range(filesCount):
        try:
            os.remove(f'b{i}.bin')
        except:
            pass