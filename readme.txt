0. Make sure you have python 3.6.4 installed and on a Windows Machine
1. Open up a command line and cd to the root directory of the project (ex: C:\Users\Armand Syahtama\Documents\CSI4107-Search-Engine-Project).
	Path is dependent on where you unzipped this project
2. Install virtualenv by typing 'pip install virtualenv' on the command line
3. Next, install virtualenvwrapper-win by typing 'virtualenvwrapper-win' on the command line
4. Make a virtual environment called search, by typing 'mkvirtualenv search'
5. The virtual environment should be activated, indicated by the '(search)' on the left side of prompt
	- You can deactivate the virtual environment by typing 'deactivate'
	- If you want to go back to the virtual environment type 'workon search'
6. While the virtual environment is activated, type 'pip install -r requirements.txt'
	- The requirements.txt file contains all the packages this project is dependent on (Flask, BeatifulSoup, ect.)
	- The command you typed should install all those packages within the virtual environment, so project should be able to work
	and you don't pollute other python projects with extraneous packages, because everything was installed in a virtual environment
7. Type 'python -m nltk.downloader stopwords' on the command line
	- This installs the stopwords corpus the project uses
8. Type 'set FLASK_APP=run.py' on the command line
	- Needed to run the User Interface designed in flask
9. To run the app, type 'flask run'
	- You should see this on the screen afterwards
	 * Serving Flask app "run.py"
 	* Environment: production
   	WARNING: Do not use the development server in a production environment.
   	Use a production WSGI server instead.
 	* Debug mode: off
 	* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	- Click on the hyperlink, and you should see the search page