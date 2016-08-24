import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr(),
  is_selected: DS.attr(),
  investigation: DS.belongsTo('investigation'),
});
