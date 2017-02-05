import Ember from 'ember';
import Card from './card';

export default Card.extend({
  entityService: Ember.inject.service(),
  deleted_entity: null,

  willRender() {
    if(this.get('event.params.entity') === undefined || this.get('deleted_entity') !== null){
      return;
    }
    let entity_str = this.get('event.params.entity');
    let self = this;
    self.get('entityService').get_entity(entity_str, self.get('investigation')).then(function(entity){
      Ember.run.scheduleOnce('afterRender', this, function() {
	self.set('deleted_entity', entity);
      });
    });
  }
});
