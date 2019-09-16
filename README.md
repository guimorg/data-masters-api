# Machine Learning - API Online Serving

## Introduction

This is an API Web Application for personal use. It was developed for Santander's Data Masters - Machine Learning Engineering Case and its purpose is to reflect how one could serve a Machine Learning model using an API.

Thinking about which type of model should be used I chose a Sentiment Analysis model from [Kaggle](https://www.kaggle.com/paoloripamonti/twitter-sentiment-analysis/notebook) (amazing job done by Paolo Ripamonti, you should check his [profile](https://www.kaggle.com/paoloripamonti)). This model was designed to be trained and used with Twitter data (1.6 million tweets) so it makes perfect sense as a Web Service listening to requests to classify and score tweets.

Sentiment Analysis is done by data scientists to identify and extract subjective information from source material, helping business understand various aspects: social sentiment of the brand, monitoring online conversations about a product or a service...

There are other tools being used in Text Classifiaction today, not only Sentiment Analysis, the most basic one, but also Intent Analysis - analyzing the user's intention behind a message -, Contextual Semantic Search - filtering messages that closely match with a given concept -, etc.

## Model Metadata

Accuracy 79%
Classification Report:

                precision   recall   f1-score  support

    NEGATIVE       0.79      0.79      0.79    159494
    POSITIVE       0.79      0.80      0.79    160506

## Architecture

### Framework

For this API I chose using **aiohttp**, an asynchronous HTTP client/server for asyncio and Python. One of its advantages is that usually scoring functions for Machine Learning models are blocking; that means that the web application should be able to deal with blocking I/O or computing functions otherwise the application will become unreachable while it waits for receiven a result from the model. For aiohttp that is easy because everything obeys the ```async``` programming in Python.

### Design Choices

To deploy this application I chose a Docker container to encapsulate the whole application:

1. Deploying applications using containers is an intelligent choice, especially for web services. You can get away with depedency nightmares, because everything inside the container is protected in its own environment.

2. It is easier to migrate to a Kubernetes environment. If an application will be gettin spikes in traffic or in workload you will probably have difficulties scaling the system. Chances are you will choose to scale up. Kubernetes helps you implement horizontal scaling for your services providing container orchestration.

There is also a smart trick to asynchronize synchronous functions using ProcessPoolExecutors with 1 worker, basically we can give synchronous functions to executors and ```await``` for them to finish processing while dealing with other requests.

### Creating new endpoints or adding new methods for requests

Following the **template** design pattern I've created a class for an endpoint that serves as BaseClass for all endpoint implementations. To add new methods just create a new function inside an endpoint class with the name of the method (get, post, delete, ...). To create a new endpoint you'll just need to create a new class that extends the Endpoint BaseClass and implement your methods.

If you need to receive arguments within the request, just add the keyword arguments for your function.

### How to Deploy a new Version

The implementation of this API is done in such a way that models.py is like a separate model from the application. This means that if you need to change preprocess or socring models you just need to change this file. If you need to deploy a new version of the model served by this API you just need to provide the name of the new pickle inside the api.conf configuration file.

Because of this the API is almost agnostic to new version of models because the model versioning can be done outside the application.

## How to use

### Cloning the repository

You can clone this repo just by executing ```git clone https://github.com/guimorg/machine-learning-api```.

### Models

Because model files are too heavy for Git you will have to download them directly from Kaggle :(. For local development using Docker or not you will have to create a directory called ```models/``` and put both files inside them. Model names in Kaggle are **tokenize.pkl** and **model.h5** and you can find them in the output portion of the [notebook](https://www.kaggle.com/paoloripamonti/twitter-sentiment-analysis/notebook).

### Python Version

You **must** have Python >3.3 to run this locally, you always can choose to build the Dockerfile and execute inside a container (RECOMMENDED).

### Configuration File

For executing locally you will have to change paths inside ```config/api.conf``` file. If you choose to do that, after setting all configurations please run: ```cp config/api.conf ~/.config/api.conf``` to set the location of the configuration file to its appropriate place.

### Using ```make```

There is a Makefile in the repo that can help you set you environment. You can execute ```make help``` to see all commands.

## Future Work

### Improving Deploy of Application

When using aiohttp in a production environment you may not be able to have optimal perfomance. That happens because, [according to documentation](https://docs.aiohttp.org/en/stable/deployment.html#standalone) the server **will not utilize all CPU cores**. For a Machine Learning application, such as this API, that is not the best solution, specially for handling multiple requests.

To improve that we can use reverse proxies and we have two approaches:

1. Using supervisord and NGINX: we can use supervisord to start out aiohttp backend, that will also help us to automatic restart after system reboot or backend crash; NGINX will be our reverse proxy to prevent attacks and to run several aiohttp instances (allowing us to use all CPU cores).

2. Using gunicorn and NGINX: we can also use Gunicorn (pre-fork worker model) to launch the application as worker process to handle incoming requests.

### Security

When dealing with APIs in the outside world (specially for System-to-Sytem communication) you have various options, each one providing advantages and disadvantages:

#### Authorization 

##### Service-to_Service Authentication

[Atlassian](https://s2sauth.bitbucket.io/spec/) created ASAP (Atlassian S2S Authentication Protocol) a mechanism used by a resource server to authenticate requests from the client in a client-server communication scenario between software services. This type of **solution** uses a protocol that enables the resource server to decide the authenticity of an incoming request based on the information contained in an access token that is include with the request. 

This soluton tries to minimize the overhead introduced by the protocol (number of requests) and avoid secret distribution. Basically, the client self-issues a token that is then sent with the request to the resource server. The resource server then, having already the public key, or discovering it, verifies the claim and signature and, if both of them are valid, return the resource.

One disadvantage of this solution is that when an access token is leaked, another server may try to use it to request a specific resource. The protocol tries to balance that with the properties of a signed JWT, that is short-lived. Also, because access tokens are very specific they cannot be used in a different context.

A big advantage of this solution is that there is no overhead of asking the autenticity of a request to a third-party server, everything happens in the client or in the resource server.

##### Isolating Network

A very common approach when dealing with security for System-to-System communication is isolating the network from the outside world protecting it from malicious requests. That way systems can talk to each other using HTTP/HTTPS without having to worry too much with security, because it is protected from other servers. 

This has an advantage of providing a safe environment for applications and/or systems to talk to each other not having to worry too much about security issues, that way developers and software engineers can spend more time thinking about new features for their applications.

A big disadvantage is that if a malicious server manages to get access inside the protected network it can then exploit any points of failure inside the network. For example, the communication if the communication inside the network is all done using HTTP requests it can perform a spoof attack. 

#### Communication

#### Using SSL

The most common and recommend way of protecting the communication is using SSL to protect the request. That way both ends can communicate without having to worry with someone spoofing the communication (opening packages and reading request contents).

### Data Persistance

An important aspect when developing a new application is keeping in track all metrics available to the application; when dealing with a Machine Learning model the concern is the same to keep track of predictions and incoming data to later assess them (retraining the model or training a new model).

1. We can keep this kind of metrics persisted in a database. The suggestion here would be using a relational database for keeping incoming data and predictions. We can also keep metrics of the requests (referer, host, time taken to process request, etc.)

2. We could also use a tool for logging each request like Kafka+Kibana to receive alerts in backend crashes, problem with requests, etc.

## Author

Guilherme de Amorim Avilla Gimenez Junior
