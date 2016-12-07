import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  updated_entity: null,

  willRender() {
    if(this.get('event.params.on') === undefined || this.get('updated_entity') !== null){
      return;
    }
    let entity_str = this.get('event.params.on');
    let self = this;
    this.get('entityService').get_entity(entity_str, this.get('investigation')).then(function(entity){
       if(entity === undefined){
	return;
       }
      Ember.run.scheduleOnce('afterRender', this, function() {
	self.set('updated_entity', entity);
      });
    });
  }
});
