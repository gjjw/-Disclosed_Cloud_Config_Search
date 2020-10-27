# This script searches for config files with the cloud_enum detected storages and applications via Google

# requirements:
# pip3 install google (here is the documentation: https://python-googlesearch.readthedocs.io/en/latest/)

# cloud_enum (https://github.com/initstring/cloud_enum) use:
# cloud_enum -k <KEYWORD> -t 10 -m <MUTATIONS_DICT> -b <BRUTEFORCE_DICT> -l <REPORT_FILE>

# this script use:
# python3 Current_Script.py <REPORT_FILE_FROM_cloud_enum> <SCRIPT_OUTPUT_FILE>


import sys
import requests
import _thread
import time
import os
import importlib
import random

try: 
    import googlesearch
except ImportError: 
    print("Google library not found, try pip install google")

# settings for Google lockout avoidance
retrbefp = 2  # nr of retries before pause
pvalue = 120  # pause in seconds (reliable Google threshold seems to be 120 for 1 request)
restoret = 100 # results for Google to return

pcount = 1
sflag = True

ftoread=sys.argv[1] #read cloud_enum output file as an argument
ftowrite=sys.argv[2] #read output file name as an argument

wfile = open(ftowrite, "w")
wfile.write("Script started as: " + sys.argv[0] +" "+ ftoread +" "+ ftowrite +"\n")
wfile.flush()
print("Script started as: " + sys.argv[0] +" "+ ftoread +" "+ ftowrite +"\n")

# url content check function
def urlcontent(urlstr, srchstr):    
    urltext=""
    urlcon=""
    txtpos=""
    txtstart=""
    txtend=""
    txt=""
    
    time.sleep(0.5) #delay for better sync of the threads
    
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
            wfile.flush()
            
    except:
        pass


# google search function
def queryfunc(searchforstr, uagent, rtr):
    
    #define file types and Google query syntax here
    query = "intext:" + searchforstr + " (filetype:config | filetype:xml | filetype:json | filetype:ini | filetype:ps1 | filetype:yaml | filetype:yml | filetype:log | filetype:cmd)"
    
    rpausev = random.randint(1, 5)
    
    print("\nQuerying Google for: " + query + "\n")
    
    for reslink in googlesearch.search(query, tld='com', user_agent=uagent, start=0, stop=rtr, num=rtr, pause=rpausev): #adjust nr of returned links (add ", stop=NR, num=NR") and pause here
        print("Checking content of: " + reslink)
        _thread.start_new_thread (urlcontent,(reslink, searchforstr))

#read and process input file
rfile = open(ftoread, "r")
for line in rfile:
    line=line.strip()
    
    #list patterns for the strings to read from the input file
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
        
        # tricks to prevent lockout by Google
        if pcount >= retrbefp or sflag:
        
            if os.path.isfile(os.getenv("HOME") + "/.google-cookie"):
                coockf = open(os.getenv("HOME") + "/.google-cookie", "w")
                coockf.write("")
                coockf.flush()
                coockf.close()
                time.sleep(1)
            
            importlib.reload(googlesearch)
            duagent = googlesearch.get_random_user_agent()
            
            if sflag:
                sflag = False
            else:
                print("\nPause " + str(pvalue) + " seconds after " + str(pcount) + " requests to Google...\n")
                time.sleep(pvalue)
                pcount = 1
                
        else:
            pcount += 1
                
        queryfunc(line, duagent, restoret)
        
#closing both files
rfile.close()
wfile.close()
