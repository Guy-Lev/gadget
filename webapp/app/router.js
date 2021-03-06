import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL,
});

Router.map(function() {
  this.route('setup');
  this.route('login');
  this.route('investigation', { path: '/investigation/:id'});
  this.route('investigation-list', { path: '/investigations'});
});

export default Router;
