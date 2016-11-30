import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),
  investigation: null,
  entity: null,
  search: null,

  actions: {
    toggle_selected() {
      let entity = this.get('entity');
      entity.toggleProperty('is_selected');
      let self = this;
      entity.save().then(function(){
	self.get('store').queryRecord('investigation', {search: self.get('search'), investigation_id: self.get('investigation.id')}).then(function(){
	  self.sendAction('refresh_model');
	});
      });
    },
  }
});
