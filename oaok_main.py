from bs4 import BeautifulSoup
from timeit import default_timer as timer
from fake_headers import Headers
import requests
import random
import time
import sys
import keyboard
import os

global original_url

global headers

original_url = "https://oaok.ru"

# Before inserting links for all models, cleaning text document from everything that is inside.
# Also somehow creates file if it didn't existed. Not touching on that.
def clean_file():
    open('models_links.txt', 'w').close()
    print("Cleaned text file.\n")

# Generating random headers, for "tricking" server into thinking that all of the requests coming from different people.
def generate_headers():
    headers = Headers(headers=True).generate()
    
    return headers

headers = generate_headers()

# Letting user choose desired delay (in seconds) between viewing models, although not setting any boundaries. 
# User can choose anything that is below or above recommended range. 
def define_delay():
    print("""Write number of seconds that will define delay between viewing models.\nRecommended range is from 2 to 5 seconds.\nWorks with float numbers.\nWriting or doing anything other will set default value.\nDefault value is 5 seconds.""")
    DELAY = input()
    
    return DELAY

# Letting user choose desired time (in minutes) to recheck models links. Only works for working mode 1.
# Once in a defined time, text document with links will be cleared, parsed from the site and inserted again
# Doing this will make sure that newly uploaded models will be included in the text document.
# Introducing minimal number of minutes, because there is no needance of frequent updates.
def define_recheck_models_time():
    print("""Write number of minutes that will define delay between rechecking model links.\nDoing this will make sure that newly uploaded models will be included in the text document.\nRecommended range is 300-600 minutes.\nWriting or doing anything other will set default value.\nDefault value is 300 minutes.""")
    RECHECK = input()
    
    return RECHECK
    

# Checking if file that stores user selected links exists. If not, create it.
def user_file_check():
    if (os.path.exists('user_models_links.txt')):
        pass
    else:
        open('user_models_links.txt', 'w').close()
        print("'user_models_links.txt' text file was not located. Created 'user_models_links.txt' inside script folder.\n")

# Grabing first page of CG-models section, so we can iterate on it to insert links to the text document.
def cg_models_link_grab():
    cg_models_link = "https://oaok.ru/cg-models/models/"
    
    try:
        html = requests.get(cg_models_link, headers=headers).content
    except:
        print("Error when tried to grab links. Try again later. Program will close in 3 seconds.")
        time.sleep(3)
        sys.exit(0)

    soup = BeautifulSoup(html, 'html.parser')
    print("Received response from CG-models section.")
    
    return soup

# Grabing first page of 3D-print section, so we can iterate on it to insert links to the text document.
def print_models_link_grab():
    print_models_link = "https://oaok.ru/3d-print/models/"
    
    try:
        html = requests.get(print_models_link, headers=headers).content
    except:
        print("Error when tried to grab links. Try again later. Program will close in 3 seconds.")
        time.sleep(3)
        sys.exit(0) 
              
    soup = BeautifulSoup(html, 'html.parser')
    print("Received response from 3D-print section.")

    return soup

# Function that iterates over page with models. If finds that next page exists, goes to the next page and iterates over.
# Until it stumbles upon last page, it will get every link for every model in previous pages.
# Writes all found links inside models_links.txt. 1 line, 1 link.
def inserting_links(soup, file):
    # Finding all items with class catalog__link
    catalog_items = soup.find_all("a", {"class": "catalog__link"})
    print("Found models in catalog.")

    # Writing in the file all found links on the first page
    for item in catalog_items:
        file.write(original_url + item['href'] + '\n')

    print("Inserted first page...")

    # Continuing on finding and writing links, this time on next pages.
    while soup.find('a', {'class': 'pagination__next'})['href'] != '#':
        next_page = original_url + soup.find('a', {'class': 'pagination__next'})['href']
        
        try:
            html = requests.get(next_page, headers=headers).content
        except:
            print("Error when tried to grab links. Try again later. Program will close in 3 seconds.")
            time.sleep(3)
            sys.exit(0)

        soup = BeautifulSoup(html, 'html.parser')
        
        catalog_items = soup.find_all("a", {"class": "catalog__link"})
        for a in catalog_items:
            file.write(original_url + a['href'] + '\n')
        
        print("Inserted another page...")
        time.sleep(1)
    
    print("Done inserting models from category.\n")

