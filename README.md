# Disclosed_Cloud_Config_Search
The script searches for publicly available configuration files related to the cloud services discovered by the cloud_enum tool.

requirements:
pip3 install google (here is the documentation: https://python-googlesearch.readthedocs.io/en/latest/)

cloud_enum (https://github.com/initstring/cloud_enum) use:
cloud_enum -k <KEYWORD> -t 10 -m <MUTATIONS_DICT> -b <BRUTEFORCE_DICT> -l <REPORT_FILE>

this script use:
python3 Current_Script.py <REPORT_FILE_FROM_cloud_enum> <SCRIPT_OUTPUT_FILE>
