import json

# Codio movie Project - Phase 2 - Json
def get_movies():
    try:
        with open("data.json", "r") as file:
            movies = json.load(file)
        return movies
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_movies(movies):
    try:
        with open ("data.json", "w") as file:
            json.dump(movies, file, indent = 2)
    except FileNotFoundError:
        return "Error: The file 'data.json' could not be found"
    except TypeError:
        return "Error: The format is incorrect (movies should be a dictionary)"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def add_movie(title, year, rating):
    """ add movies to the movie database"""
    try:
        movies = get_movies()
        if title in movies:
            return f"The movie '{title}' already exists in the database"
        movies[title] = {"year": year, "rating": rating}
        save_movies(movies)
    except Exception as e:
        return f"An error occurred while adding the movie: {e}"


def delete_movie(title):
    """ delete movies from the movie database"""

    movies = get_movies()

    if title in movies:
        del movies[title]
        save_movies(movies)
        return None
    else:
        return f"Error: The movie '{title}' was not found in the database"


def update_movie(title, rating):
    """Update the rating of a specified movie in the database"""
    movies = get_movies()

    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)
        return None
    else:
        return f"Error: The movie '{title}' was not found in the database"

# Fallback function for substring based matching
def search_movies(search_title):
    movies = get_movies()
    found_movies = []
    for title, movie_data in movies.items():
        if search_title.lower() in title.lower():
            found_movies.append((title, movie_data["year"], movie_data["rating"]))

    if found_movies:
        return found_movies
    else:
        return None


def sorted_by_rating(order):
    """Sort movies by rating in ascending or descending order"""
    movies = get_movies()

    reverse = (order == "2")

    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=reverse)
    return [(title, movie_data["year"], movie_data["rating"]) for title, movie_data in sorted_movies]


def get_movie_ratings():
    """Generate and display a histogram of movie ratings"""
    movies = get_movies()
    return [movie_data["rating"] for movie_data in movies.values()]


def sorted_by_year(order):
    """Display all movies sorted by the year of release,
        sorted by ascending or descending order"""
    movies = get_movies()

    if order == "1":
        movies_years = sorted(movies.items(), key=lambda item: item[1]["year"])
    elif order == "2":
        movies_years = sorted(movies.items(), key=lambda item: item[1]["year"], reverse=True)
    else:
        return "Invalid input. Please enter '1' or '2'"

    return [(title, movie_data["year"], movie_data["rating"]) for title, movie_data in movies_years]





