/**
 * Date instance constructor
 * @prototype
 * @class Date
 */
function Date(instance) {
  this.partyflock = instance || {};
  this.service = 'date';
}

/**
 * Retrieve agenda around date
 * @param  {String} date    date 20100304 or range 20130301-20130401
 * @param  {Object} headers 
 * @return {Promise}         
 */
Date.prototype.lookup = function lookup(date, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'date(agenda(party(name,stamp,location(name),visitors(user(id)))))'
    };
  }

  return this.partyflock.communicate(this.service, date, headers);
};  

module.exports = Date;
