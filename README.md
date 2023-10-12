# chessanalyser
How to use this abomination!!!

First download something like Mu or Thonny, anything that'll run Python, you click run in the app and the console is in the app as well. A classic IDE. 

Now, open up the chess_analyser.py file in that Python editor. Before running it, there is a little setup. You want to use either Mac, Linux or Windows engine, which are in the same folder as the chessanalyser.py file. Of course, choose the one based on what you are running. Replace the line in the chessanalyser file that says "komodo_path" with the path to your desired engine. As default, it is the path to the Mac engine, and looks like this: Macengine/komodo-14.1-64-bmi2-osx

Next, find a PGN. The PGN needs to be all on one line. An easy way to achieve this is simply to paste the PGN into your search bar, then copy it again. Once you decide whether you want the chessboard to be shown, you enter the PGN and it'll analyse!

Couple more notes: If it is black advantage, the eval will say its positive and vice versa, which is different, but deal with it. If it says Mate in -7, it is Mate in 7 moves for white. You can change how long the engine takes by modifying time on line 112 and 114
