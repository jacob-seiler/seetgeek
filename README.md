# Ticket Website: Seet Geek

## Description

Course project for Software Quality Assurance [CISC 327](http://www2.cs.queensu.ca/undergrad/courses/profile.php?id=CISC-327). Developed ticket buying and selling web application using Flask. Performed white and black box testing using Selenium and PyTest.

## How to Run

First, clone this repo:

```
git clone https://github.com/jacob-seiler/seetgeek
cd seetgeek
```

To run the application (make sure you have a python environment of 3.5+)

```
$ pip install -r requirements.txt
$ python -m qa327
```

Data will be saved to a `db.sqlite` file under your working directory.

To run all the test code:

```
$ pytest
```

You will see your browswer being controlled by the script automatically jumping around to test the website.
