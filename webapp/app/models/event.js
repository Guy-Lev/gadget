import DS from 'ember-data';
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
  time_stamp: DS.attr(),
  params: DS.attr(),
  investigation: DS.belongsTo('investigation'),
  entities: DS.hasMany('entity'),

  has_additional_params: function() {
    return this.get('params.params') !== undefined;
  }.property('params.params'),

  additional_params: function() {
    let additional_params = this.get('params.params');
    return JSON.stringify(additional_params);
  }.property('params.params'),

  formated_time_stamp:function(){
    var created_moment = moment(this.get("time_stamp"));
    return created_moment.format('DD/MM/YY HH:mm:ss:SSS');
  }.property('time_stamp'),

});
