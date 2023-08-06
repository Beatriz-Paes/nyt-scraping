# 🐾 New York times scraping

This is an automation for the NYT news site data extraction process: www.nytimes.com

With this automation it is possible:

- Search by specific term;

- Apply filters such as: section, period in months and type of content;

- Download image of each news, link, among other data;

- Extract the research results, saving in an Excel spreadsheet;


## 🚀 Starting

These instructions will allow you to get a working copy of the project on your local machine for
development and testing.

### 📋 Requirements

Create a virtual environment with the command:

```
python -m venv venv
```

Now, to activate the created venv:

```
source venv/bin/activate
```

### 🔧 Installation

With the virtual environment activated, let's install the dependencies.
To install all of the Python modules and packages listed in requirements.txt file, use:

```
pip install -r requirements.txt
```

To use, need to create a copy of the env.config file and rename it to .env,
defining the variables that will be used in automation:
- SECTIONS - options available:
  - ARTS,BOOKS,BUSINESS,FASHION,HEALTH,MAGAZINE,T_MAGAZINE,MOVIES,NEW_YORK,OPINION,SCIENCE,REAL_ESTATE,SPORTS,STYLE,TRAVEL,U_S,WORLD
- NOTICE_TYPE - options available:
  - ARTICLE,AUDIO,IMAGE_SLIDESHOW,RECIPE,INTERACTIVE_GRAPHICS,VIDEO,WIRECUTTERARTICLE
- MONTH_PERIOD - integer
- PHRASE - term or phrase to search

And finally to run:

```
python tasks.py
```
or
```
python -m robocorp.tasks run tasks.py
```

---
⌨️ by [Beatriz Paes](https://github.com/beatriz-paes) 😊