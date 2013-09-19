#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# peg.py
import urllib
import subprocess
import sys
import os
from time import gmtime, strftime
# from argparse import ArguementParser
tickets=list()
tags=dict()

#tag ideas? you can implement your own!
PEG_TAG="[PEG]" # peg post tag, internal use only (tag on ticket updates), users shouldnt see these
TIX_TAG="[TIX]" # tix @ username will generate a ticket assigned to username
INFO_TAG="[INFO]" # just a heads up, default tag
FUCK_TAG="[FUCK]" # something broke! :c
CLEAN_TAG="[CLEAN]" # ripped out stuff, removed comments, etc
TODO_TAG="[TODO]" # didn't finish what i was doing
RES_TAG="[RES]" # the last todo got fixed. if TODOS > RESOLVES, you're not done yet __TODO__ implement reporting on this
WIP_TAG="[WIP]" # end of day commits, half baked ideas, code sketches, nothing noteworthy to mention but still pushing changes, stash in server
BEER_TAG="[BEER]" # genius, beautiful, elegant code that will look like shit in the morning. AKA, review / QA this code
CRIT_TAG="[CRIT]" # mega super important turning point
NOTE_TAG="[NOTE]" # added /edited documentation
OHNO_TAG="[OHNO]" # oh no!
PROB_TAG="[PROB]" # houston, we have a problem
DNT_TAG="[DNT]" # do not touch!

#utter horseshit
BANG_TAG="[!]" #snake, get down!!
UTTER_HORSESHIT_TAG="[UTTER HORSESHIT]"
FAIC_TAG="[ >:( ]" # anger faic!
KAWAII_TAG="[~ugu~]" # uguuuuuuu~~~~
DND_TAG="[DND]" # dungeons n dragons
BRUH_TAG="[BRUH!]" # bruh!

#faces n tables
UGH_TAG=u"[ ಠ_ಠ ]"
TABLEFLIP_TAG=u"[ ╯°□°）╯┻━┻ ]"
TABLEFLIP_SOB_TAG=u"[ (ﾉಥ益ಥ）ﾉ﻿ ┻━┻ ]"
TABLEFIX_TAG=u"[ ┬──┬﻿ ¯\_(ツ) ]"
DOUBLETABLE_TAG=u"[ ┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻ ]"
WHOEVENGIVES_TAG=u"[ ┻━┻ ︵﻿ ¯\(ツ)/¯ ︵ ┻━┻ ]"
FADTABLE_SAD_TAG=u"[ ┬─┬ノ( º _ ºノ) ]"
MEGAFLIP_TAG=u"[ (ノಠ益ಠ)ノ彡┻━┻ ]"

def loadTickets(filters=None): #TODO use regex?? optimise search
    tix_list=list()
    for line in open('.peg/peg_tickets.txt','r'):
        ticket = Ticket(string=line)
        if filters:
            for filterString in filters:
                if filterString in str(ticket):
                    tix_list.append(ticket)
        else:
            tix_list.append(ticket)

def addTicket(ticket): # TODO on ticket add, auto commit only the ticket update and push to notify users
    with open(".peg/peg_tickets.txt","a+") as f:
        f.write(str(ticket)+"\n")
    subprocess.call(["git","commit", "-m", PEG_TAG+getDate(), ".peg/peg_ticekts.txt"])

# def loadTags():
#      with ".git/peg_tags.txt" as tags:
#def getMyTickets():

def getDate(): # formatted so that int comparison will work (x > y == x is more recent than y)
    return strftime("%Y%m%d%H%M%S", gmtime())

def getCommitsByTag(tag):
    ret = list()
    for commit in getPrettyCommitLog():
        if tag in commit:ret.append(commit)
    return ret

def getCommitLog():
    return subprocess.check_output(["git", "log", "--pretty=format:\"%H %an: %s\""]).split("\n") #H = long hash, h = short hash, an = author, s = comment

def getPrettyCommitLog():
    return subprocess.check_output(["git", "log", "--pretty=format:\"%an: %s\""]).split("\n")

def getFuckCommits():
    return getTaggedCommits(FUCK_TAG)

def commitWithTag(msg,tag=INFO_TAG):
    if tag == TIX_TAG:
        print lol
    print subprocess.check_output(["git", "commit", "-am","{} {}".format(tag,msg)])

def run(command,silent=False): #run the tasks
    try:    
        return subprocess.check_output(command.split(" "))
    except subprocess.CalledProcessError as e:
            if silent:
                pass
            else:
                print e

def isGitRepo():
    if os.path.exists(".git"):
        return True
    else:
        return False

def isPegRepo():
    if os.path.exists(".peg"):
        return True
    else:
        return False
def getCurrentDir():
    return run("pwd",silent=True).rstrip()

def pegInit(): #if not git repo, make it so, then make peg repo
    print "PEG INIT"
    if not isGitRepo():
        run("git init")
    if not isPegRepo():
        # init stuff
        print "INITINGGGGG"
        os.makedirs(".peg")
    else:
        print "CAN'T INIT, ONE ALREADY EXISTS"
def getLiveTickets():
        tickets = urllib.urlopen(devcenter_url).read().split('\n')
        print tickets



class Ticket:
    def __init__(self,tid=None,creator=None,date=None,notes=None,priority="TODO",category="Issue",assignee="Anyone", rawstring=None):
        if rawstring:
            #parse string from file input
            ticket_str=string.split(",")

            self._tid=ticket_str[0]
            self._date=ticket_str[1]
            self._creator=ticket_str[2]
            self._assignee=ticket_str[3]
            self._priority=ticket_str[4]
            self._category=ticket_str[5]
            self._notes=ticket_str[6]

        elif (tid and creator and date and notes) != None:
            self._tid=tid
            self._date=date
            self._creator=creator
            self._assignee=assignee
            self._priority=priority
            self._category=category
            self._notes=notes

        else:
            print "WTF ticket is malformed"

    def verboseStr(self): # each ticket split by ;, each item split by ,
        return "TID:"+self._tid+", CDATE:"+self._date+", CREATOR:"+self._creator+", ASSIGNEE:"+self._assignee+", PRIORITY:"+self._priority+", CATEGORY:"+self._category+", NOTES:"+self._notes


    def __str__(self): # each ticket split by ;, each item split by ,
        return self._tid+","+self._date+","+self._creator+","+self._assignee+","+self._priority+","+self._category+","+self._notes

class PegError(Exception):
    def __init__(self, strerr):
        Exception.__init__(self, strerr)


if __name__ == "__main__": # make calling peg.py transparent with calling git

    #stringify args with >>> argstr = " ".join(sys.argv)
    # TODO do i even want this? 
    # parser = ArgumentParser(usage="python easy-modo git. Has tickets, connects to JIRA. good times.")

    arglen=len(sys.argv)
    if arglen < 2: # called with no args
        print "peg: python easy-modo git. Has tickets, connects to JIRA. good times." #TODO JIRA N SHIT YEEEEE
        getLiveTickets();
    else:
        # parse de args~~
        if sys.argv[1] == "init":
            pegInit()
        elif isGitRepo() and isPegRepo():
            #parse args
            print "parsing args~~"
        else:
            print "Not in a peg repo. run 'peg init' to make one. they're cool!"
            sys.exit(0)


