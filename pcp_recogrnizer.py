import time
import json
import sys
import string
import threading
from concurrent.futures  import ThreadPoolExecutor

'''
    Given a Post Correspondence Problem instance, this class carries out a parallel search for a match.
'''
class pcp_recognizer:
    def __init__(self, x:list,y:list,num_threads):
        self.match =[]
        self.mLock  = threading.Lock()
        self.x = x
        self.executor = ThreadPoolExecutor(num_threads)
        self.done = False
        self.y = y
        self.futures = []

    def isPartialMatch(self,x:str,y:str)->bool:
        non_empty = len(x) > 0 and len(y)>0
        return non_empty and ( x.startswith(y) or y.startswith(x))

    def isMatch(self,x:str,y:str)->bool:
        non_empty = len(x) > 0 and len(y)>0
        return non_empty and (x==y)

    '''
        Search for a match; that is a sequence of indexes i1,..,in
        Such that x[i1]x[i2]...x[in] = y[i1]...y[in]
    '''
    def search(self,xs,ys,indexes):
        if(self.done ):
            return
        if(self.isMatch(xs,ys)):
            self.setDone(indexes)
        
        for i in range(len(self.x)):
            #Can we extend the partial match xs,ys with the i'th tuple
            if(self.isPartialMatch(xs + self.x[i] , ys + self.y[i])):
                nindex = indexes + [i]
                try:
                    '''
                        (xs + self.x[i] ,  ys + self.y[i] ) is a partial match so might lead
                        to a solution.
                        Schedule a search down this path
                    '''
                    f= self.executor.submit(self.search, xs + self.x[i],ys + self.y[i],nindex)
                    self.futures.append(f)
                except:
                    # executor possibly shutdown, because a match has been found.
                    break

    def setDone(self,indexes:list):
        self.mLock.acquire()
        self.match = indexes
        self.done = True
        print("[*] Found A Match \n", self.match)
        self.executor.shutdown(wait=False)
        self.mLock.release()

def main():
    # Read in the problem instance
    with open('pcp.config.json') as config_f:
        config = json.load(config_f)
        x,y,num_threads = config['x'],config['y'],config['num_threads']
        assert(len(x) == len(y))     
        print("[*] Searching for a match...")
        print(f"[*] Using {num_threads} Threads...")
        print("{0:15s} {1}".format("[*] Input is : ", x))
        print(f"{str.rjust(str(y),16 + len(str(y)))}")

    #Start the search
    p = pcp_recognizer(x,y,num_threads)
    p.search('','',[])
    
    while not p.done:
        time.sleep(2)
    
    #Found a match so cancel all scheduled searches
    for f in p.futures:
        f.cancel()

if __name__ == "__main__":
    main()