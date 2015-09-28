#!/usr/bin/env groovy

println 'hello'

fp = 'ls -la'.execute()

for (f in fp) { println f }

print fp.text

