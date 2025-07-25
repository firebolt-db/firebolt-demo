
DROP TABLE IF EXISTS rankings;
DROP TABLE IF EXISTS uservisits;
DROP TABLE IF EXISTS ipaddresses;
DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS searchwords;   

CREATE TABLE rankings (
  pageurl VARCHAR(256) NOT NULL,
  pagerank INT,
   avgduration INT
 )
 DISTSTYLE KEY
 DISTKEY (pageurl)
 SORTKEY (pageurl);
 
 CREATE TABLE uservisits (
   sourceip VARCHAR(256) NOT NULL,
   destinationurl VARCHAR(256) NOT NULL,
   visitdate DATE NOT NULL,
   adrevenue FLOAT NOT NULL,
   useragent VARCHAR(256) NOT NULL,
   countrycode VARCHAR(3) NOT NULL,
   languagecode VARCHAR(10) NOT NULL,
   searchword VARCHAR(256) NOT NULL,
   duration INT NOT NULL
 )
 DISTSTYLE KEY
 DISTKEY (visitdate)
 SORTKEY (visitdate, destinationurl, sourceip);
 
 CREATE TABLE ipaddresses (
   ip VARCHAR(256) NOT NULL,
   autonomoussystem INT NOT NULL,
   asname VARCHAR(256) NOT NULL
 )
 DISTSTYLE ALL;
 
 CREATE TABLE agents (
   id INT NOT NULL,
   agentname VARCHAR(256) NOT NULL,
   operatingsystem VARCHAR(256) NOT NULL,
   devicearch VARCHAR(256) NOT NULL,
   browser VARCHAR(256) NOT NULL
 )
 DISTSTYLE ALL;
 
 CREATE TABLE searchwords (
   word VARCHAR(256) NOT NULL,
   word_hash BIGINT NOT NULL,
   word_id BIGINT NOT NULL,
   firstseen DATE NOT NULL,
   is_topic BOOLEAN NOT NULL
 )
 DISTSTYLE ALL;
 
 
 -- Load data into rankings
 COPY rankings
 FROM 's3://firebolt-benchmarks-requester-pays-us-east-1/firenewt/1tb/rankings/'
 IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
 FORMAT AS PARQUET;
 
 -- Load data into uservisits
 COPY uservisits
 FROM 's3://firebolt-benchmarks-requester-pays-us-east-1/firenewt/1tb/uservisits/gz-parquet/'
 IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
 FORMAT AS PARQUET;
 
 -- Load data into agents
 COPY agents
 FROM 's3://firebolt-benchmarks-requester-pays-us-east-1/firenewt/1tb/dimensions/agents/'
 IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
 FORMAT AS PARQUET;
 
 -- Load data into ipaddresses
 COPY ipaddresses
 FROM 's3://firebolt-benchmarks-requester-pays-us-east-1/firenewt/1tb/dimensions/ipaddresses/'
 IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
 FORMAT AS PARQUET;
 
 -- Load data into searchwords
 COPY searchwords
 FROM 's3://firebolt-benchmarks-requester-pays-us-east-1/firenewt/1tb/dimensions/searchwords/'
 IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
 FORMAT AS PARQUET;