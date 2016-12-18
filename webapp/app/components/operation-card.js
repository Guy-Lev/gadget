import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  operation_entities: null,
  _save_entity:function(entity){
    if(this.get('operation_entities') === null){
      this.set('operation_entities', []);
    }
    if(this.get('selected_entity_colors') === null){
      this.set('selected_entity_colors', []);
    }

    let entities = this.get('operation_entities');
    Ember.run.scheduleOnce('afterRender', this, function() {
      entities.pushObject(entity);
    });
  },

  willRender() {
    if (this.get('event.params.on') === undefined || this.get('operation_entities') !== null){
      return;
    }

    for (var i = 0; i < this.get('event.params.on').get('length'); i++) {
      let entity_str = this.get('event.params.on').toArray()[i];
      this.get('entityService').get_entity(entity_str, this.get('investigation')).then(this._save_entity.bind(this));
    }
  },

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
