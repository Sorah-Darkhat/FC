Imports = True
if Imports:
    try:
        with open("readme.txt","r") as f:
            pass
    except:
        with open("readme.txt","w") as f:
            f.write("This Program Imports:\n\nos\npickle\nsys\nrandom\ntime\npyfiglet\n\nPlease Make Sure To Have All Of The Modules Referenced Above.\n\nHow To Use:\n\nThe Program starts by generating 2 files, readme.txt and the folder 'QTables'\nWithin QTables, the program loads a generated a file containing a list of Positions - Moves - Scores,\nIf said file fails to load, it will generate a new QTable, with blank Scores\nAnd then will ask you to feed it X ammout of games after which you can play against it\nIf the file loads, you will be asked whether you want to keep training it, and/or play it.\nFor this you may answer ( True or 1 ) if you would like to keep training and/or play it, elsewise you should answer ( False or 0 )\n\nIf you agree to play it, you will first be asked what Player you want to be, type 1 if you want to be the first to play or 2 if you want to be the second.\nAfter this you will be asked how many games you would like it to train again,\nThis is because it will train Y ammout of games from the Positions it has previously reached on your match.\n\nTo Play the game, you will be asked to enter a move, this should be a tuple containing the Line followed by the Number of Pieces Taken\n\nExample:\n\n------------------------------------------------------\nPlayer = 1\n\nYou're Player 1\n------------------------------------------------------\nCurrent Board =\n\nLine 1  -  1 : |\nLine 2  -  3 : | | |\nLine 3  -  5 : | | | | |\nLine 4  -  7 : | | | | | | |\nLine 5  -  9 : | | | | | | | | |\nYour Move = (1,1)\nAfter training the SwanAi, it is possible to see there's a patern to the best move, the goal is to create a simetry,\nWhen the simetry is broke, we can always restore it,\nBy doing so we can assure we create the final simetry that happens when all lines have 0 pieces\nThe Simetry we are looking for can be expressed in terms of binaries,\nAnd what we are trying to get is a Nim Sum of zero,\nhttps://en.wikipedia.org/wiki/Nim#Mathematical_theory \n\n\n\nCopyright (C) 2022 João Cartaxo\n\nAll rights reserved.")
            
    
    import os
    import pickle
    import sys
    import random as rd
    import time
    import pyfiglet
    import pyfiglet.fonts

StartIntro = True
if StartIntro:
    Intro = pyfiglet.figlet_format("Nim QTable\nSwan AI")
    print(Intro)
    
    print("\nPlease Read The Generated readme.txt File\n")
    
    cwd = os.getcwd()
    os.makedirs(f'{cwd}/QTables', exist_ok=True)

