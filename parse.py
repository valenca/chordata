#!/usr/bin/env python2

from pprint import pprint
from urllib import unquote
from random import choice
from sys import argv
import re

beginFile = r"irealb://"
endFile	  = r"Jazz 1300"

songSep	  = r"==0=0==="
firstSep  = r"=="
secondSep = r"="
spaceSep  = r" "

beginSong = r"1r34LbKcu7"
endSong	  = r"  Z"

def beginSectionIndicator(arr):
	arr=arr[-3:]
	if set(arr) & set("ABCDEFGi") != set():
		if set(arr) & set("{[|") != set():
			return True
	arr=arr[-4:]
	if set(arr) & set("ABCDEFGi") != set():
		if set(arr) & set(("N1","N2","2N","1N","3T","4T","5T")) != set():
			return True

	return False


def unscramble(string):
	final = ''

  	while len(string) > 50:
		part = string[:50]
		string = string[50:]
		if len(string) < 2:
			final += part
		else:
	  		final += unobfusc50(part)

  	final += string
	return final

def unobfusc50 (string):
  #the first 5 characters are switched with the last 5
  string=list(string)
  newString=string[::1]

  for i in range(5):
	newString[49 - i] = string[i];
	newString[i] = string[49 - i];
  
  for i in range(10,24):
	newString[49 - i] = string[i];
	newString[i] = string[49 - i];
 
  return "".join(newString)


def parse(string):
	# decode string
	string = unscramble(string)
	# get time signature
	time   = re.findall("T\d\d",string)
	# remove time signature
	string = re.sub("T\d\d","",string)
	# remove ending
	string = re.sub(endSong,"",string)
	# remove comments
	string = re.sub("<[^>]*>","",string)
	# remove alternate chord voicings
	string = re.sub("\([^\)]*\)","",string)
	# remove vertical aligners
	string = re.sub("XyQ","",string)
	# replace LZ separator with a new bar
	string = re.sub("LZ","|",string)
	# remove the section names
	string = re.sub("\*[A-Zi]","",string)
	# remove alternate paths
	string = re.sub("N\d","",string)
	# remove remove brackets and braces and tokenize the chords
	string = re.split("[\/|\{|\}|\[|\]|\|]",string)

	for i in range(len(string)):
		if "Kcl" in string[i]:
			string[i]=[re.sub("Kcl","",string[i])]*2
		if "x" in string[i]:
			string[i]=[re.sub("x","",string[i])]*2

	string = [i for i in string if type(i) != list]
	string = [i for i in string if i != '']

	return string

class Song:
	def __init__(self,info,tech,chords):
		self.title, self.composer = info.split(secondSep)
		self.genre, self.key	  = tech.split(secondSep)

		self.title	= self.title.replace(spaceSep, " ")
		self.genre	= self.genre.replace(spaceSep, " ")
		self.composer = self.composer.replace(spaceSep, " ")

		self.chords   = chords.strip(beginSong)

	def __repr__(self):
		return "\nTitle: %s\nComposer: %s\nGenre: %s\nKey: %s\nChords:\n%s\n" % tuple(map(str,(self.title,self.composer,self.genre,self.key,self.chords)))
		
with open("realbook.dat","r") as raw:
	songs = unquote(raw.readline()).strip(beginFile).strip(endFile).split(songSep)
	
validSongs={}

for i,song in enumerate(songs):
	song = song.split(firstSep)
	if len(song) == 3:
		song = Song(*song)
		validSongs[song.title] = song
		if len(argv)==1:
			print(parse(song.chords))

if len(argv)>1:
	print(validSongs[" ".join(argv[1:])])
	print(parse(validSongs[" ".join(argv[1:])].chords))