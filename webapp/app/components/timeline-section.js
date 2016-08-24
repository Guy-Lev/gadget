import Ember from 'ember';

export default Ember.Component.extend({
  sortKeys: ['time_stamp:desc'],
  sorted_filtered_events: Ember.computed.sort('investigation.events', 'sortKeys')
});
