# Borgia-demo
Fork of Borgia-app repo. Demo Version

## Get started : initial commands

Bootstrap vas __pour l'instant__ mieux avec less. (Cela changera avec bootstrap 4)
* S'assurer que LESS est installé (avec ``npm install -g less``)

* Charger les db et dumps :
    * ``python manage.py makemigrations users shops finances modules settings_data notifications stocks``
    * ``python manage.py migrate``
* Changer le mdp admin :
    * ``python manage.py loaddata first_member``
    * ``python manage.py shell``
    * ``from users.models import User``
    * ``u = User.objects.get(pk=2)``
    * ``u.set_password('admin')``
    * ``u.save()``
* Puis :
    * ``python manage.py loaddata initial``


### Update requirements.txt
Ce fichier contient tout les modules python nécessaires pour l'execution de borgia.
Celui-ci peut être mis à jour en théorie avec la commande suivante :

* ``pip freeze -r devel-req.txt > stable-req.txt``

Cependant, ceci ajoute TOUT les modules installés par pip. Donc également les éventuels modules ajoutés pour d'autres projet.

### Installer les modules avec le fichier requirements.txt

Pour installer les modules, il suffit d'effectuer la commande :

``pip install -r requirements.txt``


## Note pour Linux (et mac ??):

Python est installé par défaut avec deux version : 2 et 3. 2 étant la version par défaut.
Or Django (et donc Borgia) fonctionnent avec la version 3. Pour les difféfentes manip (notamment celle ci-dessus), il faut utiliser ``python3``. De même, il faudra utiliser ``pip3``


## Fonctionnement Graphique:

 Le nouveau fonctionnement est le suivant : on génère un fichier "bootstrap" modifié, en utilisant LESS :
 Les variables de bootstrap sont définies pour obtenir le template.
 Si-besoin, on ajoute un fichier de style en LESS (ici main). Cici nous permet de changer facilement de template.
 De plus ce fichier est moins volumineux, car on supprime les modules de bootstrap non-utilisés.

 Le sous-dossier less/less contient les fichiers originaux de bootstrap non-modifiés.

  #### COMPILATION DES FICHIERS LESS ####
 from static_precompiler.utils import compile_static
 compile_static(static/less/bootstrap-birse.less)
 compile_static(os.path.join(BASE_DIR, 'static', 'less', 'bootstrap-light.less'))
 compile_static(os.path.join(BASE_DIR, 'static', 'less', 'bootstrap-dark.less'))


## SharedEvent - TODO List :

- Ajouter une option pour se faire une marge (si c'est pas déjà le cas)
- Ajouter une fonction pour définir le prix par pondération (et pas par prix total)
- Ajout d'un indicateur visuel pour dire que l'ajax s'est bien (ou mal) passé

- Js loaddé partout, restreindre



## Current Version :
Build 4.4
