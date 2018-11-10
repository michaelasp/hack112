import os
def listFiles(path):
    if (os.path.isdir(path) == False):
        
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    elif os.path.isdir(path) == True:
        
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
   
    
    
        return files



a = listFiles("LeapDeveloperKit_2.3.1")

for r in a:
    print(r)
