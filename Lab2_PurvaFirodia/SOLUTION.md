# Solution

## Description

This document provides an overview of the solution for the Hadoop MapReduce assignment. The program was executed on two different Dataproc clusters: one with 2 nodes and one with 4 nodes. The execution time and output results for both configurations are documented here.

## Overview of the Solution

The objective of this project was to modify the classic Hadoop WordCount example to count URLs instead. Specifically, we needed to:

- Map URLs from input text files (including those within href tags).
- Count the number of occurrences for each URL using MapReduce.
- Only output URLs that appear more than 5 times.

The solution consists of two key components:

- Mapper: Extracts URLs from the input and assigns each URL a count of 1.
- Reducer: Aggregates the counts for each URL and filters the output to include only those with more than 5 occurrences.

The program was run on a Google Dataproc cluster with 1 master node and both 2 and 4 worker nodes to compare the execution times.

## Required Software and Dependencies

The following software is required to run this solution on a Hadoop cluster:

- Hadoop: The code is designed to run on Hadoop version 3.2.1 (version may vary depending on the cluster configuration). Ensure you check the Hadoop version with hadoop version.
- Python 3.x: For running the Python mapper and reducer scripts.
- Google Dataproc: A managed Hadoop cluster for running the MapReduce job.
- Git

## Resources Used

- [Hadoop Documentation](https://hadoop.apache.org/docs/stable/)
- [Google Cloud Dataproc Documentation](https://cloud.google.com/dataproc/docs)

## Steps Used 

- Cloned the github repository.

- Created the input directory in HDFS

`hdfs dfs -mkdir -p /user/$(whoami)/input`

- Uploaded all input files to HDFS

`hdfs dfs -put .lab2-url-lister-firodiaPurva/input/* /user/$(whoami)/input/`

- Edited the Makefile 

```
USER=student-04-1d7a2c03b022

##
## Configure the Hadoop classpath for the GCP dataproc environment
##

HADOOP_CLASSPATH=$(shell hadoop classpath)

WordCount1.jar: WordCount1.java
	javac -classpath $(HADOOP_CLASSPATH) -d ./ WordCount1.java
	jar cf WordCount1.jar WordCount1*.class	
	-rm -f WordCount1*.class

prepare:
	-hdfs dfs -mkdir -p /user/$(USER)/input
	curl https://en.wikipedia.org/wiki/Apache_Hadoop > /tmp/input.txt
	-hdfs dfs -rm /user/$(USER)/input/file01
	hdfs dfs -put /tmp/input.txt /user/$(USER)/input/file01
	curl https://en.wikipedia.org/wiki/MapReduce > /tmp/input.txt
	-hdfs dfs -rm /user/$(USER)/input/file02
	hdfs dfs -put /tmp/input.txt /user/$(USER)/input/file02

filesystem:
	-hdfs dfs -mkdir -p /user/$(USER)

run: WordCount1.jar
	-hdfs dfs -rm -r /user/$(USER)/output
	hadoop jar WordCount1.jar WordCount1 /user/$(USER)/input /user/$(USER)/output

##
## You may need to change the path for this depending
## on your Hadoop / java setup
##
HADOOP_V=3.3.6
STREAM_JAR = /usr/lib/hadoop/hadoop-streaming-$(HADOOP_V).jar

stream:
	-hdfs dfs -rm -r /user/$(USER)/stream-output
	hadoop jar $(STREAM_JAR) \
	-mapper Mapper.py \
	-reducer Reducer.py \
	-file Mapper.py -file Reducer.py \
	-input /user/$(USER)/input -output /user/$(USER)/stream-output

urlcount:
	-rm -rf urlcount-output
	hadoop jar $(STREAM_JAR) \
	-mapper URLMapper.py \
	-reducer URLReducer.py \
	-file URLMapper.py -file URLReducer.py \
	-input /user/$(USER)/input -output /user/$(USER)/urlcount-output
```

#### In Makefile I have changed Hadoop and STREAM_JAR. I have also updated urlcount and stream targets. 

- Updated the Java alternatives as it was needed

`sudo update-alternatives --config java`

- Compiled and package the Java code

`javac -source 11 -target 11 -classpath $(hadoop classpath) -d ./ WordCount1.java`

`jar cf WordCount1.jar WordCount1*.class`

- Uploaded the input files to HDFS

`make prepare`

- Executing the Hadoop Job 

`make run`

- Executing URL count job 

`make urlcount`


## Execution Times

### 2-node Cluster

- Command: `time hadoop jar WordCount1.jar WordCount1 /user/student-04-1d7a2c03b022/input /user/student-04-1d7a2c03b022/output-2nodes`

- Time: 
  - Real: 0m0.335s
  - User: 0m0.277s
  - Sys: 0m0.082s

- **2-node Cluster Output:**


  ![2-node Cluster Output](https://github.com/cu-csci-4253-datacenter-fall-2024/lab2-url-lister-firodiaPurva/blob/master/Screenshots/W2.png)


### 4-node Cluster

- Command: `time hadoop jar WordCount1.jar WordCount1 /user/student-04-1d7a2c03b022/input /user/student-04-1d7a2c03b022/output-4nodes`

- Time: 
  - Real: 0m0.293s
  - User: 0m0.251s
  - Sys: 0m0.086s

- **4-node Cluster Output:**


  ![4-node Cluster Output](https://github.com/cu-csci-4253-datacenter-fall-2024/lab2-url-lister-firodiaPurva/blob/master/Screenshots/W4.png)


## Output Verification

### Expected Output

The expected output URLs appearing more than 5 times:

- /wiki/Doi_(identifier)    18
- /wiki/ISBN_(identifier)    18
- /wiki/MapReduce    7
- /wiki/S2CID_(identifier)    14
- mw-data:TemplateStyles:r1129693374    6
- mw-data:TemplateStyles:r1133582631    121
- mw-data:TemplateStyles:r886049734    12

### Output generated - 

- **Final Output:**


  ![Final Output](https://github.com/cu-csci-4253-datacenter-fall-2024/lab2-url-lister-firodiaPurva/blob/master/Screenshots/FinalOutput.png)

## Discussion

- **Java Combiner Impact:** 

In the classic WordCount implementation, a combiner is often used to reduce the amount of data transferred between the mapper and reducer by performing partial reductions at the mapper side. However, using a combiner in this application may lead to inaccurate results. Since we are filtering out URLs with counts greater than 5, an intermediate combining step could incorrectly reduce the total counts before they reach the reducer, leading to discrepancies in the final count output.
  
- **Execution Time Comparison:**

The job ran faster with 4 worker nodes, as expected, due to the increased computational resources. However, the improvement in speed was not linear, and the overhead of managing more workers may have contributed to a diminishing return.

## Surprising Outcomes: 

The increase in worker nodes did not double the speed, which suggests that the job's performance bottleneck may be in I/O or the shuffle/sort phase rather than pure computational power.

## Collaboration

This project was completed individually. I referred to the following resources:

- Google Dataproc documentation.

- Hadoop Streaming tutorial.

- Markdown Cheat Sheet


