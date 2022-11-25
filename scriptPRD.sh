# /bin/bash

##### PRD

# activar entorno virtual
source venv/bin/activate

#BD
export DATABASE_URL=postgres://dumuajvv:8Wk5MxQufKTVrxwUwSDkmJwdPPLjelmY@motty.db.elephantsql.com/dumuajvv

#migrate produccion 
python manage.py migrate --settings=core.settings.produccion


# ------------------------------------------------------------


# para poblar la BD 
python manage.py loaddata datos.json --settings=core.settings.produccion


python manage.py runserver --settings=core.settings.produccion
