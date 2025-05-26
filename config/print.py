import environ
from pathlib import Path

# Initialize environ
env = environ.Env(
	# Set default values
	DEBUG=(bool, False),
)

# Read .env file
environ.Env.read_env()

# Now use the environment variables
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['*']
print(SECRET_KEY)
