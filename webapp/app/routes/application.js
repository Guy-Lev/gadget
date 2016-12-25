import Ember from 'ember';

import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {
     actions: {
	logout: function(){
	    this.get('session').invalidate();
	},
	login: function() {
	var self = this;

	    this.get('torii').open('google-oauth2').then(function(authorization) {
		return self.get('session').authenticate('authenticator:token', authorization).then(
		    function(data) {
			return data;
	    },
		    function(error) {
			self.controllerFor('application').send('login_error', error);
		    }
		);
	    },
	function(error) {
	  self.controllerFor('application').send('login_error', error);
	});
    }
  }


});
