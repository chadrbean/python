import json
import sys
import csv
import os

# If they are items I dont want parsed further, i set them as a string
# Keys with values as lists are automatically built and parsed
extract_fields = {
    'hostnamectl':['Static hostname','Operating System'],
    'timedatectl': ['System clock synchronized','NTP service'],
    'service_checks': ['config_failures', 'state_check', 'failed_services'],
    'missing_packages':''
    
    }


def write_csv(data):
    export_file = 'health_summary.csv'
    print(data)
    with open(export_file, 'a') as fa:
        csvwr = csv.DictWriter(fa, data.keys())
        if os.path.exists(export_file) and os.path.getsize(export_file) > 0:
            csvwr.writerow(data)
        else:
            csvwr.writeheader()
            csvwr.writerow(data)
            
        
def main():
    with open(sys.argv[1], 'r') as fr:
        for line in fr:
            data = {}
            j_data = json.loads(line)
            for k1,v1 in extract_fields.items():
                # Parse items in extract fields that are list items
                if isinstance(v1, list):
                    for l1 in v1:
                        if len(j_data[k1][l1]) > 0:
                            data[l1] = j_data[k1][l1]
                        else:
                            data[l1] = ''
                # If they are items I dont want parsed further, i set them as a string
                if isinstance(v1, str):
                    if k1 == 'missing_packages':
                        if len(k1) > 0:
                            data[k1] = j_data[k1]
                        else:
                            data[k1] = ''
                    
            write_csv(data)

main()