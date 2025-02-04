
"""
This file is to prepare some generic code for NTUC data validation and manipulation
This file is generated by Ivy Yi on 20180817
"""

__author__ = 'Ivy Yi'
import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
os.environ['SPARK_HOME']=r"C:\Users\latize\spark\spark-2.3.1-bin-hadoop2.7"
sys.path.append(r"C:\Users\latize\spark\spark-2.3.1-bin-hadoop2.7\python")

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType
from functools import reduce
from pyspark.sql.functions import substring


conf = SparkConf().setMaster("local").setAppName("NTUC")
sc = SparkContext(conf = conf)
sqlContext=SQLContext(sc)

def read_file(path):
    df = sqlContext.read.csv(path,header=True)
    return (df)

def clean_header(data,oldColumns,newColumns):
    df = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)),
                data)
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
    categorical_output_loc = r"D:\Data\NTUC\Output\categorical_output_" + data_name + ".csv"
    descriptive_output_loc = r"D:\Data\NTUC\Output\desc_output_" + data_name + ".csv"
    for column in data.schema.names:
        graph_name=r"D:\Data\NTUC\Output\categorical_output_" + data_name + "_" + column + ".png"
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

abc_path=r"D:\Data\NTUC\abc_trial.csv"
abc_test=read_file(abc_path)
cust_path=r"D:\Data\NTUC\cust_trial.csv"
cust_test=read_file(cust_path)
home_path=r"D:\Data\NTUC\HomeRelation.csv"
home_test=read_file(home_path)
abc_clean_header=['H_ID','MembersCount', 'GI_active', 'LI_active', 'IS_active', 'MembersActive', 'holdingtag', 'HouseRelationConfidence', 'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence', 'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag', 'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']
abc_test=clean_header(abc_test,abc_test.schema.names,abc_clean_header)
#abc_float_col=["GI_active","LI_active","IS_active","HouseRelationCount","TodCount","YoungCount","TeenCount","GradCount","totalkids","Total_Policies"]
abc_int_col=["MembersCount","MembersActive","GI_active","LI_active","IS_active","HouseRelationCount","TodCount","YoungCount","TeenCount","GradCount","totalkids","Total_Policies"]
abc_test=change_to_int(abc_test,abc_int_col)
#abc_test=change_to_float(abc_test,abc_float_col)
data_exploration(abc_test,"abc_test")

cust_clean_header=['CustomerSeqID',
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
cust_test=clean_header(cust_test,cust_test.schema.names,cust_clean_header)
cust_int_col=["MembersSpouse","MembersChild","MembersOthers","Tod","Young","Grad","Teen","Adult","PolicyCount"]
cust_float_col=["AgePH","ReachScore10"]
cust_test=change_to_int(cust_test,cust_int_col)
cust_test=change_to_float(cust_test,cust_float_col)
data_exploration(cust_test,"cust_test")

home_test
home_clean_header=['customerIdnumber_1',
 'Relation',
 'Add_R',
 'RelationConfidence',
 'customerIdnumber_2',
 'type',
 'PHIS_R',
 'email_R',
 'Namematch',
 'H_ID']
home_test=clean_header(home_test,home_test.schema.names,home_clean_header)
data_exploration(home_test,"home_test")



agent_path=r"D:\Data\NTUC\raw data\agent.csv"
agent_data=read_file(agent_path)
customer_path=r"D:\Data\NTUC\raw data\customer.csv"
customer_data=read_file(customer_path)
household_path=r"D:\Data\NTUC\raw data\houseview.csv"
household_data=read_file(household_path)
product_path=r"D:\Data\NTUC\raw data\product.csv"
product_data=read_file(product_path)
agent_date_col=["agentdateappointed","agentdatejoined","agentdateleft","agentdateofbirth"]
agent_data=change_to_month(agent_data,agent_date_col)
data_exploration(agent_data,"agent_data")
customer_date_col=["dateofbirth"]
customer_data=change_to_month(customer_data,customer_date_col)
data_exploration(customer_data,"customer_data")

household_clean_header=['H_ID',
 'MembersCount',
 'GI_active',
 'LI_active',
 'IS_active',
 'MembersActive',
 'holdingtag',
 'HouseRelationConfidence',
 'HouseRelationTag',
 'HouseRelationCount',
 'HouseMMOConfidence',
 'HouseholdReachConfi',
 'TodCount',
 'YoungCount',
 'TeenCount',
 'GradCount',
 'Toddler_Flag',
 'Young_Flag',
 'Teen_Flag',
 'Grad_Flag',
 'Spouse_Flag',
 'totalkids',
 'Total_Policies',
 'Decision_maker']

household_int_col=["MembersCount",'GI_active','LI_active', 'IS_active', 'MembersActive',"HouseRelationCount",'TodCount', 'YoungCount', 'TeenCount', 'GradCount','totalkids', 'Total_Policies']
household_data=clean_header(household_data,household_data.schema.names,household_clean_header)
household_data=change_to_int(household_data,household_int_col)
data_exploration(household_data,"household_data")

product_date_col=["productstartdate","productenddate"]
product_data=change_to_month(product_data,product_date_col)
data_exploration(product_data,"product_data")

customer2_path=r"D:\Data\NTUC\raw data\customer2.csv"
customer_data2=read_file(customer2_path)
customer_date_col=["dateofbirth"]
customer_data2=change_to_month(customer_data2,customer_date_col)
data_exploration(customer_data2,"customer_data2")

