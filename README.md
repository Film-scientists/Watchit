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
## Description of modules and functions
script.py is module which runs whole program. Other modules are contained in package 'files'.

auth.py contains class Authenticator, User and AuthException. They handle with user's registration and loginning. Start.py handles interaction with user on the beginning of the program. Function ask_ratings() asks for user's favourite genres and function ask_ratings() asks ratings for films. main() function of start.py unites all other functions and returns dataframe with user's ratings. 

neighbour.py is a module, where recommendation algorithm based on finding nearest neighbours is implemented. 

matrix.py is a module, where recommendation algorithm based on matrix factorization is implemented. 


recommendation_engine.py is a module which unites our two recommendations algorithms - searching for nearest neighbours and matrix factorization. Function load() gets all needed data, function quintessential() combines results of two recommendation algorithms in certain proportion and return recommnedations. Function core() unites all these processes and prints recommendations. 

film_system.py containes class FilmSystem, which ties all modules together. Methods login(self) and register(self) use classes from auth.py to register and log in user. Method get(self) uses function core() from recommendation_engine.py to get, print recommendations and save them to the file. Method main(self) organizes interaction with user.

## Credits
information will be available later
