import math
import numpy as np
import pandas as pd
from sklearn.manifold import MDS
import statsmodels.api as sm
from itertools import product, combinations
from functools import reduce

def chunker(seq, size):
    """
    [YOU DO NOT NEED TO LEARN THIS]
    Iterates by chunk size rather than 1 at a time
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def get_keywords_combination(brands, brands_synonyms):

    dict_values = []
    pair_used = []
    for brand in brands_synonyms:
        brand_keys = brand.split(",")
        for app in brands_synonyms:
            if not ((brand, app) in pair_used or (app, brand) in pair_used or (brand == app)):
                app_keys = app.split(",")
                dict_values.append(" + ".join([" ".join(item) for item in list(product(brand_keys, app_keys))]))
                pair_used.append((brand, app))
    dict_keys = list(combinations(brands, 2))
    return dict(zip(dict_keys, dict_values))

BRANDS= ['Apple', 'Blackberry', 'HTC', 'Samsung']
BRANDS_SYNONYMS = ['Apple,iPhone', 'Blackberry', 'HTC,Evo', 'Samsung,Galaxy']
TIMEFRAME = "2011-10-27 2012-01-22"

df = pd.read_csv("brand_" + TIMEFRAME + ".csv") # Google Trends Data
dates = df.pop("date")                          # Remove "date" column from df and store it into variable "dates"

start = list(dates).index("2011-11-24")         # Advertising campaign starts on 24/11/2011
end = start + 5 * 7                             # Advertising campaign goes for 5 weeks (35 days)

"""YOU DO NOT NEED TO MODIFY THIS"""

def create_similarity_matrix(df, i):
    """
    Restructures the dataframe into a similarity matrix.
    """
    brands_keywords = get_keywords_combination(
        brands=BRANDS,
        brands_synonyms=BRANDS_SYNONYMS,
    )

    # brands_keywords dictionary with reversed key, values
    brands_keywords_rev = {v: k for k, v in brands_keywords.items()}

    new_df = pd.DataFrame(index=BRANDS, columns=BRANDS)
    for name in df.columns:
        brand_1, brand_2 = brands_keywords_rev[name]
        new_df.loc[brand_1, brand_2] = df.loc[i, name] / 100
        new_df.loc[brand_2, brand_1] = df.loc[i, name] / 100
    return new_df.loc[(new_df!=0).any(axis=1)].fillna(1).astype(np.float64)

def get_x_y(sim_matrix):
    """Converts the similarity matrix into x, y mapped coordinates using Multidimensional Scaling"""
    embedding = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    res = embedding.fit_transform((1 - np.eye(len(BRANDS))) * (1 - sim_matrix))

    return res[:, 0], res[:, 1]

def get_similarity(name_1, name_2, sim_matrix_dict):
    """Get list of similarities between two brands"""
    result = []
    for sim_matrix in sim_matrix_dict.values():
        result.append(sim_matrix.loc[name_1][name_2])
    return result

def main():

    sim_matrix_dict = {}
    for i, date in enumerate(dates):
        sim_matrix_dict[date] = create_similarity_matrix(df=df, i=i)

    app_dist = pd.DataFrame(index=dates)
    for item in BRANDS:
        app_dist[item] = get_similarity("Apple", item,sim_matrix_dict)

    """YOU DO NOT NEED TO MODIFY THIS"""

    after_var = pd.Series()
    for i, item in enumerate(chunker(dates[end+1:], 7)):
        item_copy = item.copy()
        item_copy[:] = "week_" + str(i+1)
        after_var = after_var.append(item_copy)
    after_var.index = dates[end+1:]

    ad_period_df = pd.DataFrame()                    # Initialise Empty Dataframe (Table)

    """For each iteration in this loop, we are defining a new dataframe (brand_df) for each brand. After defining the new dataframe, we append it to the main dataframe (ad_period_df)"""
    for brand in ["Samsung", "HTC", "Blackberry"]:   # Loop through each Brand
        brand_df = pd.DataFrame({
            "similarity": list(app_dist[brand]),           # Distance from brand to Apple stored in column "app_dist"
            "brand_pair": [brand] * len(dates),          # Brand {Samsung, HTC, Blackberry} stored in "brand_pair" 
            "day": dates,                                # All 88 dates stored in "day"
            "during": [0] * len(dates),                  # During defined as 1 ONLY if brand is Samsung and date is during the marketing campaign (0 otherwise)
            "after": [0] * len(dates)                    # After defined as either week_1, week_2, week_3 or week_4 ONLY if brand is Samsung and date is after the marketing campaign (0 otherwise)
        })

        if brand == "Samsung":                         # Conditional Statement to help define the during and after variables
            brand_df.loc[start:end, "during"] = 1
            brand_df.loc[end+1:len(dates), "after"] = list(after_var)
        ad_period_df = pd.concat([ad_period_df, brand_df], axis=0, ignore_index=True)   # Join "brand_df" at the end of "ad_period_df"

    ad_period_dummies_df = pd.get_dummies(ad_period_df, columns=['after', 'brand_pair', 'day'], drop_first=True)
    y = ad_period_dummies_df.pop("similarity")
    X = sm.add_constant(ad_period_dummies_df)
    model = sm.OLS(y, X).fit()
    # print(model.summary())

    """YOU DO NOT NEED TO MODIFY THIS"""

    # Classifying Columns to non-control, control (sort of hard-coded)
    non_control_cols = [column for column in X.columns if column == "during" or "after_week_" in column]
    control_cols = [column for column in X.columns if not(column == "during" or "after_week_" in column)]

    # Coefficients and p-values
    df_coeffs = pd.DataFrame({"coefficients": model.params, "p": model.pvalues})

    # Create two sorted dataframes (1 for non-control; 1 for control)
    df_coeffs_sig = df_coeffs.loc[non_control_cols, :]
    df_coeffs_control = df_coeffs.loc[control_cols, :]
    df_coeffs_sig_sorted = df_coeffs_sig.reindex(df_coeffs_sig["p"].sort_values().index)
    df_coeffs_control_sorted = df_coeffs_control.reindex(df_coeffs_control["p"].sort_values().index)
    df_all = pd.concat([df_coeffs_sig_sorted, df_coeffs_control_sorted], axis=0)
    # print(pd.concat([df_coeffs_sig_sorted, df_coeffs_control_sorted], axis=0))
    # print(df_coeffs_sig_sorted)

    return df_coeffs_sig_sorted.to_dict(orient="index")