## Deploy to Heroku
 * Go to ```src``` folder
 * Run ```git push heroku master```
 * App can be found at https://type10trainer.herokuapp.com/

## Deploy to Github
 * Go to ```kymmensormijarjestelma``` folder
 * Run ```git push```

## Start app locally
 * Start the database by running the script ```start-pg.sh``` in any folder
 * Enter the virtual environment by running ```source venv/bin/activate``` in the ```kymmensormijärjestelmä``` folder
 * Start the application by runnning ```flask run``` in the ```src``` folder
 * Database can be stopped with the command ```kill $(ps x|grep pgsql/bin/postgres|grep -v grep|awk '{print $1}')```

## Automatic styling
 * run ```black .``` in the src directory

## Next steps
 * Add a link to a page which teaches the principle (where to place the fingers etc..). Or alternatively write a short version of the corresponding content myself.
 * Create several exercises for each level i.e. do the actual content
 
 Read through both the course material and tikape-material. Adjust the code while reading always when spotting something to improve:
 * Optimize the queries. Do all calculations in SQL and minimize of use Python code
 * Comment the code
 
