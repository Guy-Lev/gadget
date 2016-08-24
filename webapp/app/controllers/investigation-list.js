import Ember from 'ember';

export default Ember.Controller.extend({
  store: Ember.inject.service('store'),
  sortKeys: ['created_at:desc'],
  sortedInvestigations: Ember.computed.sort('model', 'sortKeys'),
});
