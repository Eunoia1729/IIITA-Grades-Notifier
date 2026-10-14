# IIITA-Grades-Notifier

This tool notifies on your linux desktop if any updates have been made to your semester grades.      

## Motivation
One of the professors decided to change the grades every hour to give anxiety attacks . So, decided to not waste time in checking the portal frequently and instead automate it.

## Installation
- Clone this repository:   
```
git clone https://github.com/Eunoia1729/IIITA-Grades-Notifier.git
```

- Install Google Chrome. The matching chromedriver is downloaded automatically by Selenium (4.6+).

- Inside the repository, run the below commands for preparing the notifier. You will be asked for your sudo password to install system packages.
```
cd IIITA-Grades-Notifier   
./install_dependencies.sh   
./grades-notifier.sh
```
- Your LDAP credentials will be asked  and then the automation begins !

**Note** : Your credentials remain safe and local to the session on your desktop and are wiped off after session ends.

## Troubleshooting
The scraper uses fixed XPaths into the portal's HTML. If the portal layout changes, the script will report
"No grades found"; update `GRADE_ROWS_XPATH` and `LOGIN_BUTTON_XPATH` in `grades_extractor.py`.
Grades are cached in `results.json`, which is git-ignored.

## Features
- Checks portal (https://apply.iiita.ac.in/unified_login/) every 5 minutes.
- Alerts you on you desktop if the grades have been uploaded / changed.
- Secure     

     
![Demo](https://github.com/Eunoia1729/IIITA-Grades-Notifier/blob/master/screenshot.png)

Wish you high pointers !
