#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

<<<<<<< HEAD
class CheaterException(Exception):
    pass

class Current_Tournament:
    """
    I've decided to create a tournament class to manage the current tournament id
    in python. Basically it simply keeps a reference to a created tournament and
    makes that available
    """
    tournament = None;

    def get_tournament(self):
        if self.tournament is None:
            self.tournament = create_tournament()
        return self.tournament

    def get_round(self):
=======

class Tournament_Data():
    """This just holds some run time information that needs to be shared within
    this particular execution. The reason for this is to help support multiple
    tournaments.
    """
    def __init__(self):
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
        pass



<<<<<<< HEAD

def create_tournament():
    c = connect().cursor()
    c.execute("""
    insert into tournaments (opened) values (null) returning tournament_id""")
    tournament_id = c.fetchone()[0]
    commit()
    c.close()
    return int(tournament_id)
=======
tournament = Tournament_Data()
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    However, if we already have a globally accessable connection then we will
<<<<<<< HEAD
    just return that. If dbconnection' global is set, then it is our
    connection. (todo: add check to make sure global var is actual connection)
    """

=======
    just return that. Assume is' dbconnection' global is set, then it is our
    connection. (todo: add check to make sure global var is actual connection)
    """
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    if globals().has_key('dbconnection'):
        return dbconnection
    else:
        return psycopg2.connect('dbname=tournament')

<<<<<<< HEAD
#        except psycopg2.Error as e:
#            return 'Error Code: ', e.pgerror


=======
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
def commit():
    if globals().has_key('dbconnection'):
        dbconnection.commit()
    else:
        raise Exception('It is good to commit, but there\'s no connection!')


<<<<<<< HEAD
def delete_matches(tournament_id = None):
    """
    Remove all matches from the database or a single tournament

    :param tournament_id: Pass int id of tournament to clear only those matches
    :return:
    """
    c = connect().cursor()
    if tournament_id is None:
        c.execute('delete from matches')
    else:
        c.execute("""delete from matches where tournament_id = %s"""
                  % (tournament_id,))
=======
def delete_matches():
    """Remove all the match records from the database."""
    c = connect().cursor()
    c.execute('delete from matches')
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    commit()
    c.close()


<<<<<<< HEAD
def delete_players(tournament_id = None):
    """
    Remove all players from the database or a single tournament

    :param tournament_id: Pass int id of tournament to clear only those players
    :return:
    """
    c = connect().cursor()
    if tournament_id is None:
        c.execute('delete from players')
    else:
        c.execute("""delete from players where tournament_id = %s"""
                  % (tournament_id,))
=======
def delete_players():
    """Remove all the player records from the database."""
    c = connect().cursor()
    c.execute('delete from players')
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    commit()
    c.close()


<<<<<<< HEAD
def count_players(tournament_id = None):
    """
    Returns number of players currently registered in tournament or database.

    Ommiting the tournament_id parameter will return the count of all players
    in the database rather than in a single tournament.
    :param tournament_id:
    :return:
    """
    c = connect().cursor()
    if tournament_id is None:
        c.execute('select count(*) from players')
    else:
        c.execute("""select count(*) from players where tournament_id = %d"""
                  % (tournament_id,))
=======
def count_players():
    """Returns the number of players currently registered."""
    c = connect().cursor()
    c.execute('select count(*) from players')
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    count = int(c.fetchone()[0])
    commit()
    c.close()
    return count


<<<<<<< HEAD
def register_player(player_name, tournament_id = None):
    """
    Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)


    :param player_name:   the player's full name (need not be unique).
    :param tournament_id:  explicit tournament or current if None
    :return:   the int id of newly inserted row (player id)
    """
    c = connect().cursor()
    # first we need to find an open tournament to register the player into

    if tournament_id is None or type(tournament_id) != int:
        tournament_id = globals()['the_tournament'].get_tournament()
    else:
        # We will use the tournament passed in by user, but first we'll check
        # because we can't allow registration into tournaments which have
        # begun already.
        c.execute(
            """select count(*) from matches where tournament_id = %s"""
            % (tournament_id,))
        if int(c.fetchone()[0]) > 0:
            raise CheaterException

    # insert player into tournament
    c.execute("""
    insert into players (player_name, tournament_id) values (%s, %s) returning player_id""", (player_name, tournament_id))
    player_id = int(c.fetchone()[0])
    commit()
    c.close()
    return player_id


def player_standings(tournament_id=None):
=======
def create_tournament():
    c = connect().cursor()
    c.execute("""
    insert into tournaments (status) values ('open') returning id""")
    tid = c.fetchone()[0]
    commit()
    c.close()
    return int(tid)


def register_player(name, **kwargs):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c = connect().cursor()
    # first we need to find an open tournament to register the player into
    if not 'tournament' in kwargs:
        # No tournament passed in, ok, find an 'open' tourney for our player
        c.execute("""
        select id from tournaments where status = 'open' and winner is null""")
        try:
            tid = int(c.fetchone()[0])
        except TypeError:
            # No tournament open so we need to create one!
            tid = create_tournament()
    else:
        tid = kwargs['tournament']


    # insert player into tournament
    c.execute("""
    insert into players (name, tid) values (%s, %s)""", (name, tid))
    commit()
    c.close()


