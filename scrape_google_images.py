import mechanicalsoup as ms
import os
import wget

browser = ms.StatefulBrowser()

url = "https://www.google.com/search?q=cat&sxsrf=ALeKk02OouVpPFDXjIrDvJmBUg6nnDeDAw:1610807126259&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj3nr-U1KDuAhW3QRUIHXhFBCgQ_AUoAXoECBQQAw&biw=1366&bih=695"
if browser.open(url) == '<Response [200]>':
	print('Page Access was successful')

# target the search form
browser.select_form()
browser.get_current_form()

search_term = 'olamide'
browser['q'] = search_term


response = browser.submit_selected()

print('New URL: ', browser.get_url())

new_url = browser.get_url()
browser.open(new_url)

# get HTML code
page = browser.get_current_page()

all_images = page.find_all('img')

# target the src
img_src = []
for img in all_images:
	image = img.get('src')
	img_src.append(image)

print('Total image source stored', len(img_src))

img_src = [img for img in img_src if img.startswith('https')]

# create a local repo to store cat images
path = os.getcwd()
path = os.path.join(path, search_term + "s")
print(path)

os.mkdir(path)

# download the images
counter = 0
for img in img_src:
	save_as = os.path.join(path, search_term +str(counter)+'.jpg')
	wget.download(img, save_as)
	counter += 1
