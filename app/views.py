from django.shortcuts import render, HttpResponse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


# Create your views here.
CSV_FILE = "movie_dataset.csv"


def login(request):
    return render(request, 'login.html')


def home(request):
    now_time = dict()
    now_time['now_time'] = datetime.now()
    print("this is from home page method {}".format(now_time))
    return render(request, "welcome.html", {"name": now_time})


def recommended(request):
    try:
        print("we are inside movie recommendation module", request.GET['movie_name'], "request.get", request.GET.get("movie_name", None))
        try:
            df = pd.read_csv(CSV_FILE)
            print("read movie dataset@@@@@@@@@@@@", df.head(5))
        except Exception as e:
            print("oops got an exception while reading csv file {}".format(str(e)))
        # here we have to enter the movie name which we like
        movie_user_likes = request.GET['movie_name']
        movie_user_likes = movie_user_likes.capitalize()

        if movie_user_likes:
            features = ['keywords', 'cast', 'genres', 'director']

            for feature in features:
                df[feature] = df[feature].fillna('')
            df["combined_features"] = df.apply(combine_features, axis=1)
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(df["combined_features"])
            cosine_sim = cosine_similarity(count_matrix)

            movie_index = get_index_from_title(movie_user_likes)
            similar_movies = list(enumerate(cosine_sim[movie_index]))
            sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
            i = 0
            print("Top 5 similar movies to " + movie_user_likes + " are:\n")
            movie_res_data = []

            for element in sorted_similar_movies:
                movie_res_data.append(get_title_from_index(element[0]))
                i = i + 1
                if i >= 20:
                    break

            if movie_res_data:
                print("this is from recommeded method", movie_res_data, type(movie_res_data))
                return render(request, 'recommended.html', {"output": movie_res_data})
            else:
                return render(request, "error.html")
        else:
            return render(request, "error.html")
    except Exception as e:
        print(str(e))
        return HttpResponse("oops got an exception {}".format(str(e)))


def combine_features(row):
    try:
        return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
    except Exception as e:
        print("oops got an exception in combine features method {}".format(str(e)))


def get_title_from_index(index):
    try:
        df = pd.read_csv(CSV_FILE)
        return df[df.index == index]["title"].values[0]

    except Exception as e:
        print("oops we got an exception in get title from index method {}".format(str(e)))


def get_index_from_title(title):
    try:
        df = pd.read_csv(CSV_FILE)
        return df[df.title == title]["index"].values[0]
    except Exception as e:
        print("oops we got an exception in get index from title method {}".format(str(e)))
