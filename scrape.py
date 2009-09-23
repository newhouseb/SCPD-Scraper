import re
import os
import passwords
from subprocess import Popen
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

br = Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9')]
br.set_handle_robots(False)
br.open("https://myvideosu.stanford.edu/oce/currentquarter.aspx")
#response = br.open('https://myvideosu.stanford.edu/OCE/GradCourseInfo.aspx?coll=54f5f14a-e940-41c4-9283-dc715c794a98')
assert br.viewing_html()
#print response.read()

br.select_form(name="login")
br["username"] = my_username
br["password"] = my_password

response = br.submit()
response = br.follow_link(text="Compilers")

links = []
for link in br.links(text="WMP"):
	links.append(re.search(r"'(.*)'",link.url).group(1))

for link in links:
	response = br.open(link)
	soup = BeautifulSoup(response.read())
	video = soup.find('object', id='WMPlayer')['data']
	video = re.sub("http","mms",video)

	output_name = re.search(r"[a-z]+[0-9]+/[0-9]+",video).group(0).replace("/","_") + ".wmv"

	if not os.path.exists(output_name):
		os.system("mplayer -dumpstream -dumpfile %s %s" % (output_name, video))
		os.system("podencoder %s" % output_name)
