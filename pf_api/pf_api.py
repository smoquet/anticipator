# from Naked.toolshed.shell import execute_js
from Naked.toolshed.shell import muterun_js
import json
import time

def event_run(args):
    ''' Node.js wrapper function. Calls event.js with the provided args. '''

    response = muterun_js('event.js', args)

    if response.exitcode == 0:
        # print response.stdout

        # all went well, create python object with the returned json
        loaded_json = json.loads(response.stdout)
    else:
      return 'jammer joh'
    return loaded_json

def eventsearch(query, num):
    '''
    Searches PF for 'query' and returns 'num' events
    events have 'stamp', id' and 'name'
    '''

    args = 'eventsearch' + ' "' + query + '"'
    loaded_json = event_run(args)

    parties = loaded_json['0']['party']['party']
    # print list(reversed(parties))[0]
    found_parties = []
    # events are returned chronologically, here we reverse this
    for party in list(reversed(parties))[0:num]:
        found_parties.append(party)
    return found_parties

def lineupsearch(event_id):
    ''' Searches PF for the lineup for 'event_id' '''

    args = 'lineupsearch' + ' ' + str(event_id)
    loaded_json = event_run(args)

    # events without lineup don't have 'area'
    try:
        areas = loaded_json['0']['party']['area']
        # print loaded_json
        found_artists = []
        for area in areas:
          lineup = area['lineup']

          # this needs to be on a t-shirt:
          for artist in lineup:
              if artist['type'] == 'mc':
                  # Fuck MCs
                  next

              else:
                  found_artists.append(artist['artist']['name'])
        return found_artists
    except KeyError:
        print 'event heeft geen lineup'


# lineupsearch('311374')
# print lineupsearch('317209')
# lineupsearch('325641') # lijkt leeg
# print eventsearch('frenchcore', 5)
