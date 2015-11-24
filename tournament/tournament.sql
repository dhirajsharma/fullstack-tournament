-- Table definitions for the tournament project.
-- by michael rosata

drop database if exists tournament;
create database tournament;
\c tournament;

drop table if exists
    tournaments, players, matches;

-- This table is more for historical purposes. To be able to look back and know
-- when tournaments occured. It also acts as a good way to list all tournaments
-- in the view `has_remaining_rounds` which lets us know if a tournament has
-- gone into its final round.
create table tournaments (
  tournament_id serial primary key,
  opened timestamp null default current_timestamp
);

-- Players register into tournaments. A player would have to register 2 times to
-- play in 2 tournaments
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


-- This view will tell us if a tournament still has rounds remaining. This will
-- let us know if we can intelligently run swiss_pairings. It works by taking
-- the floor of log2(players) which tells us (total rounds - 1), multiply that
-- by matches per round ceil(players in tourn / 2) and we now know how many
-- matches are in all the rounds up til the last round. So if this number is
-- greater than the total number or matches played in a round (which includes
-- bye rounds, hence the ceil()) then we can fix up another rounds pairins
-- safely.
create or replace view tournament_info as

  select a.tournament_id,
  (select count(*) from players b where b.tournament_id = a.tournament_id) as player_count,
  (select count(*) from matches c where c.tournament_id = a.tournament_id) as match_count,
  floor(
    log(
      2,
      (select count(*) from players d where d.tournament_id = a.tournament_id)
    )
  ) * ceil(
    (select count(*) from players e where e.tournament_id = a.tournament_id) / 2
  ) > (
    select count(*) from matches f where f.tournament_id = a.tournament_id
  ) as active from tournaments a group by a.tournament_id;
