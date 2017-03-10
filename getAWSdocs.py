#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib, urlparse, os, argparse

def get_options():
  parser = argparse.ArgumentParser(description='AWS Documentation Downloader')
  parser.add_argument('-d','--documentation', help='Download the Documentation', action='store_true', required=False)
  parser.add_argument('-w','--whitepapers', help='Download White Papers', action='store_true', required=False)
  parser.add_argument('-f','--force', help='Overwrite old files', action='store_true', required=False)
  args = vars(parser.parse_args())
  return (args)

# Build a list of the amazon PDF's
def list_pdfs(start_page):
  html_page = urllib.urlopen(start_page)
  # Parse the HTML page
  soup = BeautifulSoup(html_page, 'html.parser')
  pdfs =  set()
  print "Generating PDF list (this may take some time)"
  for link in soup.findAll('a'):
    try:
      uri = link.get('href')
      # Allow whitepapers to be returned
      if "whitepapers" in start_page:
        if uri.endswith("pdf"):
          if "whitepapers" in uri or "enterprise-marketing" in uri:
            pdfs.add(uri)
      # Allow all documents to be returned
      if "documentation" in start_page:
        if uri.startswith("/documentation/"):
          if not (uri.endswith("/documentation/") or uri.endswith("/kindle/") or uri.startswith("/documentation/?nc") ):
            base_url = "http://aws.amazon.com"
            url = base_url + uri
	    # Parse the HTML sub page (this is where the links to the pdf's live)
    	    html_page_doc = urllib.urlopen(url)
	    soup_doc = BeautifulSoup(html_page_doc, 'html.parser')
	    # Get the A tag from the parsed page
	    for link in soup_doc.findAll('a'):
              try:
                sub_url = link.get('href')
                if sub_url.endswith("pdf"):
                  pdfs.add(sub_url)
              except:
                continue
    except:
     continue
  return pdfs

def save_pdf(full_dir,filename,i):
  if not os.path.exists(full_dir):
    os.makedirs(full_dir)
  # Open the URL and retrieve data
  file_loc = full_dir + filename
  if not os.path.exists(file_loc) or force == True:
    if i.startswith("//"):
      i = "http:" + i
    print "Downloading : " + i  
    web = urllib.urlopen(i)
    print "Saving to : " + file_loc
    # Save Data to disk
    output = open(file_loc,'wb')
    output.write(web.read())
    output.close()
  else:
    print "Skipping " + i + " - file exists or is a dated API document, use './getAWSdocs.py --force' to force override"


def get_pdfs(pdf_list, force):
  for i in pdf_list:
   doc = i.split('/')
   doc_location = doc[3]
   filename = urlparse.urlsplit(i).path.split('/')[-1]
   # Set download dir for whitepapers
   if "whitepapers" in doc_location:
     full_dir = "whitepapers/"
   else:
     # Set download dir and sub directories for documentation
     full_dir = "documentation/"
     directory = urlparse.urlsplit(i).path.split('/')[:-1]
     for path in directory:
       if path != "":
         full_dir = full_dir + path + "/"
   try:
     save_pdf(full_dir,filename,i)
   except:
     continue

# Main
args = get_options()
# allow user to overwrite files
force = args['force']
if args['documentation']:
  print "Downloading Docs"
  pdf_list = list_pdfs("https://aws.amazon.com/documentation/")
  get_pdfs(pdf_list, force)
if args['whitepapers']:
  print "Downloading Whitepapaers"
  pdf_list = list_pdfs("http://aws.amazon.com/whitepapers/")
  get_pdfs(pdf_list, force)
  print "Downloading SAP Whitepapaers"
  pdf_list = list_pdfs("https://aws.amazon.com/sap/whitepapers/")
  get_pdfs(pdf_list, force)
