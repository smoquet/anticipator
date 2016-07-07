var Partyflock = require( '../partyflock' );

describe('I:Partyflock:artist', function() {
  'use strict';

  describe( 'lookup', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return artist info', function(done) {
      this.timeout(5000);
      return partyflockInstance.artist.lookup('1').then(function(info) {
        expect(info.artist.id).to.eql(1);
        expect(info.artist.name).to.eql('Tiësto');
        expect(info.artist.realname).to.eql('Tijs Verwest');
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.artist.lookup('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });

  describe( 'search', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return artists', function(done) {
      this.timeout(5000);
      return partyflockInstance.artist.search('frontl%').then(function(info) {
        expect(info.artist[0].id).to.eql(41794);
        expect(info.artist[0].name).to.eql('Frontliner');
        expect(info.artist[0].realname).to.eql('Barry Drooger');
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.artist.search('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });
});
