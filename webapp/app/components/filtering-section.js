import Ember from 'ember';

export default Ember.Component.extend({

  search: null,
  entered_search: null,
  sortEntityKeys: ['str_id:asc'],
  sorted_entities: Ember.computed.sort('investigation.entities', 'sortEntityKeys'),

  sortEventTypeKeys: ['name:asc'],
  sorted_event_types: Ember.computed.sort('investigation.event_types', 'sortEventTypeKeys'),

  actions: {

    on_press_search: function(){
      this.set('search', this.get('entered_search'));
    },

    on_check_entity: function(newSelection, value, operation){
      value.set('is_selected', operation === 'added' ? true : false);
      let self = this;
      value.save().then(function(){
	self.get('investigation').reload().then(function(){
	 self.sendAction('refresh_model');
	});
      });
    },

    on_check_event_type: function(newSelection, value, operation){
      value.set('is_selected', operation === 'added' ? true : false);
      let self = this;
      value.save().then(function(){
	self.get('investigation').reload().then(function(){
	  self.sendAction('refresh_model');
	});
      });
    },
  }

});
