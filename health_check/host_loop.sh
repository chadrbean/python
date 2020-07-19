IFS=","
hosts='health_check_hosts.csv'
identity_file='~/.ssh/ssh_keys/vsphere_servers'
health_defs='health_check_requirements.json'
py_script='health_check.py'
remote_location='/tmp/'
ssh_options='-o StrictHostKeyChecking=no'


while read -r col1; 
    do
        ping -c 1 $col1 > /dev/null
        if [[ $? -eq 0 ]]; then
            ssh-copy-id -f -i ~/.ssh/ssh_keys/vsphere_servers root@${col1} > /dev/null 2>&1 &&
            scp -i ${identity_file} ${ssh_options} ${py_script} ${health_defs} $col1:${remote_location} > /dev/null 2>&1  ;
            if [[ $? -eq 0 ]]; then
                ssh -i ${identity_file} ${ssh_options} $col1 "chmod 700 ${remote_location}${py_script} &&
                    cd ${remote_location} &&
                    python3 ${remote_location}${py_script}" < /dev/null >> import_data.json
                sleep 2
               
            fi
        fi
    done < $hosts

python3 health_check_parse.py import_data.json
