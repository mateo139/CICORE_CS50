 # STEEL END-PLATE THERMAL SEPARATION LAYER CALCULATOR
    - Video Demo:  <URL HERE>

## What will your software do?
My python program is web application on the base of flask framework. Aim of this application is to support structural engineern in calculation of steel end-plate connections with thermal separation layer made by NBR (which are produced by Calenberg GmbH). Application apply algorithm of Profesor Nasdala from Institute for Structural Analysis in University of Hanover in Germany.
    
## What features will it have?
Basic features:
- calculation of stresses in the structural bearing with check of allowable stresses.
- presentation of stress distribution due to influences like: axial force, prestressing forces, bending moment
- presentation of static schemes of forces acting on the connection

## How will it be executed?
Download code from [GitHub](https://github.com/mateo139/CICORE_CS50)

## Descripton of folders and files

### root directory
- app.py - it is Flask main application file. It contains routes and functions that enable requests and calculations

- requirements.txt - it contains dependencies necessary in project

- readme.md - it is basic documentation of project, containing helpful informations for running and deployng of applicaiton
- .gitignore - this file indicates which files and folders have to be ignored by Git

### __pycache__
- pycache/ - this directory contains bytecode files and it is generated automatically (what is more it should be ignored by Git)

### static
- styles.css
- welcome_image.jpg

### templates
- index.html
- result.html
- welcome.html

### venv
- bin
- include
- lib
- pyvenv.cfg


