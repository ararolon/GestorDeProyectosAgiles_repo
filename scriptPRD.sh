# /bin/bash

##### PRD

# activar entorno virtual
source venv/bin/activate

#BD
export DATABASE_URL=postgres://dumuajvv:8Wk5MxQufKTVrxwUwSDkmJwdPPLjelmY@motty.db.elephantsql.com/dumuajvv

#migrate produccion 
python manage.py migrate --settings=core.settings.produccion


# ------------------------------------------------------------
# para asegurase de que el puerto este liberado
sudo fuser -k 8000/tcp

# para poblar la BD 
echo ">>> Poblando la base de datos de produccion"
python manage.py loaddata datos.json --settings=core.settings.produccion

echo ">>> Iniciando el servidor con la base de datos de produccion"
python manage.py runserver --settings=core.settings.produccion
