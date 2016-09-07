/**
 * Artist instance constructor
 * @prototype
 * @class Artist
 */
function Artist(instance) {
  this.partyflock = instance || {};
  this.service = 'artist';
}

/**
 * Retrieve information about artist
 * @param  {String} id
 * @return {Promise}   
 */
Artist.prototype.lookup = function lookup(id, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'artist(name,realname,genre(name))'
    };
  }

  return this.partyflock.communicate(this.service, id, headers);
};  

/**
 * Search artist by name (% as wildcard)
 * @param  {String} name 
 * @return {Promise}      
 */
Artist.prototype.search = function search(name, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'artist(name='+name+',realname,genre(name))'
    };
  }

  return this.partyflock.communicate(this.service, 'search', headers);
};  


module.exports = Artist;
