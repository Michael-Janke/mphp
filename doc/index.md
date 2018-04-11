# Short Documentation

1.  [Infrastructure](#infrastructure)
    * [Restart the Server](#server-restart)
    * [Deployment](#deployment)
    * [Local Setup](#local-setup)
2.  [Data](#data)
    * [Parsing](#parsing)
    * [Adding Data](#adding-data)
3.  [App](#app)
    * [Backend](#backend)
    * [Frontend](#frontend)
    * [Analyzing the Data](#analyzing-data)

<a name="infrastructure"/>
## Infrastructure

```diff
- TODO: Short server description, Url & IP
```

<a name="server-restart"/>
### Restart the Server

```diff
- TODO: run hook script
```

<a name="deployment"/>
### Deployment

* Add git remote `git remote add server-deploy deploy@vm-mpws2017hp1.eaalab.hpi.uni-potsdam.de:/var/mp-server-repo`
* Push version to remote `git push server-deploy`

```diff
- TODO: (short) how deployment works
```

<a name="local-setup"/>
### Local Setup

Python version 3 and x64 is required.

```diff
- TODO: Node, npm, pip,...
```

#### Flask Server

To start the Flask server you need to install all requirements by running:

```
pip install -r requirements.txt
```

Then you can start the server by:

```
python app.py
```

The server should restart when file changes are detected. Also it does not die on errors and displays the error message in the browser.

#### Node Server

Go to the client directory and install dependencies:

```
cd client && npm install
```

To only start the Node server, run:

```
npm run start-client
```

To start the Flask and the Node server concurrently, just run:

```
npm start
```

This is also done by the `./start.sh` script in the root directory for lazy developers who don't want to change directories so much.

<a name="data"/>
## Data

The data is not part of this repository. It must be stored inside a manually created data folder.
Each dataset is inside its own folder called `dataset<1|2|3>`.
They can be downloaded and parsed into subsets by running:

```
python scripts/download_data.py
```

Inside each folder is a data and meta data file and a folder for subsets which contain `.npy` files for each cancer type.

<a name="parsing"/>
### Parsing

```diff
- TODO: (short) wo ist das Modul, was macht es grob
```

<a name="adding-data"/>
### Adding Data

```diff
- TODO: kurz halten, wo muss man nachgucken?
```

<a name="app"/>
## App

```diff
- TODO: Architecture Diagram, short intro
```

<a name="backend"/>
### Backend

```diff
- TODO: Shortly describe folder structure, where to find what?; Alles, was aus dem Code nicht direkt hervor geht
```

<a name="frontend"/>
### Frontend

```diff
- TODO: Short intro (Redux); Shortly describe folder structure, where to find what?
```

<a name="analyzing-data"/>
### Analyzing the Data

We decided to use IDE extensions for exploration and visualization.
This comes with the advantage of auto-completion, linting and a better version control in comparison with Jupyter notebooks.

* Atom: Hydrogen
* VS Code: Jupyter, Python
* Sublime: Jupyter

We decided to put files for exploration (dimensionality reduction, feature selection, plotting etc.) in the root folder.
Each script can load specific data with the help of the DataLoader class from the utils folder.

To get the Jupyter feeling inside the exploration files, you need to add breakpoints to the code by adding `#%%`.
This will create cells which can be executed independently after each other. Variables are stored in a session and can be explored and visualized inside the IDE.

### Suggestions and Learnings

* DataLoader should be initialized only once as it reads all the data files into memory

* When modifying modules which are imported in the exploration scripts, you need to restart the kernel before the changes get active. A new import does not help here
