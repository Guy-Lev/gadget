import Ember from 'ember';

export default Ember.Controller.extend({
  spinner: Ember.inject.service('spinner'),
  queryParams: {
    search: "search",
  },
  search: null,
actions: {
    refresh_model: function(){
      this.send("refresh");
    },
  }


});
