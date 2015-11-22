-- Table definitions for the tournament project.
-- by michael rosata

drop database if exists tournament;
create database tournament;
\c tournament;

drop table if exists
    tournaments, players, matches;

-- Reviewer said to calculate tournament id of open tournament in code by
-- calculating matches rather than listing whether the tournament is open or
-- not. I think if in the future there were thousands of tournaments it would
-- be easier to search for a column that indicates a tournament is opened or
-- closed rather than calculate # of players and matches in each tournament then
-- compare to calculation of total matches in the tournament. I am taking advice
-- of reviewer but I wonder if in a case like this it is better to not have to
-- do calculations to figure out which tournaments are closed. Maybe compromise
-- would be to not allow 2 tournaments to run at the same time and only grab
create table tournaments (
  tournament_id serial primary key,
  opened timestamp null default current_timestamp
);

create table players (
  player_id serial primary key,
  player_name varchar(30),
  tournament_id int references tournaments (tournament_id)
);

-- My code review said not to put 'loser' in table because the winner can be
-- calculated by the playerStandings function. However, recording the loser
-- in a tournament database is a function of history/recording. In competitions
-- it is always an interest to know who a winner won their matches against.
create table matches (
  match_id serial primary key,
  tournament_id integer,
  loser integer references players (player_id),
  winner integer references players (player_id) null
);
