
rm -rf .git/__pycache__
rm -rf .gitignore/__pycache__
rm -rf core/__pycache__
rm -rf permisos/__pycache__
rm -rf Proyectos/__pycache__
rm -rf .pytest_cache/__pycache__
rm -rf pytest.ini/__pycache__
rm -rf requirements.txt/__pycache__
rm -rf Sprint/__pycache__
rm -rf SSO/__pycache__
rm -rf tests/__pycache__
rm -rf UserStories/__pycache__
rm -rf Usuarios/__pycache__

rm -rf .git/migrations
rm -rf .gitignore/migrations
rm -rf core/migrations
rm -rf permisos/migrations
rm -rf Proyectos/migrations
rm -rf .pytest_cache/migrations
rm -rf pytest.ini/migrations
rm -rf requirements.txt/migrations
rm -rf Sprint/migrations
rm -rf SSO/migrations
rm -rf tests/migrations
rm -rf UserStories/migrations
rm -rf Usuarios/migrations


mkdir core/migrations
mkdir permisos/migrations
mkdir Proyectos/migrations
mkdir Sprint/migrations
mkdir SSO/migrations
mkdir UserStories/migrations
mkdir Usuarios/migrations

touch core/migrations/__init__.py
touch permisos/migrations/__init__.py
touch Proyectos/migrations/__init__.py
touch Sprint/migrations/__init__.py
touch SSO/migrations/__init__.py
touch UserStories/migrations/__init__.py
touch Usuarios/migrations/__init__.py