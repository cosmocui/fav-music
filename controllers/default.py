#########################################################################
#  CMPS 183 (Fall 2015) Project
#  Project Name: Find Your Car Parts
#  Name: Yu "Kevin" Cui
#  E-mail:  ycui8@ucsc.edu
#########################################################################

def index():
	makes = db().select(db.cars.make, distinct=True, orderby=db.cars.make)
	fits_matched = []
	fav_list = []

	# This is a search query
	if len(request.args) == 4:
		# First, get the car
		car_matched = db(
			(db.cars.make==request.args(0)) &
			(db.cars.model==request.args(1)) &
			(db.cars.submodel==request.args(2)) &
			(db.cars.mfg_year==request.args(3))
		).select().first()
		# Then get the fits rows for all matched wheel
		if car_matched is not None:
			fits_matched = db(db.fits.car==car_matched.id).select()
		# Then fetch a login-user's favorite wheel list if applicable
		user_favs = []
		if auth.user_id is not None:
			user_favs = db(db.favs.user_id==auth.user_id).select()
		# Finally, build a True/False favorite wheel list align with the wheel list for the login user
		for fit in fits_matched:
			is_fav = False
			for fav in user_favs:
				if fit.wheel.id == fav.wheel.id: # the car in the search results is favorited
					is_fav = True
			fav_list.append(is_fav)

	return dict(makes=makes, fits_matched=fits_matched, fav_list=fav_list)


# @auth.requires_signature() to-do
def get_models():
	make_selected = request.vars.make_selected
	rows = db(db.cars.make==make_selected).select(db.cars.model, distinct=True, orderby=db.cars.model)
	models = []
	for row in rows:
		models.append(row.model)
	return response.json(dict(models=models))


#@auth.requires_signature() to-do
def get_submodels():
	make_selected = request.vars.make_selected
	model_selected = request.vars.model_selected
	rows = db((db.cars.make==make_selected) &
			  (db.cars.model==model_selected)).select(db.cars.submodel, distinct=True, orderby=db.cars.submodel)
	submodels = []
	for row in rows:
		submodels.append(row.submodel)
	return response.json(dict(submodels=submodels))


#@auth.requires_signature() to-do
#to-do: bug: cannot retrieve results with submodel is with blanck, eg: 'i Sport'
def get_years():
	make_selected = request.vars.make_selected
	model_selected = request.vars.model_selected
	submodel_selected = request.vars.submodel_selected
	rows = db((db.cars.make==make_selected) &
			  (db.cars.model==model_selected) &
			  (db.cars.submodel==submodel_selected)).select(db.cars.mfg_year, distinct=True, orderby=db.cars.mfg_year)
	years = []
	for row in rows:
		years.append(row.mfg_year)
	return response.json(dict(years=years))


@auth.requires_signature()
def toggle_fav():
	wheel_id = request.vars.wheel_id
	print 'wheel_id=%s' % wheel_id
	if db((db.favs.wheel==wheel_id) & (db.favs.user_id==auth.user_id)).isempty():
		db.favs.update_or_insert(wheel=wheel_id, user_id=auth.user_id)
	else:
		db((db.favs.wheel==wheel_id) & (db.favs.user_id==auth.user_id)).delete()
	return 'ok'


def user():
	"""
	exposes:
	http://..../[app]/default/user/login
	http://..../[app]/default/user/logout
	http://..../[app]/default/user/register
	http://..../[app]/default/user/profile
	http://..../[app]/default/user/retrieve_password
	http://..../[app]/default/user/change_password
	http://..../[app]/default/user/manage_users (requires membership in
	http://..../[app]/default/user/bulk_register
	use @auth.requires_login()
		@auth.requires_membership('group name')
		@auth.requires_permission('read','table name',record_id)
	to decorate functions that need access control
	"""
	return dict(form=auth())


@cache.action()
def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request, db)


def call():
	"""
	exposes services. for example:
	http://..../[app]/default/call/jsonrpc
	decorate with @services.jsonrpc the functions to expose
	supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
	"""
	return service()
