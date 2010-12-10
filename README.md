This new version has fewer dependencies and is generally more useful...

Installation
============
    git clone git@github.com:newhouseb/SCPD-Scraper.git
    sudo easy_install mechanize
    sudo easy_install BeautifulSoup
    sudo port install mimms
    echo "my_username = \"[YOUR SUNETID]\"; my_password = \"[YOUR SUNET PASSWORD]\"" > passwords.py

Running
=======
    python scrape.py [Name of the course exactly as listed on SCPD]

So for example
    python scrape.py "Introduction to Linear Dynamical Systems"

Notes
=====
It appears that each stream is throttled to about ~80kbp/s (I'm off campus though might be different on campus), but there's nothing preventing you from pipelining multiple streams at once.  This by default runs 5 concurrent streams, if you want to up this, change the line that says processes=5

This also does no magic encoding because that can be done later (i.e. after Stanford takes everything down) and people might be picky on what format they want anyway. Originally I had this set up to encode form wmv into an iPhone friendly format, but that added a lot of gross dependencies.

Until the stream finishes it puts it at a temporary filename prefixed by a "_", that way if everything dies you don't have to go see which one's didn't fully download by opening them.  There's a mimms flag to resume automatically too, but I'm not sure of what happens when there is nothing to resume (and I'm currently downloading a bunch of things and don't feel like experimenting).

Since this uses multiprocessing, it might be tricky to Ctrl-C out of.  You can always just `killall python`
