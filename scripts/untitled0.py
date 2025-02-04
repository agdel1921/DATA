
"""
This file is to prepare some generic code for NTUC data validation and manipulation
This file is generated by Ivy Yi on 20180817
"""

__author__ = 'Latize'
import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import csv
os.environ['SPARK_HOME']=r"C:\opt\spark\spark-2.3.1-bin-hadoop2\spark-2.3.1-bin-hadoop2.7"
sys.path.append(r"C:\opt\spark\spark-2.3.1-bin-hadoop2\spark-2.3.1-bin-hadoop2.7\python")
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType
from functools import reduce
from pyspark.sql.functions import substring
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation
from pyspark.ml.stat import ChiSquareTest
from pyspark.sql.functions import col
from pyspark.mllib.stat import Statistics
import datetime
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql import functions as F
conf = SparkConf().setMaster("local").setAppName("NTUC")
sc = SparkContext(conf = conf)
sqlContext=SQLContext(sc)

def read_file(path):
    df = sqlContext.read.csv(path,header=True)
    return (df)

def clean_header(data,oldColumns,newColumns):
    df = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)), data)
    return(df)

def change_to_int(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].cast(IntegerType()))
    return(data)

def change_to_float(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].cast(FloatType()))
    return(data)

def change_to_month(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].substr(1, 7))
    return(data)

def data_exploration(data,data_name):
    categorical_data=pd.DataFrame()
    descriptive_data=pd.DataFrame()

    categorical_output_loc = r"E:/NTUC/Processed/Categorical_output_/" + data_name + ".csv"
    descriptive_output_loc = r"E:/NTUC/Processed/desc_output_/" + data_name + ".csv"
    for column in data.schema.names:
        graph_name=r"E:/NTUC/Processed/Graph_chart_/" + data_name + "_" + column + ".png"
        flag=data.schema[column].dataType
        categorical_update=data.groupby(column).count().toPandas()
        categorical_update=categorical_update.sort_values(by="count",ascending=False).reset_index(drop=True)
        categorical_data=pd.concat([categorical_data, categorical_update], axis=1, sort=False)
        if isinstance(flag,IntegerType) or isinstance(flag,FloatType):
            descriptive_update=data.describe(column).toPandas()
            descriptive_data = pd.concat([descriptive_data, descriptive_update], axis=1, sort=False)
            categorical_update_graph = categorical_update
            categorical_update_graph.set_index(column, inplace=True)
            plot = categorical_update_graph.plot.bar()
            fig = plot.get_figure()
            fig.savefig(graph_name)
    categorical_data.to_csv(categorical_output_loc, header=True, index=False)
    descriptive_data.to_csv(descriptive_output_loc, header=True, index=False)
    return()

def unique_counts(sampledata):
    path = r"E:/NTUC/Processed/UniqueOutput_/" + "unique" + ".csv"
    for i in sampledata.columns:
        sample = sampledata.toPandas()
        count = sample[i].nunique()
        print(i,": ", count)
        return()


def contentAnalysis(sampleData):
    sample12 = sampleData.toPandas()
    abc = sample12.corr(method='pearson')
    print(abc)
    path = r"E:/NTUC/Processed/correlation/"+"correlation" + ".csv"
    abc.to_csv(path,header=True, index=False)
    return()


## Reading files in pyspark data frame


## 1. edw_Product Data Review
product_path=r"E:/Working/cust_house.csv"
proddata=read_file(product_path)
#Schema and total number of columns
len(proddata.columns), proddata.columns
proddata.schema.names
proddata.count()
proddata.select(proddata.columns[:2]).take(5)
proddata.first().drop()

proddata.select(proddata["originalsumassured"]>0).count()
proddata.select("customerseqid").distinct().show()
proddata.select(proddata["sumassured"]>0).count()
#Description
abc = prod_test.describe()
contentAnalysis(prod_test)


