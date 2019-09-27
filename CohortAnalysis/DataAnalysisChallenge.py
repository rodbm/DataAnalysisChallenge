# 1) ----- Importing Packages and Libraries -----#
import pandas as pd
import os as os
import seaborn as sns
import getpass
import sqlite3
import requests
import json
from pandasql import sqldf
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt

pysqldf = lambda q: sqldf(q, globals())

# 2) ----- Defining Directory -----#
user = getpass.getuser()
path = 'C:/Users/'+user+'/Documents/nibo'
try:
    os.mkdir(path)
except:
    pass
os.chdir(path)

# 3) #----- Building Database -----#
# 3.1) #- createdOrganizations -#
r = requests.get('https://raw.githubusercontent.com/nibodev/'+
                 'DataAnalysisChallenge/master/SRC/CreatedOrganizations.sql')
sql_file = r.text.replace(' PRIMARY KEY', '')

conn = sqlite3.connect('nibo.db')
cur = conn.cursor()
cur.executescript(sql_file)
conn.commit()

createdOrganizations = pd.read_sql_query("select * from createdOrganizations;",
                                         conn)
dupl_check = pd.DataFrame(createdOrganizations.groupby('organizationId') \
                          ['organizationCreateDate'].count())
dupl_list = dupl_check \
            [dupl_check['organizationCreateDate']>1].index.values.tolist()
print('As seguintes empresas estão duplicadas na base: ' \
      +str(dupl_list).replace('[', '').replace(']', ''))
createdOrganizations.drop_duplicates(subset='organizationId', 
                                     keep='first', 
                                     inplace=True)
createdOrganizations.to_csv('createdOrganizations.csv', 
                            index=False)
# 3.2) #- accountantContracts -#
r = requests.get('https://raw.githubusercontent.com/nibodev/'+
                 'DataAnalysisChallenge/master/SRC/accountantContracts.json')
json_file = json.loads(r.text)
accountantContracts = json_normalize(json_file)
accountantContracts.to_csv('accountantContracts.csv', 
                           index=False)

# 4) #----- Data Preprocessing -----#
createdOrganizations = pd.read_csv('createdOrganizations.csv')
accountantContracts = pd.read_csv('accountantContracts.csv')

accountantContracts = \
pd.merge(accountantContracts, 
         createdOrganizations[['accountantId',
                               'accountantCreateDate']].drop_duplicates(), 
         how='left', 
         on='accountantId')
accountantContracts.drop(['ignoreField'], 
                         axis=1, 
                         inplace=True)
createdOrganizations.drop(['accountantCreateDate'], 
                          axis=1, 
                          inplace=True)
accountantContracts["signDate"] = \
accountantContracts["signDate"].str.split("T", 
                                           expand = True)[0]
accountantContracts['signDate'] = \
pd.to_datetime(accountantContracts['signDate'])
accountantContracts['accountantCreateDate'] =  \
pd.to_datetime(accountantContracts['accountantCreateDate'])
createdOrganizations['organizationCreateDate'] =  \
pd.to_datetime(createdOrganizations['organizationCreateDate'])

accountantContracts['signDate_month'] = \
accountantContracts['signDate'].dt.month
createdOrganizations['organizationCreateDate_month'] = \
createdOrganizations['organizationCreateDate'].dt.month

base_engaj_accountant = pysqldf("""
SELECT
A.accountantId,
A.signDate_month AS cohort,
A.signedOrganizationsCount AS total,
B.organizationCreateDate_month AS m,
B.count_org
FROM accountantContracts A
JOIN
(
SELECT
accountantId,
organizationCreateDate_month,
COUNT(DISTINCT organizationId) AS count_org
FROM createdOrganizations
GROUP BY
accountantId,
organizationCreateDate_month
) B ON A.accountantId = B.accountantId

""")

cohort_org = pysqldf("""
SELECT
A.cohort,
COUNT(A.accountantId) AS count_accountant,
B.total,
A.m,
SUM(count_org) AS count_org
FROM base_engaj_accountant A
LEFT JOIN
(
SELECT
cohort,
SUM(total) AS total
FROM base_engaj_accountant
GROUP BY
cohort
) B ON A.cohort = B.cohort
GROUP BY
A.cohort,
A.m,
B.total
""")

cohort_org = cohort_org[(cohort_org['cohort']>1) & (cohort_org['cohort']<12)]
cohort_org = cohort_org[cohort_org['cohort']<=cohort_org['m']]
cohort_org['m'] = cohort_org['m']-cohort_org['cohort']
cohort_org = cohort_org.reset_index(drop=True)
cohort_org['count_org'] = cohort_org.groupby('cohort')['count_org'].cumsum()
cohort_org['count_org'] = cohort_org['count_org']/cohort_org['total']
cohort_org.drop(['count_accountant', 'total'], 
                axis=1, 
                inplace=True)
cohort_org = round(cohort_org.pivot_table(index=['cohort'], 
                                          columns='m', 
                                          values='count_org'),2)

