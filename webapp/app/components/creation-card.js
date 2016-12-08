import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  created_entity: null,

  willRender() {
    if(this.get('event.params.entity') === undefined || this.get('created_entity') !== null){
      return;
    }
    let entity_str = this.get('event.params.entity');
    let self = this;
    self.get('entityService').get_entity(entity_str, self.get('investigation')).then(function(entity){
      Ember.run.scheduleOnce('afterRender', this, function() {
	self.set('created_entity', entity);
      });
    });
  }
});
