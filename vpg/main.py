import sys
import string
import time
import random
import spotify
import filemanager

def initialise(sid):
#must eventully expect arguments from form
    # must ventueally return lineup as list of strings, top tracks and playlist_name, sort+public bools, token, username
    settings_file = 'vpg/voorpretgen.ini'
    top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)
    # Pass sid along for cache storage
    spot_token = spotify.get_token(sid, client_id, client_secret, redirect_uri)
    # top_x_tracks = arguments[1] if arguments[1] else int(top_x_set)
    top_x_tracks = int(top_x_set)
    # lineup = lineup_parser(arguments[0])
    lineup = ['henk', 'angerfist']
    # dit kan nog mooier, breekt nu als de file geen extensie heeft
    # playlist_name = arguments[2] if arguments[2] else arguments[0][:-4]
    playlist_name = 'henk'
    # print "exit initialise", time.clock()
    return lineup, top_x_tracks, playlist_name, spot_token

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