# 2. TransactionData
transaction_path=r"E:\NTUC\raw_data\Data_24092018\edw_transaction_v2_240918\transaction.csv"
transaction_data=read_file(transaction_path)
len(transaction_data.columns) , transaction_data.columns
transaction_data.count()
# Transaction data header cleaning
transaction_date_col=["SubmitDate","IssueDate","PolicyStartDate","PolicyEndDate"]
transaction_float_col=["nettpremium","totalpremium","maindriverage", "maindriveryrsofexperience","vehage"]
transaction_int_col=["originalsumassured","sumassured", "vehcapacity", "noofseat", "policyseqid","productseqid", "customerseqid","servicingagentseqid","salesagentseqid"]
transaction_data=change_to_int(transaction_data,transaction_int_col)
transaction_data=change_to_float(transaction_data,transaction_float_col)
transaction_data=change_to_month(transaction_data,transaction_date_col)
#transaction_data.count()
transaction_data=transaction_data.drop('_c0')
#transaction_data=transaction_data.drop('policyseqid')
# Data Exploration
transaction_data.write.parquet("E:/NTUC/Processed/parquet_dump/transaction")
transaction_data.write.csv("transaction_data.csv", header = True)
data_exploration(transaction_data,"transaction_data")
contentAnalysis(transaction_data)
abc = transaction_data.describe().write.csv()
abx = transaction_data.toPandas()
abx.to_csv(path+"transaction.csv",header=True, index = False)
path = "E:/NTUC/Processed/DataFinal/transaction_data.csv/"
os.chdir(path)
fls = os.listdir(path)
for a2 in fls:
    if a2[-4:]=='.csv':
        structDf = pd.read_csv(a2, header=0, low_memory = True)











# 2. Customerview data
cust_path=r"E:\NTUC\raw_data\DataSet1\customer_view.csv"
cust_test=read_file(cust_path)
# Schema and total number of columns
len(cust_test.columns) , cust_test.columns
cust_test.count()

#customerview data header cleaning
custview_clean_header=['CustomerSeqID',
 'CustomerStatus',
 'GenderPH',
 'MMOPH',
 'AgePH',
 'H_ID',
 'CustomerType',
 'CustomerValueLI',
 'IndividualRelationTag',
 'ReachScore10',
 'CustomerReachConfi',
 'MembersSpouse',
 'MembersChild',
 'MembersOthers',
 'Tod',
 'Young',
 'Grad',
 'Teen',
 'Adult',
 'PolicyCount',
 'Decision_maker']

cust_test=clean_header(cust_test,cust_test.schema.names,custview_clean_header)

cust_int_col=["MembersSpouse","MembersChild","MembersOthers","Tod","Young","Grad","Teen","Adult","PolicyCount", "CustomerSeqID", "ReachScore10"]

cust_float_col=["AgePH"]

cust_test=change_to_int(cust_test,cust_int_col)

cust_test=change_to_float(cust_test,cust_float_col)
cust_test.write.csv("CustomerView.csv", header = True)
cust_test.write.parquet("E:/NTUC/Processed/parquet_dump/custview")
#Exploratory and Descriptive Analysis
data_exploration(cust_test,"custmer_view")
unique_counts(cust_test)
contentAnalysis(cust_test)

# 3. houseview file
home_path=r"E:\NTUC\raw_data\DataSet1\houseview.csv"
home_test=read_file(home_path)
# Schema and total number of columns
len(home_test.columns) , home_test.columns
home_test.count()

#Display Records
home_test.show()

# Houseview data header cleaning
home_clean_header=['H_ID','MembersCount', 'GI_active', 'LI_active', 'IS_active', 'MembersActive', 'holdingtag','HouseRelationConfidence', 'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence', 'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag', 'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']
home_test=clean_header(home_test,home_test.schema.names,home_clean_header)
#home_float_col=["GI_active","LI_active","IS_active","HouseRelationCount","TodCount","YoungCount","TeenCount","GradCount","totalkids","Total_Policies"]

