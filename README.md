Project Setup steps after downloading the repo

Download dependencies located in "requirements.txt"

Create databases defined in the models file. Navigate to your project server folder in terminal and run: 

python 
from flaskcoffee import app, db
app.app_context().push()
db.create_all()

In a terminal run the following to create the server:

cd projects/espresso-project/server/
python run.py

In another terminal run the following to boot up the svelte frontend: 

cd projects/espresso-project
npm run dev -- --open

For testing the recommendation system here are some example values:

Drink: espresso

Brewing Device: Gaggia Classic Pro

Grinder: DF 64

Bean: Red Bird Espresso 

Alternate Bean Option: Life Boost Blonde Roast (useful to alternate when testing)

Combinations of grinders and bean roast types are assigned setting ranges in the seed data csv. 

Generally it is setup to identify the roast level of the bean and then give a recommendation based on that.
