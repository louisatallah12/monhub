# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 23:18:20 2020

@author: pc
"""

import numpy as np
import math
import copy


def Terminal(state):
    if(0 not in state ):
        return True
    elif(Utility(state)!=0):
       return True
    return False


def Utility(state):
    res=0
    for i in range(len(state)):
        if(2 not in state[i,:] and 0 not in state[i,:]):
            res=-1
        if(1 not in state[i,:] and 0 not in state[i,:]):
            res=1
        if(2 not in state[:,i] and 0 not in state[:,i]):
            res=-1
        if(1 not in state[:,i] and 0 not in state[:,i]):
            res=1
    
    if([ state[i][i] for i in range(len(state)) ]==[1,1,1]):
        res= -1 
    elif([ row[-i-1] for i,row in enumerate(state) ]==[1,1,1]):
        res=-1
    elif([ state[i][i] for i in range(len(state)) ]==[2,2,2]):
        res= 1    
    elif([ row[-i-1] for i,row in enumerate(state) ]==[2,2,2]):
        res=1
    return res

def Verdict(valeur):
    if(valeur==-1):
        return "VOUS AVEZ GAGNE !!!!!"
    elif(valeur == 0):
        return "Match null"
    else:
        return "L'IA a gagné 😞"
        
def Action(state):   #renvoie la liste des cases vides
    liste=[]
    for i in range(len(state)):
        for j in range(len(state)):
            if(state[i,j]==" "):
                liste.append([i,j])
    return liste

def Result(state,a):        #a est l'indice de la liste 
    if(len(Action(state))==0):
        return ""
    i,j = Action(state)[a]
    state[i,j]="X"
    return state
    


def Max_Value(copy_state,profondeur):
    v = 0
    for i in range(len(copy_state)):
        for j in range(len(copy_state[i])):
            if copy_state[i][j] == 0:
                new_state = copy.deepcopy(copy_state)
                new_state[i][j]= 2
                max_value = Min_Max_Decision(new_state,profondeur-1,False)*profondeur
                v = max(v,max_value)
    return v

def Min_Value(copy_state,profondeur):
    min_value = 0
    for i in range(len(copy_state)):
        for j in range(len(copy_state[i])):
            if copy_state[i][j] == 0:
                new_state = copy.deepcopy(copy_state)
                new_state[i][j] = 1
                value = Min_Max_Decision(new_state,profondeur-1,True)*profondeur
                min_value = min(min_value,value)
    return min_value



def Min_Max_Decision(copy_state,profondeur,maximiser):
    if profondeur == 0 or Utility(copy_state) != 0:
        return Utility(copy_state)
    if maximiser :
        return Max_Value(copy_state,profondeur)
    else:
        return Min_Value(copy_state,profondeur)


def Joueur_IA(state):
    actions = []
    copy_state = copy.deepcopy(state)       #copie de la matrice actuelle
    for i in range(len(copy_state)):
        for j in range(len(copy_state[i])):     # selectionne les positions libres (équivalent de "Action" dans le pseudo-code)
            if copy_state[i][j] == 0:           
                copy_state[i][j] = 2
                score = Min_Max_Decision(copy_state,5,False)
                actions.append([i,j,score])
                copy_state[i][j] = 0
   
    if  actions :           # vérifie l'optimisation des différents coups tentés (-1,0,1)
        bonne = [x for x in actions if x[2] > 0] 
        neutre = [x for x in actions if x[2] == 0]
        mauvaise = [x for x in actions if x[2] < 0]
        
        if bonne :
            action = max (actions, key = lambda x : x[2])[:2]
        elif neutre :
            action = max(actions,key = lambda x : x[2])[:2]
        elif mauvaise:
            action = max(actions,key = lambda x : x[2])[:2]
            
        state[action[0]][action[1]]= 2      # atrribution de la valeur 2 à la case ij 
        actions = []            # remet la liste vide
         

def Joueur_Humain(state):
    libre = False
    while(libre is False):
        choix = input("A vous de jouer ! Saisissez une position : \n")
        if (choix == "1") :
            i,j=[0,0]
        elif (choix == "2"):
            i,j=[0,1]
        elif (choix == "3"):
            i,j=[0,2]
        elif (choix == "4"):
            i,j=[1,0]
        elif (choix == "5"):
            i,j=[1,1]
        elif (choix == "6"):
            i,j=[1,2]
        elif (choix == "7"):
            i,j=[2,0]
        elif (choix == "8"):
            i,j=[2,1]
        elif (choix == "9"):
            i,j=[2,2]
        if(state[int(i),int(j)]==0):
            state[int(i),int(j)]=1
            libre = True
        else:
            print("case déjà prise")
    return state
    
def Jeu():
    state = np.full((3,3),0) #Initialisation du plateau
    printState(state)
    while (not Terminal(state) ):
        state = Joueur_Humain(state) #Tour du joueur
        printState(state)
        Joueur_IA(state)    #Tour de l'IA
        printState(state) 
    valeur = Utility(state)
    print(Verdict(valeur))
     

def printState(state):
    #Conversion des valeurs de la matrice en charactère
    str_state = np.char.mod('%d', state)
    #Remplacement des valeurs par des signes
    str_state = np.where(str_state=="0", " ", str_state) 
    str_state = np.where(str_state=="1", "O", str_state)
    str_state = np.where(str_state=="2", "X", str_state)
    
    #Affichage
    print(' ╔═══╦═══╦═══╗\n\
 ║ '+str_state[0,0]+' ║ '+str_state[0,1]+' ║ ' +str_state[0,2]+' ║\n\
 ╠═══╬═══╬═══╣\n\
 ║ '+str_state[1,0]+' ║ '+ str_state[1,1]+ ' ║ '+str_state[1,2]+ ' ║\n\
 ╠═══╬═══╬═══╣\n\
 ║ '+ str_state[2,0] +' ║ '+str_state[2,1]+' ║ '+ str_state[2,2]+' ║\n\
 ╚═══╩═══╩═══╝ '.format(*state))
    
Jeu()