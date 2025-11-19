# survival_analysis.py - Kaplan-Meier + Cox PH on Iris dataset (synthetic survival variables)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

# --- 1. Load / prepare your data ---

df = pd.read_csv("iris.csv")

# Create synthetic “handedness-like” binary group using species
df['group'] = (df['species'] == 'virginica').astype(int)

# Create synthetic survival time and event
np.random.seed(42)
df['time'] = np.random.uniform(1, 10, size=len(df))
df['event'] = np.random.binomial(1, 0.7, size=len(df))

# Create synthetic “birth_year-like” covariate
df['birth_year'] = np.random.randint(1950, 2000, size=len(df))

# Create synthetic categorical variable “sex”
df['sex'] = np.random.choice(['M', 'F'], size=len(df))

# Binary variable used in the model
df['group_bin'] = df['group'].astype(int)
df['sex'] = df['sex'].astype('category')


# --- 2. Kaplan-Meier: survival curves by group (virginica vs others) ---

kmf_a = KaplanMeierFitter()
kmf_b = KaplanMeierFitter()

mask_a = df['group'] == 1
mask_b = df['group'] == 0

T_a = df.loc[mask_a, 'time']
E_a = df.loc[mask_a, 'event']

T_b = df.loc[mask_b, 'time']
E_b = df.loc[mask_b, 'event']

plt.figure(figsize=(8,6))
kmf_a.fit(T_a, event_observed=E_a, label='Group 1 (virginica)')
kmf_b.fit(T_b, event_observed=E_b, label='Group 0 (others)')
ax = kmf_a.plot_survival_function()
kmf_b.plot_survival_function(ax=ax)
plt.title("Kaplan-Meier Survival Curves")
plt.xlabel("Time")
plt.ylabel("Survival Probability")
plt.grid(True)
plt.show()


# --- 3. Log-rank test ---

lr = logrank_test(T_a, T_b, event_observed_A=E_a, event_observed_B=E_b)
print("Log-rank p-value:", lr.p_value)


# --- 4. Cox proportional hazards model ---

cph_df = df[['time', 'event', 'group_bin', 'birth_year', 'sex']].copy()

# Normalize birth_year
cph_df['birth_year_c'] = (cph_df['birth_year'] - cph_df['birth_year'].mean()) / cph_df['birth_year'].std()

# One-hot encode sex
cph_df = pd.get_dummies(cph_df, columns=['sex'], drop_first=True)

cph = CoxPHFitter()
cph.fit(cph_df, duration_col='time', event_col='event', formula="group_bin + birth_year_c + sex_M")
cph.print_summary()


# --- 5. PH assumption check (plots) ---
cph.check_assumptions(cph_df, p_value_threshold=0.05, show_plots=True)
