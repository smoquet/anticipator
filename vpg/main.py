import argparse
import sys
from filemanager import *
from spotify import *
import time

def parse_arguments(args):
    print "init parse_arguments", time.clock()
    # expects commandline input, two positionals username+lineup_file, two optionals
    # returns four variables
    parser = argparse.ArgumentParser(
        description='Voorpret-gen - spotify playlist generator based on lineup',
        usage='voorpretgen [options] username lineup_file')
    parser.add_argument('username', help='Spotify username')
    parser.add_argument('lineup_file', help='File with one artist per line')
    parser.add_argument('-n', metavar='top X tracks', help='Number of tracks to add to playlist')
    parser.add_argument('-p', metavar='playlist', help='Playlist name (default = lineup filename)')

    args = parser.parse_args()
    lineup_file = args.lineup_file
    username = args.username
    top_x_tracks = args.n
    playlist_name = args.p
    print "exit parse_arguments", time.clock()
    return lineup_file, top_x_tracks, playlist_name, username

def initialise(args, settings_file):
    print "init initialise", time.clock()
    # expects commandline arguments for parse_arguments, and settings_file
    # returns lineup as list of strings, top tracks and playlist _name
    arguments = parse_arguments(args)
    username = arguments[3]
    top_x_set, client_id, client_secret, redirect_uri = read_settings(settings_file)
    spot_token = get_token(username, client_id, client_secret, redirect_uri)
    top_x_tracks = arguments[1] if arguments[1] else int(top_x_set)
    lineup = lineup_parser(arguments[0])
    # dit kan nog mooier, breekt nu als de file geen extensie heeft
    playlist_name = arguments[2] if arguments[2] else arguments[0][:-4]
    print "exit initialise", time.clock()
    return lineup, top_x_tracks, playlist_name, spot_token, username

def main(args):
    print "init main", time.clock()
    # expects commandline arguments for initialise
    # is base function for all other functions
    settings_file = 'voorpretgen/voorpretgen.ini'
    lineup, top_x_tracks, playlist_name, spot_token, username = initialise(args, settings_file)
    artist_ids = artist_id_list_gen(lineup, spot_token)
    track_id_list = tracklist_gen(artist_ids, top_x_tracks, spot_token)

    write_playlist(track_id_list, playlist_name, spot_token, username)
    # print 'track_id_list= ',
    # print track_id_list
    print "exit main", time.clock()

if __name__ == "__main__":
    # initialises this file, exits to system after calling main with commandline arguments
    sys.exit(main(sys.argv[1:]))
