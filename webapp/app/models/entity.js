import DS from 'ember-data';

export default DS.Model.extend({
  str_id: DS.attr(),
  params: DS.attr(),
  investigation: DS.belongsTo('investigation'),
  events: DS.hasMany('event'),
  is_selected: DS.attr(),
});
