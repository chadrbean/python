import json
import csv
import subprocess
import datetime
from collections import defaultdict


# File For Health Check Requirements
health_requirements_file = 'health_check_requirements.json'
health_check_requirements = {}

def import_requirements():
    with open(health_requirements_file, 'r') as fr:
        for i in fr.readlines():
            data = json.loads(i)
            health_check_requirements.update(data)
            
    return health_check_requirements

def client_package_list():
    pkg_list = []
    packages = subprocess.run(['rpm', '-qa'], 
    timeout=60,
    stdout=subprocess.PIPE,
    check=True,
    universal_newlines=True)
    for pkg in packages.stdout.split():
        pkg_list.append(pkg.split(".")[0])
    return(pkg_list)

def package_check(rpm_definitions, result_client_packages):
    missing_packages = []
    for rpm_def in rpm_definitions:
        if rpm_def not in result_client_packages:
            missing_packages.append(rpm_def)
    return missing_packages



def services_check(services_definitions):
    missing_keywords = {}
    check_service = {}
    failed_service_check = []
    for k1,v1 in services_definitions.items():
        for k2,v2 in v1.items():
            if k2 == 'config_file':
                config_file = subprocess.run(['cat', v2], 
                timeout=60,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                universal_newlines=True)
                config_file = config_file.stdout
            elif k2 == 'keywords':
                for keyword in v2:
                    if keyword not in config_file:
                        missing_keywords.__setitem__(k1, keyword)
            if k2 == 'state':
                service_state = subprocess.run(['systemctl', 'status', k1], 
                timeout=60,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
                service_state = service_state
                
                if v2 == 'active':
                    if v2 in service_state.stdout and 'enabled' in service_state.stdout:
                        pass
                    else:
                        check_service.__setitem__(k1, 'Failed')
                elif v2 == 'disabled':
                    if v2 in service_state.stderr or 'could not be found' in service_state.stderr: 
                        pass
                    else:
                        check_service.__setitem__(k1, 'Failed')
                
    # Check if any services are in a failed state               
    failed_services = subprocess.run(['systemctl', 'list-unit-files', '--type', 'service', '--state', 'failed'], 
    timeout=60,
    stdout=subprocess.PIPE,
    check=True,
    universal_newlines=True)
    result_failed_services = failed_services.stdout        
    if '0 unit' in  result_failed_services:
        pass
    else:
        failed_service_check.append(result_failed_services)
    result_final_services = {'config_failures': missing_keywords, 'state_check': check_service, 'failed_services': failed_service_check}
    return result_final_services

def get_hostname():
    # Get System Hostname
    hostname_check = subprocess.run(['hostname'], 
    timeout=60,
    stdout=subprocess.PIPE,
    check=True,
    universal_newlines=True)     
    return hostname_check.stdout
    
def hostnamectl():
    hostnamectl = {}
    hostnamectl_check = subprocess.run(['hostnamectl'], 
    timeout=60,
    stdout=subprocess.PIPE,
    check=True,
    universal_newlines=True)   
    for i in hostnamectl_check.stdout.split('\n'):
        i = i.strip().split(':')
        if len(i) >  1:
            hostnamectl[i[0]] = i[1].strip()
    return hostnamectl
  

def timedatectl():
    timedatectl = {}
    timedatectl_check = subprocess.run(['timedatectl'], 
    timeout=60,
    stdout=subprocess.PIPE,
    check=True,
    universal_newlines=True)     
    for i in timedatectl_check.stdout.split('\n'):
        i = i.strip().split(':')
        if len(i) >  1:
            timedatectl[i[0]] = i[1].strip()
    return timedatectl

def main():
    health_definitions = import_requirements()
    result_client_packages = client_package_list()
    result_hostnamectl = hostnamectl()
    result_timedatectl = timedatectl()
 
    
    for k1,v1 in health_definitions.items():
        if k1 == 'rpms' and isinstance(v1, list):
            missing_packages = package_check(health_definitions['rpms'], result_client_packages)
        if k1 == 'services' and isinstance(v1, dict):
            service_check = services_check(health_definitions['services'])
    
    result_final_health_check = {'hostnamectl': result_hostnamectl, 'timedatectl':result_timedatectl, 'missing_packages': missing_packages, 'service_checks': service_check}
    
    # Add Time Stamp
    now = datetime.datetime.now()
    date_time = now.strftime('%Y-%m-%d %H:%M:%S')
    result_final_health_check.__setitem__('date_time', date_time)
    print(json.dumps(result_final_health_check))    # Print line needed for bash script

main()


