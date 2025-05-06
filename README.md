# electric-billing-system-IT1R1
FINALS PIT IT1R1

Please, if you want to commit some changes, at least use camelCase :)

check out the requirements.txt file for dependencies
just type in: pip install -r requirements.txt
inside the terminal to download the dependencies

make sure though you are using python 3.12, I used 3.12.9 for this

this is just a school project, kwh.py script 
is only for demonstration purposes :)
the kwh.py basically updates the database automatically
everyday as if a user is actually consuming electricity

Do note that you have to be windows for the stuff to work because
when you run the main.py file, the program also executes other scripts
and at the same time turn them into detached processes, which for some
reasons, detached process flag I believe does not exist in 
posix (UNIX-based) operating systems, such as MacOS, Linux-based distributions, etc.

You can probably instead run these scripts (kwh.py, billScript.py) independently using separate terminal
tabs or windows.

I just made it this way because I find it cool to turn these scripts into
detached processes lol

The way I do the simulation is by changing the date and time of my
device and the database automatically makes updates which is kinda
like the highlight of the program.

I tried doing the "changing the date and time" on my Linux Ubuntu and for some reasons it doesn't work

Also, when I'm using my Ubuntu, I get some errors about the PIL module and idk how to fix it
