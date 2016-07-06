var Promise = require( 'bluebird' );

var Partyflock = require( '../partyflock' );

  describe('I:Partyflock:party', function() {
  'use strict';

  describe( 'search', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return parties', function(done) {
      this.timeout(5000);
      return partyflockInstance.party.search('unlocked').then(function(info) {
        expect(info.party.party).to.be.ok();
        expect(info.party.party.length).to.eql(1);
        expect(info.party.party[0].name).to.eql('Unlocked');
        expect(info.party.party[0].id).to.eql(292433);
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.party.search('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });

  describe( 'lookup', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return party lookup', function(done) {
      this.timeout(5000);
      return partyflockInstance.party.lookup('1').then(function(info) {
        expect(info.party).to.be.ok();
        expect(info.party.id).to.eql(1);
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.party.lookup('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });
});
