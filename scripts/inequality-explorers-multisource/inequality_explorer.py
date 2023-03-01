# %% [markdown]
# # Source-switching Inequality Data Explorer
# This code creates the tsv file for the main inequality explorer in the inequality topic page, available [here](https://owid.cloud/admin/explorers/preview/inequality)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "inequality.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each type of welfare measure or tables considered.

# %%
# LUXEMBOURG INCOME STUDY
# Read Google sheets
sheet_id = "1UFdwB1iBpP2tEP6GtxCHvW1GGhjsFflh42FWR80rYIg"

# All the tables sheet (this contains PIP, WID and LIS dataset information, it is located in the LIS spreadsheet because there is no unified sheet for this)
sheet_name = "all_the_tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
all_the_tables = pd.read_csv(url, keep_default_na=False)

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_welfare = pd.read_csv(url, keep_default_na=False)

# Equivalence scales
sheet_name = "equivalence_scales"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_equivalence_scales = pd.read_csv(url, keep_default_na=False)

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_povlines_rel = pd.read_csv(url)

# Tables sheet
sheet_name = "tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_tables = pd.read_csv(url, keep_default_na=False)

# WORLD INEQUALITY DATABASE
# Read Google sheets
sheet_id = "18T5IGnpyJwb8KL9USYvME6IaLEcYIo26ioHCpkDnwRQ"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_welfare = pd.read_csv(url, keep_default_na=False)

# Tables sheet
sheet_name = "tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_tables = pd.read_csv(url, keep_default_na=False)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Inequality Data Explorer",
    "selection": [
        "Chile",
        "Brazil",
        "South Africa",
        "United States",
        "France",
        "China",
    ],
    "explorerSubtitle": "",
    "isPublished": "false",
    "googleSheet": "",
    "wpBlockId": "",
    "entityType": "country or region",
}

# Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient="index", columns=None)
# Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type of welfare to iterate by different survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%
# Table generation
###########################################################################################
# LUXEMBOURG INCOME STUDY (LIS)
###########################################################################################
sourceName = "Luxembourg Income Study (LIS) (2022)"
dataPublishedBy = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2021). Luxembourg, LIS."
sourceLink = "https://www.lisdatacenter.org/our-data/lis-database/"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

df_tables_lis = pd.DataFrame()
j = 0

