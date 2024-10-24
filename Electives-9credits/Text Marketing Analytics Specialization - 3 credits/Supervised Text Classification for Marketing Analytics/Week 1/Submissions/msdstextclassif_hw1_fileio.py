# -*- coding: utf-8 -*-
"""Copy of MSDSTextClassif_HW1_FileIO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tNI7AtyamWtCOoJx89mH8b7ItSy-Lmje

# MSDS Text Classification. Assignment #1: File I/O

## ⚡️ Make a Copy

Save a copy of this notebook in your Google Drive before continuing. Be sure to edit your own copy, not the original notebook.

## Overview

### 🐍 Python is required for this course

Some programming background, and general familiarity with Python syntax is expected in this course. For a condensed Python review, take a look at the [Python review notebook](https://drive.google.com/file/d/17WGK_Exij4_N3k--CKok3y8ZqE1ZsCqW/view?usp=sharing).

### 🎓 Assessing your current abilities

This assignment and Assignment #2 are designed to quickly assess your preparedness for moving forward in the course. Some students will find these assignments to be easy. **Many of you will find them to be challenging** and should plan your time accordingly. Generally, you should find both Assignment #1 and #2 to be doable, and if not then you should take a step back to review.


> ⚠️  If the work below is difficult for you, then you will want to be absolutely certain to go through the Python review materials before moving forward.

### ☑️ Skill checks

Besides general familiarity with Python syntax, the problems here and in Assignment #2 will assess your following abilities:

 * Write basic Python functions that meet specified requirements
 * Load data from files in your Google Drive account
 * Work with and manipulate Python data structures, particularly lists and dictionaries
 * Use Python control-flow constructs, particularly for-loops and if-statements
 * Manipulate Python strings

### 📝 Completing the assignment

There is a function definition below for you to complete. You will need to write the code to meet the function specifications, and submit the .py version of this notebook to the grader.

> **⚠️  Don't code outside the lines.** Keep your function implementation code inside the function blocks. Be sure not to write any code above the `/autorade` delimiter other than the specified function code. Any experimentation or testing code should go below the `/autograde` indicator, and will be ignored by the grader.

## 📁 Getting the data files

This assignment, and upcoming lab and project work in this course will make use of a [News category dataset](https://www.kaggle.com/rmisra/news-category-dataset) made available through Kaggle.

> **💡  JSON vs JSON-L.** Although Kaggle data file has a ".json" file name, it is actually a JSON-L file, which is of the format of one JSON document per line in the file. This has implications for how you load the data. You will practice loading both file types in this assignment.


**We have made some alternative versions of this file available** in the course assets for use in this assignment and the upcoming labs and project so you can experience working with different data file types.


### Uncompressed copy of just 1 data line

**News_Category_Dataset_v2.1**

What do you get if you take just a single line from a json-L file? You've got just a regular JSON file. This file is here just to give you a chance to work with loading a standard JSON file.


### Uncompressed copy of 100 JSON-L lines

**News_Category_Dataset_v2.100**

This will give you a chance to work with Python's standard file opening, and to see in comparison how nicely the gzip module exposes an API for compressed files that works much like that for regular files.

This file is just 100 lines to make it easier to work with this assignment. You will not be doing any kind of real analysis on this partial dataset.


### Gzipped version of the full data file

**News_Category_Dataset_v2.json.gz**

Here, we have compressed the data file as a .gz file, rather than a .zip file. Gzip files are easier to work with in Python. If you are curious about archive and compression formats, check out [this article from itsfoss](https://itsfoss.com/tar-vs-zip-vs-gz/).


---

Before continuing, you will need to:

 * Download the files from the course assets
 * Upload them to the root of your Google Drive account

> ⤵️ **Before moving forward:** download the data files from the course assets and upload them to the root of your Google Drive.

## Mount Google Drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""## 🔨 Do the work

You should now be ready to go. To complete the assignment:

 1. Complete the implementation of the `read_json` function.

    The function definition line is created for you below. Your job is to complete the function so that it works to specification.

2. Write any exploratory and testing code only below the `/autograde` note.

3. Download the completed notebook as a .py file:

    File > Download > Download .py

    ⚠️ The .ipynb file will not work with the grader. Be sure to download the .py file

4. Submit the file to the Coursera grader for assessment.

### Complete the read_json function

Implement a function called read_json which can read both standard JSON files as well as so-called JSON-L files (i.e. 1 JSON document per line). Files may be uncompressed (plain text) or compressed with gzip (indicated by a .gz file name)

 * .gz files should be opened with the [gzip open function](https://docs.python.org/3/library/gzip.html#gzip.open)
 * otherwise, the file should be opened with the [standard Python open function](https://docs.python.org/3/library/functions.html#open)
 * A standard json file is assumed unless `lines` is set to True, which means the file should be processed as JSON-L
 * The data of a JSON file should be returned as a Python dictionary
 * The data of a JSON-L file should be returned as a list of dictionaries.
"""

import gzip
import json


def read_json(filename, lines=False):
    """A function to load the data from various JSON file types.
    Support should be included for reading both json, and json-L
    formatted files, which may be uncompressed or gzip compressed
    files.

    JSON-L format is indicated by the `lines` parameter being set
    to True.

    Returns a dictionary for a json document, or a list of dictionaries
    for a json-L document.
    """
    pass
    # TODO: open the file, load the data and return it as either
    # a dictionary (for a json file with lines=False), or a list (for a json-l
    # file with lines=True)

    # Be sure to handle both uncompressed and gz-compressed files.

    data = []
    with open(filename, 'r') as file:
        if filename.endswith('.gz'):
            file = gzip.open(filename, 'rt')

        if lines:
            for line in file:
                data.append(json.loads(line))
        else:
            data = json.load(file)

    return data

#~~ /autograde # do not delete this code cell

"""---
### ⚠️  **Caution:** No arbitrary code above this line

The only code written above should be the implementation of your graded function. For experimentation and testing, only add code below.

---

### Load a single data record

The **_v2.1.json** version of the data file has just 1 data entry in it. It is structurally a valid JSON file, as opposed to the JSON-L format of the full data set. This is an uncompressed file.
"""

data1 = read_json("drive/MyDrive/News_Category_Dataset_v2.1.json")
data1

"""### Load a partial record set

The **_v2.100.json** version of the file is a 100-line subset of the data. Because this is multiple records, like the full data set it is a JSON-L file rather than a pure JSON file. This file is uncompressed.
"""

data100 = read_json("drive/MyDrive/News_Category_Dataset_v2.100.json", lines=True)
data100[0:3]

"""### Load the full record set

This is a gzip compressed version of the data file that was originally distributed by Kaggle.
"""

data = read_json("drive/MyDrive/News_Category_Dataset_v2.json.gz", lines=True)
data[0:3]

