class KeyMsg(object):
    def __init__(self):
        self.isCustomize = False

    def setName(self,name):
        self.name = name

    def setEntityKey(self,key):
        self.EntityKey = key

    def setContent(self,content):
        self.Content = content

    def setCustomize(self,num):
        self.isCustomize = num

    #Get methond
    def isCustomizeOrnot(self):
        return True if self.isCustomize else False

    def getName(self):
        return self.name

    def getEntityKey(self):
        return self.EntityKey

    def getContent(self):
        return self.Content

