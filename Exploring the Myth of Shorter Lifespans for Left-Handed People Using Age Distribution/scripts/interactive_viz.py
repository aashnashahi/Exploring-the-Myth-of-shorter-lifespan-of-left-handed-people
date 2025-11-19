
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import interact, IntSlider, Dropdown, fixed, FloatSlider, Checkbox, VBox, HBox, HTML
from IPython.display import display

# Data loaders
LH_URL = ("https://gist.githubusercontent.com/mbonsma/8da0990b71ba9a09f7de395574e54df1/"
          "raw/aec88b30af87fad8d45da7e774223f91dad09e88/lh_data.csv")
DEATH_URL = ("https://gist.githubusercontent.com/mbonsma/2f4076aab6820ca1807f4e29f75f18ec/"
             "raw/62f3ec07514c7e31f5979beeca86f19991540796/cdc_vs00199_table310.tsv")

lh = pd.read_csv(LH_URL)
lh['Birth_year'] = 1986 - lh['Age']
lh['Mean_lh'] = lh[['Female','Male']].mean(axis=1)

deaths = pd.read_csv(DEATH_URL, sep='\\t', skiprows=[1])
deaths = deaths.dropna(subset=['Both Sexes']).reset_index(drop=True)
deaths['Age'] = deaths['Age'].astype(int)

def P_lh_given_A(ages_of_death, lefthanded_data, study_year=1990):
    ages = np.asarray(ages_of_death, dtype=int)
    early_1900s_rate = lefthanded_data['Mean_lh'].iloc[-10:].mean()
    late_1900s_rate = lefthanded_data['Mean_lh'].iloc[:10].mean()
    byears = study_year - ages
    lh_map = lefthanded_data.set_index('Birth_year')['Mean_lh'].to_dict()
    res = np.zeros_like(ages, dtype=float)
    min_by = lefthanded_data['Birth_year'].min()
    max_by = lefthanded_data['Birth_year'].max()
    for i, by in enumerate(byears):
        if by < min_by:
            res[i] = early_1900s_rate / 100.0
        elif by > max_by:
            res[i] = late_1900s_rate / 100.0
        else:
            try:
                res[i] = lh_map[int(by)] / 100.0
            except KeyError:
                nearest = min(lh_map.keys(), key=lambda k: abs(k - by))
                res[i] = lh_map[nearest] / 100.0
    return res

def P_lh(death_distribution, lefthanded_data, study_year=1990):
    ages = death_distribution['Age'].to_numpy(dtype=int)
    p_lh_a = P_lh_given_A(ages, lefthanded_data, study_year)
    weights = death_distribution['Both Sexes'].to_numpy(dtype=float)
    return (weights * p_lh_a).sum() / weights.sum()

def P_A_given_lh(ages, death_distribution, lefthanded_data, study_year=1990):
    ages = np.asarray(ages, dtype=int)
    age_index = death_distribution.set_index('Age')['Both Sexes'].to_dict()
    P_A = np.array([age_index.get(int(a), 0.0) for a in ages], dtype=float)
    if P_A.sum() == 0:
        return np.zeros_like(P_A)
    P_A = P_A / P_A.sum()
    P_left = P_lh(death_distribution, lefthanded_data, study_year)
    P_lh_A = P_lh_given_A(ages, lefthanded_data, study_year)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (P_lh_A * P_A) / P_left
    res = np.nan_to_num(res)
    if res.sum() > 0:
        res = res / res.sum()
    return res

def P_A_given_rh(ages, death_distribution, lefthanded_data, study_year=1990):
    ages = np.asarray(ages, dtype=int)
    age_index = death_distribution.set_index('Age')['Both Sexes'].to_dict()
    P_A = np.array([age_index.get(int(a), 0.0) for a in ages], dtype=float)
    if P_A.sum() == 0:
        return np.zeros_like(P_A)
    P_A = P_A / P_A.sum()
    P_right = 1.0 - P_lh(death_distribution, lefthanded_data, study_year)
    P_rh_A = 1.0 - P_lh_given_A(ages, lefthanded_data, study_year)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (P_rh_A * P_A) / P_right
    res = np.nan_to_num(res)
    if res.sum() > 0:
        res = res / res.sum()
    return res

def plot_lh_rates():
    fig = px.line(lh, x='Birth_year', y='Mean_lh', title='Mean percent left-handed by birth year', markers=True,
                  labels={'Mean_lh': 'Mean % left-handed', 'Birth_year': 'Birth year'})
    fig.update_yaxes(tickformat='%')
    fig.show()

