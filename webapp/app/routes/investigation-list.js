import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    this.store.findAll('user');
    return this.store.findAll('investigation'); //limit this call to first 50 or so
  }
});