home_int_col=["MembersCount","MembersActive","GI_active","LI_active","IS_active","HouseRelationCount","TodCount","YoungCount","TeenCount","GradCount","totalkids","Total_Policies"]
home_test=change_to_int(home_test,home_int_col)
home_test.write.csv("HouseView.csv", header = True)
home_test.write.parquet("E:/NTUC/Processed/parquet_dump/houseView")

#home_test=change_to_float(home_test,home_float_col)
#Exploratory and Descriptive Analysis
data_exploration(home_test,"houseView_exploration")
unique_counts(home_test)
contentAnalysis(home_test)


# 4. Reading houseRelation File
homeRelation_path=r"E:\NTUC\raw_data\DataSet1\relation_houseview.csv"
homeRelation_test=read_file(homeRelation_path)
# Schema and total number of columns
len(homeRelation_test.columns) , homeRelation_test.columns
homeRelation_test.count()
homeRelation_test=homeRelation_test.drop('_c0')
#HomeRelation data header cleaning
homeRelation_test
homeRelation_clean_header=['customerIdnumber_1',
 'Relation',
 'Add_R',
 'RelationConfidence',
 'customerIdnumber_2',
 'type',
 'PHIS_R',
 'email_R',
 'Namematch',
 'H_ID']
homeRelation_test=clean_header(homeRelation_test,homeRelation_test.schema.names,homeRelation_clean_header)
homeRelation_test.write.parquet("E:/NTUC/Processed/parquet_dump/homeRelation")

data_exploration(homeRelation_test, "homeRelation_test")
unique_counts(homeRelation_test)

# 5. Agent Data
agent_path=r"E:\NTUC\raw_data\Data_24092018\edw_agent_v2_240918\agent.csv"
agent_data=read_file(agent_path)
len(agent_data.columns) , agent_data.columns
agent_data.count()
agent_int_col=["agentseqid"]
agent_data=change_to_int(agent_data,agent_int_col)
agent_data.write.csv("agent.csv", header = True)

agent_date_col=["agentdateappointed","agentdatejoined","agentdateleft","agentdateofbirth"]
agent_data=change_to_month(agent_data,agent_date_col)
# Data Exploration
agent_data.write.parquet("E:/NTUC/Processed/parquet_dump/agent")
data_exploration(agent_data,"agent_data")
contentAnalysis(agent_data)

# 6. TransactionData
transaction_path=r"E:\NTUC\raw_data\Data_24092018\edw_transaction_v2_240918\transaction.csv"
transaction_data=read_file(transaction_path)
len(transaction_data.columns) , transaction_data.columns
transaction_data.count()
# Transaction data header cleaning
transaction_date_col=["SubmitDate","IssueDate","PolicyStartDate","PolicyEndDate"]
transaction_float_col=["nettpremium","totalpremium","maindriverage", "maindriveryrsofexperience","vehage"]
transaction_int_col=["originalsumassured","sumassured", "vehcapacity", "noofseat", "policyseqid","productseqid", "customerseqid","servicingagentseqid","salesagentseqid"]
transaction_data=change_to_int(transaction_data,transaction_int_col)
transaction_data=change_to_float(transaction_data,transaction_float_col)
transaction_data=change_to_month(transaction_data,transaction_date_col)
#transaction_data.count()
transaction_data=transaction_data.drop('_c0')
#transaction_data=transaction_data.drop('policyseqid')
# Data Exploration
transaction_data.write.parquet("E:/NTUC/Processed/parquet_dump/transaction")
transaction_data.write.csv("transaction_data.csv", header = True)
data_exploration(transaction_data,"transaction_data")
contentAnalysis(transaction_data)
abc = transaction_data.describe().write.csv()

# 7. Lapse_Policy Data
lapsedPolicy_path=r"E:\NTUC\raw_data\Data_24092018\edw_lapsedpolicies_v1_280918\edw_lapsedpolicies.csv"
lapsed_Policy_data=read_file(lapsedPolicy_path)
len(lapsed_Policy_data.columns) , lapsed_Policy_data.columns
lapsed_Policy_data.count()

