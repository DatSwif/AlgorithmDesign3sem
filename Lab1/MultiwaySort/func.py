import time
import os

def splitFile(infileName, filesCount, fileSize):
    """splits the file into that amount of equal files"""
    startTime = time.time()

    infile = open(infileName, 'rb')
    outfileArr = [open("b0.bin", 'wb')]
    currOutfileInd = 0
    outfilesOpen = 1
    prevNum = b'\x00\x00\x00\x00'

    for i in range(fileSize//4):
        buffer = infile.read(4)
        if buffer < prevNum:
            currOutfileInd = (currOutfileInd + 1) % filesCount
            if outfilesOpen < filesCount:
                outfileArr.append(open(f"b{outfilesOpen}.bin", 'wb'))
                outfilesOpen += 1
        outfileArr[currOutfileInd].write(buffer)
        prevNum = buffer

    for i in range(outfilesOpen):
        outfileArr[i].close()
    infile.close()
        
    endTime = time.time()
    print(f"File split in {endTime - startTime} seconds.")

def BtoC(filesCount):
    infileArr = []

    outfileArr = [open(f"c0.bin", 'wb')]
    outfilesOpen = 1
    currOutfileInd = 0
    lastInSeries = b'\x00\x00\x00\x00'

    waitingNumbers = []
    for i in range(filesCount):
        infileArr.append(open(f"b{i}.bin", 'rb'))
        waitingNumbers.append(infileArr[i].read(4))
    seriesCount = 1

    while True:
        min = b'\xff\xff\xff\xff'
        trueMin = b'\xff\xff\xff\xff'
        minInd = 0
        trueMinInd = 0
        for i in range(0, filesCount):
            if (waitingNumbers[i] >= lastInSeries) and (waitingNumbers[i] <= min):
                min = waitingNumbers[i]
                minInd = i
            if waitingNumbers[i] <= trueMin: 
                trueMin = waitingNumbers[i]
                trueMinInd = i

        if min == b'\xff\xff\xff\xff':
            if trueMin == b'\xff\xff\xff\xff':
                for i in range(len(infileArr)):
                    infileArr[i].close()
                for i in range(len(outfileArr)):
                    outfileArr[i].close()
                return outfilesOpen, seriesCount
            elif outfilesOpen < filesCount:
                outfileArr.append(open(f"c{outfilesOpen}.bin", 'wb'))
                outfilesOpen += 1
                seriesCount += 1
                currOutfileInd += 1
            else:
                currOutfileInd = (currOutfileInd + 1) % filesCount
                seriesCount += 1

            outfileArr[currOutfileInd].write(trueMin)
            lastInSeries = trueMin
            waitingNumbers[trueMinInd] = infileArr[trueMinInd].read(4)
            if not waitingNumbers[trueMinInd]:
                waitingNumbers[trueMinInd] = b'\xff\xff\xff\xff'
        else:
            outfileArr[currOutfileInd].write(min)
            lastInSeries = min
            waitingNumbers[minInd] = infileArr[minInd].read(4)
            if not waitingNumbers[minInd]:
                waitingNumbers[minInd] = b'\xff\xff\xff\xff'

def CtoB(filesCount):
    infileArr = []

    outfileArr = [open(f"b0.bin", 'wb')]
    outfilesOpen = 1
    currOutfileInd = 0
    lastInSeries = b'\x00\x00\x00\x00'

    waitingNumbers = []
    for i in range(filesCount):
        infileArr.append(open(f"c{i}.bin", 'rb'))
        waitingNumbers.append(infileArr[i].read(4))
    seriesCount = 1

    while True:
        min = b'\xff\xff\xff\xff'
        trueMin = b'\xff\xff\xff\xff'
        minInd = 0
        trueMinInd = 0
        for i in range(0, filesCount):
            if (waitingNumbers[i] >= lastInSeries) and (waitingNumbers[i] <= min):
                min = waitingNumbers[i]
                minInd = i
            if waitingNumbers[i] <= trueMin: 
                trueMin = waitingNumbers[i]
                trueMinInd = i

        if min == b'\xff\xff\xff\xff':
            if trueMin == b'\xff\xff\xff\xff':
                for i in range(len(infileArr)):
                    infileArr[i].close()
                for i in range(len(outfileArr)):
                    outfileArr[i].close()
                return outfilesOpen, seriesCount
            elif outfilesOpen < filesCount:
                outfileArr.append(open(f"b{outfilesOpen}.bin", 'wb'))
                outfilesOpen += 1
                seriesCount += 1
                currOutfileInd += 1
            else:
                currOutfileInd = (currOutfileInd + 1) % filesCount
                seriesCount += 1

            outfileArr[currOutfileInd].write(trueMin)
            lastInSeries = trueMin
            waitingNumbers[trueMinInd] = infileArr[trueMinInd].read(4)
            if not waitingNumbers[trueMinInd]:
                waitingNumbers[trueMinInd] = b'\xff\xff\xff\xff'
        else:
            outfileArr[currOutfileInd].write(min)
            lastInSeries = min
            waitingNumbers[minInd] = infileArr[minInd].read(4)
            if not waitingNumbers[minInd]:
                waitingNumbers[minInd] = b'\xff\xff\xff\xff'

def mergeFiles(filesCount):
    filesFilled = filesCount
    while filesFilled > 1:
        startTime = time.time()
        filesFilled, seriesCount = BtoC(filesFilled)
        stoppedAt = 'c0.bin'
        if filesFilled > 1:
            filesFilled, seriesCount = CtoB(filesFilled)
            stoppedAt = 'b0.bin'
        endTime = time.time()
        print(f"Merging numbers into {seriesCount} series was completed. Another {endTime - startTime} seconds elapsed.")

    os.remove('sorted.bin')
    os.rename(stoppedAt, 'sorted.bin')
    print(f"Sorting done. Check file 'sorted.bin' to see sorted contents of the initial file.")

def clearGarbage(filesCount):
    for i in range(filesCount):
        try:
            os.remove(f'b{i}.bin')
        except:
            pass
        try:
            os.remove(f'c{i}.bin')
        except:
            pass