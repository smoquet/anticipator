ANTICIPATOR

Anticipator is a Spotify playlist generator, based on the lineup of the event
of your choice. Uses the Partyflock api for lineup info.

requirements:
- virtualenv (well, recommended)
- postgresql (well, just pg_config actually.)
- node
- npm install
- gulp sass
- pip install -r requirements.txt
- a PF api key in pf_api/pf.secret (good luck with that)

python manage.py migrate
python manage.py runserver