# Identifying Cluster Discriminant Features In Cancer Data

Repository for analysing gene expression data.

The goal is to identify genes which are differently expressed in healthy and unhealthy people and
which can be used to cluster cancer types into their categories.

## Getting the data

The data is not part of this repository. It must be stored inside a manually created data folder.
Each dataset is inside its own folder called dataset<1|2|3>.
It can be downloaded and parsed into subsets by running:

```
python scripts/download_data.py
```

Inside each folder is a data and meta data file and a folder for subsets which contains .npy files for each cancer type.

**Later we could move the subsets directly inside the dataset folder and remove the original file to save disk space**

# Setup servers

python version 3 and x64 is required

## Flask server

To start the Flask server you need to install all requirements by running:

```
pip install -r requirements.txt
```

Then you can start the server by:

```
python app.py
```

The server should restart when file changes are detected. Also it does not die on errors and displays the error message in the browser.

## Node server

* Go to the client directory `cd client`
* Install dependencies by running `npm install`
* Start the server using `npm start`, a tab should be opened automatically

# Analyzing the data

We decided to use IDE extensions for exploration and visualization.
This comes with the advantage of auto-completion, linting and a better version control in comparison with Jupyter notebooks.

* Atom: Hydrogen
* VS Code: Jupyter, Python
* Sublime: Jupyter

We decided to put files for exploration (dimensionality reduction, feature selection, plotting etc.) in the root folder.
Each script can load specific data with the help of the DataLoader class from the utils folder.

To get the Jupyter feeling inside the exploration files, you need to add breakpoints to the code by adding **#%%**.
This will create cells which can be executed independently after each other. Variables are stored in a session and can be explored and visualized inside the IDE.

**Suggestions and Learnings:**

* DataLoader should be initialized only once as it reads all the data files into memory

* When modifying modules which are imported in the exploration scripts, you need to restart the kernel before the changes get active. A new import does not help here
