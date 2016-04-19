import sys
import spotipy
import spotipy.util as util
from main import *
import time



def get_token(username, client_id, client_secret, redirect_uri):
    spotify = spotipy.Spotify()
    scope = 'playlist-modify-private'
    token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return token

def artist_id_list_gen(artist_list, spot_token):
    # expects artists as strings in a list
    # returns list of id's as unicode strings and internally keeps track of search failures

    def get_artist_id(name, spot_token):
        print "init get_artist_id", time.clock()
        # expects artist name as string
        # returns the associated ID as unicode, if no spotipy search result returns input name
        i = 0
        l = 10
        spotify = spotipy.Spotify(auth=spot_token)
        # search for artist in spotipy, and assign first result to results
        results = spotify.search(q= 'artist:'+ name, limit = l, offset = i, type='artist')

        try:
            # search for id in results
            print "exit get_artist_id", time.clock()
            temp_list =[]

            for x in range(l):
                # test if name is exact match,
                if results[u'artists'][u'items'][x][u'name'].lower() == name:
                    # return the first exact match
                    return results[u'artists'][u'items'][x][u'id']
                else:
                    # if no return has been hit, append all mismatches in temp_list
                    temp_list.append(results[u'artists'][u'items'][x][u'id'])
        except IndexError:
            # if no results at all (index error) return name
            print "exit get_artist_id", time.clock()
            return name
        # return the first result of mismatches (this return ony happens when all result are mismatches)
        return temp_list[0]

    # append ID id_list or name in search_failure list
    artist_id_list = []
    artis_fail_search_list = []
    for name in artist_list:
        x = get_artist_id(name, spot_token)
        if type(x) == unicode:
            artist_id_list.append(x)
        else:
            artis_fail_search_list.append(name)

    return artist_id_list

def tracklist_gen(artist_id_list, n, spot_token):
    print "init tracklist_gen", time.clock()
    # expects list of artist id's and an integer for how many tracks per artists, maximum == 10!
    # returns a list of top track id's
    country_code = 'NL'
    spotify = spotipy.Spotify(auth=spot_token)
    top_tracks = []
    # for each artist id, get the top track search results
    for artist_id in artist_id_list:
        top_tracks.append(spotify.artist_top_tracks(artist_id, country=country_code))

    # for each top track search result, get all the track id's within and append them
    top_track_ids = []
    for x in top_tracks:
        count = 0
        for x in x[u'tracks']:
            count += 1
            if count <= n:
                top_track_ids.append(x[u'id'])
    # print spotify.track(top_track_ids[0])
    # print spotify.track(top_track_ids[5])
    # print top_track_ids
    # print 'len =' , len(top_track_ids)
    print "exit tracklist_gen", time.clock()
    return top_track_ids
    # return 0

def write_playlist(track_id_list, playlist_name, spot_token, username):
    print "init write_playlist", time.clock()
    # writes playlist in spotify
    # initialised in main
    # returns nothing
    spotify = spotipy.Spotify(auth=spot_token)
    # print 'name = ', playlist_name
    # creates a private playlist in spotify for current user
    playlist = spotify.user_playlist_create(username, playlist_name, public=False)
    playlist_id = playlist['id']
    # adds tracks in playlist that was just created
    for i in range(len(track_id_list)/100 + 1):
        try:
            # print track_id_list[i*100:(i+1)*100]
            spotify.user_playlist_add_tracks(username, playlist_id, track_id_list[i*100:(i+1)*100], position=None)
        except IndexError:
            # print track_id_list[i*100:]
            spotify.user_playlist_add_tracks(username, playlist_id, track_id_list[i*100:], position=None)
    print "exit write_playlist", time.clock()
