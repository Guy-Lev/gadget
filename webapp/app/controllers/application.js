import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),
  current_user:function(){
    return this.get('model');
  }.property('model'),

  iframe: function() {
    return this.get("view") === "iframe";
  }.property("view"),

  actions: {
    login_error: function(error) {
      if (error === 401) {
	this.set('modal_content', 'Gadget must be used with Infinidat accounts');
      } else {
	this.set('modal_content', 'There was an error logging you in: ' + error);
      }
      Ember.Logger.error(error);
      Ember.$('#appmodal').openModal();
    },
    invalidate_session: function() {
      this.get('session').invalidate();
    }
  },

});
