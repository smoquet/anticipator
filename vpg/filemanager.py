import time

def lineup_parser(file_path):
    print "init lineup_parser", time.clock()
    # leest strings in lijst, split op hardreturns, negeert blank lines, en lowercased strings
    # returns list of artists as strings
    result = []
    with open(file_path) as f_in:
        lines = (line.rstrip() for line in f_in)
        lines = list(line for line in lines if line)
        for x in lines:
            result.append(x.lower())
        # print 'lines ==' , result
    print "exit read_settings", time.clock()
    return result

def read_settings(file_path):
    print "init read_settings", time.clock()
    # reads ini file and returns variables as list
    # the order is topX[0],  SPOTIPY_CLIENT_ID[1], SPOTIPY_CLIENT_SECRET[2], SPOTIPY_REDIRECT_URI[3]
    docum = open(file_path)
    lines = docum.readlines()
    result = []
    for x in lines:
        if x[0] == "[":
            next

        # this monster a) splits on '=', then selects the 2nd element, strips
        # newlines and '-s
        else: result.append(x.split('=')[1].rstrip().replace("'", ""))
    print "exit read_settings", time.clock()
    return result
