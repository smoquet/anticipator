var Partyflock = require('partyflock');
var fs = require('fs');
var consumerSecret = fs.readFileSync("./pf.secret", "utf8").trim();

var consumerKey = '4ba03d0a359ec1d0'

var partyflockInstance = new Partyflock(consumerKey, consumerSecret, 'partyflock.nl', true)

var event = partyflockInstance.party.search('prspct').then(function(res) {
  // Returns array with party Objects
  // process.stdout.write(String(res))
  console.log(arguments)
})

var bla = "blaat"

// process.stdout.write(String(event));

return bla
