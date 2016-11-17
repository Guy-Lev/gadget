import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  operation_entities: null,

  selected_entities: function(){
    let selected_entities = [];
    for (let i = 0; i < this.get('operation_entities').toArray().length; i++) {
      let e = this.get('operation_entities').toArray()[i];
      if (e.get('is_selected')){
	selected_entities.push(e);
      }
    }
    return selected_entities;
  }.property('operation_entities' ,'operation_entities.@each.is_selected'),

  _save_entity:function(entity){
    let entities = this.get('operation_entities');
    entities.push(entity);
  },

  operation_entities_from_params:function(){
    this.set('operation_entities', []);
    for (var i = 0; i < this.get('event.params.on').get('length'); i++) {
      let entity_str = this.get('event.params.on').toArray()[i];
      this.get('entityService').get_entity(entity_str).then(this._save_entity.bind(this));
    }
  }.on('init'),

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
