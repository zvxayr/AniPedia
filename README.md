# AniPedia [![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) ![t](https://img.shields.io/badge/status-unstable-red.svg)

## Setup

### Installation
```console
$ python -m pip install pubsub
$ python -m pip install wxPython
```

### Database (build from raw)
- Download or clone this repository
- Download the files `AnimeList.csv`, `UserList.csv`, and `UserAnimeList.csv` from the [MyAnimeList Dataset](https://www.kaggle.com/azathoth42/myanimelist) by *Azathoth*
- Move the csv files to the root directory of the repository
- Run the following console command at the root directory of the repository

```sh
$ python -m database.converter
```

### Database (compiled)
- Download `database.db` from this [link](https://mymailmapuaedu-my.sharepoint.com/:u:/g/personal/cpfornoles_mymail_mapua_edu_ph/EcJ1zt65JBlLobFzxfVljZQBJt4Mbi7wIJa6uGlr15jAFA?e=8oAD4d) and copy it to the root directory of the repository

## Testing
Move to the root directory of the repository and run the command
```console
$ python -m unittest
```

## Running
```console
$ python -m main
```