# Main working force function.
# Checks working mode choice, depending on the choice does while loop.
# Initially it was just one while loop without function.
# But timer for rechecking models links is needed, and I don't know how to do all of it without wrapping in function.
# Inside while loop randomly generates number, goes to the line under that number, views link in that line.
def viewing_links(lines, choice):
    match choice:
        case "1":
            # Storing elapsed time for rechecking models links.
            time_elapsed_seconds = 0
            while True:
                start = timer()

                random_link_number = random.randint(0, len(lines) - 1)
                random_link = lines[random_link_number].strip()

                try:
                    requests.get(random_link, headers=headers).content
                except requests.exceptions.MissingSchema:
                    print("Couldn't find links inside 'user_models_links.txt' file.\nFollow the instructions for writing links inside text document. Program will close in 5 seconds.")
                    time.sleep(5)
                    sys.exit(0)
                except:
                    print("Error when tried to send request to the random link.\nPossible reasons:\n1. No Internet connection.\n2. HTTP 429 Too Many Requests error. Wait a little bit and increase delay time.\nProgram will close in 10 seconds.")
                    time.sleep(10)
                    sys.exit(0)
                
                print("Viewed random item from catalog: " + random_link)
                time.sleep(DELAY)
                
                end = timer()
                time_elapsed_seconds += (end - start)
                
                # If elapsed time equals RECHECK variable, rewrite all links inside the file.
                if int(time_elapsed_seconds / 60) >= RECHECK:
                    time_elapsed_seconds = 0
                    print("Rechecking model links.")
                    clean_file()
                    with open("models_links.txt", "w") as file:
                        inserting_links(cg_models_link_grab(), file)
                        inserting_links(print_models_link_grab(), file)
                    file_name = 'models_links.txt'
                    print("Restarting program\n")
                    lines = read_lines(file_name)
                else:
                    continue
        case "2":
            while True:
                random_link_number = random.randint(0, len(lines) - 1)       
                random_link = lines[random_link_number].strip()
                
                try:
                    requests.get(random_link, headers=headers).content
                except requests.exceptions.MissingSchema:
                    print("Couldn't find links inside 'user_models_links.txt' file.\nFollow the instructions about writing links inside text document. Program will close in 5 seconds.")
                    time.sleep(5)
                    sys.exit(0)
                except:
                    print("Error when tried to send request to the random link.\nPossible reasons:\n1. No Internet connection.\n2. HTTP 429 Too Many Requests error. Wait a little bit and try increasing delay time.\nProgram will close in 10 seconds.")
                    time.sleep(10)
                    sys.exit(0)
                
                print("Viewed random item from catalog: " + random_link)
                time.sleep(DELAY)

# Reads and returns all lines inside provided text document, for later usage.
def read_lines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    print("Read lines from text file.\n")
    return lines
    
# Letting user choose betwen 2 working modes.
while True:
    print("There is 2 working modes for program:\n1: grabbing every model from CG-Model and 3D-print sections and randomly view them.\n2: creating your text document with models where you want increase views.\nWrite 1 or 2 respectively:")
    choice = str(input())
    if choice != "1" or choice != "2":
        break
    else:
        print("Not supported mode. There is only 2 options: 1 or 2.\n")
        continue

# DELAY can only be in int or float format, nothing else.
while True:
    DELAY = define_delay()
    try:
        DELAY = int(DELAY)
        break
    # Checking for float value
    except ValueError:
        try:
            DELAY = float(DELAY)
            break
        # If its not float, then it's something other than numbers. Setting default value.
        except ValueError:
            print("Setting default value for delay between viewing models: 5 seconds.\n")
            DELAY = 5
            break

# Match upon selected working mode.
match choice:
    # In case 1, cleans file, inserts links, provides value to the file_name variable. 
    case "1":
        while True:
            RECHECK = define_recheck_models_time()
            try:
                RECHECK = int(DELAY)
                if (RECHECK < 300):
                    print("Setting default value for delay between rechecking models links to: 300 minutes.\n")
                    RECHECK = 300
                break
            except ValueError:
                print("Setting default value for delay between rechecking models links: 300 minutes.\n")
                RECHECK = 300
                break
        
        clean_file()
        with open("models_links.txt", "w") as file:
            inserting_links(cg_models_link_grab(), file)
            inserting_links(print_models_link_grab(), file)
        file_name = 'models_links.txt'
        print("Starting program\n")
        lines = read_lines(file_name)
        viewing_links(lines, choice)
    # In case 2, checks for user_file, provides value to the file_name variable
    case "2":
        user_file_check()
        print("In the user_models_links text file, add links to models.\n1 link per 1 line.\nWhen you are finished with this, close text file and press Enter.\n")
        while True:
            if keyboard.is_pressed('enter'):
                break
            else:
                continue
        # Added test to check if user wrote anything to the file.
        if (os.path.getsize('user_models_links.txt') == 0):
            print("File is empty. Add links. Program will close in 3 seconds")
            time.sleep(3)
            sys.exit(0)
        else:
            pass
        file_name = 'user_models_links.txt'
        print("Starting program\n")
        lines = read_lines(file_name)
        viewing_links(lines, choice)