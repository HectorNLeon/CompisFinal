class Direcciones(object):
    def __init__(self, start, end):
            self.start = start
            self.end = end
            self.actual = self.start

    def getDir(self):
        self.actual += 1
        if(self.actual > self.end):
            return -1 
        return self.actual - 1
        
    def increaseDir(self, num):
        self.actual += num
        if(self.actual > self.end):
            return -1

    def getSize(self):
        size = self.end - self.start
        self.actual = self.start
        return size

    def resetActual(self):
        self.actual = self.start


