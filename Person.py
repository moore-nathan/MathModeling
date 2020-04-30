class Person:
    def __init__(self, type, daysSick=0, numInfected=0):
        self.type = type
        self.daysSick = daysSick
        self.numInfected = numInfected

    def __repr__(self):
        return 'Person(%r, %r)' %(self.type, self.daysSick, self.numInfected)
