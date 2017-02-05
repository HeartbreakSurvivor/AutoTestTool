class KeyMsg(object):
    def __init__(self):
        self.isCustomize = 0

    def setName(self,name):
        self.name = name

    def setEntityKey(self,key):
        self.EntityKey = key

    def setContent(self,content):
        self.Content = content

    def setCustomize(self,num):
        self.isCustomize = num

    #Get methond
    def getName(self):
        return self.name

    def getEntityKey(self):
        return self.EntityKey

