import numpy as np
from glob import glob
import os
class Cache:
    def __init__(self):
        self._cache = {}
        self.loadCache()

    def loadCache(self):
        if not os.path.exists("data/cache"):
         os.makedirs("data/cache")
        files = glob("data/cache/*.*")
        for file in files:
            head, tail = os.path.split(file)
            key, ext = os.path.splitext(tail)
            if ext == ".npy":
                self._cache[key] = np.load(file).flat[0]
            elif ext == ".txt":
                file = open(file, 'r')
                self._cache[key] = file.read()
                file.close()

    def isCached(self, key):
        return key in self._cache

    def cache(self, key, data):
        self._cache[key] = data
        if isinstance(data, str):
            file = open("data/cache/"+key+".txt", 'w')
            file.write(data)
            file.close()
        else:
            np.save("data/cache/"+key, data)

    def getCache(self, key):
        return self._cache[key]

    


