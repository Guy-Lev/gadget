import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  operation_entities: null,

   _save_entity:function(entity){
     let entities = this.get('operation_entities');
     if (entities === null){
       entities = [];
       this.set('operation_entities', entities);
     }
     entities.push(entity);
  },

  compute_operation_entities:function(){
    if (this.get('event.params.on') === null){
      return;
    }

    for (var i = 0; i < this.get('event.params.on').get('length'); i++) {
      let entity_str = this.get('event.params.on').toArray()[i];
      this.get('entityService').get_entity(entity_str, this.get('investigation')).then(this._save_entity.bind(this));
    }
  }.on('init'),

  selected_entities: function(){
    if (this.get('operation_entities') === null){
      return;
    }
    let selected_entities = [];
    for (let i = 0; i < this.get('operation_entities').get('length'); i++) {
      let e = this.get('operation_entities').objectAt(i);
      if (e.get('is_selected')){
	selected_entities.push(e);
      }
    }
    return selected_entities;
  }.property('operation_entities' ,'operation_entities.@each.is_selected'),

  actions: {
    on_check_entity: function(newSelection, value, operation){
      value.set('is_selected', operation === 'added' ? true : false);
      let self = this;
      value.save().then(function(){
	self.get('investigation').reload().then(function(){
	  self.send("refresh");
	});
      });
    },
  }
});
