import Ember from 'ember';
import color from "npm:color";

export function colorFromString(s) {
  let hash = 0;
  if (s === undefined) {
    return hash;
  }
  for (let i = 0; i < s.length; i++) {
      let char = s.charCodeAt(i);
    hash = ((hash<<5)-hash)+char;
    hash = hash & hash; // Convert to 32bit integer
  }
  hash ^= s.length;
  hash = Math.abs(hash)%100 / 100;
  hash += 0.618033988749895; //golden ratio
  hash %= 1;
  let rgb =  color({h: hash * 300, s: 90, v: 85}).rgbNumber();
  return "#" + rgb.toString(16);
}

export default Ember.Helper.helper(colorFromString);