def player_standings(tourney_id=None):
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    """Returns a list of the players and their win records, sorted by wins.
    :arg tourney_id int - optional, the tournament that you want standings from

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
<<<<<<< HEAD
        player_name: the player's full name (as registered)
=======
        name: the player's full name (as registered)
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect().cursor()
<<<<<<< HEAD
    if tournament_id is not None:
        # Get specific Tournament id
        c.execute("""
        select player_id, player_name, (select count(*) from matches where winner = player_id)
        as wins,
        (select count(*) from matches where winner = player_id or loser = player_id)
        as matches
        from players where tournament_id = %s order by wins desc""", (tournament_id,))
=======
    if tourney_id is not None:
        # Get specific Tournament id
        c.execute("""
        select id, name, (select count(*) from matches where winner = id)
        as wins,
        (select count(*) from matches where winner = id or loser = id)
        as matches
        from players where tid = %s order by wins desc""", (tourney_id,))
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
        rows = c.fetchall()
    else:
        # We get all standings regardless of Tournament id
        c.execute("""
<<<<<<< HEAD
        select player_id, player_name, (select count(*) from matches where winner = player_id) as wins,
        (select count(*) from matches where winner = player_id or loser = player_id)
=======
        select id, name, (select count(*) from matches where winner = id) as wins,
        (select count(*) from matches where winner = id or loser = id)
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
        as matches from players order by wins desc""")
        rows = c.fetchall()

    # Commit standings and close connection.
    commit()
    c.close()
    # Return the players standings
    return list((r[0], r[1], int(r[2]), int(r[3])) for r in rows)


def report_match(winner, loser=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect().cursor()
    c.execute("""
    -- Get the tournament id of match using id of winner in sub-query.
    -- Calculate Round # using ceiling(.5(total matches/ total players))
    -- Record the winner, loser
<<<<<<< HEAD
    INSERT into matches (tournament_id, winner, loser)
    values (
         (select tournament_id from players where player_id = %s),
         %s,
         %s) -- returning winner, loser""",
              (winner, winner, loser))
=======
    INSERT into matches (tid, rid, winner, loser)
    values (
         (select tid from players where id = %s),
         (ceiling(
           (select count(*) from matches where tid = (select tid from
           players where id = %s)) / 2) ),
           %s,
           %s) -- returning rid, winner, loser""",
              (winner, winner, winner, loser))

>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    try:
        rows = c.fetchall()
        # Print out the match information to console.
        for row in rows:
            print 'round: ', row[0]
            print 'winner: ', row[1]
            print 'loser: ', row[2]
<<<<<<< HEAD
    except psycopg2.DatabaseError:
=======
    except:
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
        pass

    # Commit the round and close connection.
    commit()
    c.close()
 
 
def swiss_pairings(tourney_id=None):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    c = connect().cursor()
    # We need to know what tournament the players are in
    if tourney_id is None:
<<<<<<< HEAD
        # The code review asks to find runing tournament_id through calculation
        # rather than storing the id in the sql. Since only 1 tournament will
        # run at a time I have a python class to manage the tournament_id
        tournament_id = the_tournament.get_tournament()
    else:
        tournament_id = tourney_id

    c.execute("""
        select count(*) from matches where tournament_id = %s
    """, (tournament_id,))
    # We get the matches, because we can't swiss pair without having wins/loses
    matches_this_tourney = int(c.fetchone()[0])
    #TODO: Make sure that we haven't exceeded the amount of logical rounds.
    # If matches are 0, then there's no rank, we can arbitrarily match players
    if matches_this_tourney > 0:
        c.execute("""
        select player_id, player_name,
        round(
            (select count(*) from matches where winner = player_id) /
            (select count(*) from matches where winner = player_id or loser = player_id)
        , 2) as rank
        from players where players.tournament_id = %s order by rank desc
        """, (tournament_id,))
    else:
        # We will just match players by their order in tourney database
        c.execute("""
            select player_id, player_name from players where players.tournament_id = %s
        """, (tournament_id,))
=======
        c.execute("""
                select id from tournaments where status = 'open' limit 1
              """)
        tid = int(c.fetchone()[0])
    else:
        tid = tourney_id

    c.execute("""
        select count(*) from matches where tid = %s
    """, (tid,))
    # We get the matches, because we can't swiss pair without having wins/loses
    matches_this_tourney = int(c.fetchone()[0])
    # If matches are 0, then there's no rank, we can arbitrarily match players
    if matches_this_tourney > 0:
        c.execute("""
        select id, name,
        round(
            (select count(*) from matches where winner = id) /
            (select count(*) from matches where winner = id or loser = id)
        , 2) as rank
        from players where players.tid = %s order by rank desc
        """, (tid,))
    else:
        # We will just match players by their order in tourney database
        c.execute("""
            select id, name from players where players.tid = %s
        """, (tid,))
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf

    rows = c.fetchall()
    # pairs will hold our lists which will populate with match-ups of players
    pairs = []
    len_of_rows = len(rows)
    for i in xrange(0, len(rows), 2):
        if i + 1 < len_of_rows:
            pairs.append((rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1]))
        else:
            pairs.append((rows[i][0], rows[i][1], None, 'Bye This Round'))

    # return the pairs of freshly matched players
    c.close()
    commit()
