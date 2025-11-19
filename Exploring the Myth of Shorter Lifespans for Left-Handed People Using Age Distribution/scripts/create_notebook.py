# create_notebook.py
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

out_path = "notebook5_fixed_v4.ipynb"

nb = new_notebook()
nb.metadata = {
    "kernelspec": {"name": "python3", "display_name": "Python 3"},
    "language_info": {"name": "python"},
}

nb.cells = [

    new_markdown_cell("# Left-handedness age-gap analysis & survival analysis examples\n"
                      "This notebook reproduces the Bayes-rule analysis showing how cohort-dependent "
                      "rates of left-handedness can create an apparent gap in mean age at death, "
                      "and includes a short survival-analysis example."),

    new_markdown_cell("## Part A — Bayes-rule reproduction of the left-handed age-gap"),

    new_code_cell("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt"),

    new_code_cell(
        "LH_URL = (\"https://gist.githubusercontent.com/mbonsma/8da0990b71ba9a09f7de395574e54df1/\"\n"
        "          \"raw/aec88b30af87fad8d45da7e774223f91dad09e88/lh_data.csv\")\n"
        "DEATH_URL = (\"https://gist.githubusercontent.com/mbonsma/2f4076aab6820ca1807f4e29f75f18ec/\"\n"
        "             \"raw/62f3ec07514c7e31f5979beeca86f19991540796/cdc_vs00199_table310.tsv\")\n\n"
        "lh = pd.read_csv(LH_URL)\n"
        "lh['Birth_year'] = 1986 - lh['Age']\n"
        "lh['Mean_lh'] = lh[['Female','Male']].mean(axis=1)\n\n"
        "deaths = pd.read_csv(DEATH_URL, sep='\\t', skiprows=[1])\n"
        "deaths = deaths.dropna(subset=['Both Sexes']).reset_index(drop=True)\n"
        "deaths['Age'] = deaths['Age'].astype(int)\n\n"
        "lh.head(), deaths.head()"
    ),

    new_markdown_cell("### Plot left-handed rates by birth year"),

    new_code_cell(
        "plt.figure(figsize=(8,4))\n"
        "plt.plot(lh['Birth_year'], lh['Mean_lh'], marker='o')\n"
        "plt.xlabel('Birth year')\n"
        "plt.ylabel('Mean % left-handed')\n"
        "plt.title('Digitized left-handedness rates (Gilbert & Wysocki, 1986 data)')\n"
        "plt.grid()\n"
        "plt.show()"
    ),

    new_markdown_cell("### Plot death distribution (1999)"),

    new_code_cell(
        "plt.figure(figsize=(8,4))\n"
        "plt.plot(deaths['Age'], deaths['Both Sexes'], marker='o')\n"
        "plt.xlabel('Age')\n"
        "plt.ylabel('Number of deaths (Both Sexes)')\n"
        "plt.title('US deaths by age (1999)')\n"
        "plt.grid()\n"
        "plt.show()"
    ),

    new_markdown_cell("### Functions for Bayes-rule model"),

    new_code_cell(
        "def P_lh_given_A(ages_of_death, lefthanded_data, study_year=1990):\n"
        "    ages = np.asarray(ages_of_death, dtype=int)\n"
        "    early = lefthanded_data['Mean_lh'].iloc[-10:].mean()\n"
        "    late = lefthanded_data['Mean_lh'].iloc[:10].mean()\n"
        "    byears = study_year - ages\n"
        "    d = lefthanded_data.set_index('Birth_year')['Mean_lh'].to_dict()\n"
        "    res = []\n"
        "    for by in byears:\n"
        "        if by in d: res.append(d[by]/100)\n"
        "        elif by < min(d): res.append(early/100)\n"
        "        else: res.append(late/100)\n"
        "    return np.array(res)\n\n"
        "def P_lh(deaths, lh, study_year=1990):\n"
        "    p = P_lh_given_A(deaths['Age'], lh, study_year)\n"
        "    w = deaths['Both Sexes'] / deaths['Both Sexes'].sum()\n"
        "    return np.sum(p*w)\n\n"
        "def P_A_given_lh(ages, deaths, lh, study_year=1990):\n"
        "    ages = np.asarray(ages)\n"
        "    pop = deaths.set_index('Age')['Both Sexes']\n"
        "    P_A = np.array([pop.get(a,0) for a in ages], float)\n"
        "    P_A /= P_A.sum()\n"
        "    P_L = P_lh(deaths, lh, study_year)\n"
        "    P_LA = P_lh_given_A(ages, lh, study_year)\n"
        "    out = (P_LA * P_A) / P_L\n"
        "    out /= out.sum()\n"
        "    return out\n\n"
        "def P_A_given_rh(ages, deaths, lh, study_year=1990):\n"
        "    ages = np.asarray(ages)\n"
        "    pop = deaths.set_index('Age')['Both Sexes']\n"
        "    P_A = np.array([pop.get(a,0) for a in ages], float)\n"
        "    P_A /= P_A.sum()\n"
        "    P_R = 1 - P_lh(deaths, lh, study_year)\n"
        "    P_RA = 1 - P_lh_given_A(ages, lh, study_year)\n"
        "    out = (P_RA * P_A) / P_R\n"
        "    out /= out.sum()\n"
        "    return out"
    ),

    new_code_cell(
        "ages = np.arange(6,115)\n"
        "p_lh = P_A_given_lh(ages, deaths, lh)\n"
        "p_rh = P_A_given_rh(ages, deaths, lh)\n"
        "mean_lh = np.sum(ages * p_lh)\n"
        "mean_rh = np.sum(ages * p_rh)\n"
        "print('Mean age LH:', mean_lh)\n"
        "print('Mean age RH:', mean_rh)\n"
        "plt.plot(ages, p_lh, label='P(A|LH)')\n"
        "plt.plot(ages, p_rh, label='P(A|RH)')\n"
        "plt.legend()\nplt.show()"
    ),
]

with open(out_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Notebook written:", out_path)
