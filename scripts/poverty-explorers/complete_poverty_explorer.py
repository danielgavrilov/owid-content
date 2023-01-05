# %% [markdown]
# # Poverty Data Explorer of World Bank data: Expanded metrics
# This code creates the tsv file for the expanded poverty metrics explorer from the World Bank PIP data, available [here](https://owid.cloud/admin/explorers/preview/poverty-explorer-expanded)

# %%
import pandas as pd
import numpy as np
import textwrap

outfile = "../../explorers/poverty-explorer-expanded.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each poverty line or survey type.

# %%
#Read Google sheets
sheet_id = '17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8'

#Absolute poverty sheet
sheet_name = 'povlines_abs'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_abs = pd.read_csv(url, dtype={'dollars_text':'str'})

#Relative poverty sheet
sheet_name = 'povlines_rel'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
povlines_rel = pd.read_csv(url)

#Survey type sheet
sheet_name = 'survey_type'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
survey_type = pd.read_csv(url)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
#The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {'explorerTitle': 'Poverty Data Explorer of World Bank data: Expanded metrics',
               'selection': ['Mozambique', 'Nigeria', 'Kenya', 'Bangladesh', 'Bolivia', 'World'],
               'explorerSubtitle': "<i><a href='https://github.com/owid/poverty-data'>Download Poverty data on GitHub</a></i>",
               'isPublished': 'false',
               'googleSheet': 'https://docs.google.com/spreadsheets/d/17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8',
               'wpBlockId': '52633',
               'entityType': 'country or region'}

#Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient='index', columns=None)
#Assigns a cell for each entity separated by comma (like in `selection`)
df_header= df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type to iterate by different poverty lines and survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%
#Table generation
df_tables = pd.DataFrame()
j=0

for survey in range(len(survey_type)):

    #Headcount ratio (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'Share of population below ${povlines_abs.dollars_text[p]} a day'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below ${povlines_abs.dollars_text[p]} a day.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "OrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'Number of people below ${povlines_abs.dollars_text[p]} a day'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_abs.dollars_text[p]} a day.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "Reds"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Total shortfall (abs)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - total daily shortfall'
        df_tables.loc[j, 'slug'] = f'total_shortfall_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The total shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day. This is the amount of money that would be theoretically needed to lift the {survey_type.text[survey]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "Oranges"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall ($ per day)
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - average daily shortfall'
        df_tables.loc[j, 'slug'] = f'avg_shortfall_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day (averaged across the population in poverty).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = povlines_abs.scale_avg_shortfall[p]
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "Purples"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall (% of poverty line) [this is the income gap ratio]
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - income gap ratio'
        df_tables.loc[j, 'slug'] = f'income_gap_ratio_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrRd"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Poverty gap index
    for p in range(len(povlines_abs)):
        df_tables.loc[j, 'name'] = f'${povlines_abs.dollars_text[p]} a day - poverty gap index'
        df_tables.loc[j, 'slug'] = f'poverty_gap_index_{povlines_abs.cents[p]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The poverty gap index calculated at a poverty line of ${povlines_abs.dollars_text[p]} a day. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line.  It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "RdPu"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount ratio (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - share of population below poverty line'
        df_tables.loc[j, 'slug'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total number of people below poverty line'
        df_tables.loc[j, 'slug'] = f'headcount_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Total shortfall (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - total daily shortfall'
        df_tables.loc[j, 'slug'] = f'total_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The total shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}. This is the amount of money that would be theoretically needed to lift the {survey_type.text[survey]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, 'unit'] = np.nan
        df_tables.loc[j, 'shortUnit'] = np.nan
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall ($ per day)
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - average daily shortfall'
        df_tables.loc[j, 'slug'] = f'avg_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of of {povlines_rel.text[pct]} {survey_type.text[survey]} (averaged across the population in poverty).'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "international-$ at 2017 prices"
        df_tables.loc[j, 'shortUnit'] = "$"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "1;2;5;10;20;20.0001"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall (% of poverty line) [this is the income gap ratio]
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - income gap ratio'
        df_tables.loc[j, 'slug'] = f'income_gap_ratio_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The average shortfall from a poverty line of of {povlines_rel.text[pct]} {survey_type.text[survey]} (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Poverty gap index
    for pct in range(len(povlines_rel)):
        df_tables.loc[j, 'name'] = f'{povlines_rel.percent[pct]} of median - poverty gap index'
        df_tables.loc[j, 'slug'] = f'poverty_gap_index_{povlines_rel.slug_suffix[pct]}'
        df_tables.loc[j, 'sourceName'] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[j, 'description'] = f'The poverty gap index calculated at a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line.  It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.'
        df_tables.loc[j, 'sourceLink'] = "https://pip.worldbank.org/"
        df_tables.loc[j, 'dataPublishedBy'] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, 'unit'] = "%"
        df_tables.loc[j, 'shortUnit'] = "%"
        df_tables.loc[j, 'tolerance'] = 5
        df_tables.loc[j, 'type'] = "Numeric"
        df_tables.loc[j, 'colorScaleNumericMinValue'] = 0
        df_tables.loc[j, 'colorScaleNumericBins'] = "3;6;9;12;15;18;21"
        df_tables.loc[j, 'colorScaleEqualSizeBins'] = "true"
        df_tables.loc[j, 'colorScaleScheme'] = "YlOrBr"
        df_tables.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

