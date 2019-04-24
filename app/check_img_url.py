import requests

def is_url_image(url):
	if not url:
		return False
	allowed_img_files = ("image/png", "image/jpeg", "image/jpg")
	r = requests.head(url)
	if r.headers["content-type"] in allowed_img_files:
	  return True
	return False
# Reference from stack overflow post:
# https://stackoverflow.com/questions/10543940/check-if-a-url-to-an-image-is-up-and-exists-in-python