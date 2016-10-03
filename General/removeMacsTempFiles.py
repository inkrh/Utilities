import os

def RemoveMacsTempFiles(path):
    i = 0
    print("Starting")
    for root,subdirs,files in os.walk(path):
        for f in files:
            
            fp = os.path.join(root,f)
            ##print("Checking " + f)
            if f.startswith("._"):
                print("Deleting " + fp)
                os.system("rm -rf "+ fp)
                i+=1
    print("Done - removed " + str(i) + " files.")
