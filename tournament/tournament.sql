-- Table definitions for the tournament project.
-- by michael rosata

drop view if exists rankings;

drop table if exists
    players, tournaments, matches;


create table tournaments (
    id serial primary key,
    status varchar(6) default 'open' not null,
    round integer default 1 not null,
    winner varchar(10) null
);

create table players (
    id serial primary key,
    name varchar(30),
    tid int references tournaments (id)
);


create table matches (
    tid integer,
    rid integer,
    loser integer references players (id),
    winner integer references players (id) null,
    primary key (tid, rid, winner)
);
-- pair players with opponent who has won ~ same # of matches

-- a view that lists players in the order of their ranking
-- create or replace view rankings (id, name, ranking) as 
--    select id, name, round(
--        (select count(*) from matches where winner = id) /
--        (select count(*) from matches where winner = id or loser = id)
--    , 2) as ranking
--from players order by ranking desc;

-- a view that lists players in the order of their ranking
create or replace view rankings (id, name, ranking) as 
    select id, name, (
        (select count(*) from matches where winner = players.id))
    as ranking
from players group by players.id order by ranking desc;

-- todo: create trigger rankings_update before insert on matches execute procedure sort_rankings