#Make tolerance integer (to not break the parameter in the platform)
df_tables['tolerance'] = df_tables['tolerance'].astype("Int64")

# %% [markdown]
# ### Tables for variables showing breaks between surveys
# These variables consider a breaks in the series due to changes in surveys' methodology.

# %%
#Create master table for line breaks
df_spells = pd.DataFrame()
j=0

for i in range(len(df_tables)):
    for c_spell in range(1,7):
        df_spells.loc[j, 'master_var'] = df_tables.slug[i]
        df_spells.loc[j, 'name'] = "Consumption surveys"
        df_spells.loc[j, 'slug'] = f"consumption_spell_{c_spell}"
        df_spells.loc[j, 'sourceName'] = df_tables.sourceName[i]
        df_spells.loc[j, 'description'] = df_tables.description[i]
        df_spells.loc[j, 'sourceLink'] = df_tables.sourceLink[i]
        df_spells.loc[j, 'dataPublishedBy'] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, 'unit'] = df_tables.unit[i]
        df_spells.loc[j, 'shortUnit'] = df_tables.shortUnit[i]
        df_spells.loc[j, 'tolerance'] = df_tables.tolerance[i]
        df_spells.loc[j, 'type'] = df_tables.type[i]
        df_spells.loc[j, 'colorScaleNumericMinValue'] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, 'colorScaleNumericBins'] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, 'colorScaleEqualSizeBins'] = df_tables.colorScaleEqualSizeBins[i]
        df_spells.loc[j, 'colorScaleScheme'] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, 'survey_type'] = df_tables.survey_type[i]
        j += 1

    for i_spell in range(1,8):
        df_spells.loc[j, 'master_var'] = df_tables.slug[i]
        df_spells.loc[j, 'name'] = "Income surveys"
        df_spells.loc[j, 'slug'] = f"income_spell_{i_spell}"
        df_spells.loc[j, 'sourceName'] = df_tables.sourceName[i]
        df_spells.loc[j, 'description'] = df_tables.description[i]
        df_spells.loc[j, 'sourceLink'] = df_tables.sourceLink[i]
        df_spells.loc[j, 'dataPublishedBy'] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, 'unit'] = df_tables.unit[i]
        df_spells.loc[j, 'shortUnit'] = df_tables.shortUnit[i]
        df_spells.loc[j, 'tolerance'] = df_tables.tolerance[i]
        df_spells.loc[j, 'type'] = df_tables.type[i]
        df_spells.loc[j, 'colorScaleNumericMinValue'] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, 'colorScaleNumericBins'] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, 'colorScaleEqualSizeBins'] = df_tables.colorScaleEqualSizeBins[i]
        df_spells.loc[j, 'colorScaleScheme'] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, 'survey_type'] = df_tables.survey_type[i]
        j += 1

#Make tolerance integer (to not break the parameter in the platform)
df_spells['tolerance'] = df_spells['tolerance'].astype("Int64")

# %% [markdown]
# ## Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# %%
#Grapher table generation