Defs = True
if Defs:
    class GameState:
        def __init__(self,nline):
            if nline==0:
                raise ValueError
            Lines=[]
            for i in range(nline):
                Lines.append((2*i+1))
            self.Lines=Lines
            self.P1=True
            self.P2=False
            self.Player=(self.P1,self.P2)
            self.Movelog=[]
            self.GameOver=False
            self.CheckMoves()
            self.Who='None'
            
        def CheckMoves(self):
            ValidMoves=[]
            for line in range(len(self.Lines)):
                ValidMoves.append([])
                for i in range(self.Lines[line]):
                    ValidMoves[-1].append((line+1,i+1))
                if ValidMoves[-1]==[]:
                    ValidMoves.pop()
            self.ValidMoves=ValidMoves
            return self.ValidMoves
        
        def ValidList(self):
            self.CheckMoves()
            Vist=[]
            for line in self.ValidMoves:
                for move in line:
                    Vist.append(move)
            return Vist
            
        def CheckResult(self):
            self.GameOver=True
            for Line in self.Lines:
                if Line != 0:
                    self.GameOver = False
            if self.GameOver==True:
                if self.P1:
                    self.Who='Player 1'
                else:
                    self.Who='Player 2'
            else:
                self.Who='The Game is Still being Played'
        def MakeMove(self,Move):
            MoveLine=Move[0]-1
            self.Movelog.append([self.Lines.copy(),Move])
            self.Lines[MoveLine]-=Move[1]
            self.CheckResult()
            self.CheckMoves()
            if self.P1:
                self.P2=True
                self.P1=False
            else:
                self.P1=True
                self.P2=False
                
        def UndoMove(self):
            Move=self.Movelog[-1]
            UndoMove=(Move[0],-Move[1])
            self.MakeMove(UndoMove)
                
        def ChangeLines(self,NewLines):
            self.Lines=NewLines
            self.CheckResult()
            
    def RandomBoard(GameSize):
        Game=GameState(GameSize)
        Game.Lines=[rd.randint(0,i*2+1) for i in range(len(Game.Lines))]
        Game.CheckResult()
        while Game.GameOver:
            Game.Lines=[rd.randint(0,i*2+1) for i in range(len(Game.Lines))]
            Game.CheckResult()
        return Game
    
    def Train(QTable,GameSize,NGames,ExplorationRate,FocusTrain=False,PlayerMatches=[],nobar=False,Analysis=False):
        P1=0
        P2=0
        for Iterator in progressbar(range(NGames),"Training",40,bol=nobar):
            if FocusTrain:
                Game=GameState(GameSize)
                Game.ChangeLines(PlayerMatches[Iterator].copy())
            else:
                RC = rd.random()
                if RC <= ExplorationRate:
                    Game = RandomBoard(GameSize)
                else:
                    Game=GameState(GameSize)
            while not Game.GameOver:
                for Posi in QTable:
                    if Game.Lines == Posi[0]:
                        Position = Posi
                MaxValue = max(Position[1][1])
                move = Position[1][0][Position[1][1].index(MaxValue)]
                Game.MakeMove(move)
                    
            if Game.Who == "Player 1":
                W=1
                if Analysis:
                    P1+=1
            else:
                W=-1
                if Analysis:
                    P2+=1
            
            i=0
            for Pos in Game.Movelog:
                i+=1
                for P in QTable:
                    if Pos[0] == P[0]:
                        Position = P
                
                for ind in range(len(Position[1][0])):
                    Move = Position[1][0][ind]
                    if Move == Pos[1]:
                        Index = ind
                if (i+1) % 2 == 0:
                    Position[1][1][Index]+=W
                else:
                    Position[1][1][Index]-=W
        if not Analysis:
            return QTable.copy()
        else:
            return QTable.copy(), (P1,P2)
        
    def progressbar(it, prefix="", size=60, out=sys.stdout,bol=False): # Python3.3+
        if not bol:
            count = len(it)
            def show(j):
                x = int(size*j/count)
                print(f'{prefix}[{u"#"*x}{"."*(size-x)}] {j}/{count}',end='\r', file=out, flush=True)
            show(0)
            for i, item in enumerate(it):
                yield item
                show(i+1)
        else:
            for i,item in enumerate(it):
                yield item
                
    def DrawGame(Game,GameIntro=False,P2=False):
        if not GameIntro:
            print("Current Board =\n")
            for i in range(len(Game.Lines)):
                print(f"Line{i+1:^3} - {Game.Lines[i]:^3}:","| "*Game.Lines[i])
        else:
            GeneratorText = 'Creating The Match'
            Txt = ''
            for i in GeneratorText:
                Txt+=i
                print(f"{Txt}",end='\r',flush=True)
                time.sleep(0.03)
            for Pair in range(2,6):
                if Pair % 2 == 0:
                    Txt+= ' '
                    Txt+= '.'
                    for j in range(3):
                        print(f"{Txt}",end="\r", flush=True)
                        time.sleep(0.3)
                        Txt+= '.'
                else:
                    Txt = Txt[:-5:]
                    Txt+='     '
                    print(f"{Txt}",end="\r", flush=True)
                    time.sleep(0.5)
                    Txt = Txt[:-5:]
            print("")
            if not P2:
                SwanTxt=' Hello There :)'
            else:
                SwanTxt=" I Have Already Done My Move, Don't Keep Me Waiting... !"
            ST='Swan:'
            for i in SwanTxt:
                ST+=i
                print(f"{ST}",end='\r',flush=True)
                time.sleep(0.05)
            print("\n")
            GeneratorText = 'Generating The Board'
            Txt = ''
            for i in GeneratorText:
                Txt+=i
                print(f"{Txt}",end='\r',flush=True)
                time.sleep(0.03)
            for Pair in range(2,6):
                if Pair % 2 == 0:
                    Txt+= ' '
                    Txt+= '.'
                    for j in range(3):
                        print(f"{Txt}",end="\r", flush=True)
                        time.sleep(0.3)
                        Txt+= '.'
                else:
                    Txt = Txt[:-5:]
                    Txt+='     '
                    print(f"{Txt}",end="\r", flush=True)
                    time.sleep(0.5)
                    Txt = Txt[:-5:]
            print("")
            maxsize=2*max(Game.Lines)
            for i in range(len(Game.Lines)):
                Ltxt=''
                for char in f"Line{i+1:^3} - {Game.Lines[i]:^3}: ":
                    Ltxt+=char
                    print(f"{Ltxt}",end="\r",flush=True)
                    time.sleep(0.015)
                movingline = "| "
                changingline = ' '*maxsize
                NLines=0
                Old=''
                while NLines<Game.Lines[i]:
                    for j in range(maxsize+1):
                        changedline=changingline[0:NLines*2] + changingline[NLines*2:-j:]
                        changedline+=movingline[0:j]
                        if changedline == Old:
                            pass
                        else:
                            print(f"Line{i+1:^3} - {Game.Lines[i]:^3}:",changedline,end='\r',flush=True)
                            time.sleep(0.02)
                        Old=changedline
                    NLines+=1
                    changingline = changedline + " "*(maxsize-NLines*2)
                if Game.Lines[i] == 0:
                    print(f"Line{i+1:^3} - {Game.Lines[i]:^3}:",end="\r",flush=True)
                print("")
                
    def SwanTalks():
        SwanLines=["With every mistake, another oportunity","I don't judge, I only play.","I'm not that evil...","I'm faster than you think :)","Even if you beat me, you won't next time","There's only so many possibilities..."]
        RandomValue = rd.random()
        if RandomValue > 0.7:
            print("")
            SwanTxt=rd.choice(SwanLines)
            ST='Swan:'
            for i in SwanTxt:
                ST+=i
                print(f"{ST}",end='\r',flush=True)
                time.sleep(0.05)
            time.sleep(1)
        print("")

