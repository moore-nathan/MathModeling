class Person:
    def __init__(self, id, type, daysSick=0, numInfected=0):
        self.numInfected = numInfected
        self.type = type
        self.daysSick = daysSick
        self.id = id

    def __repr__(self):
        return 'Person(%r, %r, %r %r)' %(self.id, self.type, self.daysSick, self.numInfected)
