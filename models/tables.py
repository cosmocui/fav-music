db.define_table('cars',
				Field('make', required=True),
				Field('model', required=True),
				Field('submodel'),
				Field('mfg_year', required=True))

db.define_table('wheels',
				Field('pn', required=True),
				Field('brand', required=True),
				Field('model', required=True),
				Field('price', 'double', required=True),
				Field('description', 'text'),
				Field('finishing'),
				Field('diameter', 'integer', required=True),
				Field('width', 'double'),
				Field('bolt'),
				Field('offset_val', 'integer'),
				Field('image', 'upload'))

# For cars-wheels N-to-N relationship
db.define_table('fits',
				Field('car', 'reference cars', required=True),
				Field('wheel', 'reference wheels', required=True))

# For wheel-user N-to-N relationship
db.define_table('favs',
				Field('wheel', 'reference wheels', required=True),
				Field('user_id', 'reference auth_user', required=True))
