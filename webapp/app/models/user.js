import DS from 'ember-data';

export default DS.Model.extend({
    name: DS.attr('string'),
    email: DS.attr('string'),
    roles: DS.hasMany('role'),
    isAdmin: function() {
	for (var i = 0; i < this.get('roles').get('length'); i++) {
	    let role = this.get('roles').toArray()[i];
	    if (role.get('name') === "admin"){
		return true;
	    }
	}
	return false;
    }.property("roles", "roles.@each.name"),

    display_name: function() {
	if (this.get('name')) {
	    return this.get('name');
	}

	if (this.get('email')) {
	    return this.get('email');
	}

	return "...";
    }.property("name", "email")
});
