#!/bin/bash
apps=$(brew list)

for APP in $apps
do
  brew desc $APP
done
