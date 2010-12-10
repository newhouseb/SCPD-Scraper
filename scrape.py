import re
import os
import passwords
import sys
from subprocess import Popen
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from multiprocessing import Pool

def download(work):
	if os.path.exists(work[1]):
		print "Already downloaded", work
		return

	print "Starting", work
	# Put it in a temp file
	if os.system("mimms -c %s %s" % (work[0], "_" + work[1])) == 0:
		# Move the file on success
		os.system("mv %s %s", "_" + work[1], work[1])
	print "Finished", work

if __name__ == '__main__':
	# Pretend we're just a regular old user (this is naughty, don't try this at home kids)
	br = Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9')]
	br.set_handle_robots(False)
	br.open("https://myvideosu.stanford.edu/oce/currentquarter.aspx")
	assert br.viewing_html()

	# Import from a module outside of version control your SUNET id and password
	br.select_form(name="login")
	br["username"] = passwords.my_username
	br["password"] = passwords.my_password

	# Open the course page for the title you're looking for 
	response = br.submit()
	response = br.follow_link(text=sys.argv[1])

	# Build up a list of lectures
	links = []
	for link in br.links(text="WMP"):
		links.append(re.search(r"'(.*)'",link.url).group(1))

	videos = []
	# These are done serially purely just to not look suspicious, we could probably parallelize this as well
	for link in links:
		response = br.open(link)
		soup = BeautifulSoup(response.read())
		video = soup.find('object', id='WMPlayer')['data']
		video = re.sub("http","mms",video)
		output_name = re.search(r"[a-z]+[0-9]+[a-z]?/[0-9]+",video).group(0).replace("/","_") + ".wmv"
		videos.append((video, output_name))

	# Make a thread pool and download 5 files at a time
	p = Pool(processes=5)
	p.map(download, videos)
