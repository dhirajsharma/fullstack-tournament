### Tournament Project

This is the Relational Database Project for the Udacity FullStack Nanodegree. Please note that the test functions inside tournament_test.py have been renamed to satisfy general Python industry best practices that we were instructed to follow in the first course. So if ran against a different copy of tournament_test.py the test file will not run. Follow the instructions below to download and run the tests. Thanks!


Instructions
------
> To setup the project, first clone the repo using `git clone https://github.com/mrosata/fullstack-tournament.git` and then move into the project directory using `cd fullstack-tournament`.
> Next, you will want to setup the vagrant box on your system, to do this simply move into the root project folder `cd fullstack-tournament` and then run the command `vagrant up`. This will take a couple moments to complete setup, once it is done you may connect to the vagrant box from the current folder using the command `vagrant ssh`.
> At this point you are now working from inside the virtual machine. Your command line should begin with the word 'vagrant', if not then the VagrantFile was not able to successfully install. Visit https://atlas.hashicorp.com/boxes/search and search for 'ubuntu/trusty32'. It should be on the first page, you may need to download the box in order to continue. For those of you who see the 'vagrant' prefixed command prompt, change directories into the tournament project `cd /vagrant/tournament`
> Enter psql using command `psql` and then enter `create database tournament;`.
> Now you may exit psql using `\q`
> You should now be back at vagrant command line in directory '/vagrant/tournament'. To setup initial state of the tournament database simply run the command `psql tournament < tournament.sql` which shall build the initial tournament database tables.
> run the test file by `python tournament_test.py`
> 
> All 8 tests should pass.


Michael Rosata 2015.
Udacity Full Stack Nanodegree