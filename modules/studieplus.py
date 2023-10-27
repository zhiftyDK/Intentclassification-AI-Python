from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

currentAssignments = []

def getAssignments():
    return currentAssignments

username = ""
password = ""

while(True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://all.uddataplus.dk/opgave/?id=id_menu_opgaver")
        page.click("a.select2-choice")
        page.click("text=College360")
        page.click("button#btnUnilogin")
        page.click("body > div.container-fluid.page-container.outer > div > div > main > div > form > nav > ul > li:nth-child(1) > button")
        page.fill("input#username", username)
        page.click("button[type=submit]")
        page.fill("input#form-error", password)
        page.click("button[type=submit]")
        page.wait_for_selector("button.btn-info")
        assignments = page.inner_html(".dataTable")
        soup = BeautifulSoup(assignments, "html.parser")
        assignments = []
        for tr in soup.find_all("tr"):
            labels = ["Subject", "Assignment", False, "Hours", False, False, "Due date", False, False, False]
            assignment = []
            i = 0
            for div in tr.find_all("div", {"__gwt_cell" : True}):
                if labels[i] != False:
                    assignment.append(f"{labels[i]}: {div.string}")
                i += 1
            if assignment != []:
                assignments.append(assignment)
        currentAssignments = assignments
        print(getAssignments())
    time.sleep(60 * 5)
    
