var Partyflock = require('partyflock');
var fs = require('fs');
var moment = require('moment');

var consumerKey = '4ba03d0a359ec1d0'

// pull consumerSecret from env var or file
if (process.env.PF_SECRET) {
  // console.log('env var found')
  var consumerSecret = process.env.PF_SECRET
  // console.log(consumerSecret)
}
else {
  var consumerSecret = fs.readFileSync("./pf_api/pf.secret", "utf8").trim();
}

var partyflockInstance = new Partyflock(consumerKey, consumerSecret, 'partyflock.nl', true)

// var artist = partyflockInstance.artist.search('frontl%').then(function(res) {
//   console.log(arguments[0])
// })

// read commandline arguments
process.argv.forEach(function (val, index, array) {
  // console.log(index + ': ' + val);
  // console.log(typeof(val));
});

//mode selector
var mode = process.argv[2]

if (mode == 'eventsearch') {
  // ugly 'function' equivalent since I cba to write proper JS
  // searches PF api for events

  // accept search query and replace spaces with % for PF api (% = *, so this is not an exact match, but good enough)
  var searched_event = process.argv[3].split(' ').join('%');

  var headers = {
    // search for matching parties from t+2 years backwards (2 years = 63072000s)
    'Pf-ResultWish': 'party(name=%'+searched_event+'%,stamp<'+(moment.utc().unix() + 63072000)+')'
  };

  // console.log(headers);

  // Returns array with party Objects filled according to headers specification
  var event = partyflockInstance.party.search(searched_event, headers).then(function(res) {
    console.log(JSON.stringify(arguments))

  //catch errors
  }).catch(console.log)
}
else if (mode == 'lineupsearch') {
  // searches PF api for lineup given an event_id
  var event_id = process.argv[3];

  var headers = {
    // specify which details we want from PF
 'Pf-ResultWish': 'party(name,area(lineup(artist(name),type)))'
  };

  // console.log(headers);
  // console.log(event_id);

  // Returns array with artist Objects
  var event = partyflockInstance.party.lookup(event_id, headers).then(function(res) {
    console.log(JSON.stringify(arguments))

  // catch errors
  }).catch(console.log)
}
