#!/bin/bash
#!/usr/bin/env python3

# Ask the user for credentials
echo "Enter LDAP Credentials :"
read -p 'Username: ' uservar
read -sp 'Password: ' passvar
export uservar
export passvar

python3 intro.py

while true ; do python3 grades_extractor.py & sleep 5m ; done