lapsed_Policy_data_int_col=["policyseqid","salesagentseqid","servicingagentseqid","customerseqid","ProductSeqID" ]
lapsed_Policy_data=change_to_int(lapsed_Policy_data,lapsed_Policy_data_int_col)
lapPolicy_date_col=["SubmitDate","IssueDate","PolicyStartDate","PolicyEndDate"]
lapsed_Policy_data=change_to_month(lapsed_Policy_data,lapPolicy_date_col)
# Data Exploration
lapsed_Policy_data.write.parquet("E:/NTUC/Processed/parquet_dump/LapsePolicy")
lapsed_Policy_data.write.csv("lapsed_Policy_data.csv", header = True)
data_exploration(lapsed_Policy_data,"lapsed_Policy")
contentAnalysis(lapsed_Policy_data)

# 8. customer_demography data
cust_demo_path=r"E:\NTUC\raw_data\Data_24092018\edw_customerdemog_historydetails_v1_280918\edw_customerdemog.csv"
cust_demo_data=read_file(cust_demo_path)
len(cust_demo_data.columns) , cust_demo_data.columns
cust_demo_data.count()
#cust_demo_col=["agentdateappointed","agentdatejoined","agentdateleft","agentdateofbirth"]
#agent_data=change_to_month(agent_data,agent_date_col)
cust_demo_data_int_col=["customerseqid"]
cust_demo_data=change_to_int(cust_demo_data,cust_demo_data_int_col)

# Data Exploration
data_exploration(cust_demo_data,"cust_demo_data")
contentAnalysis(cust_demo_data)
cust_demo_data.write.parquet("E:/NTUC/Processed/parquet_dump/customerData")
cust_demo_data.write.csv("cust_demo_data.csv", header = True)
# 9. travelPolicy data
travel_policy_path=r"E:\NTUC\raw_data\Data_24092018\edw_travelpolicy_v1_280918\edw_travelpolicy.csv"
travel_policy=read_file(travel_policy_path)
len(travel_policy.columns) , travel_policy.columns
travel_policy.count()

travel_policy_int_col=["policyseqid", "productseqid", "NoOfChildren"]
travel_policy=change_to_int(travel_policy,travel_policy_int_col)
# Data Exploration
data_exploration(travel_policy,"travel_policy")
travel_policy.write.parquet("E:/NTUC/Processed/parquet_dump/travel_policy")
travel_policy.write.csv("travel_policy.csv", header = True)
# 10. customer data
cust_path=r"E:\NTUC\raw_data\Data_24092018\edw_customer_v2_240918\customer.csv"
customer_data=read_file(cust_path)
len(customer_data.columns) , customer_data.columns
customer_data.count()



customer_data_int_col=["customerseqid"]
customer_data=change_to_int(customer_data,customer_data_int_col)


#customer_data=customer_data.drop('customerseqid')
# Data Exploration
data_exploration(customer_data,"customer_data")
customer_data.write.parquet("E:/NTUC/Processed/parquet_dump/customer")
customer_data.write.csv("customer_data.csv", header = True)

#Joining CustomerView and HouseView Tables on H_ID column

# Making Alias
cust = cust_test.alias('cust')
home = home_test.alias('home')
cust.head(5)
home.head(5)
len(cust.columns)
len(home.columns)
#Inner Join
inner_join = cust.join(home, cust.H_ID == home.H_ID)
inner_join.collect()
inner_join.count()
print(cust_test.count() - inner_join.count())
count = inner_join.map(lambda x: len(x)).distinct().collect()
len(inner_join.columns) , inner_join.columns

