import func
import os
import time

infileName = input('Enter the file name: ')
filesCount = int(input('How many files to split into: '))

if not os.path.isfile(infileName):
    print("File doesn't exist, please create the file with FileGenerator.py:")
else:
    fileSize = os.stat(infileName).st_size
    print(f"\nSorting the contents of {infileName}.")
    startTime = time.time()

    func.splitFile(infileName, filesCount, fileSize)
    func.mergeFiles(filesCount)

    endTime = time.time()
    print(f"\nTotal time to sort the file: {round((endTime - startTime) * 1000)/1000} seconds.")
    print(f"Total file size: {round((fileSize//1024) * 1000)/1000}KB.")
    print(f"Algorithm speed: {round(((fileSize/1073741824) / ((endTime - startTime) / 600)) * 100000)/100000}GB/10min")

    func.clearGarbage(filesCount)