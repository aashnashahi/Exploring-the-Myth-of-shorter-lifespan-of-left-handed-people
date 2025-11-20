**📘 Exploring the Myth of Shorter Lifespans for Left-Handed People**
Using Age Distributions, Bayesian Reasoning, and Survival Analysis
This project investigates a long-standing and widely repeated claim:

“Left-handed people die younger than right-handed people.”

A 1991 study once reported a shocking 9-year difference in average age of death between left- and right-handed individuals. This alarming conclusion spread widely in news headlines and popular science.

However, modern analyses suggest the original conclusion was misleading.
This project replicates and expands the core reasoning using:

*📊 Real death distribution data*

*✍️ Historical left-handedness prevalence data*

*🧠 Bayesian probability modeling*

*📈 Survival analysis (Kaplan-Meier & Cox PH)*

*🧪 Synthetic simulations and sensitivity analysis*

The goal is to show how changes in cultural acceptability — not biology — created an illusion that left-handed people die younger.

**📂 Repository Structure**
sql
Copy code
Exploring-the-Myth-of-shorter-lifespan-of-left-handed-people/
│
├── datasets/
│   ├── iris.csv
│   └── requirement.txt
│
├── notebooks/
│   └── main_analysis.ipynb      ← The primary analysis notebook (cleaned & fixed)
│
├── scripts/
│   ├── create_notebook.py
│   └── survival_analysis.py
│
├── outputs/
│   └── .gitkeep                 ← placeholder for generated plots/results
│
├── requirements.txt
├── .gitignore
└── README.md
**📑 Project Summary**
*⭐ Why did early studies think left-handers died younger?*
Because left-handedness was not socially accepted for people born in earlier generations.
Older individuals were more likely to have been forced to write right-handed in school, so very few elderly people reported being left-handed — even if they originally were.

Therefore:

Most young people appear left-handed (accurate)

Most old people appear right-handed (inaccurate — forced switching)

If you look at death records, the “left-handers” skew young

The “right-handers” include almost all elderly people

Result → false appearance that left-handers die earlier

This notebook mathematically reproduces this phenomenon.

**🔬 Methods Used**
**1️⃣ Left-Handedness Rate Reconstruction**
Using digitized data from Gilbert & Wysocki (1992):

Left-handedness as a function of age

Converted to left-handedness as a function of birth year

**2️⃣ Death Distribution Modeling**
Using U.S. CDC mortality data (1999):

Probability of dying at each age → P(A)

**3️⃣ Bayesian Inference**
We compute:

P(LH | A) – probability of being left-handed given age at death

P(LH) – overall probability of left-handedness in the population

P(A | LH) – age-at-death distribution conditioned on being left-handed

P(A | RH) – same for right-handers

This replicates the original paper’s method using clear Bayesian reasoning.

**4️⃣ Survival Analysis (Kaplan-Meier + Cox Regression)**
The survival_analysis.py script demonstrates:

Kaplan-Meier survival curves by group

Log-rank test

Cox proportional hazards model

PH assumption testing

(A synthetic dataset is used but the structure supports real data.)

**🧩 Key Results**
*🎯 Main Finding*
Using real demographic data and accurate Bayesian conditioning:

Left-handers do not die earlier.
The apparent age gap is an artifact caused entirely by changing left-handedness rates over time.

*📉 Reproduced Effect*
The notebook reproduces a 5–6 year artificial “age gap”, similar to the 1991 study’s 9 years — without using any actual lifespan differences.

*📅 Modern Relevance*
Repeating the study in 2018 yields only a 2-year gap, which disappears completely with updated datasets because left-handedness rates are now stable.

**🛠️ Installation & Setup**

*1. Clone the repository:*

git clone https://github.com/aashnashahi/Exploring-the-Myth-of-shorter-lifespan-of-left-handed-people.git

cd Exploring-the-Myth-of-shorter-lifespan-of-left-handed-people

*2. Install dependencies:*

pip install -r requirements.txt

*3. Launch the main notebook:*

jupyter notebook notebooks/main_analysis.ipynb

**🧪 Running Survival Analysis (optional)**

This will generate Kaplan-Meier plots and fit a Cox model (using synthetic data unless replaced with real inputs).

**📈 Outputs**
All generated plots or exported files should be saved into:

outputs/
This directory is tracked with a placeholder (.gitkeep).

**🙋‍♀️ Authors**
Aashna Shahi
Pratiksha Bahuguna




