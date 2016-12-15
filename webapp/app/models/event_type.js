import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
  name: DS.attr(),
  is_selected: DS.attr(),
  investigation: DS.belongsTo('investigation'),

  is_update: Ember.computed.equal('name', 'update'),
  is_error: Ember.computed.equal('name', 'error'),
  is_operation: Ember.computed.equal('name', 'operation'),
  is_creation: Ember.computed.equal('name', 'creation'),

});
