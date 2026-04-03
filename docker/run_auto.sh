#!/bin/bash
cd /home/frappe/frappe-bench
bench --site lms.localhost execute "with open('/workspace/lms_automated_flow.py') as f: exec(f.read())"