df_graphers = pd.DataFrame()

j=0

for survey in range(len(survey_type)):

    #Headcount ratio (abs)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_share[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle[p]}'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. Depending on the country and year, it relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount (abs)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_number[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle[p]}'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices. Depending on the country and year, it relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Total shortfall (abs)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_total_shortfall[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'total_shortfall_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Total shortfall from poverty line"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_total_shortfall[p]}'
        df_graphers.loc[j, 'note'] = "This data is expressed in international-$ at 2017 prices. The cost of closing the poverty gap does not take into account costs and inefficiencies from making the necessary transfers."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall ($ per day)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_avg_shortfall[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'avg_shortfall_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall ($ per day)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_avg_shortfall[p]}'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall (% of poverty line)
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'{povlines_abs.title_income_gap_ratio[p]}'
        df_graphers.loc[j, 'ySlugs'] = f'income_gap_ratio_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall (% of poverty line)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'{povlines_abs.subtitle_income_gap_ratio[p]}'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Poverty gap index
    for p in range(len(povlines_abs)):

        df_graphers.loc[j, 'title'] = f'Poverty gap index at ${povlines_abs.dollars_text[p]} a day'
        df_graphers.loc[j, 'ySlugs'] = f'poverty_gap_index_{povlines_abs.cents[p]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Poverty gap index"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_abs.povline_dropdown[p]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line).'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount ratio (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_share[pct]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_ratio_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Share in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Headcount (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'{povlines_rel.title_number[pct]}'
        df_graphers.loc[j, 'ySlugs'] = f'headcount_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Number in poverty"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}.'
        df_graphers.loc[j, 'note'] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Total shortfall (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Total shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'total_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Total shortfall from poverty line"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel.text[pct]} {survey_type.text[survey]}. This data is adjusted for inflation and for differences in the cost of living between countries.'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall ($ per day) (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Average shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'avg_shortfall_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall ($ per day)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel.text[pct]} {survey_type.text[survey]}, averaged across the population in poverty.'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Average shortfall (% of poverty line) (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Average shortfall from a poverty line of {povlines_rel.text[pct]} {survey_type.text[survey]} (as a share of the poverty line)'
        df_graphers.loc[j, 'ySlugs'] = f'income_gap_ratio_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Average shortfall (% of poverty line)"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'This is the average shortfall expressed as a share of the poverty line, sometimes called the "income gap ratio". It captures the depth of poverty in which those below {povlines_rel.text[pct]} {survey_type.text[survey]} a day are living.'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

    #Poverty gap index (rel)
    for pct in range(len(povlines_rel)):

        df_graphers.loc[j, 'title'] = f'Poverty gap index at {povlines_rel.text[pct]} {survey_type.text[survey]}'
        df_graphers.loc[j, 'ySlugs'] = f'poverty_gap_index_{povlines_rel.slug_suffix[pct]}'
        df_graphers.loc[j, 'Metric Dropdown'] = "Poverty gap index"
        df_graphers.loc[j, 'Poverty line Dropdown'] = f'{povlines_rel.dropdown[pct]}'
        df_graphers.loc[j, 'Household survey data type Dropdown'] = f'{survey_type.dropdown_option[survey]}'
        df_graphers.loc[j, 'tableSlug'] = f'{survey_type.table_name[survey]}'
        df_graphers.loc[j, 'subtitle'] = f'The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line).'
        df_graphers.loc[j, 'note'] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. It relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, 'sourceDesc'] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, 'type'] = np.nan
        df_graphers.loc[j, 'yAxisMin'] = 0
        df_graphers.loc[j, 'facet'] = np.nan
        df_graphers.loc[j, 'selectedFacetStrategy'] = np.nan
        df_graphers.loc[j, 'hasMapTab'] = "true"
        df_graphers.loc[j, 'tab'] = "map"
        df_graphers.loc[j, 'mapTargetTime'] = 2019
        df_graphers.loc[j, 'survey_type'] = survey_type['table_name'][survey]
        j += 1

df_graphers['Show breaks between less comparable surveys Checkbox'] = "false"
# %% [markdown]
# ### Grapher views to show breaks in the curves

# %%
df_graphers_spells = pd.DataFrame()
j=0

for i in range(len(df_graphers)):
    df_graphers_spells.loc[j, 'title'] = df_graphers['title'][i]
    df_graphers_spells.loc[j, 'ySlugs'] = "consumption_spell_1 consumption_spell_2 consumption_spell_3 consumption_spell_4 consumption_spell_5 consumption_spell_6 income_spell_1 income_spell_2 income_spell_3 income_spell_4 income_spell_5 income_spell_6 income_spell_7"
    df_graphers_spells.loc[j, 'Metric Dropdown'] = df_graphers['Metric Dropdown'][i]
    df_graphers_spells.loc[j, 'Poverty line Dropdown'] = df_graphers['Poverty line Dropdown'][i]
    df_graphers_spells.loc[j, 'Household survey data type Dropdown'] = df_graphers['Household survey data type Dropdown'][i]
    df_graphers_spells.loc[j, 'tableSlug'] = df_graphers['survey_type'][i] + "_" + df_graphers['ySlugs'][i]
    df_graphers_spells.loc[j, 'subtitle'] = df_graphers['subtitle'][i]
    df_graphers_spells.loc[j, 'note'] = df_graphers['note'][i]
    df_graphers_spells.loc[j, 'sourceDesc'] = df_graphers['sourceDesc'][i]
    df_graphers_spells.loc[j, 'type'] = df_graphers['type'][i]
    df_graphers_spells.loc[j, 'yAxisMin'] = df_graphers['yAxisMin'][i]
    df_graphers_spells.loc[j, 'facet'] = 'entity'
    df_graphers_spells.loc[j, 'selectedFacetStrategy'] = 'entity'
    df_graphers_spells.loc[j, 'hasMapTab'] = "false"
    df_graphers_spells.loc[j, 'tab'] = np.nan
    df_graphers_spells.loc[j, 'mapTargetTime'] = np.nan
    df_graphers_spells.loc[j, 'Show breaks between less comparable surveys Checkbox'] = "true"
    j += 1

df_graphers = pd.concat([df_graphers, df_graphers_spells], ignore_index=True)


# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
#Add related question link
df_graphers['relatedQuestionText'] = np.nan
df_graphers['relatedQuestionUrl'] = np.nan

#Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers['mapTargetTime'] = df_graphers['mapTargetTime'].astype("Int64")

#Select one default view
df_graphers.loc[(df_graphers['ySlugs'] == "headcount_ratio_215")
                & (df_graphers['tableSlug'] == "inc_or_cons")
                & (df_graphers['Show breaks between less comparable surveys Checkbox'] == "false"), ['defaultView']] = "true"

# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
#Define list of variables to iterate: survey types and the list of variables (the latter for spell tables)
survey_list = list(survey_type['table_name'].unique())
var_list = list(df_spells['master_var'].unique())

#Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

#Auxiliar variable `survey_type` is dropped and graphers table is converted into a tab-separated text
graphers_tsv = df_graphers.drop(columns=['survey_type'])
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

#This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

#The dataframes are combined, including tables which are filtered by survey type and variable
with open(outfile, "w", newline="\n", encoding='utf-8') as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for i in survey_list:
        table_tsv = df_tables[df_tables['survey_type'] == i].copy().reset_index(drop=True)
        table_tsv = table_tsv.drop(columns=['survey_type'])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write("\ntable\t" + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/" + i + "/poverty_" + i + ".csv\t" + i)
        f.write("\ncolumns\t" + i + "\n\n" + table_tsv_indented)

    for var in var_list:
        for i in survey_list:
            table_tsv = df_spells[(df_spells['master_var'] == var) & (df_spells['survey_type'] == i)].copy().reset_index(drop=True)
            table_tsv = table_tsv.drop(columns=['master_var', 'survey_type'])
            table_tsv = table_tsv.to_csv(sep="\t", index=False)
            table_tsv_indented = textwrap.indent(table_tsv, "\t")
            f.write("\ntable\t" + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/comparability_data/" + i + "/" + var + ".csv\t" + i + "_" + var)
            f.write("\ncolumns\t" + i + "_" + var + "\n\n" + table_tsv_indented)
