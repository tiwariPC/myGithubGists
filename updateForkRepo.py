#!/usr/bin/env python
import os,sys,optparse,argparse
#coded by Deepak


usage = "usage: python updateForkRepo.py -N repoName -o addressOfForkedRepo -b branchName  -u addressRepoYouForkedFrom"
'''
EXAMPLE:python updateForkRepo.py -N genproductions -o https://github.com/deepakcern/genproductions.git -b master  -u https://github.com/cms-sw/genproductions.git"
'''
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-b", "--branch",  dest="branch",default="master")
parser.add_argument("-N", "--name",  dest="name",default="ExoPieSlimmer")
parser.add_argument("-o", "--origin",  dest="origin",default="")
parser.add_argument("-u", "--upstream",  dest="upstream",default="")
args = parser.parse_args()

branch = args.branch
repo   = args.name
forkedRepo = args.origin
sourceRepo   = args.upstream

clean = True

os.system('rm -rf tempDir')
os.system('mkdir tempDir')

os.chdir('tempDir')

'''
========================================
clone your fork to your computer
========================================
'''
os.system('git clone -b '+branch +'  '+forkedRepo)



'''
========================================
go to forked repo
========================================
'''
os.chdir(repo)


'''
========================================
Add the "upstream" to your cloned repository ("origin")
========================================
'''
os.system('git remote add upstream  '+sourceRepo)



'''
========================================
#Fetch the commits (and branches) from the "upstream"
========================================
'''
os.system('git fetch upstream')



========================================
'''
Switch to the branch of your fork ("origin")
========================================
'''
os.system('git checkout '+branch)



'''
========================================
Stash the changes of your  branch
========================================
'''
os.system('git stash')



'''
========================================
Merge the changes from the "master" branch of the "upstream" into your  branch of your "origin"
========================================
'''
os.system('git merge upstream/'+branch)



'''
=======================================
Resolve merge conflicts if any and commit your merge
========================================
'''
os.system('git commit -am "Merged from upstream" ')



'''
========================================
Push the changes to your fork
========================================
'''
os.system('git push')
print 'done'

if clean:os.system('rm -rf tempDir')
