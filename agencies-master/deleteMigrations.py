import os

from config.settings import BASE_DIR

files = ['admin', 'auth', 'contenttypes', 'sessions']
# files = ['admin']

path = 'C:/repositorios/AGENCIES/agencies'
pathEnv = os.path.join(path, 'env/Lib/site-packages/django/contrib')

for l in files:
    print(l)
    for d in os.listdir(os.path.join(pathEnv, l, 'migrations')):
    # for d in os.scandir(os.path.join(pathEnv, l, 'migrations')):
        if d != '__init__.py' and d != '__pycache__':
            print(d)
            os.remove(os.path.join(pathEnv, d, 'migrations'))

# print(os.listdir(pathEnv))