innerJ_clean_header=['CustomerSeqID',
 'CustomerStatus',
 'GenderPH',
 'MMOPH',
 'AgePH',
 'H_ID',
 'CustomerType',
 'CustomerValueLI',
 'IndividualRelationTag',
 'ReachScore10',
 'CustomerReachConfi',
 'MembersSpouse',
 'MembersChild',
 'MembersOthers',
 'Tod',
 'Young',
 'Grad',
 'Teen',
 'Adult',
 'PolicyCount',
 'Decision_maker','h_ID','MembersCount', 'GI_active', 'LI_active', 'IS_active', 'MembersActive', 'holdingtag','HouseRelationConfidence', 'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence', 'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag', 'Spouse_Flag', 'totalkids', 'Total_Policies', 'decision_Maker']

inner_join=clean_header(inner_join,inner_join.schema.names,innerJ_clean_header)
inner_join = inner_join.drop("h_ID","decision_Maker" )
inner_join.describe().write.csv("Description_innerjoin.csv")
abc.write().csv()
inner_join.write.csv("innerJoinCustHomeview.csv")

# Left_Join
left_join = cust.join(home, cust.H_ID == home.H_ID, how = 'left_outer')
left_join.count()


# Right_Join
right_join = cust.join(home, cust.H_ID == home.H_ID, how = 'right')
right_join.count()

# Full_Join
full_outer = cust.join(home, cust.H_ID == home.H_ID, how = 'full')
full_outer.count()
#Exploratory and descriptive Data Analysis
data_exploration(inner_join,"innerJoin")


# Customer data (combined with customer view) exploration
customer_path1=r"customer.csv"
customer_data1=read_file(customer_path1)
len(customer_data1.columns), customer_data1.columns
abc = customer_data1.describe().show().write().csv()
abc.write().csv()
customer_path1=r"D:\NTUC\raw_data\Data_set2\customer_new.csv"
customer_data=read_file(customer_path1)
len(customer_data.columns), customer_data.columns
abc = customer_data.describe()
df2=abc.toPandas()
df2.to_csv("Description.csv")
household_path=r"D:\NTUC\raw_data\DataSet1\houseview.csv"
household_data=read_file(household_path)
product_path=r"D:\NTUC\raw_data\Data_set2\product.csv"
product_data=read_file(product_path)

customer_date_col=["dateofbirth"]
customer_data=change_to_month(customer_data,customer_date_col)
data_exploration(customer_data,"customer_data")

customer2_path=r"D:\Data\NTUC\raw data\customer2.csv"
customer_data2=read_file(customer2_path)
customer_date_col=["dateofbirth"]
customer_data2=change_to_month(customer_data2,customer_date_col)
data_exploration(customer_data2,"customer_data2")








final_data=transaction_data.join(product_data,on='productseqid',how="left")
final_data=final_data.join(customer_data,on= 'customerseqid',how="left")
final_data=final_data.join(customer_view_data,on='customerseqid',how="left")
drop_col=[ 'mmoemail','mmomail', 'mmophone','mmosms','productstartdate','productenddate','CustomerStatus',
 'GenderPH',
 'MMOPH','CustomerValueLI',
 'IndividualRelationTag','CustomerReachConfi',
 'MembersSpouse',
 'MembersChild',
 'MembersOthers',
 'Tod',
 'Young',
 'Grad',
 'Teen',
 'Adult',
 'PolicyCount',
 'Decision_maker','_c0']
for col in drop_col:
    final_data=final_data.drop(col)
final_data=final_data.drop('CustomerSeqID')
output_loc=r"D:\Data\NTUC\raw data\aftermerge20180912.csv"
final_data.repartition(10).write.option("header", "true").csv(output_loc)

