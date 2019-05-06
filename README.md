# Titanic_Project

The goal of this project is to use a machine learning model to accurately predict if a person will survive on the Titanic. We used Flask and a SQLAlchemy to query the SQLite databse on the back-end. On the front end we used a Bootstrap template and used Javascript to draw the graphs and make the webpage interactive. The machine learning models were created and tested in Jupyter Notebook then saved to .pkl files so they could be imported into the Flask app.

Once you run the app, click Get Started to go to the form. Enter data into the form to see your chances of living or surviving on the Titanic!

If you wish to look at the data, the metadata is included here for convenience:

Metadata:

Variable Notes pclass: A proxy for socio-economic status (SES) 1st = Upper 2nd = Middle 3rd = Lower

age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

sibsp: The dataset defines family relations in this way... Sibling = brother, sister, stepbrother, stepsister Spouse = husband, wife (mistresses and fiancés were ignored)

parch: The dataset defines family relations in this way... Parent = mother, father Child = daughter, son, stepdaughter, stepson Some children travelled only with a nanny, therefore parch=0 for them.
