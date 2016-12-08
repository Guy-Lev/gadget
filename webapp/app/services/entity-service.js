import Ember from 'ember';
//import MultiDict from 'multi-key-dict';

export default Ember.Service.extend({
  store: Ember.inject.service('store'),
  init() {
    //this.set('_cache', new MultiDict());
    this.set('_cache', Ember.Object.create());
  },

  get_entity:function(entity_str, investigation) {
    let self = this;
    let CacheKey = entity_str + '@' + investigation.get('id').toString();
    let returned = this._cache.get(CacheKey);
    if (returned  === undefined) {
      self = this;
      return this.get('store').query('entity', {investigation_id: investigation.get('id')}).then(function(entities){
	for (var i = 0; i < entities.get('length'); i++) {
	  let entity = entities.toArray()[i];
	  self._cache.set(entity.get('str_id') + '@'+ investigation.get('id').toString(), entity);
	}
	return self._cache.get(CacheKey);
      });
    }

    return new Ember.RSVP.Promise(function(resolve) {
      resolve(returned);
    });
  },

});
