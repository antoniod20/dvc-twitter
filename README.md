# Reproducible pipeline from Twitter API using DVC

In this project I built a pipeline using DVC from my previously created notebook, called the [Twitter API](https://colab.research.google.com/drive/1zMdbSovvxC8_a50KMAm3EAt9rDiJQZXK?usp=sharing).
Due to the size of my notebook, I only put the most important parts of my work into the pipeline.
This parts are:
 - Creation of dataset (I reduced the size of the dataset due to time reasons)
 - Creation of a NetworkX graph
 - Generation of the image of the graph

The pipeline graph is the following:

      +-------+
      | fetch |
      +-------+
           *
           *
           *
      +-------+
      | graph |
      +-------+
           *
           *
           *
    +------------+
    | egonetwork |
    +------------+

## Setup

### Download

To download the project, proceed with cloning.

```sh
git clone https://github.com/antoniod20/dvc-twitter.git
```

### Configuration
The project was carried out with Python 3.6.9. It is therefore advisable to have a version of Python at least higher than version 3 installed.
To install all the libraries needed to run the project, it is necessary to run this command line:
```sh
pip install -r src/requirements.txt
```

## Run

To launch the pipeline, the following steps must be run:
- First command
```sh
cd .\dvc-twitter\dvc-twitter-api\
```
- Second command
```sh
dvc repro
```

## Resources & Libraries

* [Tweepy](http://docs.tweepy.org/en/latest/) - Twitter API
* [NetworkX](https://networkx.org/documentation/stable/index.html) - Useful to handle the study of graphs and networks
* [Pandas](https://pandas.pydata.org/docs/) - Useful to handle the CSV file
* [Matplotlib](https://matplotlib.org/3.3.3/contents.html) - Provides functions for embedding plots into applications

## Author

* **[Antonio Donvito](https://github.com/antoniod20)** 
