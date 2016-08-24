import DS from 'ember-data';
import Ember from 'ember';
/* global moment */

export default DS.Model.extend({
  name: DS.attr(),
  state: DS.attr(),
  update: DS.attr(),

  update_json: function() {
    let update = this.get('update');
    return JSON.stringify(update);
  }.property('update'),

  event_type: DS.belongsTo('event_type'),
  is_update: Ember.computed.equal('event_type.name', 'update'),
  is_error: Ember.computed.equal('event_type.name', 'error'),
  is_operation: Ember.computed.equal('event_type.name', 'operation'),


  time_stamp: DS.attr(),
  params: DS.attr(),
  investigation: DS.belongsTo('investigation'),
  entities: DS.hasMany('entity'),

  formated_time_stamp:function(){
    var created_moment = moment(this.get("time_stamp"));
    return created_moment.format('DD/MM/YY HH:mm:ss:SSS');
    }.property('time_stamp'),

});
