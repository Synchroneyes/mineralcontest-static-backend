---
title: Configurer le plugin Mineral Contest
description: Cette article explique comment configurer le plugin Mineral Contest.
author: Synchroneyes

---

# Configuration du plugin Mineral Contest

[[toc]]


## Introduction


Au sein du plugin MineralContest, il existe deux différentes façon de configurer le plugin. La première est les fichiers de configuration, la seconde est les commandes en jeu.

## Configuration du plugin


Par défaut, le plugin est préconfiguré pour fonctionner sur un serveur qui vient tout juste d'être crée et ne requiert aucune configuration. Cependant, en fonction de vos besoins, vous pouvez être amené à modifier la configuration du plugin.
La configuration du plugin est disponible dans `plugins/mineralcontest/config/plugin_config.yml`

```yaml
world_name: world                   # Le nom du monde à utiliser, si vous souhaitez executer le plugin dans un monde en particulier, changez la valeur
language: french                    # Le langage à utiliser, ne pas changer. Il manque des traductions dans le plugin pour la version english.
enable_metrics: true                # Activer ou non l'envoi de statistique.
enable_auto_update: true            # Activer ou non la mise à jour automatique du plugin
enable_mysql_storage: false         # Activer ou non l'utilisation de MySQL pour le plugin
enable_community_version: false     # Activer ou non la version communautaire sur le plugin. C'est-à-dire ajouter la possibilité de démarrer plusieurs parties en même temps, non recommandé
min_player_per_group: 6             # Pour la version communautaire, le nombre de joueur minimum par groupe pour que la partie démarre
player_location_refresh_rate: 10    # Nombre de tick entre chaque rafraichissement des HUD des joueurs
enable_bloc_warning: true          # Afficher ou non un message d'avertissement lorsqu'on intéragit avec un bloc dans le monde "world_name"
enable_lobby_bloc_protection: true # Activer ou non la protection des blocs dans le monde "world_name"
```



Pour activer ou désactiver un paramètre, il suffit de saisir true ou false. `true` pour activer, `false` pour désactiver

## Utilisation de MySQL


Le plugin supporte l'utilisation de MySQL et enregistre certaines informations dans votre base de données tel que les achats dans la boutique, les statistiques d'une partie (les éliminations, les kits choisis, les joueurs, les coffres...). Libre à vous d'activer ou non cette fonctionnalité. Elle n'est pas obligatoire.
Le plugin va automatiquement créer les tables et tout ce qui est nécessaire.
Le fichier se trouve dans `plugins/mineralcontest/config/mysql_config.yml`
```yaml
host: "hostname" # Le nom d'hôte de votre base de donnée
port: 3306 # Le port de votre BDD
username: "username" # Le nom d'utilisateur à utiliser
password: "password" # Le mot de passe
database: "database" # Le nom de la base de donnnée à utiliser
```


## Configuration du coffre d'arène


Il est possible de configurer les objets pouvant apparaître dans le coffre d'arène ainsi que les probabilités de ces derniers.
Le fichier de configuration est présent dans `plugins/mineralcontest/config/arena/arena_chest_content.yml`

```yaml
chest_content:
  gold_item:
    name: GOLD_INGOT
    probability: 35
  iron_item:
    name: IRON_INGOT
    probability: 50
  diamond_item:
    name: DIAMOND
    probability: 10
  emerald_item:
    name: EMERALD
    probability: 5
```

Vous pouvez ajouter de nouveaux élements, exemple:
```yaml
chest_content:
  random_item:
    name: DIAMOND_SWORD
    probability: 1
  gold_item:
    name: GOLD_INGOT
    probability: 35
  iron_item:
    name: IRON_INGOT
    probability: 50
  diamond_item:
    name: DIAMOND
    probability: 10
  emerald_item:
    name: EMERALD
    probability: 4
```
La liste des nom d'objets est disponible ici: https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html - La somme totale des probabilités doit être 100

## Configuration d'une partie de Mineral Contest

Le fichier de configuration d'une partie mineralcontest est assez large et vaste. Vous avez deux moyens de modifier les paramètres d'une partie. La première est de modifier manuellement le fichier présent dans `plugins/mineralcontest/config/game/game_settings.yml`. La seconde est en jeu via le biais de la commande `/mcvar xxx`

Le fichier ci-dessous contient l'ensemble des paramètres:

