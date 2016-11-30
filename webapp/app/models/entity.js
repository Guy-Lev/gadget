import DS from 'ember-data';
import gen from "npm:color-generator";

export default DS.Model.extend({
  str_id: DS.attr(),
  params: DS.attr(),
  color: function(){
    return gen(0.9).rgbString();
  }.property('str_id'),
  events: DS.hasMany('event'),
  is_selected: DS.attr(),
});
