Documentation pour le scripting
=======================

C'est quoi une Rule ?
---------------
Une rule (ou règle) est le patron (template) d'un tour. Il permet de générer une phrase qui sera affichée aux joueurs.

Il est composé de :
* min_sip `Entier: Le nombre minimum de gorgées que cette règle distribuera`
* max_sip `Entier: Le nombre maximum de gorgées que cette règle distribuera`
* nb_players `Entier: Le nombre de joueurs impliqués dans cette règle`
* description `String: Une description de la règle, utile uniquement pour nous y retrouver en tant de developpeurs`
* randomizable `Booléen: Cette règle peut-elle tomber par hasard au cours d'une partie ou doit-elle être invoquée par une autre règle (voir l'exemple)`
* script `Le script qui sera executé à chaque fois que la règle utilisée`

Comment scripter ?
---------------
#### Définir une variable pour une Game:

```python
# On peut stocker un entier (0, 1, 50),
# une chaîne de caractères (taille maximale de 500 caractères)
# ou un objet de la base, par exemple une Rule ou une Game.
game.set_value("variable_name", "variable_value")
```

#### Récupérer une variable

```python
game.get_value("variable_name")
```
Si la variable n'existe pas, `get_value` retourne `None`. Il est possible de modifier cette valeur par défaut en passant un second argument, par exemple `game.get_value("variable_name", False)`.

#### Définir un nouveau tour de jeu

```python
turn.generate("La string à afficher aux joueurs")
```

#### Récupérer le nombre de gorgées

```python
nombre_gorgees = nb_sip
```
`nb_sip` est prédéfini à une valeur aléatoire comprise entre `min_sip` et `max_sip`

#### Récupérer la liste des joueurs impliqués dans la règle

```python
joueurs_impliques = involved_players
joueur1 = joueurs_impliques.pop()
joueur2 = joueurs_impliques.pop()
```

#### Faire boire un joueur

```python
joueur1 = involved_players.pop()
# Le joueur bois le nombre de gorgées généré par la règle 
game.has_drink(joueur1, sip=nb_sip)

# Le joueur prend un cul sec
game.has_drink(joueur1, bottom=True)
```

#### Créer une règle qui en suit un autre
```python
turn.future(min_turn=3, max_turn=6, rule=rule.next, players=[])
```
`min_turn` est le nombre de tours minimum avant que cette règle apparaisse
`max_turn` est le nombre maximum de tours avant que cette règle apparaisse
`rule` est la règle qui doit intervenir
`players` est la liste des joueurs impliqués dans la règle à venir

Exemples
-------------
### A faire boire B, puis B se venge
Réalisons une règle où le joueur A fait boire 3 à 4 gorgées au joueur B, puis le joueur B se venge 2 à 3 tours après.

#### La règle initiale
* `script` :

```python
# On récup nos deux joueurs à partir de la liste des joueurs impliqués
donneur = involved_players.pop()
buveur = involved_players.pop()
#On enregistre le faite qu'un joueur ai bu
game.has_drink(buveur, nb_sip=nb_sip)

# On crée le tour de vengeance
turn.future(min_turn=2, max_turn=3, rule=rule.next, players=[donneur, buveur])

# On génère la phrase à afficher
turn.execute("%s fait boire %s gorgées à %s" % (donneur, nb_sip, buveur))
```

* `values` :
    * min_sip = 3
    * max_sip = 4
    * nb_players = 2
    * next = La règle définie ci-dessous
    * randomizable = True `Cette règle peut tomber aléatoirement`

#### La règle de vengeance
* `script` :

```python
# On récup nos deux joueurs à partir de la liste des joueurs impliqués
ex_donneur = involved_players.pop()
ex_buveur = involved_players.pop()

#On enregistre le faite qu'un joueur ai bu
game.has_drink(ex_donneur, nb_sip=nb_sip)

# On génère la phrase à afficher
turn.execute("%s se venge et fait boire %s gorgées à %s" % (ex_buveur, nb_sip, ex_donneur))
```

* `values` :
    * min_sip = 3
    * max_sip = 4
    * nb_players = 0 `Cette valeur n'a aucune importance, car les joueurs impliqués sont choisis par la règle "mère"`
    * next = None `Il n'y a pas de règle suivante`
    * randomizable = False `On ne veut pas voir cette règle apparaitre s'il n'y a pas eu la première`
