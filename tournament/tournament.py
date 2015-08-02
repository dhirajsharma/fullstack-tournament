#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class Tournament_Data():
    """This just holds some run time information that needs to be shared within
    this particular execution. The reason for this is to help support multiple
    tournaments.
    """
    def __init__(self):
        pass



tournament = Tournament_Data()


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    However, if we already have a globally accessable connection then we will
    just return that. Assume is' dbconnection' global is set, then it is our
    connection. (todo: add check to make sure global var is actual connection)
    """
    if globals().has_key('dbconnection'):
        return dbconnection
    else:
        return psycopg2.connect('dbname=tournament')

def commit():
    if globals().has_key('dbconnection'):
        dbconnection.commit()
    else:
        raise Exception('It is good to commit, but there\'s no connection!')


def delete_matches():
    """Remove all the match records from the database."""
    c = connect().cursor()
    c.execute('delete from matches')
    commit()
    c.close()


def delete_players():
    """Remove all the player records from the database."""
    c = connect().cursor()
    c.execute('delete from players')
    commit()
    c.close()


def count_players():
    """Returns the number of players currently registered."""
    c = connect().cursor()
    c.execute('select count(*) from players')
    count = int(c.fetchone()[0])
    commit()
    c.close()
    return count


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
    """Returns a list of the players and their win records, sorted by wins.
    :arg tourney_id int - optional, the tournament that you want standings from

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect().cursor()
    if tourney_id is not None:
        # Get specific Tournament id
        c.execute("""
        select id, name, (select count(*) from matches where winner = id)
        as wins,
        (select count(*) from matches where winner = id or loser = id)
        as matches
        from players where tid = %s order by wins desc""", (tourney_id,))
        rows = c.fetchall()
    else:
        # We get all standings regardless of Tournament id
        c.execute("""
        select id, name, (select count(*) from matches where winner = id) as wins,
        (select count(*) from matches where winner = id or loser = id)
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
    INSERT into matches (tid, rid, winner, loser)
    values (
         (select tid from players where id = %s),
         (ceiling(
           (select count(*) from matches where tid = (select tid from
           players where id = %s)) / 2) ),
           %s,
           %s) -- returning rid, winner, loser""",
              (winner, winner, winner, loser))

    try:
        rows = c.fetchall()
        # Print out the match information to console.
        for row in rows:
            print 'round: ', row[0]
            print 'winner: ', row[1]
            print 'loser: ', row[2]
    except:
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
    return unique_swiss_pairings(pairs, tid)


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
            select ((select count(*) from matches where tid = %s and
            winner = %s and loser = %s) + (select count(*) from matches where
            tid = %s and winner = %s and loser = %s)) as num
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
