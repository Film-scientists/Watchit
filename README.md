# WatchIt
## Description
"WatchIt" is a recommender system, which helps you to choose movies, that fit best to your prefernces. Start with choosing your
favourite categories of films. Then evaluate movies, that you have already seen. Taking to account your ratings, system picks up and 
proposes 10 films, that match your tastes. 
## Instalation
git clone ...
Run only script.py
## Usage example
First of all you need to register to our system. Then, you have 2 options:'get' - to get recommendations and 'see' - to see previous recomendations. ![](images/start.jpg)
Let's get some recommendations! At first you have to choose at least 3 your favourite genres. ![](images/genres.jpg)
Now we propose you to rate best films of these genres. Rate at least 20 films. ![](images/rating.jpg)
After you rate 20 films, you get recommendations! ![](images/rec.jpg)
## Data 
Our recommendation system is based on the dataset of users and their ratings from movielens.org. Program's input are 3 user's favourite genres and 20 ratings of films. The output is list of 20 recommended films. Recomendations are saved to the file, so user will be able to find them next time he runs the program. 
## System structure
script.py is module which runs whole program. Other modules are contained in package 'files'. auth.py contains class Authenticator, User and AuthException. They handle with user's registration and loginning. Start.py handles interaction with user on the beginning of the program. Function ask_ratings() asks for user's favourite genres and function ask_ratings() asks ratings for films. main() function of start.py unites all other functions and returns dataframe with user's ratings. 
## Credits
information will be available later
