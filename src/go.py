# -*- coding: utf-8 -*-
import codecs;
file = open("../data/serrablo153.txt", encoding='utf-8')

#import codecs
#fileObj = codecs.open( "../data/serrablo153.txt", "r", "utf-8" )
#u = fileObj.readline() # Returns a Unicode string from the UTF-8 bytes in the file

while 1:
    line = file.readline()
    if not line:
        break
    pass 
    print (line)
    
