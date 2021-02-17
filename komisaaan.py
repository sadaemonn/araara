import subprocess, os, sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    from bs4 import BeautifulSoup
except ImportError:
    install("bs4")
try:
    import requests
except ImportError:
    install("requests")
try:
    from PIL import Image
except ImportError:
    install("Pillow")
#initialize
url = input("Enter a chapter url from mangaread.co:\n")
print("\nPlease wait. It may take 1 minute... (depends on the number of pages)\n")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

directory = str(soup.find("li", class_="active").text)[13:-44]
if os.path.isdir(directory) != True:
    os.mkdir(directory)
pages = soup.find("div", class_="select-pagination")
links = pages.find_all("option")

#fetch the images
n = 0
for link in links:
    newUrl = link["data-redirect"]
    response = requests.get(newUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    img = soup.find("img", class_="wp-manga-chapter-img")
    if n < 10: a = "00"
    elif 9 < n < 100: a = "0"
    else: a = ""
    with open(directory+"/"+ "image-%s" % a + str(n) +".jpg", 'wb') as f:
        f.write(requests.get(img["src"]).content)
    n += 1

#create a pdf
imageList = []
directory = directory + '/'
for item in os.listdir(directory)[1:]:
    imag = Image.open(directory + item)
    imageList.append(imag)
img1 = Image.open(directory + 'image-000.jpg')
img1.save(directory[:-1] + '.pdf', save_all=True, append_images=imageList)

#delete the pictures, keep the pdf
for item in os.listdir(directory):
    os.remove(directory + item)
os.rmdir(directory)

print("Done! Check your pdf file. It's located at the same directory as this file.")
