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

    def isCached(self, key):
        return len(glob("data/cache/" + key +".*")) > 0

    def cache(self, key, data):
        if self.isCached(key):
            return
        if isinstance(data, str):
            file = open("data/cache/"+key+".txt", 'w')
            file.write(data)
            file.close()
        else:
            np.save("data/cache/"+key, data)

    def getCache(self, key):
        files = glob("data/cache/" + key +".*")
        if len(files) > 0:
            file = files[0]
            head, tail = os.path.split(file)
            key, ext = os.path.splitext(tail)
            if ext == ".npy":
                result = np.load(file).flat[0]
            elif ext == ".txt":
                file = open(file, 'r')
                result = file.read()
                file.close()
        return result

    


