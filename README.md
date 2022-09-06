# Disney Move Data Analysis with GPT-3


[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

>This demos shows how to use GPT-3 to not only generate strip charts using a given dataset (in this case, the disney-dash-data.csv dataset), but also update it in real time with only natural language queries:.


## Features

- Extracts data from disney-dash-data.csv
- Plotly creates graphs to visualize data
- GPT-3 uses davinci engine to respond in natural language and provide data

![Alt Text](https://media.giphy.com/media/XVlgfsCa4uyGC96OzS/giphy.gif)



## OpenAI GPT-3 API Access
>To receive and API-Key from OpenAI all you need to do is navigate to https://openai.com/api/ and create and account then hover over your profile on the top right of the page and click the view API Keys tab copy your key and past it in your code remember to create a variable and then call upon it otherwise it wont work

## Instructions

To get started, first clone this repo:
```
git clone https://github.com/plotly/dash-sample-apps.git
cd dash-sample-apps/apps/dash-gpt3-bars
```

Create a conda env:
```
conda create -n dash-gpt3-bars python=3.7.6
conda activate dash-gpt3-bars
```

Or a venv (make sure your `python3` is 3.6+):
```
python3 -m venv venv
source venv/bin/activate  # for Windows, use venv\Scripts\activate.bat
```

Install all the requirements:

```
pip install -r requirements.txt
```

You can now run the app:
```
python app.py
```

and visit http://127.0.0.1:8050/.



## License

MIT




