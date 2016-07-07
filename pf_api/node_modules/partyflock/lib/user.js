/**
 * User instance constructor
 * @prototype
 * @class User
 */
function User(instance) {
  this.partyflock = instance || {};
  this.service = 'user';
}

/**
 * Retrieve information about a user
 * @param  {String} id    
 * @param  {Object} headers 
 * @return {Promise}         
 */
User.prototype.lookup = function lookup(id, headers) {
  if(typeof headers !== 'object') {
    headers = {
      'Pf-ResultWish': 'user(nick,userimage(large=0,filetype,width,height))'
    };
  }

  return this.partyflock.communicate(this.service, id, headers);
}; 

module.exports = User;
