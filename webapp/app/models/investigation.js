import DS from 'ember-data';
/* global moment */

export default DS.Model.extend({
  name: DS.attr(),
  created_at: DS.attr(),
  created_by: DS.belongsTo('user'),
  log_url: DS.attr(),
  ready: DS.attr(),
  error: DS.attr(),
  warning: DS.attr(),
  entities: DS.hasMany('entity'),
  events: DS.hasMany('event'),
  event_types: DS.hasMany('event_type'),

  selected_event_types: function(){
    let selected_event_types = [];
    for (let i = 0; i < this.get('event_types').toArray().length; i++) {
      let e = this.get('event_types').toArray()[i];
      if (e.get('is_selected')){
	selected_event_types.push(e);
      }
    }
    return selected_event_types;
  }.property('event_types','event_types.@each.is_selected'),

  selected_entities: function(){
    let selected_entities = [];
    for (let i = 0; i < this.get('entities').toArray().length; i++) {
      let e = this.get('entities').toArray()[i];
      if (e.get('is_selected')){
	selected_entities.push(e);
      }
    }
    return selected_entities;
  }.property('entities' ,'entities.@each.is_selected'),

  formated_date:function(){
    var created_moment = moment(this.get("created_at"));
    return created_moment.format('DD/MM/YY HH:mm:ss');
    }.property('created_at'),
  save_changes: function() {
    //TODO: save state of investigation
  }

});
