import Ember from 'ember';
import config from '../config/environment';

export default Ember.Component.extend({

  email: null,
  is_proxy: false,
  is_real: false,
  tagName: 'img',
  large: false,

  attributeBindings: ['src'],
  classNames: ['img-circle', 'navbar-gravatar'],
  classNameBindings: ['is_proxy:proxy', 'is_real:real', 'large'],

  _cache_key_name: function() {
    return 'cached-avatar:' + this.get('email');
  }.property('email'),

  src: function() {
    const email = this.get('email');
    if(!email){
      return;
    }
    let fallback_img = this.get('fallback_img_url');
    //let returned = 'https://www.gravatar.com/avatar/' + email; //TODO
    let returned = 'http://infinibook.infinidat.com/image/' + email;
    if (fallback_img) {
      returned += '?d=404';
    } else {
      returned += '?d=mm';
    }
    return returned;
  }.property('email'),

  fallback_img_url: function() {
    let fallback = config.APP.avatars.fallback_image_url;
    if (!fallback) {
      return null;
    }
    fallback = fallback.replace('__EMAIL__', this.get('email'));
    return fallback;

  }.property(),

  didInsertElement: function() {
    let self = this;
    this.$().on('error', function() {
      let fallback = self.get('fallback_img_url');
      if (fallback) {
        localStorage.setItem(this.get('_cache_key_name'), fallback);
      }
      this.set('src', fallback);
    }.bind(this));
  },

  willDestroyElement: function(){
    this.$().off();
  }

});
