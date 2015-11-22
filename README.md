### Tournament Project

This is the Relational Database Project for the Udacity FullStack Nanodegree. Please note that the test functions inside tournament_test.py have been renamed to satisfy general Python industry best practices that we were instructed to follow in the first course. So if ran against a different copy of tournament_test.py the test file will not run. Follow the instructions below to download and run the tests. Thanks!

This project will aid in managing Swiss Style Tournaments. The following functions are available for you to use in your programs. First you will want to import the `tournament` module to take advantage of it's utilities.

```py
from tournament import *

# connect only connects to database 1 time, subsequent calls return original object 
# We stil can get unique cursors. To illustrate this point:
connect() == connect()                     # True  same object returned
connect().cursor() == connect().cursor()   # False 
 
# You don't need to connect to the database, rather to setup
# a new tournament and get a return id of new tournament as an int.
tournament_id = create_tournament()

# Register players into the current tournament
register_player('Alena Stakroft') # returns int ID of player.
# Optionally, register a player into a specific tournament. 
# (If the tournament has started it will throw Error)
register_player('Cheater McNally', 2)

# Remove all players from a specific tournament or the entire database
delete_players(tournament_id) # Remove all players from tournament
delete_players() # all gone
# Same thing with matches. Pass an integer to drop all matches from tournament
# or no arguments shall drop every match from the database.
delete_matches(tournament)
delete_matches()

# Need to find out the current running tournament? There's a global for that,
the_tournament.get_tournament()

# All good tournaments must register players, so let's get a few for examples.
p1 = register_player("Krunk Fu Panda")
p2 = register_player("Alena Sarkov")
p3 = register_player("Darkling")
p4 = register_player("Caelaina Sardothian")

# To report matches you must supply the id of the winner. You may optionally supply
# the id of the loser for historical record and whatnot, but it's not required.
# I would suggest recording losers, you may use None when there is a "bye"
report_match(p1)
report_match(p2, p3)

# Get a list of all players from every tournament and their standins. This returns 
# a list of tuples containing (player_id int, name str, wins int, losses int)
standings = player_standings()
print standings  # output a long list of players in order best to worst
standings = player_standings(4)
print standings # only the players in the listed tournament

# The grand utility of the module is swiss pairing which returns a list of pairs
# of players for the next round matchup of current tournament. More info also below.
swiss_pairings() # output a list of tuples containing matchups as 
                 # (player id, p1 name, player2 id, p2 name)
```

#### Additional Information
The `swiss_pairings()` function returns a list of pairs of players for the next round of a match.
>>  Assuming that there are an even number of players registered, each player appears exactly once in the pairings.  Each player is paired with another player with an equal or nearly-equal win record, that is, a player adjacent to him or her in the standings. The function returns a list of tuples, each of which contains `(id1, name1, id2, name2)` where `id1` is the first player's unique id, `name1` is the first player's name, `id2` is the second player's unique id and `name2` is the second player's name. This list will contain a tuple for each pair needed in next round. If there is an odd amount of players in the tournament then one of the players will get a "bye" round and the "bye" is represented as `None` because there is no id for a non-existant player. [(22, 'mike', None, 'Bye This Round')]. **Each player will only have one "bye" per tournament**


Installation and Testing
-----
1. To setup the project, first clone the repo using `git clone https://github.com/mrosata/fullstack-tournament.git` and then move into the project directory using `cd fullstack-tournament`.
2. Next, you will want to setup the vagrant box on your system, to do this simply move into the root project folder `cd fullstack-tournament` and then run the command `vagrant up`. This will take a couple moments to complete setup, once it is done you may connect to the vagrant box from the current folder using the command `vagrant ssh`.
3. At this point you are now working from inside the virtual machine. Your command line should start with "vagrant@vagrant-ubuntu-trusty-32:~", navigate to the project directory by entering `cd /vagrant/tournament`
4. Run `psql < tournament.sql` to create a new database named "tournament".
5. To execute tests, `python tournament.sql`

> All 8 tests should pass.


Michael Rosata 2015.
Udacity Full Stack Nanodegree