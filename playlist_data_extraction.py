import pandas as pd
import requests
import json
import config

class DataExtractor:

    @classmethod
    def retrieve_playlist_content(cls, playlist_id):

        #API request to retrieve playlist data
        url = "https://spotify-scraper.p.rapidapi.com/v1/playlist/contents"

        querystring = {"playlistId":f"{playlist_id}"}

        headers = {
            "X-RapidAPI-Key": config.playlist_api_key,
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        try:
            #Save playlist content as json file
            playlist_content = response.json()

            with open(f"{playlist_id}_content.json", "w") as f:
                json.dump(playlist_content, f)
        except:
            print(response.status_code)
    
    @classmethod
    def playlist_to_song_data(cls, playlist_id):
        #Note: retrieve_playlist_content() method needs to be run beforehand

        #Open json file with playlist content
        f = open(f"{playlist_id}_content.json")

        playlist_content = json.load(f)
        try:
            #Extract relevant song info from playlist content
            url = [x["shareUrl"] for x in playlist_content["contents"]["items"]]
            song_name = [x["name"] for x in playlist_content["contents"]["items"]]
            song_id = [x["id"] for x in playlist_content["contents"]["items"]]
            release_year = [x["album"]["date"] for x in playlist_content["contents"]["items"]]

            #Convert song data to dataframe
            song_dict = {"url": url,
                        "title": song_name,
                        "spotify_id": song_id,
                        "release_year": release_year}

            df = pd.DataFrame(song_dict)
            return df
        
        except:
            print(playlist_content)
            raise KeyError

        

if __name__ == "__main__":

    #Add playlist id found on spotify
    playlist_id = "1lZcsX16FNzMdcdUatMHbf"

    #Get playlist content using API
    playlist = DataExtractor.retrieve_playlist_content(playlist_id)

    try:
        #Try extracting song data
        df = DataExtractor.playlist_to_song_data(playlist_id)

        df.to_csv("schlager_songs.csv", mode= "a", index= False, header= False)

        songs = pd.read_csv("schlager_songs.csv")

        songs.drop_duplicates(inplace= True)
        print(songs)
        print(songs.info())

    except:
        #Print playlist data if relevant song data can't
        #be extracted
        file = open(f"{playlist_id}_content.json")
        file_content = json.load(file)
        print(file_content)
    