import func
import os
import time

infileName = input('Enter the file name: ')
filesCount = int(input('How many files to split into: '))

if not os.path.isfile(infileName):
    print("File doesn't exist, please create the file with FileGenerator.py:")
else:
    fileSize = os.stat(infileName).st_size
    numsPerFile = fileSize // 4 // filesCount
    rest = fileSize // 4 % numsPerFile

    print(f"\nSorting the contents of {infileName} into 'c.bin'.")
    startTime = time.time()
    
    print(f"\nSplitting the file into {filesCount} files, {numsPerFile} numbers in each:")
    func.splitFile(infileName, filesCount, numsPerFile)

    for i in range(filesCount - 1):
        print(f"\nSorting file number {i}")
        func.sortFile(f"b{i}.bin", numsPerFile, i)
    print(f"\nSorting file number {filesCount - 1}")
    func.sortFile(f"b{filesCount - 1}.bin", numsPerFile, i, rest)

    print("Merging the files")
    func.mergeFiles(filesCount, fileSize)

    endTime = time.time()
    print(f"\nTotal time to sort the file: {round((endTime - startTime) * 1000)/1000} seconds.")
    print(f"Total file size: {round((fileSize//1024) * 1000)/1000}KB.")
    print(f"Algorithm speed: {round(((fileSize/1073741824) / ((endTime - startTime) / 600)) * 100000)/100000}GB/10min")

    func.clearGarbage(filesCount)