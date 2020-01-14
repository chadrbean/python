#!/usr/bin/env python3
import csv
import os
from multiprocessing import Process, current_process   
import json
import time
import uszipcode
search = SearchEngine(simple_zipcode=True)


def data_to_process():
    with open("2010_census_city_county.csv", "r", encoding="mac-roman") as f:
        csvr = csv.reader(f)
        count_cdp = 0
        all_records = []
        for line in csvr:
            final_dict = {}
            
            f_row = line[5].split("-")  
            if len(f_row) > 1: 
                state = f_row[0].strip()
                final_dict.update({"state":state})
        # Create City and County
            g_row = line[6].split(",")
            if len(g_row) > 1:
                if "CDP" in g_row[0]:
                    count_cdp += 1
                    continue
                else:
                    city = g_row[0].strip()
                    county = g_row[1].strip()
                    final_dict.update({"city":city})
                    final_dict.update({"county":county})
                all_records.append(final_dict)
        return all_records

def workfunc(results):
    
    process_id = os.getpid()
    print(process_id)
    with open("multi_proc_test.json", "a") as w:   
    # Use os library to get process id and print id 
    # print("Process Id {} ".format(process_id))
        for i in results:
            json.dump(i, w)
            w.write("\n")

count = 0
if __name__ == '__main__':
    processors =[]
    results = data_to_process()

    for i in range(500):
        process = Process(target=workfunc, args=(results,))
        processors.append(process)
        process.start()
        count += 1
        
    for process in processors:
        # This join is to say join all the processes together and wait for them to be completed
        process.join()

    print(count)


