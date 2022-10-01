# Son-of-the-creator


# PostgreSQL with Fastapi CRUD APPLICATION

This is a simple CRUD application built using PostgreSQL and FastAPI. 

## Running the server


Set your [URI connection string] as a parameter in `.env`. Make sure you replace the username and password placeholders with your own credentials.


Install the required dependencies:

```
python -m pip install -r requirements.txt
```

Start the server:
```
python -m uvicorn main:app --reload
```
In this section I've used ORM by putting a code that will look in the database and check if there is a certain table need for a specific model and there is no table it automatically creates the table, so will nolonger be creating the table in the pgAdmin the code will now be doing it for use.

I've also created the database.py , models.py models 
Intsall the required dependencies:

```
python -m pip install -r requirements.txt

```

Start the server:

```
python -m uvicorn main:app --reload

```
In this section l've changed the codes from SQL to traditonal python code by using ORM which l introduced in the previous task earlier which is a layer of abstraction that sits between the database and us.

l also introdued the schemas module or sometime called the pydantic model that is responsible for defining the structure of a request and response.

This model ensures that when a user wants to create a post the request will only go through if it has the 'title' , content and all other requiremnents in the body.

I also stored all my models in the folder Packages which changes the way to run the server now


Start the server:

```
python -m uvicorn Packages.main:app --reload

```
ln this section I modified the module models.py with adding the Users class that will automatically create a table for users in the database and also created the module utils.py that will handle the encryption of passwords in the database once a user account has been created.

In this section I created the module auth.py that will authenticated the uses when they Login their accountsand l've also creater the File routers which contains auth, post and user.py 

ln this section i created Jtw token that will help to increase security in our API for our users as they Login.

In this section l've created the user authenticator that will only allow user to create, read, update and delet once they have logged in.  

I established the relationship  between the tables in the database which are books and users in a way that i can assign a particular post to its user, 'showing who posted the post'.
Now in this section one can only delete a post if he/she is the ower of the post that they may want to delete.

In this section clean some of my cords mainly in the main.py module and i also edited the get_post router making it possible for users to be able to search for individual post and also skip some post if they do want them.

In this section i created the .env file that holds all the environment variables 