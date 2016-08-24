import DS from 'ember-data';

export default DS.Model.extend({
  investigation_id: DS.attr(), 
  selected_event_types: DS.attr(),
  selected_entities: DS.hasMany('entity'),
});
