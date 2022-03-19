from ftplib import FTP 

ftp = FTP('192.168.0.98')
ftp.login('ali', 'Bismillah')

folder_name = 'test'
file_name =  'result.jpg'
if folder_name is not None:
    try: 
        ftp.cwd(folder_name)
    except:
        print('Cannot create folder')
        #return False
try:    
    ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
    ftp.quit()
    #return True
except:
    print('Cannot send file')
    #return False