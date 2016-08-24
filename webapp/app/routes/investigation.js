import Ember from 'ember';
import App from '../app';

export default Ember.Route.extend({
  spinner: Ember.inject.service('spinner'),
  queryParams: {
    search: {refreshModel: true}
  },
  params: {},

  load_model: function(params) {
    Ember.Logger.info(`Loading model with search ${this.get("params")}`);
    return Ember.RSVP.hash({
      investigation: this.store.queryRecord('investigation', {search: params.search, investigation_id: params.id}),
    });
  },
  model: function(params) {
    this.set("params", params);
    return this.load_model(params);
  },

  setupController(controller, model) {
    this._super(...arguments);
    controller.setProperties(model);
  },

  deactivate: function() {
    this._super();
    this.get('pollster').stop();
  },

  afterModel: function(model) {
    this._super();
    var self = this;

    if (Ember.isNone(this.get('pollster'))) {
      this.set('pollster', App.Pollster.create({
	onPoll: function() {
	  var model = self.get("controller.model");
	  if (model.investigation.get('ready')) {
	    self.get('spinner').hide('gadget-spinner');
	    return false;
	  } else {
	    self.get('spinner').show('gadget-spinner');
	    model.investigation.reload();
	    return true;
	  }
	}
      }));
    }

    if (!model.investigation.get('ready')) {
      self.get('spinner').show('gadget-spinner');
      model.investigation.reload();
      this.get('pollster').start();
    }
  },

  actions: {
    refresh: function(){
      this.load_model(this.get("params"));
    },
  }

});
