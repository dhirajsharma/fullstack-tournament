#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


# Exception which is raised when trying to register a new player into a
# tournament that has already begun playing.
class CheaterException(Exception):
    pass

# Exception raised when you try to get pairings for a tournament that has
# no more remaining rounds.
class NoMoreTournamentRounds(Exception):
    pass

# When information is asked to be found that doesn't make sense to the current
# tournament, player or round.
class TournamentMixupWarning(Warning):
    pass


class Current_Tournament:
    """
    I've decided to create a tournament class to manage the current tournament id
    in python. Basically it simply keeps a reference to a created tournament and
    makes that available
    """
    tournament = None

    def get_tournament(self):
        """Return the current tournament id or create new tournament"""
        if self.tournament is None:
            self.tournament = create_tournament()
        return self.tournament

    def tournament_info(self, tournament_id=None):
        """Get a tuple showing (number players, matches played, rounds left)"""
        if tournament_id is None:
            tournament_id = self.get_tournament()

        c = connect().cursor()
        c.execute("""
        select player_count, match_count, active from
        tournament_info where tournament_id = %s""", (tournament_id,))
        row = c.fetchone()
        if len(row) < 3:
            raise Exception
        commit(c)
        return int(row[0]), int(row[1]), bool(row[2])


def tournament_from_player(player_id):
    """Get the tournament id from player id"""
    c = connect().cursor()
    try:
        c.execute("""
        select tournament_id from players where player_id = %s""", (player_id,))
        row = c.fetchone()
        tournament_id = int(row[0])
    except psycopg2.DataError:
        tournament_id = None
    return tournament_id


def opponent_from_player(player_id):
    """Get the opponent id from the player id passed in for current round"""
    tournament_id = tournament_from_player(player_id)
    if tournament_id is None:
        raise CheaterException
    pairings = swiss_pairings(tournament_id)
    if not len(pairings) > 0:
        return False
    for pair in pairings:
        if pair[0] == player_id:
            return pair[2]
        if pair[2] == player_id:
            return pair[0]

    # Raise Warning because user is passing weird info, could be mistake
    raise TournamentMixupWarning


def create_tournament():
    c = connect().cursor()
    c.execute("""
    insert into tournaments (opened) values (null) returning tournament_id""")
    tournament_id = c.fetchone()[0]
    commit(c)
    return int(tournament_id)


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    However, if we already have a globally accessable connection then we will
    just return that. If dbconnection' global is set, then it is our
    connection. (todo: add check to make sure global var is actual connection)
    """

    if globals().has_key('dbconnection'):
        return dbconnection
    else:
        return psycopg2.connect('dbname=tournament')


def commit(cursor=None):
    """Commit the current data and close a cursor if passed in"""
    if globals().has_key('dbconnection'):
        dbconnection.commit()
        if cursor is not None:
            cursor.close()
    else:
        raise Exception('It is good to commit, but there\'s no connection!')


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
    commit(c)


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
    commit(c)


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
    count = int(c.fetchone()[0])
    commit(c)
    return count


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
        tournament_id = globals()['tournaments'].get_tournament()

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
    commit(c)
    return player_id


def player_standings(tournament_id=None):
    """Returns a list of the players and their win records, sorted by wins.
    :arg tourney_id int - optional, the tournament that you want standings from

    If you pass no argument or None as tournament_id then you will get results
    of the current tournament. If you pass the 'all' as the tournament_id then
    you will get player standings from the entire database. Throughout all
    tournaments

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        player_name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect().cursor()
    if tournament_id == 'all':
        c.execute("""
        select player_id, player_name, (select count(*) from matches
        where winner = player_id) as wins,
        (select count(*) from matches where winner = player_id
        or loser = player_id) as matches
        from players order by wins desc""", (tournament_id,))
    else:
        if tournament_id is None:
            tournament_id = tournaments.get_tournament()

        # Get specific Tournament id
        c.execute("""
        select player_id, player_name, (select count(*) from matches
        where winner = player_id) as wins,
        (select count(*) from matches where winner = player_id
        or loser = player_id) as matches
        from players where tournament_id = %s order by wins desc"""
                  , (tournament_id,))

    rows = c.fetchall()
    # Commit standings and close connection.
    commit(c)
    # Return the players standings
    return list((r[0], r[1], int(r[2]), int(r[3])) for r in rows)


def report_match(winner, opponent=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
     # We can use the opponent_from_player to figure out who the loser should be
    c = connect().cursor()
    c.execute("""
    -- Get the tournament id of match using id of winner in sub-query.
    -- Calculate Round # using ceiling(.5(total matches/ total players))
    -- Record the winner, loser
    INSERT into matches (tournament_id, winner, loser)
    values (
         (select tournament_id from players where player_id = %s),
         %s,
         %s) -- returning winner, loser""",
              (winner, winner, opponent))
    try:
        rows = c.fetchall()
        # Print out the match information to console.
        for row in rows:
            print 'round: ', row[0]
            print 'winner: ', row[1]
            print 'loser: ', row[2]
    except psycopg2.DatabaseError:
        pass

    # Commit the round and close connection.
    commit(c)
 
 
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
    # If not tournament_id was passed in then we need to solve for it
    if tourney_id is None:
        tournament_id = tournaments.get_tournament()
    else:
        tournament_id = tourney_id


    players, matches_played, active = tournaments.tournament_info(tournament_id)
    # We get the tournament status so that we know if this tournament can pair
    if not active:
        raise NoMoreTournamentRounds

    #TODO: Make sure that we haven't exceeded the amount of logical rounds.
    # If matches are 0, then there's no rank, we can arbitrarily match players
    if matches_played > 0:
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
    commit(c)
    return unique_swiss_pairings(pairs, tournament_id)


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
            select ((select count(*) from matches where tournament_id = %s and
            winner = %s and loser = %s) + (select count(*) from matches where
            tournament_id = %s and winner = %s and loser = %s)) as num
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

# This will manage the id of the current tournament.
tournaments = Current_Tournament()