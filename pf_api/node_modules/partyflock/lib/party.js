/**
 * Party instance constructor
 * @prototype
 * @class Party
 */
function Party(instance) {
  this.partyflock = instance || {};
  this.service = 'party';
}

/**
 * Retrieve data about a party
 * @param  {String} id    
 * @param  {Object} headers 
 * @return {Promise}         
 */
Party.prototype.lookup = function lookup(id, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'party(name,area(lineup(time_start,time_end,artist(name),type)))'
    };
  }

  return this.partyflock.communicate(this.service, id, headers);
};

/**
 * Search party by name (% as wildcard)
 * @param  {String} name 
 * @return {Promise}      
 */
Party.prototype.search = function search(name, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'party(name=' + name + ')'
    };
  }

  return this.partyflock.communicate(this.service, 'search', headers);
};

module.exports = Party;
