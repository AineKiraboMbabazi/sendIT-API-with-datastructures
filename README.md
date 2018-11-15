[![Build Status](https://travis-ci.com/AineKiraboMbabazi/sendIT-API-with-datastructures.svg?branch=develop)](https://travis-ci.com/AineKiraboMbabazi/sendIT-API-with-datastructures)
[![Maintainability](https://api.codeclimate.com/v1/badges/2e87bcc8b79832fddceb/maintainability)](https://codeclimate.com/github/AineKiraboMbabazi/sendIT-API-with-datastructures/maintainability)

[![Coverage Status](https://coveralls.io/repos/github/AineKiraboMbabazi/sendIT-API-with-datastructures/badge.svg?branch=develop)](https://coveralls.io/github/AineKiraboMbabazi/sendIT-API-with-datastructures?branch=develop)


# sendIT-API-with-datastructures
# sendIT-
SendIT is a courier service provider that enable users to create parcel delivery orders, view delivery parcel delivery order history, Edit parcel delivery order, cancel parcel delivery order, view details of a particular parcel delivery order and also provider a platform for the administrator to edit the delivery status of an order and to set the current location of the parcel

# Getting started #
create a directory on your computer by doing the following 
- Open the terminal, for linux
```
 Ctrl+Alt+ T
 ```
 - Create a directory for the project by typing the following in your terminal
 ```
 mkdir projectname
 ```
 - Change into the directory created by using the following command
 ```cd projectname
 ```
## Clone the repository
After creating the directory, the next step is to clone this project by using the following command
```
$ git clone (https://github.com/AineKiraboMbabazi/sendIT-API-with-datastructures.git
$ cd sendIT-API-with-datastructures-
```

## Preprequisites ##
make sure that you have python3 and postman installed on your computer
```
snap install postman
```

# Running the project #
To run this project, 
- Navigate to the directory where the project was cloned.
run 
```
    python3 run.py
```
-Copy the link from the terminal and paste it in postman. This should load the index page
- Create a user by appending, 

```
/api/v1/users
```
at the end of the url and change the method to post
In the post body add a dictionary with the following fields
```
{
	"email":" your@mail.com",
	"password":"anything "
	
}
```
- Use the same url to get all users by changing the method to
```
 GET
```
- To get all parcels created by a particular user, append
```
/api/v1/users/1/parcels
```
- Create a parcel by appending, 

```
/api/v1/parcels
```
at the end of the url and change the method to POST
In the post body add a dictionary with the following fields
```
{
    "userId":1,
	"status":"intransit ",
	"pickup":"jinja",
	"destination":"entebbe"
    
}
```
- Use the same url to get all users by changing the method to
```
 GET
```
- To get particular parcel, append
```
/api/v1/parcels/1
```
- To cancel parcel,  change method to PUT and append
```
/api/v1/parcels/1
```
- To cancel delete,  change method to DELETE and append
```
/api/v1/parcels/1
```
# Built with #
* python
* REST

# Authors #
** Ainekirabo Mbabazi **


