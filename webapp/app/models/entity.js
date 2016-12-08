import DS from 'ember-data';
import { colorFromString } from 'webapp/helpers/color-from-string';

export default DS.Model.extend({
  str_id: DS.attr(),
  params: DS.attr(),
  events: DS.hasMany('event'),
  is_selected: DS.attr(),
  color: function(){
    return colorFromString(this.get('str_id'));
  }.property('str_id'),

});