merge_path=r"C:\Users\latize\merge\merged.csv"
merge_data=read_file(merge_path)
merge_data_clean_header=['customerseqid',
 'productseqid',
 'policyseqid',
 'SubmitDate',
 'IssueDate',
 'PolicyStartDate',
 'PolicyEndDate',
 'nettpremium',
 'totalpremium',
 'originalsumassured',
 'sumassured',
 'businesstype',
 'PolicyStatusDescription',
 'PolicyStatusCategory',
 'maindriverage',
 'maindriveryrsofexperience',
 'maindriveroccupation',
 'vehmodelcode',
 'vehbrand',
 'vehtypename',
 'vehusagename',
 'vehcapacity',
 'vehage',
 'noofseat',
 'coeflag',
 'importcarflag',
 'salesagentseqid',
 'servicingagentseqid',
 'productname',
 'productline',
 'productcategory',
 'productsubcategory',
 'ismain',
 'governmentschemeintegrated',
 'entityid',
 'dateofbirth',
 'gender',
 'nationality',
 'race',
 'educationlevel',
 'maritalstatus',
 'staffflag',
 'PostalCode',
 'dwellingtype',
 'AgePH',
 'H_ID',
 'CustomerType',
 'ReachScore10']
merge_data=clean_header(merge_data,merge_data.schema.names,merge_data_clean_header)
select_columns1=['H_ID', 'policyseqid']
select_columns2=['customerseqid', 'policyseqid']
select_columns3=['customerseqid','PolicyCount']
select_data1=merge_data.select(select_columns1)
select_data1=select_data1.distinct()
select_data2=transaction_data.select(select_columns2)
select_data2=select_data2.distinct()
select_data3=customer_view_data.select(select_columns3)
select_columns3_new=['CustomerSeqId','PolicyCount']
select_data3=clean_header(select_data3,select_data3.schema.names,select_columns3_new,)

report1=select_data1.groupBy('H_ID').count().toPandas().sort_values(by="count",ascending=False).reset_index(drop=True)
report2=select_data2.groupBy('customerseqid').count().toPandas().sort_values(by="count",ascending=False).reset_index(drop=True)
report2=select_data2.groupBy('customerseqid').count()
report3=report2.join(select_data3,report2.customerseqid==select_data3.CustomerSeqId,how="outer")
report3=report3.toPandas()
output_loc2=r"D:\Data\NTUC\output\report2.csv"
report2.to_csv(output_loc2,index=False)
output_loc3=r"D:\Data\NTUC\output\report3.csv"
report3.to_csv(output_loc3,index=False)
select_columns4=['H_ID','Total_Policies']
select_columns5=['H_ID','customerseqid']
select_columns6=['customerseqid','policyseqid']
select_data4=household_data.select(select_columns4)
select_data5=customer_view_data.select(select_columns5)
select_data6=transaction_data.select(select_columns6)
select_data7=select_data5.join(select_data6,on='customerseqid',how="left")
select_data7=select_data7.na.drop(subset=["policyseqid"])
select_data4_clean_header=['H_ID1','Total_Policies']
select_data4=clean_header(select_data4,select_data4.schema.names,select_data4_clean_header)
report4=select_data5.groupBy("H_ID").count().toPandas().sort_values(by="count",ascending=False).reset_index(drop=True)
output_loc4=r"D:\Data\NTUC\output\report4.csv"
report4.to_csv(output_loc4,index=False)
report5=select_data5.groupBy("H_ID").sum("PolicyCount").toPandas().sort_values(by="sum(PolicyCount)",ascending=False).reset_index(drop=True)
output_loc5=r"D:\Data\NTUC\output\report5.csv"
report5.to_csv(output_loc5,index=False)
report4=select_data5.groupBy("H_ID").count()
report4_new_ocl=["H_ID","count(PolicySeqID)"]
report5=select_data5.groupBy("H_ID").sum("PolicyCount")
report6=report4.join(report5,on="H_ID",how="inner").toPandas()
output_loc6=r"D:\Data\NTUC\output\report6.csv"
report6.to_csv(output_loc6,index=False)
report6=report4.join(report5,on="H_ID",how="inner")
report7=select_data4.join(report6,select_data4.H_ID1==report5.H_ID,how="outer").toPandas()
output_loc7=r"D:\Data\NTUC\output\report7.csv"
report7.to_csv(output_loc7,index=False)
report8=select_data7.groupBy("H_ID").count()
report9=select_data4.join(report8,select_data4.H_ID1==report8.H_ID,how="outer").toPandas()
output_loc9=r"D:\Data\NTUC\output\report9.csv"
report9.to_csv(output_loc9,index=False)



