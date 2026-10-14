"""Log in to the IIITA portal, read the grades and notify on a change."""
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

try:
    import notify2
except ImportError:  # optional desktop notifications
    notify2 = None

PORTAL_URL = "https://apply.iiita.ac.in/unified_login/"
RESULTS_FILE = Path("results.json")
# Brittle absolute XPaths: update them if the portal layout changes.
LOGIN_BUTTON_XPATH = "/html/body/div/div/div/section/form/div[3]/input[2]"
GRADE_ROWS_XPATH = "/html/body/div/div/div[3]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div"


def fetch_results(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)  # Selenium Manager downloads the driver
    try:
        driver.get(PORTAL_URL)
        time.sleep(3)
        driver.find_element(By.ID, "id_username").send_keys(username)
        driver.find_element(By.ID, "id_password").send_keys(password)
        driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
        time.sleep(10)  # raise this on a slow connection
        return [row.text for row in driver.find_elements(By.XPATH, GRADE_ROWS_XPATH)]
    finally:
        driver.quit()


def notify(message):
    if notify2 is None:
        return
    try:
        notify2.init("IIITA GRADE NOTIFIER")
        notify2.Notification("IIITA GRADE NOTIFIER", message).show()
    except Exception as exc:  # no D-Bus session, etc.
        print(f"Desktop notification failed: {exc}")


def main():
    try:
        username, password = os.environ["uservar"], os.environ["passvar"]
    except KeyError:
        sys.exit("Set the uservar and passvar environment variables (see README).")

    try:
        results = fetch_results(username, password)
    except WebDriverException as exc:
        sys.exit(f"Extraction attempt failed: {exc.msg}")
    if not results:
        sys.exit("No grades found. Check your credentials or the XPaths for the portal layout.")

    previous = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else None
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    if previous is not None and Counter(results) == Counter(previous):
        print(f"{now}: No updates found")
        return
    print(f"{now}: Updates found")
    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print("\n".join(results))
    notify("Grades have been updated. Check the terminal output for details.")


if __name__ == "__main__":
    main()
