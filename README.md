# CSI4107-Search-Engine-Project

Search Engine Project for CSI4107

1. Make sure you have python 3.6.4 installed and on a Windows Machine
2. Open up a command line and cd to the root directory of the project (ex: C:\Users\Armand Syahtama\Documents\CSI4107-Search-Engine-Project).
   Path is dependent on where you unzipped this project
3. Install virtualenv by typing 'pip install virtualenv' on the command line
4. Next, install virtualenvwrapper-win by typing 'pip install virtualenvwrapper-win' on the command line
5. Make a virtual environment called search, by typing 'mkvirtualenv search'
6. The virtual environment should be activated, indicated by the '(search)' on the left side of prompt
   - You can deactivate the virtual environment by typing 'deactivate'
   - If you want to go back to the virtual environment type 'workon search'
7. While the virtual environment is activated, type 'pip install -r requirements.txt'
   - The requirements.txt file contains all the packages this project is dependent on (Flask, BeatifulSoup, ect.)
   - The command you typed should install all those packages within the virtual environment, so project should be able to work
     and you don't pollute other python projects with extraneous packages, because everything was installed in a virtual environment
8. Type 'python -m nltk.downloader stopwords' on the command line
   - This installs the stopwords corpus the project uses
9. Type 'set FLASK_APP=run.py' on the command line
   - Needed to run the User Interface designed in flask
10. To run the app, type 'flask run'

- You should see this on the screen afterwards

* Serving Flask app "run.py"
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

- Click on the hyperlink, and you should see the search page

### All the json files required to run the modules for this project have already been set up. However if you want to set up the files yourself, you can do the following

- Make sure your virtual environment is on
  For each file setup, type "python filesetup.py [file_type]"

The valid file_types are as follows:

- corpus: sets up both the UO corpus and the Reuters Corpus
- dict: sets up the dictionary
- index: sets up the inverted index
- list: sets up the list of topics for use in the UI
- bigram: sets up the bigram model
- docterm: sets up the doc-term table to be used for thesaurus set up
- thesaurus: sets up thesaurus
- knn: classifies the topics of unlabeled articles with knn
- nb: classifies the topics of unlabeled articles with nb
