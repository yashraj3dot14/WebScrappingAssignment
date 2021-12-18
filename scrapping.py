import numpy
import requests
from bs4 import BeautifulSoup
from PIL import Image

import pytesseract
from scipy import ImageFilter
from scipy.ndimage import gaussian_filter
import mechanize

req = requests.get("#")

soup = BeautifulSoup(req.content, "html.parser")

#print(soup.prettify())

#fecthing options
select_tag = soup.find("select")
options = select_tag.find_all("option")
option_value = []
for option in options:
    option_value.append(option)


#fetching captcha
threshold1 = 140
threshold2 = 140
sigma = 1.5
captcha = soup.find('img')['src']
org_img = Image.open(captcha)
org_img.save("org.png")
bnw = org_img.convert('L') #converting black and white
bnw.save('bnw.png')

first_threshold = bnw.point(lambda px : px >threshold1 and 255)
first_threshold.save(first_threshold.png)
blur = numpy.array(first_threshold) #we are creating image array here
blur_img = gaussian_filter(blur, sigma= sigma)
blur_img = Image.fromarray(blur_img)
blur_img.save('blur.png')

final_img = blur_img.point(lambda px : px > threshold2 and 255)
final_img = final_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
final_img = final_img.filter(ImageFilter.SHARPEN)
final_img.save('final.png')
captcha_numbers = pytesseract.image_to_string(Image.open('final.png'))


#for filling textbox and submit
browser = mechanize.Browser()
browser.open("https://drt.gov.in/front/page1_advocate.php")
browser.select_form(nr=0)
browser["name"] = "sha" #filling textbox
response = browser.submit()
browser.submit() #submitting the form
