/**
 * Location instance constructor
 * @prototype
 * @class Location
 */
function Location(instance) {
  this.partyflock = instance || {};
  this.service = 'location';
}

/**
 * Retrieve data about a location
 * @param  {String} id    
 * @param  {Object} headers 
 * @return {Promise}         
 */
Location.prototype.lookup = function lookup(id, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'location(name,agenda(party(name=b%,stamp=%)))'
    };
  }

  return this.partyflock.communicate(this.service, id, headers);
}; 

/**
 * Search location by name (% as wildcard)
 * @param  {String} name 
 * @return {Promise}      
 */
Location.prototype.search = function search(name, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'location(name=' + name + ',address,city(country(name)))'
    };
  }

  return this.partyflock.communicate(this.service, 'search', headers);
};  

module.exports = Location;
