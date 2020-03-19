# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:09:50 2020

@author: bmart
"""

import sqlite3
from os import listdir
from os.path import isfile, join
import time
import random

class db():
    def __init__(self):
        self.dbName = "palabras.db"
        self.tableName = "palabras"
        self.c = 0
        self.conn = 0
        self.createTable()
        
    def createTable(self):
        self.connectDB()
        sql = '''CREATE TABLE IF NOT EXISTS palabras (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      word TEXT NOT NULL)'''
        self.c.execute(sql)
        self.conn.commit()
        self.closeDB()
    
    def connectDB(self):
        self.conn = sqlite3.connect(self.dbName)
        self.c = self.conn.cursor()
    
    def closeDB(self):
        self.c.close()
        self.conn.close()

    def insertWord(self, word):
        self.connectDB()
        palabra = [word]
        sql = '''INSERT INTO palabras (word) VALUES (?)'''
        self.c.execute(sql, palabra)
        self.conn.commit()
        self.closeDB()
    
    def getWord(self, number):
        self.connectDB()
        sql = "SELECT * FROM palabras WHERE id==?"
        self.c.execute(sql, [str(number)])
        for word in self.c:
            print(word)
        self.conn.commit()
        self.closeDB()
        return word
    
class wordManage():
    def __init__(self):
        self.files = list()
        
    def readAllFiles(self):
        self.files = [f for f in listdir("words") if isfile(join("words", f))]
    
    def getWordsList(self):
        wordsList = list()
        database = db()
        for file in self.files:
            with open("words/"+file, encoding = "utf-8", mode = 'r') as f:
                text = f.readlines()
                wordsList.append(text)
                numberWords = 0
        for wordList in wordsList:
            numberWords += len(wordList)
        print("Número de palabras: ", numberWords)
        
        completed = 0;
        for wordList in wordsList:
            for word in wordList:
                database.insertWord(word.split(',')[0])
                completed+=1
                print(str(completed)+"/"+str(numberWords)+"  --  "+str((completed/numberWords)*100)+"%")

database = db()

#words = wordManage()
#words.readAllFiles()
#a = time.time()
#words.getWordsList()
#b = time.time()
#result = b-a
#print(result)
##########################

######## Sentence generation
def generate(numberWords):
    sentence = str()
    for i in range(numberWords):
        select = random.randint(1, 90939)
        word = database.getWord(select)
        sentence += word[1].split("\n")[0] + " "
    return sentence

sentence = generate(7)
print(sentence)