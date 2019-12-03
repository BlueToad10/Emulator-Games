import os

def fileSubFolderConvert(directory, oldFileType, newFileType):
    for object in os.listdir(directory):
        if object.endswith(str(oldFileType)) and not object == "fileFolderConvert.py":
            l = open(str(directory) + "\\" + object, "r")
            s = open(str(directory) + "\\" + str(object).replace(str(oldFileType), str(newFileType)), "w+")
            for line in l:
                s.write(line)
                print(line)
            l.close()
            s.close()
            os.remove(str(directory) + "\\" + str(object))
        
fileSubFolderConvert("lib\\pygame\\docs", ".html", ".txt")
fileSubFolderConvert("lib\\pygame", ".html", ".txt")
