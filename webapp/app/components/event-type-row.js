import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),
  investigation: null,
  event_type: null,
  search: null,

  actions: {
    toggle_selected() {
      let event_type = this.get('event_type');
      event_type.toggleProperty('is_selected');
      let self = this;
      event_type.save().then(function(){
	self.get('store').queryRecord('investigation', {search: self.get('search'), investigation_id: self.get('investigation.id')}).then(function(){
	  self.sendAction('refresh_model');
	});
      });
    },
  }
});
