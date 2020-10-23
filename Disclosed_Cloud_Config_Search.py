# This script searches for config files with the cloud_enum detected storages and applications via Google

# requirements:
# pip3 install google (here is the documentation: https://python-googlesearch.readthedocs.io/en/latest/)

# cloud_enum (https://github.com/initstring/cloud_enum) use:
# cloud_enum -k <KEYWORD> -t 10 -m <MUTATIONS_DICT> -b <BRUTEFORCE_DICT> -l <REPORT_FILE>

# this script use:
# python3 Current_Script.py <REPORT_FILE_FROM_cloud_enum> <SCRIPT_OUTPUT_FILE>

try: 
    from googlesearch import search 
except ImportError: 
    print("Google library not found, try pip install google")

import sys
import requests
import _thread
import time

ftoread=sys.argv[1] #read cloud_enum output file as an argument
ftowrite=sys.argv[2] #read output file name as an argument

wfile = open(ftowrite, "w")
wfile.write("Script started as: " + sys.argv[0] +" "+ ftoread +" "+ ftowrite +"\n")
print("Script started as: " + sys.argv[0] +" "+ ftoread +" "+ ftowrite +"\n")

# url content check function
def urlcontent(urlstr, srchstr):
    urltext=""
    urlcon=""
    txtpos=""
    txtstart=""
    txtend=""
    txt=""
    time.sleep(1) #delay for better sync of the threads
    try:
        urlcon = requests.get(urlstr, allow_redirects=True)
        urltext = str(urlcon.content)
                
        while srchstr.lower() in urltext.lower():
            txtpos=""
            txtstart=""
            txtend=""
            txt=""
            wfile.write("\n----------------------------------------------------\n")
            print("----------------------------------------------------\n")
            print(srchstr + " found in:\n" + urlstr + "\n")
            wfile.write("\n" + srchstr + " found in:\n" + urlstr + "\n")
            print("Text fragment:\n")
            wfile.write("\nText fragment:\n")
            
            #text fragment search and recording functionality block
            
            txtpos=urltext.lower().find(srchstr.lower())
            if txtpos<100:
                txtstart=0
            else:
                txtstart=txtpos-100
            txtend=txtpos+200
            txt=urltext[txtstart:txtend]
            urltext=urltext[txtend:]
            
            print(txt + "\n")
            wfile.write(txt + "\n")
            
    except:
        pass


# google search function
def queryfunc(searchforstr):
    
    #define file types and Google query syntax here
    #query = searchforstr + " (filetype:config | filetype:txt | "
    #query = query + "filetype:xml | filetype:json)"
    
    query = searchforstr + " (filetype:config | filetype:json)"
    
    print("Querying Google for: " + query)
    
    for reslink in search(query, pause=10): #adjust nr of returned links (add ", stop=NR") and pause here
        print("Checking content of: " + reslink)
        _thread.start_new_thread (urlcontent,(reslink, searchforstr))

# read and process input file
rfile = open(ftoread, "r")
for line in rfile:
    line=line.strip()
    
    #list patterns for the strings to read in the input file
    if ("Protected S3 Bucket:" in line) or \
       ("HTTP-OK Storage Account:" in line) or \
       ("HTTPS-Only Storage Account:" in line) or \
       ("Registered Azure" in line) or \
       ("Protected Google Bucket:" in line) or \
       ("OPEN GOOGLE BUCKET:" in line) or \
       ("OPEN AZURE CONTAINER:" in line) or \
       ("OPEN S3 BUCKET:" in line) or \
       ("Google App Engine" in line):
        
        rcolpos=line.rfind(":",0,len(line))
        line=line[rcolpos+1:len(line)]
        
        while line[0]=="/":
            line=line[1:len(line)]
            
        while line[-1]=="/":
            line=line[0:len(line)-1] 
        
        queryfunc(line)
        
#closing both files
rfile.close()
wfile.close()
        
        
