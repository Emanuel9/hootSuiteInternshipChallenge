# hootSuiteInternshipChallenge

I. Summary

I know that the initial problem implies that first of all, I should bring using Wikipedia API all the informations regarding births, deaths, events and holidays_and_observances
for all the days of an year in my mongo database, however I was thinking about another solution that I've implemented in fetch_wikipedia_data.py file and argumented in this file. 

If this solution is not ok, although solves the problem, I will change and store only once every single data related to all days of the year.


II. This is my idea:

I was thinking about not storing everything from start, maybe there are informations that there are not an interesting source for users, so they'll never request informations about
that day. Why should I use memory without any purpouse? So I won't, for every request the user made, I'll proceed as follows:



1 - The following request http://127.0.0.1:5000/?year=2005&day=November_3&category=births or any other request with that format will be made by user.

2 - I'll check if I already have data in my mongo database in order to satisfy user's request and response with requested data.

3 - In case I don't have in my mongo database a response for that request, well I'll get what I am searching for using wikipedia API, 
then I'll store the data I borught through API in my mongo database and lastly, I'll respond to user with my response for his request. 
Next time the request will be made, I'll respond immediately with my data stored in database.



III. Instructions of using this python script


Database name ---  hootsuite:

Choose database(if it is not created, mongo will create this) --- use hootsuite

I'll use a collection in order to store my data for user, so I'll create pages collection --- db.createCollection("pages")

Run the applacation that uses flask web framework that offers me a server : python fetch_wikipedia_data.py



IV. Code steps


1 -  I'll get from user's request year, day and category request parameters
2 -  I'll setup a connection to my previously hootsuite created database
3 -  I will implement my idea and hope that everything is fine :)