for tab in range(len(lis_tables)):
    # Define country as entityName
    df_tables_lis.loc[j, "name"] = "Country"
    df_tables_lis.loc[j, "slug"] = "country"
    df_tables_lis.loc[j, "type"] = "EntityName"
    j += 1

    # Define year as Year
    df_tables_lis.loc[j, "name"] = "Year"
    df_tables_lis.loc[j, "slug"] = "year"
    df_tables_lis.loc[j, "type"] = "Year"
    j += 1

    for wel in range(len(lis_welfare)):
        for eq in range(len(lis_equivalence_scales)):
            # Gini coefficient
            df_tables_lis.loc[
                j, "name"
            ] = f"Gini coefficient ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"gini_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"The Gini coefficient is a measure of the inequality of the {lis_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare["scale_gini"][
                wel
            ]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Reds"
            j += 1

            # Share of the top 10%
            df_tables_lis.loc[
                j, "name"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"share_p90_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the richest 10% as a share of total {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare["scale_top10"][
                wel
            ]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Greens"
            j += 1

            # Share of the bottom 50%
            df_tables_lis.loc[
                j, "name"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the bottom 50% ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"share_bottom50_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the poorest 50% as a share of total {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_bottom50"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Blues"
            j += 1

            # P90/P10
            df_tables_lis.loc[
                j, "name"
            ] = f"P90/P10 ratio ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"p90_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"P90 is the the level of {lis_welfare['welfare_type'][wel]} below which 90% of the population lives. P10 is the level of {lis_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_p90_p10_ratio"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "OrRd"
            j += 1

            # P90/P50
            df_tables_lis.loc[
                j, "name"
            ] = f"P90/P50 ratio ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"p90_p50_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"P90 is the the level of {lis_welfare['welfare_type'][wel]} above which 10% of the population lives. P50 is the median – the level of {lis_welfare['welfare_type'][wel]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_p90_p50_ratio"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Purples"
            j += 1

            # P50/P10
            df_tables_lis.loc[
                j, "name"
            ] = f"P50/P10 ratio ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"p50_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"P50 is the median – the level of {lis_welfare['welfare_type'][wel]} below which 50% of the population lives. P10 is the the level of {lis_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_p50_p10_ratio"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrRd"
            j += 1

            # Palma ratio
            df_tables_lis.loc[
                j, "name"
            ] = f"Palma ratio ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"palma_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"The Palma ratio is a measure of inequality: it is the share of total {lis_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_palma_ratio"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Oranges"
            j += 1

            # Headcount ratio (rel)
            df_tables_lis.loc[
                j, "name"
            ] = f"50% of median {lis_welfare['welfare_type'][wel]} - share of population below poverty line ({lis_welfare['technical_text'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_tables_lis.loc[
                j, "slug"
            ] = f"headcount_ratio_50_median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"% of population living in households with {lis_welfare['welfare_type'][wel]} below 50% of the median {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30"
            df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
            j += 1

    df_tables_lis["tableSlug"] = lis_tables["name"][tab]

df_tables_lis["sourceName"] = sourceName
df_tables_lis["dataPublishedBy"] = dataPublishedBy
df_tables_lis["sourceLink"] = sourceLink
df_tables_lis["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_lis["tolerance"] = tolerance
df_tables_lis["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

###########################################################################################
# WORLD INEQUALITY DATABASE (WID)
###########################################################################################

# Table generation

sourceName = "World Inequality Database (WID.world) (2022)"
dataPublishedBy = "World Inequality Database (WID), https://wid.world"
sourceLink = "https://wid.world"
colorScaleNumericMinValue = 0
tolerance = 5
new_line = "<br><br>"

df_tables_wid = pd.DataFrame()
j = 0

for tab in range(len(wid_tables)):
    # Define country as entityName
    df_tables_wid.loc[j, "name"] = "Country"
    df_tables_wid.loc[j, "slug"] = "country"
    df_tables_wid.loc[j, "type"] = "EntityName"
    j += 1

    # Define year as Year
    df_tables_wid.loc[j, "name"] = "Year"
    df_tables_wid.loc[j, "slug"] = "year"
    df_tables_wid.loc[j, "type"] = "Year"
    j += 1

    for wel in range(len(wid_welfare)):
        # Gini coefficient
        df_tables_wid.loc[
            j, "name"
        ] = f"Gini coefficient ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p0p100_gini_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"The Gini coefficient is a measure of the inequality of the {wid_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_gini"][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Reds"
        j += 1

        # Share of the top 10%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p90p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 10% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top10"][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 1%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 1% ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p99p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 1% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top1"][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 0.1%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 0.1% ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p99_9p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.1% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top01"][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 0.01%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 0.01% ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p99_99p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.01% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top001"][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 0.001%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 0.001% ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p99_999p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.001% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top0001"][
            wel
        ]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # P90/P10
        df_tables_wid.loc[
            j, "name"
        ] = f"P90/P10 ratio ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p90_p10_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"P90 is the the level of {wid_welfare['welfare_type'][wel]} below which 90% of the population lives. P10 is the level of {wid_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_p90_p10_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
        j += 1

        # P90/P50
        df_tables_wid.loc[
            j, "name"
        ] = f"P90/P50 ratio ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p90_p50_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"P90 is the the level of {wid_welfare['welfare_type'][wel]} above which 10% of the population lives. P50 is the median – the level of {wid_welfare['welfare_type'][wel]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_p90_p50_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Purples"
        j += 1

        # P50/P10
        df_tables_wid.loc[
            j, "name"
        ] = f"P50/P10 ratio ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"p50_p10_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"P50 is the median – the level of {wid_welfare['welfare_type'][wel]} below which 50% of the population lives. P10 is the the level of {wid_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_p50_p10_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "YlOrRd"
        j += 1

        # Palma ratio
        df_tables_wid.loc[
            j, "name"
        ] = f"Palma ratio ({wid_welfare['technical_text'][wel].capitalize()})"
        df_tables_wid.loc[j, "slug"] = f"palma_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"The Palma ratio is a measure of inequality: it is the share of total {wid_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_palma_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Oranges"
        j += 1

    df_tables_wid["tableSlug"] = wid_tables["name"][tab]

df_tables_wid["sourceName"] = sourceName
df_tables_wid["dataPublishedBy"] = dataPublishedBy
df_tables_wid["sourceLink"] = sourceLink
df_tables_wid["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_wid["tolerance"] = tolerance

###########################################################################################
# WORLD BANK POVERTY AND INEQUALITY PLATFORM
###########################################################################################

# Concatenate all the tables into one
df_tables = pd.concat([df_tables_lis, df_tables_wid], ignore_index=True)
# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by welfare type.

# %%
# Grapher table generation

###########################################################################################
# LUXEMBOURG INCOME STUDY (LIS)
###########################################################################################

yAxisMin = 0
mapTargetTime = 2019

df_graphers_lis = pd.DataFrame()

j = 0

for tab in range(len(lis_tables)):
    for wel in range(len(lis_welfare)):
        for eq in range(len(lis_equivalence_scales)):
            # Gini coefficient
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} inequality: Gini coefficient ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"gini_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "Gini coefficient"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"The Gini coefficient is a measure of the inequality of the {lis_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # Share of the top 10%
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the top 10% ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"share_p90_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "Top 10% share"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the richest 10% as a share of total {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # Share of the bottom 50%
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the bottom 50% ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"share_bottom50_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "Bottom 50% share"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the poorest 50% as a share of total {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # P90/P10
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} inequality: P90/P10 ratio ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"p90_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "P90/P10"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"P90 and P10 are the levels of {lis_welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "type"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # P90/P50
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} inequality: P90/P50 ratio ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"p90_p50_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "P90/P50"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "type"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # P50/P10
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} inequality: P50/P10 ratio ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"p50_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "P50/P10"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {lis_welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "type"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # # Palma ratio
            df_graphers_lis.loc[
                j, "title"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} inequality: Palma ratio ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"palma_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[j, "Metric Dropdown"] = "Palma ratio"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"The Palma ratio is the share of total {lis_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

            # Headcount ratio (rel)
            df_graphers_lis.loc[
                j, "title"
            ] = f"Relative poverty: Share of people below 50% of the median income ({lis_welfare['title'][wel].capitalize()}, {lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_50_median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_graphers_lis.loc[j, "Source Dropdown"] = lis_tables["source_name"][tab]
            df_graphers_lis.loc[
                j, "Metric Dropdown"
            ] = f"Share in relative poverty (< 50% of the median)"
            df_graphers_lis.loc[
                j, "Welfare type Dropdown"
            ] = f"{lis_welfare['dropdown_option'][wel]} ({lis_equivalence_scales['text'][eq]})"
            df_graphers_lis.loc[
                j, "subtitle"
            ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 50% of the median {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
            df_graphers_lis.loc[j, "note"] = np.nan
            df_graphers_lis.loc[j, "type"] = np.nan
            df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers_lis.loc[j, "hasMapTab"] = "true"
            df_graphers_lis.loc[j, "tab"] = "map"
            j += 1

    df_graphers_lis["tableSlug"] = lis_tables["name"][tab]


# Add yAxisMin and mapTargetTime
df_graphers_lis["yAxisMin"] = yAxisMin
df_graphers_lis["mapTargetTime"] = mapTargetTime

###########################################################################################
# WORLD INEQUALITY DATABASE (WID)
###########################################################################################

# Grapher table generation

yAxisMin = 0
mapTargetTime = 2019

df_graphers_wid = pd.DataFrame()

j = 0

for tab in range(len(wid_tables)):
    for wel in range(len(wid_welfare)):
        # Gini coefficient
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} inequality: Gini coefficient {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p0p100_gini_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Gini coefficient"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The Gini coefficient is a measure of the inequality of the {wid_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 10%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the top 10% {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p90p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Top 10% share"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 10% as a share of total {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 1%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the top 1% {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p99p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Top 1% share"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 1% as a share of total {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 0.1%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the top 0.1% {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p99_9p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Top 0.1% share"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.1% as a share of total {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 0.01%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the top 0.01% {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[
            j, "ySlugs"
        ] = f"p99_99p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Top 0.01% share"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.01% as a share of total {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 0.001%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the top 0.001% {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[
            j, "ySlugs"
        ] = f"p99_999p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Top 0.001% share"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 0.001% as a share of total {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # P90/P10
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} inequality: P90/P10 ratio {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p90_p10_ratio_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "P90/P10"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"P90 and P10 are the levels of {wid_welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # P90/P50
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} inequality: P90/P50 ratio {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p90_p50_ratio_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "P90/P50"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # P50/P10
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} inequality: P50/P10 ratio {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"p50_p10_ratio_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "P50/P10"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {wid_welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # # Palma ratio
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} inequality: Palma ratio {wid_welfare['title'][wel].capitalize()}"
        df_graphers_wid.loc[j, "ySlugs"] = f"palma_ratio_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[j, "Metric Dropdown"] = "Palma ratio"
        df_graphers_wid.loc[
            j, "Welfare type Dropdown"
        ] = f"{wid_welfare['dropdown_option'][wel]}"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The Palma ratio is the share of total {wid_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

    df_graphers_wid["tableSlug"] = wid_tables["name"][tab]

# %% [markdown]
# Add yAxisMin and mapTargetTime
df_graphers_wid["yAxisMin"] = yAxisMin
df_graphers_wid["mapTargetTime"] = mapTargetTime

# Concatenate all the graphers dataframes
df_graphers = pd.concat([df_graphers_lis, df_graphers_wid], ignore_index=True)

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["Source Dropdown"] == "Luxembourg Income Study (LIS)")
    & (df_graphers["Metric Dropdown"] == "Gini coefficient")
    & (df_graphers["Welfare type Dropdown"] == "Disposable income (equivalized)"),
    ["defaultView"],
] = "true"


# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: table names (from table dataframe)
table_list = list(df_tables["tableSlug"].unique())

# Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

# Graphers table is converted into a tab-separated text
graphers_tsv = df_graphers
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

# This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# The dataframes are combined, including tables and links to the datasets
with open(outfile, "w", newline="\n", encoding="utf-8") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for tab in table_list:
        table_tsv = (
            df_tables[df_tables["tableSlug"] == tab].copy().reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["tableSlug"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write(
            "\ntable\t"
            + all_the_tables.loc[all_the_tables["name"] == tab, "link"].item()
            + "\t"
            + tab
        )
        f.write("\ncolumns\t" + tab + "\n\n" + table_tsv_indented)
