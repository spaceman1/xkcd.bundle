from PMS import Plugin, Log, DB, Thread, XML, HTTP, JSON, RSS, Utils
from PMS.MediaXML import MediaContainer, DirectoryItem, PhotoItem

PLUGIN_PREFIX   = "/photos/xkcd"
XKCD_BASE        = "http://www.xkcd.com"
archived = "new"

####################################################################################################
def Start():
  Plugin.AddRequestHandler(PLUGIN_PREFIX, HandlePhotosRequest, "xkcd", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", contentType="items")

####################################################################################################
def HandlePhotosRequest(pathNouns, count):
  dir = MediaContainer("art-default.jpg", "InfoList", "xkcd")
  global archived
  if archived == "new":
    archived = XML.ElementFromString(HTTP.GetCached(XKCD_BASE + "/archive/", 10000), True).xpath('//div[@id="middleContent"]//a')

  for item in archived[count*20:count*20+20]:
    title = item.text
    imgHTML = XML.ElementFromString(HTTP.GetCached(XKCD_BASE + item.get("href"), 10000), True).xpath('id("middleContent")//img')[0]
    img = imgHTML.get("src")
    desc = imgHTML.get("title")
    subtitle = item.get('title')
    ph = PhotoItem(img, title, desc, img)
    ph.SetAttr('subtitle',subtitle)
    dir.AppendItem(ph)
  dir.AppendItem(DirectoryItem("next20","Next 20...",""))
    
  return dir.ToXML()
