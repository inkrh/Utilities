import shutil, errno, os

##not my code
def copyAnything(src, dst):
    try:
        print("Copying " + src + " to " + dst + "\n(this may take some time)")
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

##my code
def replaceLine(line, oldName,newName):
    output = line
    output = output.replace(oldName,newName)
    output = output.replace(oldName.lower(),newName.lower())
    output = output.replace(oldName.upper(),newName.upper())
    output = output.replace(oldName.capitalize(),newName.capitalize())
    return output

def replaceName(dst,oldName,newName):
    for root,subdirs,files in os.walk(dst):
        
        for f in files:
            
            fp = os.path.join(root,f)
            ##strip out bin and obj and packages dir
            ##NB should really do this before copying...
            if "/bin/" in fp or "/obj/" in fp or "/packages/" in fp:
                os.remove(fp)
            ##go through files replace name
            elif not fp.endswith("dll") and not fp.endswith("pdb") and not ".git" in root:
                
                o = []
                i = []
                ##read file contents
                print("Reading : " + fp)
                with open(fp,'r') as fi:
                    i = fi.readlines()
                
                for line in i:
                    output = replaceLine(line, oldName,newName)
                    o = o + [output]
                ##only rewrite if changed
                if not i == o:
                    print("Editing : " + fp)
                    with open(fp,'w') as fo:
                        fo.writelines(o)
                ##rename file        
                newfp = replaceLine(fp,oldName,newName)
                if not newfp == fp:
                    print("Renaming " + fp + " to " + newfp)
                    os.renames(fp,newfp)
               
def CopyProject(src, dst, oldName, newName):
    copyAnything(src,dst)
    replaceName(dst,oldName,newName)
    


    
                    
        
