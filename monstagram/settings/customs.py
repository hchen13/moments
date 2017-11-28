class EthanWarning(Exception):
    def __str__(self):
        origin = super(EthanWarning, self).__str__()
        return "Ethan's WARNING: {}".format(origin)

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': [
		# 'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.TokenAuthentication',
	]
}