cohort_acc = base_engaj_accountant.copy()

cohort_acc.drop(['total','m','count_org'], 
                axis=1, 
                inplace=True)
cohort_acc = pd.merge(cohort_acc, 
                      accountantContracts[['accountantId', 'cancelDate']], 
                      how='left', 
                      on='accountantId')
cohort_acc['cancelDate'] =  pd.to_datetime(cohort_acc['cancelDate'], 
                                           format="%d/%m/%Y")
cohort_acc['m'] = cohort_acc['cancelDate'].dt.month
cohort_acc.drop(['cancelDate'], 
                axis=1, 
                inplace=True)

cohort_acc['m'] = cohort_acc['m'].fillna(0)

cohort_acc = pysqldf("""
SELECT
A.cohort,
B.total,
A.m,
COUNT(DISTINCT CASE WHEN m>0 THEN A.accountantId ELSE NULL END) AS count_dp_acc
FROM cohort_acc A
LEFT JOIN
(
SELECT
cohort,
COUNT(DISTINCT accountantId) AS total
FROM cohort_acc
GROUP BY
cohort
) B ON A.cohort = B.cohort
GROUP BY
A.cohort,
A.m,
B.total
""")

cohort_acc = cohort_acc[(cohort_acc['cohort']>1) & (cohort_acc['cohort']<12)]

cohort_list = ['2','3','4','5','6','7','8','9']
m_list = ['2','3','4','5','6','7','8','9']

for cohort in cohort_list:
    for m in m_list:
        m = int(m)
        cohort = int(cohort)
        df= []
        total = int(cohort_acc.loc[cohort_acc['cohort'] == cohort] \
                    ['total'].tolist()[0])
        df.append((cohort,total,m,0))
        df = pd.DataFrame(df)
        df.rename(columns = {0:'cohort',
                             1:'total',
                             2:'m',
                             3:'count_dp_acc'}, 
                  inplace = True)
        cohort_acc = cohort_acc.append(df)

cohort_acc = cohort_acc.sort_values(by=['cohort','m']).reset_index(drop=True)

cohort_acc = pysqldf("""
SELECT
cohort,
total,
m,
SUM(count_dp_acc) AS count_dp_acc
FROM cohort_acc
GROUP BY
cohort,
total,
m
""")

cohort_acc = cohort_acc[cohort_acc['cohort']<=cohort_acc['m']]
cohort_acc['m'] = cohort_acc['m']-cohort_acc['cohort']
cohort_acc = cohort_acc.reset_index(drop=True)
cohort_acc['count_dp_acc'] = \
cohort_acc.groupby('cohort')['count_dp_acc'].cumsum()
cohort_acc['count_acc'] = cohort_acc['total']-cohort_acc['count_dp_acc']
cohort_acc['count_acc'] = cohort_acc['count_acc']/cohort_acc['total']
cohort_acc.drop(['count_dp_acc', 'total'], 
                axis=1, 
                inplace=True)
cohort_acc = round(cohort_acc.pivot_table(index=['cohort'], 
                                          columns='m', 
                                          values='count_acc'),2)

# 5) #----- Plotting the Cohorts -----#
plt.figure(figsize = (11,9))
plt.title('First Cohort Analysis: Organization Creation Rate')
cohort_org_plot = sns.heatmap(data = cohort_org, 
                              annot = True, 
                              fmt = '.0%', 
                              vmin = 0.0,
                              vmax = 1.0,
                              cmap = "YlGnBu")

plt.figure(figsize = (11,9))
plt.title('Second Cohort Analysis: Accountant Churn')
cohort_acc_plot = sns.heatmap(data = cohort_acc, 
                              annot = True, 
                              fmt = '.0%', 
                              vmin = 0.0,
                              vmax = 1.0,
                              cmap = "YlGnBu")

# 6) #----- Cohorts Correlation Hypothesis: Qualitative Analysis -----#
cohort_org = cohort_org.T
cohort_acc = cohort_acc.T

df_corr = pd.merge(pd.DataFrame(cohort_org.corrwith(cohort_acc)), 
              pd.DataFrame(base_engaj_accountant.groupby('cohort') \
                           ['accountantId'].nunique()), 
              how='left', 
              on='cohort').dropna()

df_corr = df_corr.rename(columns={0: 'corr', 'accountantId': 'acc_weight'})

sns.regplot(cohort_org[2], cohort_acc[2])
sns.regplot(cohort_org[3], cohort_acc[3])
sns.regplot(cohort_org[4], cohort_acc[4])
sns.regplot(cohort_org[5], cohort_acc[5])
sns.regplot(cohort_org[6], cohort_acc[6])

print('The weighted correlation between the lack of accountant engagement '+
      'rate and accountant churn rate is of '+
str(round((((df_corr['corr']*df_corr['acc_weight']).sum())/
     df_corr['acc_weight'].sum())*(-1), 4)*100)+'%.')