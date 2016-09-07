var Promise = require( 'bluebird' );

var Partyflock = require( '../partyflock' );

  describe('I:Partyflock:user', function() {
  'use strict';

  describe( 'lookup', function() {
    var partyflockInstance;
    beforeEach(function() {
      partyflockInstance = new Partyflock();
    });

    it( 'should return user lookup', function(done) {
      this.timeout(5000);
      return partyflockInstance.user.lookup('2269').then(function(info) {
        expect(info.user).to.be.ok();
        expect(info.user.id).to.eql(2269);
      }).then(done, done);
    });

    it( 'should return false', function(done) {
      this.timeout(5000);
      return partyflockInstance.user.lookup('-1').then(function(info) {
        expect(info).to.not.be.ok();
      }).then(done, done);
    });
  });
});
