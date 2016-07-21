import filemanager
import os
import random
import sys
import string
import spotify
import time

def initialise():
    '''reads settings file and fills vars with the read values and some defaults'''
    settings_file = 'vpg/voorpretgen.ini'
    top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)
    top_x_tracks = int(top_x_set)

    # on Heroku the SPOTIPY_REDIRECT_URI env var is set to the production url
    # the following code ensures that is used
    if os.environ.get('SPOTIPY_REDIRECT_URI'):
        redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
    return top_x_tracks, client_id, client_secret, redirect_uri

def init_spot(redirect_uri, client_id, client_secret, sid):
    '''gets spotify token and username
    spot_token is either the spot_token or redirect_uri
    '''
    # on Heroku the SPOTIPY_REDIRECT_URI env var is set to the production url
    # the following code ensures that is used
    if os.environ.get('SPOTIPY_REDIRECT_URI'):
        redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
    spot_token = spotify.get_token(sid, client_id, client_secret, redirect_uri)
    # if we have a spot_token, get the username
    username = spotify.get_username(spot_token[1]) if spot_token[0] else ''
    return spot_token, username

def main(args):
    print "init main", time.clock()
    # expects commandline arguments for initialise
    # is base function for all other functions
    settings_file = 'vpg/voorpretgen.ini'
    lineup, top_x_tracks, playlist_name, spot_token, username = initialise(args, settings_file)
    if not spot_token:
        return
    artist_ids = spotify.artist_id_list_gen(lineup, spot_token)
    track_id_list = tracklist_gen(artist_ids, top_x_tracks, spot_token)

    # write_playlist(track_id_list, playlist_name, spot_token, username)
    # print 'track_id_list= ',
    # print track_id_list
    print "exit main", time.clock()

if __name__ == "__main__":
    # initialises this file, exits to system after calling main with commandline arguments
    sys.exit(main(sys.argv[1:]))
