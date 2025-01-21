# Telaverge Assessment

Problem Statement -

Consider 2 replicas of a server among which the client request is 
distributed in round robin manner with time quantum taken as 1 
second. The client is repeatedly sending request to replicas. If
 some how the connection is dead the back up of the requests are 
 maintained in the server. Once the connection is regained the 
 request should start from the previous request served before the 
 connection termination.

Solution -

created a flask application ( [app.py](http://app.py) ) 

[app.py](http://app.py) description -

This is a simple application that accepts the counter and message from the client and display it on webpage. It also shows the specifies pod name which is currently serving the client requests.

Also this application is connected to database and stores the message received, counter and time stamp at which request is served.

Dockerfile

Now to create the image for the application Next I created Dockerfile ( It is a file that contains specifications about how to create the container, what dependencies are required to install. )

app-deployment.yaml

This file contains the specifications about application pods like how they should be created, managed and updated.

Information about how many replicas should run in kubernetes cluster.

app-service.yaml

This file contains the services we want to utilize for application.

Ex. - One of the service as per problem statement was to use LoadBalancing.

app-ingress.yaml

Example - 

Let’s say you have your restaurant in a mall.
But the mall has many stores ( services ) but you want to give map to your customers to come to your restaurant when they enter the mall. So Ingress.yaml provides a map to the traffic.

mysql-deployment.yaml

This file defines a deployment in Kubernetes to run and manage a mysql database container. It specifies the details of how the MySQL database should be set up, such as the image, environment variables, and the number of replicas.

How to setup -

1- Start minikube

2- ensure the image are available in minikube’s docker environment

3- create image inside the minikube environment

4- apploy the deployment and services

5- login to MySQL create table in counter_db database

6- open deployment by running ( minikube service flask-service )

7- send message to server ( start client )

8- stop client

9- see the database by loging into MySQL account.