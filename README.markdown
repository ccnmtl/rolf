# Rolf is a web based deployment tool

Rolf is aimed at letting you deploy an application to production (or
staging, or wherever) in one step. If your deployment takes more than
one step, you're doing it wrong. 

A typical deployment process will checkout a clean copy of your
application code, tag it (for easy rollbacks later), copy the code to
the production server, update/build any dependencies needed, and
restart or HUP a server process on the production server. 

A deployment in Rolf consists of a collection of settings (eg,
repository URL, production host, target directory) and a list of
stages that will be run in order, halting if any of the stages fail. 

Users can log in to Rolf and hit the big "push" button for a
deployment. The stages each run, logging all the commands executed and
the STDOUT and STDERR returned. If a push ever fails, or broken code
gets pushed to production, it's easy to go back through the Rolf
pushes to select a previous one that was successful and hit a
"rollback" button and Rolf will run a deployment with that version of
code to get your application back to a running state as soon as
possible.  

## Features

* very simple interface, makes it hard to mess up a deployment
* Category/Application/Deployment hierarchy
* Deployment Stages can be written in Bash or Python
* Stages can be shared across applications/deployments and browsed in
  a "cookbook"
* basic permissions model so you can let users push/rollback an
  application without necessarily having the ability to modify the
  deployment steps or settings (handy to let designers push)
* drag and drop reordering of stages
* easy rollback to a known good state
* interactive step by step push mode for debugging your deployment
* easy to "clone" a deployment

## Screenshots

![All Apps Listing](https://github.com/ccnmtl/rolf/raw/master/doc/screenshots/rolf_all_apps.png)

![A Push in Progress](https://github.com/ccnmtl/rolf/raw/master/doc/screenshots/rolf_pushing.png)

![Stages of a Deployment](https://github.com/ccnmtl/rolf/raw/master/doc/screenshots/rolf_stages2.png)

![Cookbook](https://github.com/ccnmtl/rolf/raw/master/doc/screenshots/rolf_cookbook.png)

## Documentation

Please see the [wiki](https://github.com/ccnmtl/rolf/wiki) for
instructions on installing, configuring, and using Rolf. 
