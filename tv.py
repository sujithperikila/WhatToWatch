from datetime import datetime
import os
import requests
import datetime

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

    def get_cast(self,id):
        url = 'https://api.tvmaze.com/shows/'+str(id)+'/cast'
        cast = requests.get(url,verify=False)
        if cast.status_code==200:
            cast_list = []
            cast = cast.json()
            for per in cast:
                cast_list.append(per['person']['name'])

        return cast,cast_list
    def get_show_details(slef,id):
        url = 'https://api.tvmaze.com/shows/'+str(id)
        data = requests.get(url,verify=False)
        if data.status_code==200:
            return data.json()

    def get_shows_today(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        # url = 'https://api.tvmaze.com/schedule/web?date='+str(date)    # date in year-month-day format
        url = 'https://api.tvmaze.com/schedule/'
        s = requests.get(url,verify=False)
        if s.status_code == 200:
            shows_list = []
            s = s.json()
            for x in s:
                if x['show']['rating']['average'] != None:
                    shows_list.append(x['show'])
            if len(shows_list)>0:
                newlist = sorted(shows_list, key=lambda d: d['rating']['average'])
                return newlist[::-1]
            else:
                return []
        else:
            return []




if __name__=="__main__":
    obj = show()
    # cast,c_list=obj.get_cast(36708)
    # print(c_list)
    
    ans = obj.get_shows_today()