# VietstocksDB

## Introduction

This project aims to gather financial data of Vietnamese stocks from 24hmoney.vn and store them in a MongoDB database.
The data is then used to rank the top 50 stocks based on Earnings Yield and Return on equity. The ranking method is
based on the book "The Little Book That Still Beats the Market" by Joel Greenblatt.

# Installation

- You have two options: Pipenv or Anaconda

## Install dependencies with Pipenv

```pipenv install```

## Install dependencies with Anaconda

- Create a new environment

  ```conda create --name <env> --file requirements.txt```
- Activate the environment

  ```conda activate <env>```

## Environment variables explanation

- API_URL: 24hmoney API url. At the time of this writing. It is https://api-finance-v2.24hmoney.vn
- MONGODB_URL: Mongodb connection string. Remember to create your own replica set and
  add `&replicaSet=<your replica set name>` to the end of the connection string

## Usage

- Run the script

  ```python main.py```
- You can also check out the notebook to see my implementation of ranking the top 50 stocks based on Earnings Yield and
  Return on equity. Remember to put the vietStocks.json file in ```data``` folder which has the data of ```vietStocks```
  database collection from MongoDB that you get after running ```main.py```