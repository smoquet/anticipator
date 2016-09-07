var Partyflock = require( '../partyflock' );

describe('I:Partyflock:date', function() {
  'use strict';

  describe( 'lookup', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return date information', function(done) {
      this.timeout(5000);
      return partyflockInstance.date.lookup('20151012').then(function(info) {
        expect(info.date.agenda).to.be.ok();
        expect(typeof info.date.agenda).to.eql('object');
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.date.lookup('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });
});
