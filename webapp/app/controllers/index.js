import Ember from 'ember';

export default Ember.Controller.extend({
  store: Ember.inject.service('store'),
  session: Ember.inject.service(),
  name: "",
  log_url: "",
  actions: {
    logout: function() {
      this.get('session').invalidate();
    },
    create: function() {
      let record = this.get("store").createRecord('investigation', {
	name: this.get('name'),
	log_url: this.get('log_url'),
      });
      let self = this;
      record.save().then(function(record) {
	self.transitionToRoute("investigation", record.get('id'));
	console.log("investigation id is " + record.get('id'));
      });

    }
  }
});