"""
check on household id
"""
H1_list=household_data.select("H_ID").values.tolist()
H2_df=merge_data.select("H_ID").distinct()

H1_list = set(list(household_data.select("H_ID").toPandas()['H_ID']))
H2_list = set(list(H2_df.toPandas()['H_ID']))
H3_list=set(list(customer_view_data.select("H_ID").toPandas()['H_ID']))
difference=list(set(H1_list).symmetric_difference(set(H2_list)))
len(difference)
output_loc=r"D:\Data\NTUC\output\difference.csv"
pd.DataFrame(difference).to_csv(output_loc,index=False)
difference=list(set(H1_list).symmetric_difference(set(H2_list)))
difference=list(set(H3_list).symmetric_difference(set(H1_list)))

"""
check on Customerid
"""
C1=set(list(transaction_data.select('customerseqid').distinct().toPandas()['customerseqid']))
C2=set(list(customer_data.select('customerseqid').distinct().toPandas()['customerseqid']))
difference2=list(C1-C2)
output_loc2=r"D:\Data\NTUC\output\difference2.csv"
pd.DataFrame(difference2).to_csv(output_loc2,index=False)
difference2_df=pd.DataFrame(difference2,columns=["customerseqid"])
sp_difference2_df = sqlContext.createDataFrame(difference2_df)
difference_transaction=sp_difference2_df.join(select_data6,on="customerseqid",how="left")
output_loc3=r"D:\Data\NTUC\output\difference3.csv"
difference_transaction.toPandas().to_csv(output_loc3,index=False)
output_loc4=r"D:\Data\NTUC\output\difference4.csv"
difference_transaction.groupBy("customerseqid").count().toPandas().to_csv(output_loc4,index=False)
C3=set(list(customer_view_data.select('customerseqid').distinct().toPandas()['customerseqid']))
difference3=C3-C2
len(difference3)
output_loc5=r"D:\Data\NTUC\output\difference5.csv"
pd.DataFrame(list(difference3)).to_csv(output_loc5,index=False)
difference4=C2-C3
difference5=C2-C1





sqlDF = spark.sql()




#Logistic Regression
lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
lrModel = lr.fit(left_join)
# Print the coefficients and intercept for logistic regression
print("Coefficients: " + str(lrModel.coefficients))
print("Intercept: " + str(lrModel.intercept))
# Extract the summary from the returned LogisticRegressionModel
trainingSummary = lrModel.summary
# Obtain the objective per iteration
objectiveHistory = trainingSummary.objectiveHistory
print("objectiveHistory:")
for objective in objectiveHistory:
    print(objective)

# Obtain the receiver-operating characteristic as a dataframe and areaUnderROC.
trainingSummary.roc.show()
print("areaUnderROC: " + str(trainingSummary.areaUnderROC))

# Set the model threshold to maximize F-Measure
fMeasure = trainingSummary.fMeasureByThreshold
maxFMeasure = fMeasure.groupBy().max('F-Measure').select('max(F-Measure)').head()
bestThreshold = fMeasure.where(fMeasure['F-Measure'] == maxFMeasure['max(F-Measure)']) \
    .select('threshold').head()['threshold']
lr.setThreshold(bestThreshold)



# We can also use the multinomial family for binary classification
mlr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, family="multinomial")

# Fit the model
mlrModel = mlr.fit(left_join)

# Print the coefficients and intercepts for logistic regression with multinomial family
print("Multinomial coefficients: " + str(mlrModel.coefficientMatrix))
print("Multinomial intercepts: " + str(mlrModel.interceptVector))


# Index labels, adding metadata to the label column.
# Fit on whole dataset to include all labels in index.
labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(left_join)





