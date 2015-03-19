import vk
import webbrowser
import urllib.request
from urllib.parse import urlparse, parse_qs
from os.path import isfile
import os


OWNER_ID = '17530607'
APP_ID = '4805368'
SCOPE = 'audio'

class AuthVK():
    def __init__(self,app_id,scope):
        self.app_id = app_id
        self.scope = scope

        self.auth_in_browser()
        self.parse_redirect_url()

    def auth_in_browser(self):
        url = 'https://oauth.vk.com/authorize?' \
              'client_id={app_id}&' \
              'scope=audio&' \
              'redirect_uri=https://oauth.vk.com/blank.html&' \
              'display=page&v=5.0&' \
              'response_type=token'.format(app_id=self.app_id)
        webbrowser.open(url)
        print('Give access to your audio files and\n')
        self.redirect_url = input('Copy and paste url from address bar(click the right mouse button -> Paste) - ')

    def parse_redirect_url(self):
        parsed_URL = urlparse(self.redirect_url)
        parsed_fragment = parse_qs(parsed_URL.fragment)
        self.access_token = parsed_fragment.get('access_token')[0]

class Get_music(object):
    def __init__(self,access_token, owner_id=None):
        self.access_token = access_token
        self.owner_id = owner_id
        self.folder = 'vkmusic'
        self.download_music()

    def download_music(self):
        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass
        vkapi = vk.API(access_token=self.access_token)
        if self.owner_id == None:
            audio = vkapi.audio.get()
        else:
            audio = vkapi.audio.get(owner_id=self.owner_id)
        for i in range(0,len(audio['items'])):
            url = audio['items'][i]['url']
            audiofile = urllib.request.urlopen(url).read()
            filename = "{folder}{sep}{artist}{minus}{title}{expansion}".format(
                folder=self.folder,
                sep=os.sep,
                artist=audio['items'][i]['artist'],
                minus=' - ',
                title=audio['items'][i]['title'],
                expansion='.mp3')
            if isfile(filename):
                continue
            try:
                f = open(filename,'wb')
            except OSError:
                filename = "{folder}{sep}{owner}_{id}{expansion}".format(
                    folder=self.folder,
                    sep=os.sep,
                    owner=audio['items'][i]['owner_id'],
                    id=audio['items'][i]['id'],
                    expansion='.mp3')
                if isfile(filename):
                    continue
                f = open(filename,'wb')
            f.write(audiofile)
            f.close()
            print('{}{}{} was downloaded.\t{}/{}'.format(filename,i+1,len(audio['items'])))
        print('All audiofiles was downloaded')

if __name__== '__main__':
    auth = AuthVK(APP_ID,SCOPE)
    music = Get_music(auth.access_token)
    #music = Get_music(AuthVK.access_token,owner_id=OWNER_ID)   #just example