```yaml
config:
  cvar:
    mp_randomize_team: '0' # Activer ou non la composition aléatoire des équipes, 0 = désactivé, 1 = activé
    mp_enable_item_drop: '1' # Permet d'activer ou non le drop d'item à la mort. 0 pour aucun, 1 pour les minerais uniquement, 2 pour tout
    SCORE_IRON: '10' # Le nombre de point que rapporte le dépot d'un lingot de fer
    SCORE_GOLD: '50' # Le nombre de point que rapporte le dépot d'un lingot de d'or
    SCORE_DIAMOND: '150' # Le nombre de point que rapporte le dépot d'un diamant
    SCORE_EMERALD: '300' # Le nombre de point que rapporte le dépot d'un émeraude
    SCORE_REDSTONE: -3 # Le nombre de point que les autres équipes vont perdre lors du dépot d'une Redstone dans le coffre
    mp_enable_friendly_fire: '1' # Activer ou non les dégats entre membre d'une même équipe
    mp_enable_old_pvp: '1' # Activer ou non un mode PVP similaire à la version 1.8
    mp_enable_block_adding: '1' # Activer ou non la pose de bloc dans la zone d'arène/base
    drop_chest_on_death_time: '60' # La durée d'apparition d'un coffre de joueur mort en seconde
    mp_set_playzone_radius: '1000' # Le rayon d'action d'une partie. Plus la valeur est grande, plus la partie jouable sera grande
    max_teleport_time: '15' # La durée durant laquelle les joueurs peuvent faire /arene, en seconde
    points_per_kill: '0' # Le nombre de point qu'un joueur peut rapporter à son équipe en éliminant un adversaire
  settings:
    game_time: '60' # La durée d'une partie, en minute
    death_time: '10' # Le délai de réapparition, en seconde
    pre_game_timer: '10' # Le délai avant de démarrer une partie quand tout le monde est prêt, en seconde
    enable_monster_in_protected_zone: '0' # Activer ou non l'apparition de monstre dans la zone arène/base
    end_game_timer: '60' # La durée de la période de fin de partie, avant de retourner au monde principal, en seconde
    protected_zone_area_radius: '55' # Le rayon en bloc qui défini la taille de l'arène et des bases
    drop_chest_on_death: '1' # Activer ou non l'apparition de coffre contenant l'ensemble des items d'un joueur à la mort. Il fonctionne avec le mp_enable_item_drop. Au lieu de faire tomber les objets au sol, un coffre apparait avec les objets
    drop_chest_on_death_time: '60' # La durée d'apparition du coffre, en seconde
    enable_chat_from_other_worlds: '1' # Activer ou non le chat entre les différents mondes, si l'option communautaire est activée
    enable_nether: '0' # Activer ou non l'accès au Nether
  shop:
    enable_shop: '1' # Activer ou non les boutiques dans les bases
  kits:
    enable_kits: '1' # Activer ou non l'utilisation de kit
  arena:
    chest_opening_cooldown: '5' # Le temps en seconde avant d'ouvrir le coffre de l'arène
    max_time_between_chests: '15' # La durée en minute maximale entre chaque apparition du coffre
    min_time_between_chests: '10' # La durée en minute minimale entre chaque apparition du coffre
    chicken_spawn_time: '5' # Au bout de combien de minute avant la fin les vagues de poulets doivent commencer. Exemple si 5 alors les vagues commenceront 5 minutes avant la fin
    chicken_spawn_interval: '30' # Le délai entre chaque vague d'apparition, en secondes
    chicken_spawn_min_count: '2' # Le nombre minimum de poulet dans une vague
    chicken_spawn_max_count: '5' # Le nombre maximum de poulet dans une vague
    chicken_spawn_min_item_count: '1' # Le nombre minimum d'objets qu'un poulet peut faire tomber à sa mort
    chicken_spawn_max_item_count: '3' # Le nombre maximum d'objets qu'un poulet peut faire tomber à sa mort
    max_item_in_chest: '20' # Le nombre maximum d'objets dans le coffre d'arène
    min_item_in_chest: '10' # Le nombre minimum d'objets dans le coffre d'arène
    arena_warn_chest_time: '10' # Permet de définir le temps restant en seconde avant de mettre un message dans le chat annonçant l'arrivée du coffre d'arène
    arena_safezone_radius: '5' # Permet de modifier le rayon de safezone de la zone de téléportation de l'arène
  airdrop:
    max_time_between_drop: '25' # Permet de définir le temps maximum en minute entre chaque largage
    min_time_between_drop: '20' # Permet de définir le temps minimum en minute entre chaque largage
    max_distance_from_arena: '300' # Permet de définir la distance maximale en bloc entre la génération de position du largage et le centre de l'arène
    min_distance_from_arena: '150' # Permet de définir la distance maximale en bloc entre la génération de position du largage et le centre de l'arène
    normal_falling_speed: '40' # Permet de définir la vitesse de chute lorsque le parachute est présent (en nombre de ticks, 20 ticks environ égale à 1 sec)
    max_item_in_drop: '40' # Permet de définir le nombre d'item minimum présent dans le coffre du largage
    min_item_in_drop: '30' # Permet de définir le nombre d'item minimum présent dans le coffre du largage
    drop_opening_time: '10' # Permet de définir le nombre définir le temps d'ouverture du coffre du largage
    drop_display_time: '5' # Permet de définir combien de temps en seconde le message contenant la localisation du largage doit s'afficher
  game:
    enable_hunger: '1' # Activer ou non la faim
```

## Configuration de l'équipement par défaut d'un joueur

Il est possible de configurer l'équipement par défaut d'un joueur de deux manières, via une commande en jeu (`/mcdefaultitems`) ou via un fichier de configuration `plugins/mineralcontest/config/game/player_base_items.yml`.
```yaml
items:
  IRON_HELMET: 1
  IRON_CHESTPLATE: 1
  IRON_LEGGINGS: 1
  IRON_BOOTS: 1
  COOKED_BEEF: 63
  ARROW: 63
  BOW: 1
  IRON_SWORD: 1
```
La liste des nom d'objets est disponible ici: https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html. Le nombre est la quantité`
