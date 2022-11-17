# /bin/bash

# activar entorno virtual
source venv/bin/activate

# para asegurase de que el puerto este liberado
sudo fuser -k 8000/tcp

# eliminar la base de datos dbdesarrollo con psql con sudo su postgres 
sudo -u postgres PGPASSWORD=postgres dropdb dbdesarrollo --username=postgres > /dev/null 2>&1


# crear la base de datos dbdesarrollo con psql con sudo su postgres
sudo -u postgres PGPASSWORD=postgres createdb dbdesarrollo --username=postgres > /dev/null 2>&1

# creado 
# ------------------------------------------------------------
#                   Documentacion
# Ingresar a la carpeta docs

echo ">>>>>>>>> Ahora se va a generar la documentacion"
read -p ">>>>>>>>> Presione enter para continuar"
cd docs

# Para borrar la carpeta de la documentacion
rm -rvf _build

# Para crear los objetos de la documentacion
sphinx-apidoc -o . ..

# Para crear la documentacion
make html > /dev/null 2>&1

echo ">>>>>>>>> Ahora se va abrir la documentacion en el navegador"
read -p ">>>>>>>>> Presione enter para continuar"
# abrir en el navegador
firefox _build/html/index.html &

# salir de la carpeta docs
cd ..

# ------------------------------------------------------------
#                    Pruebas Unitarias 
# migrarcion
python manage.py migrate

# Para crear las pruebas unitarias
pytest 

# ------------------------------------------------------------

# para poblar la BD de prueba
python manage.py loaddata datos.json



python manage.py runserver