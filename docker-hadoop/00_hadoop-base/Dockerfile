FROM debian:9

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

ENV HADOOP_HOME /opt/hadoop
ENV HIVE_HOME /opt/hive
ENV SPARK_HOME /opt/spark
ENV FLUME_HOME /opt/flume

ENV HADOOP_MAPRED_HOME ${HADOOP_HOME}
ENV HADOOP_COMMON_HOME ${HADOOP_HOME}
ENV HADOOP_HDFS_HOME ${HADOOP_HOME}
ENV YARN_HOME ${HADOOP_HOME}
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop
ENV YARN_CONF_DIR ${HADOOP_HOME}/etc/hadoop

ENV PATH $PATH:$HADOOP_HOME/bin
ENV PATH $PATH:$HADOOP_HOME/sbin
ENV PATH $PATH:$HIVE_HOME/bin
ENV PATH $PATH:$SPARK_HOME/bin
ENV PATH $PATH:$FLUME_HOME/bin

#Install required packages/dependencies
RUN apt-get -y update &&\
    apt-get install -y openjdk-8-jdk wget net-tools netcat procps scala python python-pip unzip ||\ 
    (apt-get install -y --fix-missing && apt-get install -y openjdk-8-jdk wget net-tools netcat procps scala python python-pip unzip)

#Install Hadoop   
RUN cd /opt && wget https://archive.apache.org/dist/hadoop/core/hadoop-2.7.7/hadoop-2.7.7.tar.gz &&\
    tar xzf hadoop-2.7.7.tar.gz &&\
    rm hadoop-2.7.7.tar.gz &&\
    mv hadoop-2.7.7 hadoop

#Install Spark
RUN cd /opt &&\ 
    wget https://archive.apache.org/dist/spark/spark-2.2.3/spark-2.2.3-bin-without-hadoop.tgz &&\
    tar xzf spark-2.2.3-bin-without-hadoop.tgz &&\
    rm spark-2.2.3-bin-without-hadoop.tgz &&\
    mv spark-2.2.3-bin-without-hadoop spark &&\
    cd /opt/spark/jars && wget https://repo1.maven.org/maven2/org/apache/spark/spark-hive_2.11/2.2.3/spark-hive_2.11-2.2.3.jar &&\
    pip install hdfs

#Install Hive
RUN cd /opt && wget https://archive.apache.org/dist/hive/hive-2.3.9/apache-hive-2.3.9-bin.tar.gz &&\
    tar xzf apache-hive-2.3.9-bin.tar.gz &&\
    rm apache-hive-2.3.9-bin.tar.gz &&\
    mv apache-hive-2.3.9-bin hive &&\
    wget https://jdbc.postgresql.org/download/postgresql-9.4.1212.jar -O ${HIVE_HOME}/lib/postgresql-jdbc.jar &&\
    cd ${HIVE_HOME}/lib &&\
    cp ${SPARK_HOME}/jars/scala-library*.jar . &&\
    cp ${SPARK_HOME}/jars/spark-core*.jar . &&\
    cp ${SPARK_HOME}/jars/spark-network-common*.jar . &&\
    cp ${SPARK_HOME}/jars/spark-unsafe*.jar .

#Install Flume
RUN cd /opt && wget https://archive.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz &&\
    tar xzf apache-flume-1.9.0-bin.tar.gz &&\
    rm apache-flume-1.9.0-bin.tar.gz &&\
    mv apache-flume-1.9.0-bin flume

#Install Livy
RUN cd /opt && wget https://ftp.unicamp.br/pub/apache/incubator/livy/0.7.1-incubating/apache-livy-0.7.1-incubating-bin.zip &&\
    unzip apache-livy-0.7.1-incubating-bin.zip &&\
    rm apache-livy-0.7.1-incubating-bin.zip &&\
    mv apache-livy-0.7.1-incubating-bin livy

#Uninstall not required packages
RUN apt-get remove -y wget unzip &&\
    apt-get autoremove -y

COPY core-site.xml hdfs-site.xml mapred-site.xml yarn-site.xml ${HADOOP_HOME}/etc/hadoop/
COPY hive-site.xml spark-env.sh ${SPARK_HOME}/conf/
COPY hive-site.xml ${HIVE_HOME}/conf/
COPY wait.sh wait-namenode.sh wait-resourcemanager.sh /usr/local/bin/