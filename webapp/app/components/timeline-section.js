import Ember from 'ember';

export default Ember.Component.extend({
  descending: true,
  sortKeys: Ember.computed('descending', function(){
    if(this.get('descending')){
      return['time_stamp:desc'];
    }
    return['time_stamp:asc'];
  }),
  sorted_filtered_events: Ember.computed.sort('investigation.events', 'sortKeys'),
  actions: {
    toggle_sorting_order() {
      this.toggleProperty('descending');
    },
  }
});
