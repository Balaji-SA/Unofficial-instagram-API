from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import re
import json
from pyfiglet import Figlet

def setup():
    custom_fig = Figlet(font='cyberlarge')
    print(custom_fig.renderText('-------TASC-------'))
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    user_id = input("Enter the Instagram Username to be analyzed: ")
    url = "https://www.instagram.com/" + user_id + "/?hl=en"
    driver.get(url)
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="lxml")
    return soup
def user_page():
    soup=setup()
    try:
        data = json.loads(soup.find('script', type='application/ld+json').text)
    except:
        print("Private account or you may have Enetered the user_id wrong")
        return 0
    print("Bio: ", data['description'])
    posts = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/p/.*")}):
        posts.append(link.get('href'))
    return posts
def fetch_post_data():
    posts=[]
    places = []
    Active_dates = []
    captions = []
    posts=user_page()
    for i in range(len(posts)):
        epost = urllib.request.urlopen("https://instagram.com" + posts[i])
        soup = BeautifulSoup(epost, features="lxml")
        data = json.loads(soup.find('script', type='application/ld+json').text)
        # print(data)
        try:
            places.append(data['contentLocation']['name'])
            print("Place: ", data['contentLocation']['name'], end=" ")
            print("\t")
        except KeyError:
            print("Place: No place Mentioned", end=" ")
            print("\t")
        try:
            Active_dates.append(data['uploadDate'])
            print("Date: ", data['uploadDate'], end=" ")
            print("\t")

        except KeyError:
            Active_dates.append("NO date")
            print("No date Mentioned", end=" ")
            print("\t")
        try:
            captions.append(data['caption'])
            print("Caption: ", data['caption'], end=" ")
            print("\t")
        except:
            captions.append("None")
            print("Caption: No caption Detected", end=" ")
            print("\t")
        image_data = soup.findAll("script")[4].text
        try:
            image_data = image_data[image_data.find("Image may contain: ") + 18:image_data.find("is_video")]
            contents = []
            contents = image_data.split(",")
            del contents[len(contents) - 1]
            final_contents = []
            for k in contents:
                final_contents.append(k.strip())
            print("Contents in the post: ", final_contents)
        except:
            print("No content Description available")
        print("\n")
        print(
            "______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
    return places
def analyze_data():
    places=[]
    places=fetch_post_data()
    freqcount = []
    for i in places:
        freqcount.append(places.count(i))
    maxi = max(freqcount)
    mini = min(freqcount)
    most_visited = []
    rare_visited = []
    for i in range(len(freqcount)):
        if (freqcount[i] == maxi):
            most_visited.append(places[i])
        elif (freqcount[i] == mini):
            rare_visited.append(places[i])
    print("Mostly visited Places: ", set(most_visited))
    print("Rarely visited places: ", set(rare_visited))
    # print("Active Dates: ", Active_dates)
    # print("captions: ",captions)
def main():
    analyze_data()

main()

