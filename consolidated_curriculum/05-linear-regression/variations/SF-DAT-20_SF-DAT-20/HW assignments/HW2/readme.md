# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) HW #2: Exploratory Analysis
DS | Unit Project 2

### PROMPT

In this project, you will implement the exploratory analysis plan developed in Project 1. This will lay the groundwork for our our first modeling exercise in Project 3.

Before completing an analysis, it is critical to understand your data. You will need to identify all the biases and variables in your model in order to accurately assess the strengths and limitations of your analysis and predictions.

Following these steps will help you better understand your dataset.

**Goal:** An IPython notebook writeup that provides a dataset overview with visualizations and statistical analysis.

---

### DELIVERABLES

#### IPython Notebook Exploratory Analysis

- **Requirements:**
  - Read in your dataset, determine how many samples are present, and ID any missing data
  - Create a table of descriptive statistics for each of the variables (n, mean, median, standard deviation)
  - Describe the distributions of your data
  - Plot box plots for each variable
  - Create a correlation matrix


- **Bonus:**
    - Drop outliers from your dataset
    - Add dummy variables based on GPA.

- **Submission:**
    - This project is due on Feb 17th 2016 at 6:30PM. Please submit it to Michael Twardos via Slack.

---

### TIMELINE

| Deadline | Deliverable| Description |
|:-:|---|---|
| Lesson 6 | HW 2  | Exploratory Data Analysis   |

---

### EVALUATION

Your project will be assessed using the following standards:

Parse the Data



Requirements for these standards will be assessed using the scale below:

    Score | Expectations
    ----- | ------------
    **0** | _Incomplete._
    **1** | _Does not meet expectations._
    **2** | _Meets expectations, good job!_
    **3** | _Exceeds expectations, you wonderful creature, you!_

While your total score is a helpful gauge of whether you've met overall project goals, __specific scores are more important__ since they'll show you where to focus your efforts in the future!

---

### RESOURCES

#### Dataset  
We'll be using the same dataset as UCLA's Logit Regression in R tutorial to explore logistic regression in Python. Our goal will be to identify the various factors that may influence admission into graduate school. It containes four variables- admit, gre, gpa, rank.

- 'admit' is a binary variable. It indicates whether or not a candidate was admitted admit =1) our not (admit= 0)
- 'gre' is GRE score
- 'gpa' stands for Grade Point Average
- 'rank' is the rank of an applicant's undergraduate alma mater, with 1 being the highest and 4 as the lowest


#### Starter code
For this project we will be using an IPython notebook. This notebook will use matplotlib for plotting and visualizing our data. This type of visualization is handy for prototyping and quick data analysis. We will discuss more advanced data visualizations for disseminating your work.


#### Additional Links
- [Pandas Docs](http://pandas.pydata.org/pandas-docs/stable/)
- [Useful Pandas Snippets](https://gist.github.com/bsweger/e5817488d161f37dcbd2)

---

