import urlparse

PLUGIN_PREFIX   = "/photos/xkcd"
CACHE_1YEAR = 365 * CACHE_1DAY
####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "xkcd", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("_List", viewMode="List", mediaType="items")

####################################################################################################

def MainMenu():
	dirTitle = 'XKCD'
	archiveURL = 'http://xkcd.com/archive/'
	archiveXPath = '//div[@class="s"]/h1/following-sibling::a'
	dir = MediaContainer(title1=dirTitle)
	
	for comic in HTML.ElementFromURL(archiveURL).xpath(archiveXPath):
		comicURL = urlparse.urljoin(archiveURL, comic.get('href'))
		try:
			title = comic.xpath('./font')[0].text
		except:
			title = comic.text
		dir.Append(Function(PhotoItem(GetPhotoItem, title=title, thumb=Function(GetPhotoItem, url=comicURL)), url=comicURL))
	return dir

def GetPhotoItem(url, sender=None):
	xpaths = ['//div[@class="s"]/a/img', '//div[@class="s"]/img']
	page = HTML.ElementFromURL(url, cacheTime=CACHE_1YEAR)
	for xpath in xpaths:
		imgs = page.xpath(xpath)
		if len(imgs) != 0:
			img = imgs[0].get('src')
			return Redirect(img)
