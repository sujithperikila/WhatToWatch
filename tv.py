import os
import sqlite3
import requests


class show:
    def __init__(self):
        pass
    def search(self,term):
        url = 'https://api.tvmaze.com/search/shows?q='+str(term)
        show_matches = requests.get(url,verify=False)
        if show_matches.status_code==200:
            show_list = []
            show_matches = show_matches.json()
            for match in show_matches:
                if match['score']>=0.5:
                    show_list.append(match['show'])
                
            return show_list
        else:
            return []








if __name__=="__main__":
    obj = show()
    ans = obj.search('legacies')
    print(ans)
    
