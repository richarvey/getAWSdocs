#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse
import posixpath
import os
import sys

# Build a list of the amazon service sections
def get_services():
    html_page = urllib2.urlopen("http://aws.amazon.com/documentation/")
    # Parse the HTML page
    soup = BeautifulSoup(html_page)
    urls = []
    services = []
    # Get the A tag from the parsed page
    for link in soup.findAll('a'):
        try:
            url = link.get('href')
	    # ignore links to self
	    if url.startswith("/documentation/"):
                #print link.get('href')
		if not (url.endswith("/documentation/") or url.startswith("/documentation/?nc") ):
		    services.append(link.get('href'))
		    directory = "." + link.get('href')
		    if not os.path.exists(directory):
		        os.makedirs(directory)
        except: continue
    return services

# Download the PDFs that exist on the service pages
def get_pdfs(services):
    base_url = "http://aws.amazon.com"
    for uri in services:
	# Construct the ful URL for the service page
	url = base_url + uri
	print "\nDownloading PDF's for : " + url + "\n"
	# Parse the HTML page
	html_page_doc = urllib2.urlopen(url)
	soup_doc = BeautifulSoup(html_page_doc)
	# Get the A tag from the parsed page
	for link in soup_doc.findAll('a'):
            pdf = link.get('href')
	    # Check link is a PDF file
	    try:
		check = pdf.endswith("pdf")
	    except: continue
	    # Now download if the link is a PDF file
            if check == True:
		# We need to work out the file name for saving
                path = urlparse.urlsplit(pdf).path
                filename = "." + uri + posixpath.basename(path)
        # Nasty. AWS have uploaded ALL API versions as PDFs, not just the latest.
        # They are all named as <service><docname><date>.pdf so we are
        # just checking the last character before the dot and skipping download
        # if it is a digit.
		if (not (os.path.isfile(filename) or filename[len(filename) - 5 ].isdigit()) or (len(sys.argv) > 1 and sys.argv[1] == "--force")):
			print "Downloading : " + pdf
			# Open the URL and retrieve data
			try:
				web = urllib2.urlopen(pdf)
				print "Saving to : " + filename
				# Save Data to disk
				output = open(filename,'wb')
				output.write(web.read())
				output.close()
			except: continue
		else:
			print "Skipping file " + filename + " - file exists or file is a dated API PDF, use './getAWSdocs.py --force' to force download"

services_list = get_services()
get_pdfs(services_list)
