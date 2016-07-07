var Partyflock = require('partyflock');
var fs = require('fs');
var moment = require('moment');

var consumerKey = '4ba03d0a359ec1d0'
var consumerSecret = fs.readFileSync("./pf.secret", "utf8").trim();

var partyflockInstance = new Partyflock(consumerKey, consumerSecret, 'partyflock.nl', true)

// var artist = partyflockInstance.artist.search('frontl%').then(function(res) {
//   console.log(arguments[0])
// })

process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
  console.log(typeof(val));
});

var mode = process.argv[2]

if (mode == 'eventsearch') {
  var searched_event = process.argv[3].split(' ').join('%');

  var headers = {
    'Pf-ResultWish': 'party(name='+searched_event+'%,stamp<'+(moment.utc().unix() + 63072000)+')'
  };

  console.log(headers);

  var event = partyflockInstance.party.search(searched_event, headers).then(function(res) {
  // var event = partyflockInstance.party.search('unlocked').then(function(res) {
    // Returns array with party Objects
    // process.stdout.write(Json(arguments[0].party.party.slice(-4)))
    console.log(arguments[0].party.party.slice(-process.argv[4]))
  }).catch(console.log)
} else if (mode == 'lineupsearch') {
  // andere dingen
}

var bla = "blaat"

// process.stdout.write(String(event));

return bla
