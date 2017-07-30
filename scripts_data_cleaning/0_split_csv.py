import os
import pyexcel

originPath = "/Users/giovanniabbatepaolo/Desktop/csvFiles"
destinPath = "/Users/giovanniabbatepaolo/Desktop/csvSplit"


for file in os.listdir(originPath):
    if '.xlsx' in file:
        filePath = originPath + '/' + file
        book = pyexcel.get_book(file_name = filePath)
        book.save_as(destinPath + file + ".csv")