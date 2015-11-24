### Tournament Project

This is the Relational Database Project for the Udacity FullStack Nanodegree. Please note that the test functions inside tournament_test.py have been renamed to satisfy general Python industry best practices that we were instructed to follow in the first course. So if ran against a different copy of tournament_test.py the test file will not run. 

This project will help manage multiple Swiss style tournaments. It includes a main module for use with all your swiss style competition needs including (registration, match recording, ranking and pairing) along with a test file which will help you find issues should you have issues or decide to extend the project yourself. An install of Postgres > 9.3 is suggested for use in this project and users without a Postgres install will benefit from the Vagrantfile packaged in this repo. If you need help building the database read the section `Installation and Testing` below.

Use `import * from tournament` to import `tournament.py` from the same directory

```py
# If you installed database, import functionality into your project.
from tournament import *

# a cutom connect function manages a single database connection through entire
# execution, subsequent calls return original connection. We stil can get 
# unique cursors. To illustrate this point:
connect() is connect()                     # True  same object returned
connect().cursor() is connect().cursor()   # False different cursors
 
# You don't need to manage db connections, rather just go setup
# a new tournament and get a return id of new tournament as an int.
tournament_id = create_tournament()

# Register players into the current tournament
register_player('Alena Stakroft') # returns int ID of player.
# Optionally, register a player into a specific tournament. 
register_player('Cheater McNally', 2)
# Note: that if you register a player into a tournament that has 
# already begun the module will raise a CheaterException.

# Remove all players from a specific tournament or the entire database
delete_players(tournament_id) # Remove all players from tournament
delete_players() # all gone
# Same thing with matches. Pass an integer to drop all matches from tournament
# or no arguments shall drop every match from the database.
delete_matches(tournament)
delete_matches()

# Need to find out the current running tournament? There's a global manager, use:
tournaments.get_tournament()

# tournament_info method has info on any tournament handled by the program, by default
# it will return the current tournament's info, pass by id to see another tournaments 
# info. Returns tuple with (player count, matches played, bool if rounds remain)
tournaments.tournament_info(id)

# All good tournaments must register players, so let's get a few for examples.
p1 = register_player("Krunk Fu Panda")
p2 = register_player("Alena Sarkov")
p3 = register_player("Caelaina Sardothian")

# The swiss_pairing() function isn't required. You can create your own round 1 
# matchups. Report matches by supplying the id of the winner and the loser.
# A "bye" is reported using None as the loser.
report_match(p1, p3)
report_match(p2, None)

# listed rankings for current tournament, a list of tuples that have format
# (player_id int, name str, wins int, losses int)
print player_standings()
# get a previous tournament or similatanous tournaments player rankings.
print player_standings(4)
# Get a list of all players from every tournament and their standins. 
print player_standings('all')

# The grand utility of the module is swiss pairing which returns a list of pairs
# of players for the next round matchup of current tournament. More info also below.
swiss_pairings() # output a list of tuples containing matchups as 
                 # (player id, p1 name, player2 id, p2 name)
                 
# There are 3 utility functions that you may use as well
player_id = 10
# get the tournament that the current player is in
print tournament_from_player(player_id)  # 1
# get the current opponent this round for a player
opponent_from_player(player_id)
# Start a new tournament, for multiple tournaments
create_tournament()
```

#### Additional Information
The `swiss_pairings()` function returns a list of pairs of players for the next round of a match.
>- Assuming that there are an even number of players registered, each player appears exactly once in the pairings.  Each player is paired with another player with an equal or nearly-equal win record, that is, a player adjacent to him or her in the standings. The function returns a list of tuples, each of which contains `(id1, name1, id2, name2)` where `id1` is the first player's unique id, `name1` is the first player's name, `id2` is the second player's unique id and `name2` is the second player's name. This list will contain a tuple for each pair needed in next round. If there is an odd amount of players in the tournament then one of the players will get a "bye" round and the "bye" is represented as `None` because there is no id for a non-existant player. [(22, 'mike', None, 'Bye This Round')]. **Each player will only have one "bye" per tournament**

Swiss Pairing Exceptions
-----
`CheaterException` is raised when trying to register a new player into a tournament that has already begun playing.

`NoMoreTournamentRounds` will be raised when you try to get pairings for a tournament that has no more remaining rounds.

`class TournamentMixupWarning` is a warning raised if information is passed into utility functions such as `opponent_from_player` that don't make sense. For example if you pass a player id into the function that shouldn't have an opponent because the id doesn't exist then it will raise the warning.


Installation and Testing
-----
1. To setup the project, first clone the repo using `git clone https://github.com/mrosata/fullstack-tournament.git` and then move into the project directory using `cd fullstack-tournament`.
2. Next, you will want to setup the vagrant box on your system, to do this simply move into the root project folder `cd fullstack-tournament` and then run the command `vagrant up`. This will take a couple moments to complete setup, once it is done you may connect to the vagrant box from the current folder using the command `vagrant ssh`.
3. At this point you are now working from inside the virtual machine. Your command line should start with "vagrant@vagrant-ubuntu-trusty-32:~", navigate to the project directory by entering `cd /vagrant/tournament`
4. Run `psql < tournament.sql` to create a new database named "tournament".
5. To execute tests, `python tournament_test.py`

> All 8 tests should pass. If they don't you can pass the blame onto me in the [issues section](https://github.com/mrosata/fullstack-tournament/issues)


[Michael Rosata](mailto:mrosata1984@gmail.com) 2015.
[Udacity Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)