ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'decide-penyagolosa.herokuapp.com'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd9k0cu1rtpjq09',
        'USER': 'aadmjtiqvdltdv',
        'PASSWORD': '88bbce7f4e921bee0c13387a490c9f9c017ed510aeba36c1c7b99612425c59c7',
        'HOST': 'ec2-52-17-1-206.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits


KEYBITS = 256
