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
- static/ - the purpose of this directory is to collect static files (eg. CSS and images)
- styles.css - it contains styles and images
- welcome_image.jpg - it is image used in welcome section

### templates
- templates/ - it is used for rendering web pages
- welcome.html - it is used for rendering of welcome section 
- index.html - it is template of input section
- result.html - it is template of result section

### venv
- venv/ - it is a director due to virtual environment purpose. it contains dependencies and packages from the project. It is recommended to ignore this directory with version control system



