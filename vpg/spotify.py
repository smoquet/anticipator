import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from main import *
import time

def get_token(sid, client_id, client_secret, redirect_uri):
    '''
    gets a token for user, and caches it for re-use.
    returns a (bool,token/url) tuple
        either (True, token) or (False, uri)
    '''
    print 'spotify.get_token entered'
    # called upon in initialise function
    spotify = spotipy.Spotify()
    scope = 'playlist-modify-private'
    # door module oauth2 aaan te roepen creeren we een object van classe SpitifyOAuth, die
    # initieren we met de input die tussen haakjes staat en slaan we op in sp_oauth
    # in de cache path is de naam van het bestand waarin de spotify token wordt opgeslagen.
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
        scope=scope, cache_path=".cache-" + sid )
    print 'sp_oauth =', sp_oauth
    # check to see if there is a cached token, by calling upon object in sp_oauth
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        # maak een url voor e bezoeker om heen te gaan een te authoriseren
        auth_url = sp_oauth.get_authorize_url()
        # return tupe with False and the redirect url in auth_url.
        return (False, auth_url)
    # otherwise return the token
    return (True, token_info['access_token'])

def get_username(spot_token):
    spotify = spotipy.Spotify(auth=spot_token)
    username = spotify.current_user()['id']

    return username

def make_token(spot_response, username, client_id, client_secret, redirect_uri):
    # gets a token from spotify and caches it
    scope = 'playlist-modify-private'
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
        scope=scope, cache_path=".cache-" + username )
    code = sp_oauth.parse_response_code(spot_response)
    #gets token and caches it in
    token_info = sp_oauth.get_access_token(code)
    return token_info['access_token']

def artist_id_list_gen(artist_list, spot_token):

    if artist_list != type(list):
        raise ValueError('artist_list is not a list , but a ', type(artist_list))
    '''
     expects artists as strings in a list
     returns list of id's as unicode strings
     and internally keeps track of search failures
     '''

    def remove_unicode(string):
        import unicodedata
        return unicodedata.normalize('NFKD', string).encode('ascii','ignore')


    def get_artist_id(name, spot_token):
        print "init get_artist_id", time.clock()
        print "artist name = ", name
        # expects artist name as string
        # returns the associated ID as unicode, if no spotipy search result returns input name
        i = 0
        l = 10
        spotify = spotipy.Spotify(auth=spot_token)
        # search for artist in spotipy, and assign first result to results
        results = spotify.search(q= 'artist:'+ name.lower(), limit = l, offset = i, type='artist')
        # print 'results abii= ', results
        number_of_results = len(results[u'artists'][u'items'])
        # print 'length_of_results =', length_of_results
        temp_list =[]
        # the if statement here implies a failed serach and thus an append
        if number_of_results == 0:
            temp_list.append(name)
        try:
            # search for id in results
            # print "exit get_artist_id", time.clock()
            for x in range(number_of_results):
                # test if name is exact match,
                if results[u'artists'][u'items'][x][u'name'].lower() == name:
                    # return the first exact match
                    return results[u'artists'][u'items'][x][u'id']
                else:
                    # if no return has been hit, append all mismatches in temp_list
                    temp_list.append(results[u'artists'][u'items'][x][u'id'])
        except IndexError:
            # print 'IndexError hit'
            # if no results at all (index error) return name
            print "exit get_artist_id", time.clock()
            # print 'returned name =', name
            return name
        # return the first result of mismatches (this return ony happens when all result are mismatches)
        # print 'returned temp_list[0] = ', temp_list[0]
        return temp_list[0]

    # append ID id_list or name in search_failure list
    artist_id_list = []
    artis_fail_search_list = []
    # x = remove_unicode(artist_list)
    # artist_list_as_type_list = x.split(',')


    # for name in artist_list_as_type_list:
    for name in artist_list:
        x = get_artist_id(name, spot_token)
        if type(x) == unicode:
            artist_id_list.append(x)
        else:
            artis_fail_search_list.append(name)

    return artist_id_list

def tracklist_gen(artist_id_list, n, spot_token):
    # expects list of artist id's and an integer for how many tracks per artists, maximum == 10!
    # returns a list of top track id's
    country_code = 'NL'
    spotify = spotipy.Spotify(auth=spot_token)
    top_tracks = []
    # print "tracklist_gen artist_id_list = ", artist_id_list
    # for each artist id, get the top track search results
    for artist_id in artist_id_list:
        top_tracks.append(spotify.artist_top_tracks(artist_id, country=country_code))

    # for each top track search result, get all the track id's within and append them
    top_track_ids = []
    # print 'top_tracks = ', top_tracks

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
    # print 'top_track_ids = ', top_track_ids
    return top_track_ids
    # return 0

def write_playlist(track_id_list, playlist_name, spot_token, username):
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
