#!/bin/bash

# Ask the user for credentials
echo "Enter LDAP Credentials :"
read -p 'Username: ' uservar
read -sp 'Password: ' passvar
echo
export uservar
export passvar

.venv/bin/python intro.py

# Check every 5 minutes
while true ; do .venv/bin/python grades_extractor.py ; sleep 5m ; done