<<<<<<< HEAD
    return unique_swiss_pairings(pairs, tournament_id)
=======
    return unique_swiss_pairings(pairs, tid)
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf


def unique_swiss_pairings(pairs, tournament_id, passes=0):
    """
    This function checks to make sure that pairs of players have not met before
    in this tournament. This function also handles ensuring that one player
    does not get more then 1 "bye" per tournament as "byes" are treated like a
    player won a game against no one. So If this function see's a player that
    is set to face an unregistered opponent.. it will change the pairings and
    the returned pairings will have not only 1 time only match-ups for this
    tournament, but also 1 time only 1 per player "bye" for this tournament
    """
    c = connect().cursor()
    # Make sure that we were handed a list.
    if type([]) != type(pairs):
        raise ValueError("Must pass type List into unique_swiss_pairings")
    # Store this query, which checks how many matches 2 players had together.
    sql_times_players_met = """
<<<<<<< HEAD
            select ((select count(*) from matches where tournament_id = %s and
            winner = %s and loser = %s) + (select count(*) from matches where
            tournament_id = %s and winner = %s and loser = %s)) as num
=======
            select ((select count(*) from matches where tid = %s and
            winner = %s and loser = %s) + (select count(*) from matches where
            tid = %s and winner = %s and loser = %s)) as num
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
    """
    # Now we will adjust to make sure no 2 opponents have met this tournament.
    all_good_so_far = True
    for i in range(0, len(pairs)-1):
        # basically here we add up any matches either player won where pairing
        # player was the opponent, anything above 0 means they played before!
        c.execute(sql_times_players_met,
                  (tournament_id, pairs[i][0], pairs[i][2],
                   tournament_id, pairs[i][2], pairs[i][0]))
        amnt = c.fetchone()[0]
        if amnt > 0:
            all_good_so_far = False
            # These 2 players have played before, so we must repair them.
            if i + 1 < len(pairs):
                # Counter Clockwise Twist of 2x2 pairing
                new_pair1 = (pairs[i+1][0], pairs[i+1][1],
                             pairs[i][0], pairs[i][1])
                new_pair2 = (pairs[i][2], pairs[i][3],
                             pairs[i+1][2], pairs[i+1][3])
                # Switch in the new pairings into the list
                pairs[i] = new_pair1
                pairs[i+1] = new_pair2
                if i + 1 == len(pairs):
                    # We update passes because we're in the bottom 2 pairs
                    passes = passes + 1
            else:
                if passes < 2:
                    # Bottom row + less than 3 passes through, so we will
                    # switch paired players, then counter clockwise twist
                    new_pair1 = (pairs[i][2], pairs[0][3],
                                 pairs[i-1][0], pairs[i-1][1])
                    new_pair2 = (pairs[i][0], pairs[i][1],
                                 pairs[i-1][2], pairs[i-1][3])
                    # Switch in the new pairings into the list
                    pairs[i-1] = new_pair1
                    pairs[i] = new_pair2
                    # Always increment passes in the bottom pair because this
                    # will cause a cycling issue where same 4 players are moved
                    # around but all 4 have played each other already
                    passes = passes + 1
                else:
                    passes = 0
                    # This is 4th time rotating/switching bottom pairs, so lets
                    # cycle up 2nd row to the 3rd and get new players in loop
                    swapped_pair1 = (pairs[i-1][0], pairs[i-1][1],
                                     pairs[i-1][2], pairs[i-1][3])
                    swapped_pair2 = (pairs[i-2][0], pairs[i-2][1],
                                     pairs[i-2][2], pairs[i-2][3])
                    # how do I know I can do i-2? because we are bottom row, if
                    # there were less then 4 rows, we couldn't make all these
                    # passes through bottom 2 rows switching players around, the
                    # tournament would end before ever getting to this point
                    pairs[i-2] = swapped_pair1
                    pairs[i-1] = swapped_pair2
    # If all good, return the pairs, else, we need to run all pairs in this
    # matching through this function again to see if our changes fixed pairings
    if all_good_so_far:
        return pairs
    else:
        print 'Need to search through the pairings again... MAKING CHANGES!!'
        return unique_swiss_pairings(pairs, tournament_id, passes)


"""Try to use the same connect across the whole module"""
dbconnection = connect()
<<<<<<< HEAD

# This will manage the id of the current tournament.
the_tournament = Current_Tournament()
=======
>>>>>>> bc8bf1c66abe876160d532e451023d31befbfbbf
