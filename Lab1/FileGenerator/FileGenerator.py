import os
import time
import psutil

def createFile(infileName, filesCount, bytesPerBuffer):
    """makes a file and fills it with unsorted numbers"""
    startTime = time.time()
    
    infile = open(infileName, 'wb')
    infile.close()
    for i in range(filesCount):
        splitTime = time.time()
        numbers = []
        buffer = bytearray(os.urandom(bytesPerBuffer))
        infile = open(infileName, 'ab')
        infile.write(buffer)
        infile.close()
        print(f"{round((100/filesCount*(i+1))*1000)/1000}% of generating done in {round((time.time() - splitTime)*1000)/1000} seconds.")

    endTime = time.time()
    print(f"File generated in {round((endTime - startTime)*1000)/1000} seconds.")

infileName = input('Enter the file name: ')
totalBytes = int(input('Enter the file size in B: ')) #*1024*1024

max_space = psutil.virtual_memory().available * 0.8
maxBytesPerBuffer = max_space - max_space % 4

filesCount = 1
while totalBytes // maxBytesPerBuffer > filesCount:
    filesCount += 1

bytesPerBuffer = totalBytes // filesCount - totalBytes // filesCount % 4

createFile(infileName, filesCount, bytesPerBuffer)