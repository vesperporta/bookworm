#!/usr/bin/env bash

# run migrations
echo "Running migrations..."
python manage.py showmigrations
python manage.py migrate
python manage.py showmigrations

echo "Loading language tags"
python manage.py load_languages
echo "Loading country tags"
python manage.py load_countries
echo "Create default set of tags"
python manage.py create_model_tags

# load default data
echo "Creating default user..."
python manage.py createdefaultsuperuser

# echo "Load development data from fixtures..."
# python manage.py loaddata localisation_data.json
# python manage.py loaddata development_fixture.json
