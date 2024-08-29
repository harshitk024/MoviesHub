from django.shortcuts import render , HttpResponseRedirect
import pandas as pd 
import pickle 
import requests 

# importing the dataset and model
movies_dict = pickle.load(open("movies_dict.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
df = pd.DataFrame(movies_dict)

# function for fetching the movies poster

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7a33e1786754d93b478eacaa3c6435a3&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Fuction for recommending movies 


def recommend_movies(movie):
    index = df[df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = df.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# Create your views here.

def index(request):
    return render(request,"main/index.html")

# Recommend View
def  recommend(request):

    message = False

    if (request.method == "POST"): 
           name = request.POST.get("search")
           id = df[df['title'] == name]['id']
           
           if(len(id) == 0):
                message = "Sorry! , This movie is not available"
                return render(request,"main/index.html",{"message" : message})
           else:
                url = f"https://api.themoviedb.org/3/movie/{int(id)}?api_key=7a33e1786754d93b478eacaa3c6435a3"
                req = requests.get(url)
                req = req.json()

                poster_path = req['poster_path']
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                
                genres = []
                for ele in req['genres']:
                     genres.append(ele['name'])


                cast = requests.get(f"https://api.themoviedb.org/3/movie/{int(id)}/credits?api_key=7a33e1786754d93b478eacaa3c6435a3")
                cast = cast.json()

                for i in cast['crew']:
                     if i['job'] == "Director" :
                         director = i['name']

                     
                return render(request,"main/movie.html" , {'movie_id' : id.values[0] , "image" :full_path,"title" : req["title"],
                                               "overview" : req['overview'] , "genres" : genres , "rating" : format(req['vote_average'],".2f"), "director" : director , "recommended_movies_img" : recommend_movies(req['title'])[1]})




    return render(request,"main/index.html")