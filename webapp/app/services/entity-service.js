import Ember from 'ember';

export default Ember.Service.extend({

  store: Ember.inject.service('store'),
  init() {
    this.set('_cache', Ember.Object.create());
  },

  get_entity:function(entity_str) {
    let self = this;
    let returned = this._cache.get(entity_str);
    if (returned  === undefined) {
      self = this;
      return this.get('store').findAll('entity', {str_id: entity_str}).then(function(entities){
	for (var i = 0; i < entities.get('length'); i++) {
	  let entity = entities.toArray()[i];
	  self._cache.set(entity.get('str_id'), entity);
	}
	return self._cache.get(entity_str);
      });
    }

    return new Ember.RSVP.Promise(function(resolve) {
      resolve(returned);
    });
  },

});
