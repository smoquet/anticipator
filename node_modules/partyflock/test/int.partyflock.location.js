var Partyflock = require( '../partyflock' );

describe('I:Partyflock:location', function() {
  'use strict';

  describe( 'lookup', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return locations', function(done) {
      this.timeout(5000);
      return partyflockInstance.location.lookup('7731').then(function(info) {
        expect(typeof info.location).to.eql('object');
        expect(info.location.id).to.eql(7731);
        expect(info.location.name).to.eql('North Sea Venue');
        expect(info.location.agenda).to.be.ok();
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.location.lookup('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });

  describe( 'search', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return location search', function(done) {
      this.timeout(5000);
      return partyflockInstance.location.search('ziggo%').then(function(info) {
        expect(typeof info.location).to.eql('object');
        expect(info.location.length).to.eql(1);
        expect(info.location[0].id).to.eql(16643);
        expect(info.location[0].name).to.eql('Ziggo Dome');
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.location.search('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });
});
