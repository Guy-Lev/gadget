import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  updated_entity: null,

  compute_updated_entity:function(){
    if (this.get('event.params.on') === null){
      return;
    }
    if(this.get('event.params.on') !== null){
      let entity_str = this.get('event.params.on');
      let self = this;
      this.get('entityService').get_entity(entity_str, this.get('investigation')).then(function(entity){
	self.set('updated_entity', entity);});
    }
  }.on('init'),
});