if __name__ == "__main__":
    Running =True
    while Running:
        Core = True
        if Core:
            GameSize=int(input("Game Size = "))      # Number of Lines
            
            try:
                with open(f"QTables\QTable_S={GameSize}", "rb") as f: # Load The QTable
                    QTable = pickle.load(f)
                    Trained = True
            except:
                Game=GameState(GameSize)  # If it fails to load the QTable, Makes a New QTable
                QTable = []
                Position = [0 for i in range(len(Game.Lines))]
                
                line=len(Game.Lines)-1
                pieces=0
                while Position[0] < 2:
                    pieces+=1
                    Position[line] = pieces
                    Game.ChangeLines(Position)
                    QTable.append((Position.copy(),[Game.ValidList(),[0 for _ in range(len(Game.ValidList()))]])) #Creates a copy of the Board State
                    if Position[line] == line*2+1:                                                                 #Adds the Valid Moves and Attributes 0 to each in a second list          
                        while Position[line] == line*2+1:    #While the line has 2(n-1) + 1 elements (The Game's Default), then go to the next line, when out of the loop add 1
                            line-=1
                        if line >= 0:
                            Position[line]+=1
                            while line < len(Game.Lines)-1:
                                line+=1
                                Position[line]=0
                            line=len(Game.Lines)-1
                            pieces=-1
                        else: # If it tries to move to line( -1 ) because line 0 has been filled, then end the whole loop
                            Position[0] = 2 # Break the loop, without appending the new value
                Trained = False
            
            if Trained:
                TrainMore = eval(input("Would You Like To Keep Training ? (True or False) = "))
            else:
                TrainMore=True
            
            if TrainMore:
                NGames=int(input("Number Of Training Games = "))     
                ExplorationRate = float(input("Random Exploration Rate = "))   # Random Starting Boards, it's faster for large boards ( Example 10 Lines, Where bruteforcing every position X ammout of times becomes ridiculous)
                                                                               # This allows the game to enter positions it may overlook when playing itself
                st=time.time()
                
                Train(QTable,GameSize,NGames,ExplorationRate) # Trains the QTable
                
                print(f"\nTime Needed To Train Using {NGames} Games = {time.time()-st:.2f}s")
            
            
            Play=eval(input("\nDo you wanna Play ? (True or False) = "))
            if Play:
                DefaultSpecialTrain=int(input("Number Of Special Training Games = ")) # Number of Games it will play on the Positions Achieved when playing the Player, 
                                                                                      # helps for large boards, where again, some Positions may be overlooked, 
                                                                                      #( starting at random Positions although is much faster, can still be unreliable or take longer than we want )
                print("------------------------------------------------------")
                P = int(input("Player = "))
                if P == 1:
                    print("\nYou will be Player 1")
                    Game=GameState(GameSize)
                    FirstRound = True
                    while not Game.GameOver:
                        print("------------------------------------------------------")  
                        if FirstRound:
                            DrawGame(Game,GameIntro=True) # Makes a fancy animation
                            FirstRound = False
                        else:
                            DrawGame(Game) # Draws the board, without the animation
                        while True:
                            try:
                                move = input("Your Move = ")
                                move = eval(move)
                                if move not in Game.ValidList():
                                    raise ValueError
                            except:
                                print("\nInvalid Move\nTry Again")
                                move = eval(input("Your Move = "))
                            finally:
                                if move in Game.ValidList():
                                    break
                        Game.MakeMove(move)
                        
                        if not Game.GameOver:
                            for Posi in QTable:
                                if Game.Lines == Posi[0]:
                                    Position = Posi
                            MaxValue = max(Position[1][1])
                            move = Position[1][0][Position[1][1].index(MaxValue)]
                            print(f"Computer Move = {move}")
                            SwanTalks()
                            Game.MakeMove(move)
                if P == 2:
                    print("\nYou will be Player 2")
                    Game=GameState(GameSize)
                    FirstRound = True
                    while not Game.GameOver:
                        for Posi in QTable:
                            if Game.Lines == Posi[0]:
                                Position = Posi
                        MaxValue = max(Position[1][1])
                        move = Position[1][0][Position[1][1].index(MaxValue)]
                        print(f"Computer Move = {move}")
                        SwanTalks()
                        Game.MakeMove(move)
                        
                        if not Game.GameOver:
                            print("------------------------------------------------------")  
                            if FirstRound:
                                DrawGame(Game,GameIntro=True,P2=True)
                                FirstRound = False
                            else:
                                DrawGame(Game)
                            while True:
                                try:
                                    move = input("Your Move = ")
                                    move = eval(move)
                                    if move not in Game.ValidList():
                                        raise ValueError
                                except:
                                    print("\nInvalid Move\nTry Again")
                                    move = eval(input("Your Move = "))
                                finally:
                                    if move in Game.ValidList():
                                        break
                            Game.MakeMove(move)
                        
                print("------------------------------------------------------")   
                
                print(f"{Game.Who} won the match")
                Positions = []
                for Log in Game.Movelog:
                    Positions.append(Log[0]) # Gets the Positions It Entered and Trains Them, If the Player Beats the Computer a first time, it shouldn't beat it a second...
                if DefaultSpecialTrain > 0:
                    print(f"\nTraining for {DefaultSpecialTrain} Games In The Positions Found")
                    st=time.time()
                    for _ in progressbar(range(DefaultSpecialTrain),"Special Training",40):
                        Train(QTable,GameSize,NGames=len(Positions),ExplorationRate=0,FocusTrain=True,PlayerMatches=Positions,nobar=True)
                        
                    print(f"\nThe Special Training Took {time.time()-st:.2f}s")
            
            
            RunAnalysis = eval(input("\nDo You Wish To Run An Analysis ? (True or False) = "))
            
            if RunAnalysis:
                QTable,PValues=Train(QTable,GameSize,100,0,Analysis=True)
                P1=PValues[0]
                P2=PValues[1]
                print("")
                print(f"Swan is winning {P1}% of the games as Player 1")
                print(f"Swan is winning {P2}% of the games as Player 2")
                
                if P1==100 or P2==100:
                    if P1 > P2:
                        PV = "Player 1"
                    elif P2 > P1:
                        PV = "Player 2"
                    print(f"The Board Of Size = {GameSize} Is Determined With {PV} As The Winner")
                
            with open(f"QTables\QTable_S={GameSize}", "wb") as f:
                pickle.dump(QTable,f)                
                
            Running = eval(input("\nDo You Wish To Reload The Program ? (True or False) = "))
            print("\n")    
            
            if not Running:
                if Play:
                    Outro = pyfiglet.figlet_format("Thanks For Playing: )")
                else:
                    Outro = pyfiglet.figlet_format("")
                Outro += pyfiglet.figlet_format("Joao Cartaxo\n2020226704\nFCTUC")
                print(Outro)
            
input("")