def plot_death_distribution():
    fig = px.line(deaths, x='Age', y='Both Sexes', title='US deaths by age (1999)', markers=True,
                  labels={'Both Sexes': 'Number of deaths'})
    fig.show()

def plot_conditional_distributions(study_year=1990):
    ages = np.arange(6,115,1)
    p_lh = P_A_given_lh(ages, deaths, lh, study_year=study_year)
    p_rh = P_A_given_rh(ages, deaths, lh, study_year=study_year)
    df = pd.DataFrame({'Age': ages, 'P(A|LH)': p_lh, 'P(A|RH)': p_rh})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Age'], y=df['P(A|LH)'], mode='lines', name='P(A|LH)'))
    fig.add_trace(go.Scatter(x=df['Age'], y=df['P(A|RH)'], mode='lines', name='P(A|RH)'))
    fig.update_layout(title=f'Conditional distributions P(A|LH) vs P(A|RH) (study_year={study_year})',
                      xaxis_title='Age at death', yaxis_title='Probability')
    fig.show()

def mc_sample_gaps(death_distribution, lefthanded_data, study_year=1990, sample_size=2000, n_sims=1000, random_seed=123):
    rng = np.random.default_rng(random_seed)
    ages_pop = death_distribution['Age'].to_numpy(dtype=int)
    weights = death_distribution['Both Sexes'].to_numpy(dtype=float)
    probs = weights / weights.sum()
    p_lh_by_age = dict(zip(ages_pop, P_lh_given_A(ages_pop, lefthanded_data, study_year)))
    gaps = np.empty(n_sims, dtype=float)
    for i in range(n_sims):
        sampled_ages = rng.choice(ages_pop, size=sample_size, p=probs)
        is_lh = np.array([rng.random() < p_lh_by_age.get(int(a), 0.0) for a in sampled_ages])
        if is_lh.sum() == 0 or (~is_lh).sum() == 0:
            gaps[i] = np.nan
            continue
        lh_mean = sampled_ages[is_lh].mean()
        rh_mean = sampled_ages[~is_lh].mean()
        gaps[i] = lh_mean - rh_mean
    return gaps

def plot_mc_hist(sample_size=2000, n_sims=1000, study_year=1990):
    gaps = mc_sample_gaps(deaths, lh, study_year=study_year, sample_size=sample_size, n_sims=n_sims)
    gaps = gaps[~np.isnan(gaps)]
    fig = px.histogram(gaps, nbins=50, title=f'MC distribution of LH mean - RH mean (sample_size={sample_size}, n_sims={n_sims})')
    fig.update_layout(xaxis_title='LH mean age - RH mean age (years)', yaxis_title='Count')
    fig.show()

# Combined interactive dashboard
def show_interact():
    display(HTML("<h3>Interactive exploration: left-handedness & age at death</h3>"))
    # controls
    action = Dropdown(options=[('LH rates','lh_rates'), ('Death distribution','deaths'), ('Conditional distributions','conditional'), ('Monte Carlo histogram','mc')],
                      description='Action:')
    study_year = IntSlider(value=1990, min=1950, max=2018, step=1, description='Study year:')
    sample_size = IntSlider(value=2000, min=100, max=5000, step=100, description='Sample size:')
    n_sims = IntSlider(value=1000, min=100, max=5000, step=100, description='MC sims:')
    auto_run = Checkbox(False, description='Auto-run on change', indent=False)

    controls = HBox([action, study_year, sample_size, n_sims, auto_run])
    output_box = VBox()

    def update(*args):
        output_box.children = []
        act = action.value
        sy = study_year.value
        ss = sample_size.value
        ns = n_sims.value
        if act == 'lh_rates':
            plot_lh_rates()
        elif act == 'deaths':
            plot_death_distribution()
        elif act == 'conditional':
            plot_conditional_distributions(study_year=sy)
        elif act == 'mc':
            plot_mc_hist(sample_size=ss, n_sims=ns, study_year=sy)

    action.observe(lambda change: update(), names='value')
    study_year.observe(lambda change: update() if auto_run.value else None, names='value')
    sample_size.observe(lambda change: update() if auto_run.value else None, names='value')
    n_sims.observe(lambda change: update() if auto_run.value else None, names='value')
    auto_run.observe(lambda change: update() if change['new'] else None, names='value')

    display(controls)
    display(output_box)
