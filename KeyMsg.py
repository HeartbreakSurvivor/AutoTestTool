class KeyMsg(object):
    def __init__(self,name,key,content,iscustomer=0):
        self.isCustomize = iscustomer
        self.name = name
        self.EntityKey = key
        self.Content = content

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

