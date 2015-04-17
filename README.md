# getAWSdocs

### About

One thing that strikes me as odd with Amazon and the documentation on AWS is that there is no download all button, to make it easy to get all the documentation in one go. After creating a simple bash script that kept breaking and needed updating, I decided to rewrite in python to make it a little easier to maintain.  

I hope some of you find this useful.

### Requirements

Make sure all these python modules are intalled:

+ BeautifulSoup
+ urllib2
+ urlparse

example:

```bash
sudo pip install BeautifulSoup
```

### Usage

To get all documents:

```bash
./getAWSdocs.py
```

Files that exist on disk will not be re-downloaded (so by default only new sections/files are downloaded). To override this default and force re-download of files that exist on disk, use

./getAWSdocs.py --force

Thats it!

[@ric_harvey](https://twitter.com/ric_harvey)
[@paulwakeford] (https://twitter.com/paulwakeford)
