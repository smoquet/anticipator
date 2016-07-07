[![partyflock_logo_and_text_for_light_3000px](https://cloud.githubusercontent.com/assets/777823/10575029/0ab3e2fc-765a-11e5-9791-2668eef0b3e8.png)](https://partyflock.nl/)

#  node-partyflock
[![Build Status](https://travis-ci.org/DeviaVir/node-partyflock.svg?branch=master)](https://travis-ci.org/DeviaVir/node-partyflock)

Node.JS Promise-based library to communicate with the Partyflock API

This library creates a new instance of "Partyflock" for you, exposing a few methods you can use to communicate.

To start a new Partyflock instance:

```js
var Partyflock = require('partyflock');

var partyflockInstance = new Partyflock(consumerKey, consumerSecret, endpoint /* optional */, debug /* optional */)
```

`consumerKey` and `consumerSecret` can be requested via `kantoor@partyflock.nl`, with a brief explanation for the purpose. `endpoint` will usually be `partyflock.nl` and can be left empty if you're using that endpoint.

# Installing

Run in your project root:
```sh
~ npm install --save partyflock
```

Require in your code:
```js
var Partyflock = require('partyflock');
```

# Running the integration tests

Some of the integration tests are based off of real world data, that means that this data can change and the tests might fail over time. This is expected behaviour.

You can run the tests by copying `config/data.example.js` to `config/data.js` and filling out your real data.

Then it's as easy as:

```sh
~ npm test
```

# Methods

**Notes and acknowledgements**:
- Every method accepts an optional `headers` parameter. This can be used to send a custom Pf header, examples will be supplied below.
- When any error occurs or no results could be found, `false` will be returned.

## Artist

### partyflockInstance.artist.lookup

```js
partyflockInstance.artist.lookup('1').then(function(res) {
  // Returns artist Object with artist info
});
```

### partyflockInstance.artist.search

```js
partyflockInstance.artist.search('frontl%').then(function(res) {
  // Returns array with artist Objects
});
```


## Date

```js
partyflockInstance.date.lookup('20151012').then(function(res) {
  // Returns object with agenda information, res.date.agenda contains array of parties
});
```

**Alternative headers**

```js
var headers = {
  'Pf-ResultWish': 'date(agenda(party(name,fbid,stamp,notime,door_close_hour,door_close_mins,duration_secs,genre(name),flyer(type,size=thumb,width,height,link),location(name,address,zipcode,latitude,longitude,city(name,country(name))),organization(name),area(incomplete,lineup(time_start,time_end,artist(name))))))'
};

// alternatively
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitors(certain(user(id))))))'
};

// alternatively
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitors(user(id)))))'
};

// alternatively
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitors(maybe(user(id))))))'
};

// alternatively
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitors(maybe(user(id)),certain(user(id))))))'
};

// alternatively
var headers = {
  'Pf-ResultWish': 'date(agenda(party(name,min_age,stamp,notime,duration_secs,price(what,price,currency,membership,membership_name,available,sold_out,vip,type,access,time_hour,time_mins,consumptions,passepartout,group_amount),genre(name),flyer(type,size=thumb,width,height,link),location(name,address,zipcode,latitude,longitude,city(name,country(name))),organization(name),area(lineup(time_start,time_end,artist(name))))))'
};

// alternatively
var headers = {
  'Pf-ResultWish': 'date(agenda(party(name,min_age,stamp,notime,duration_secs,price(what,price,currency,membership,membership_name,available,sold_out,vip,type,access,time_hour,time_mins,consumptions,passepartout,group_amount),genre(name),flyer(type,size=thumb,width,height,link),location(name,address,zipcode,latitude,longitude,city(name,country(name))),organization(name),area(lineup(time_start,time_end,artist(name))))))'
};

// alternatively, single date, limit to max distance of 50 km to amsterdam
var headers = {
  'Pf-Latitude': '52.3738',
  'Pf-Longitude': '4.891',
  'Pf-Radius': '50',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,notime,duration_secs,genre(name),flyer(type,size=thumb,width,height,link),location(name,address,zipcode,latitude,longitude,city(name,country(name))),organization(name),area(lineup(time_start,time_end,artist(name))))))'
};

// alternatively, visitor counts
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitorcounts(maybe,certain))))'
};

// alternatively, tickets
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),tickets(type,domain,data))))'
};
var headers = {
  'Pf-HourOffset': '6',
  'Pf-ResultWish': 'date(agenda(party(cost_door,cost_presale,sold_out,name,stamp,duration_secs,genre(name),area(lineup(time_start,time_end,artist(name),type)),min_age,site,visitorcounts(certain),tickets(type,domain,data),cancelled,flyer(id,size=thumb,link),location(name,address,zipcode,latitude,longitude,site,email,phone,city(name,country(id=1))))))'
};

partyflockInstance.date.lookup('20151012', headers).then(function(res) {
  // Result changed based off of the new custom headers
});
```

## Location

```js
partyflockInstance.location.lookup('7731').then(function(res) {
  // Returns location Object with location information
});
```

Two locations in the same requests:
```js
partyflockInstance.location.lookup('7731, 21').then(function(res) {
  // Returns array with location Objects
});
```

```js
partyflockInstance.location.search('ziggo%').then(function(res) {
  // Returns array with location Objects
});
```

**Alternative headers**

```js
var headers = {
  'Pf-ResultWish': 'location(name,flyer(type,size=thumb,width,height,link),address,zipcode,latitude,longitude,city(name,country(name)),agenda(party(name,stamp,notime,duration_secs,genre(name),flyer(type,size=thumb,width,height,link),organization(name),area(lineup(time_start,time_end,artist(name))))))'
};

// alternatively
var headers = {
  'Pf-ResultWish': 'location(name,address)'
};

partyflockInstance.location.lookup('7731', headers).then(function(res) {
  // Result changed based off of the new custom headers
});

// when sending custom headers for search, don't forget to add your search parameter (ziggo%)
var headers = {
  'Pf-ResultWish': 'location(name=ziggo%,address,city(country(name)))'
};

partyflockInstance.location.search('ziggo%', headers).then(function(res) {
  // Result changed based off of the new custom headers
});
```

## Party

```js
partyflockInstance.party.search('unlocked').then(function(res) {
  // Returns array with party Objects 
})
```

**Alternative headers**

```js
// when sending custom headers for search, don't forget to add your search parameter (unlocked)
var headers = {
  'Pf-ResultWish': 'party(name=unlocked,stamp<'+moment.utc().unix()+')'
};

// alternatively
var headers = {
  'Pf-Latitude': '52.1080891',
  'Pf-Longitude': '4.2730927',
  'Pf-Radius': '10',
  'Pf-ResultWish': 'party(name,location(name,locationtype=%beach%),stamp>'+moment.utc().unix()+',duration_secs,lineup(artist(name)))'
};

partyflockInstance.party.search('unlocked', headers).then(function(res) {
  // Result changed based off of the new custom headers
});
```

## User

```js
partyflockInstance.user.lookup('2269').then(function(res) {
  // Returns user Object
});
```
