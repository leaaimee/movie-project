import movie_storage
from colorama import init, Fore, Style
init()
import datetime
import matplotlib.pyplot as plt
import random
from rapidfuzz import process
from rapidfuzz.fuzz import ratio

menu_color = Fore.CYAN
input_color = Fore.YELLOW
error_color = Fore.RED
success_color = Fore.BLUE
highlight_color = Fore.MAGENTA

def menu_choice(select):
    """Execute a menu option based on the user's selection"""

    menu_actions = {
        "0": exit_program,
        "1": list_movies,
        "2": add_movie_to_storage,
        "3": delete_movie,
        "4": update_movie,
        "5": stats,
        "6": random_movie,
        "7": search_movie,
        "8": sorted_by_rating,
        "9": sorted_by_year,
        "10": filter_movies,
        "11": db_histogram
    }

    action = menu_actions.get(select)
    if action:
        action()
        return True
    else:
        print(error_color + "Invalid choice. Please enter a number from 1 - 10" + Style.RESET_ALL)
        return True

def exit_program():
    """Exit the program."""
    print(success_color + "Bye!" + Style.RESET_ALL)
    return False


def list_movies():
    """Display all movies and their ratings in the database"""
    movies = movie_storage.get_movies()
    if not movies:
        print(error_color + "No movies found in the database." + Style.RESET_ALL)
        return

    movie_count = len(movies)
    print(success_color + f"\nOur database currently stores {movie_count} movies\n" + Style.RESET_ALL)

    for title, movie_data in movies.items():
        year = movie_data["year"]
        rating = movie_data["rating"]
        print(f"{title} ({year}): Rating: {rating:.1f}")


def add_movie_to_storage():
    """Add a new movie with a rating to the database"""
    while True:
        title = input(input_color + "Please enter the title of the new movie you'd like to add to the database: " + Style.RESET_ALL)
        if not title.strip():
            print(error_color + "Please enter a valid title" + Style.RESET_ALL)
        else:
            break
    while True:
        try:
            year = int(input(input_color + "Enter the year of the release  " + Style.RESET_ALL))
            current_year = datetime.datetime.now().year
            if 1900 <= year <= current_year:
                break
            else:
                print(error_color + f"Please enter the correct "
                                    f"year of release fom 1900 to {current_year} in a 4-digit format " + Style.RESET_ALL)
        except ValueError as e:
            print(error_color + f"Error: {e}. Please enter a valid integer" + Style.RESET_ALL)

    while True:
        try:
            rating = float(input(input_color + "Did you like this movie? Please leave a rating from 1 - 10 " + Style.RESET_ALL))
            if 1 <= rating <= 10:
                break
            else:
                print(error_color + "Rating must be between 1 and 10" + Style.RESET_ALL)
        except ValueError as e:
            print(error_color + f"Error {e}. Please enter a number between 1 and 10" + Style.RESET_ALL)

    error_message = movie_storage.add_movie(title, year, rating)
    if error_message:
        print(error_color + error_message + Style.RESET_ALL)
    else:
        print(success_color + f"The movie {title} has been added successfully" + Style.RESET_ALL)


def delete_movie():
    """Remove a specified movie from the database"""
    title = input(input_color + "Which movie would you like to remove from the database" + Style.RESET_ALL)

    error_message = movie_storage.delete_movie(title)
    if error_message:
        print(error_color + error_message + Style.RESET_ALL)
    else:
        print(success_color + f"The movie {title} has been removed successfully" + Style.RESET_ALL)


def update_movie():
    """Update the rating of a specified movie in the database"""
    while True:
        title = input(input_color + "Which movie rating should be updated " + Style.RESET_ALL)
        if not title.strip():
            print(error_color + "Please enter a valid title" + Style.RESET_ALL)
        else:
            break

    movies = movie_storage.get_movies()
    movie_titles = {t.lower(): t for t in movies.keys()}

    if title.lower() in movie_titles:
        original_title = movie_titles[title.lower()]
        while True:
            try:
                rating = float(input(input_color + "Please update the rating (1-10): " + Style.RESET_ALL))
                if 1 <= rating <= 10:
                    break
                else:
                    print(error_color + "Rating must be between 1 and 10" + Style.RESET_ALL)
            except ValueError as e:
                print(error_color + f"Error: {e} Please enter a number between 1 and 10." + Style.RESET_ALL)

        try:
            movie_storage.update_movie(original_title, rating)
            print(success_color + f"The rating of the movie {title} has been updated to {rating}" + Style.RESET_ALL)
        except Exception as e:
            print(error_color + f"Error updating movie: {e}" + Style.RESET_ALL)
    else:
        print(error_color + f"The movie {title} is not in the database" + Style.RESET_ALL)


def stats():
    """Display statistics about the movie ratings,
       including average, median, best, and worst ratings"""
    movies = movie_storage.get_movies()
    print(highlight_color + f"\nMovie Statistics\n" + Style.RESET_ALL)

    # Calculate average rating
    average_rating = sum(movie_data["rating"] for movie_data in movies.values()) / len(movies)
    print(highlight_color + f"The average rating of movies in this database is: {average_rating:.1f}" + Style.RESET_ALL)

    # Calculate median rating
    ratings = [movie_data["rating"] for movie_data in movies.values()]
    ratings.sort()
    n = len(ratings)
    if n % 2 == 0:
        median = (ratings[n // 2 - 1] + ratings[n // 2]) / 2
    else:
        median = ratings[n // 2]

    median = round(median, 1)
    print(highlight_color + f"The median rating is: {median}" + Style.RESET_ALL)

    # provides the best movie(s)
    best_rating = 0
    best_movie = []
    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        if rating > best_rating:
            best_rating = rating
            best_movie = [title]
        elif rating == best_rating:
            best_movie.append(title)
    print(highlight_color + f"The best movie(s) in our database with a rating of {best_rating}: " + ", ".join(best_movie) + Style.RESET_ALL)

    # provides the worst movie(s)
    worst_rating = 10
    worst_movie = []
    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        if rating < worst_rating:
            worst_rating = rating
            worst_movie = [title]
        elif rating == worst_rating:
            worst_movie.append(title)
    print(highlight_color + f"The worst movie(s) our database with a rating of {worst_rating}: " + ", ".join(worst_movie) + Style.RESET_ALL)


def random_movie():
    """Choose a random movie from the database and display its title and rating."""
    movies = movie_storage.get_movies()

    chosen_movie = random.choice(list(movies.keys()))
    rating = movies[chosen_movie]["rating"]
    year = movies[chosen_movie]["year"]
    print(highlight_color + f"Your randomly chosen movie is: " + Style.RESET_ALL)
    print(highlight_color + f"'{chosen_movie}'({year}) with the rating of: {rating }" + Style.RESET_ALL)


def search_movie():
    """Search for a movie by title in the database
    and display its title and rating if found."""
    search_title = input(input_color + "Which movie you are looking for? " + Style.RESET_ALL).lower()

    found_movies = movie_storage.search_movies(search_title)

    if found_movies:
        for title, year, rating in found_movies:
            print(highlight_color + f"The movie {title} fom {year} is available at the database and has a rating of: {rating}" + Style.RESET_ALL)
        return

    movies = movie_storage.get_movies()
    if not movies:
        print(error_color + "The database is currently empty. Please add some movies first!" + Style.RESET_ALL)
        return

    # The fuzzy buster
    print(error_color + f"No exact matches for '{search_title}'. Searching for similar movies..." + Style.RESET_ALL)
    matches = process.extract(search_title, list(movies.keys()), limit=3, scorer=ratio)
    threshold = 50 if len(search_title) > 5 else 60
    similar_movies = [match for match in matches if match[1] >= threshold]

    if similar_movies:
        print(error_color + "Did you mean:" + Style.RESET_ALL)
        for match, score, _ in similar_movies:
            movie = movies[match]
            print(f"- {match} ({movie['year']}): Rating {movie['rating']:.1f}")
    else:
        print(error_color + f"No similar movies found for '{search_title}'." + Style.RESET_ALL)


def sorted_by_rating():
    """Display all movies sorted by their rating in ascending or descending order"""
    print(highlight_color + f"\nMovies ranked by rating:\n" + Style.RESET_ALL)

    while True:
        try:
            order = input(highlight_color + "Press '1' for ascending order or '2' for descending order: " + Style.RESET_ALL)
            if order not in ['1', '2']:
                raise ValueError(error_color + "Invalid input. Please enter '1' or '2'" + Style.RESET_ALL)
            break
        except ValueError as e:
            print(error_color + f"Wrong input. Error message: {e}" + Style.RESET_ALL)

    sorted_movies = movie_storage.sorted_by_rating(order)

    for title, year, rating in sorted_movies:
        print(f"{title} ({year}) with a rating of: {rating}")


def sorted_by_year():
    """Display all movies sorted by the year of release,
        sorted by ascending or descending order"""
    print(highlight_color + f"\nMovies ranked by year of release : \n" + Style.RESET_ALL)

    while True:
        try:
            order = input(highlight_color + "Press '1' for ascending order or '2' for descending order" + Style.RESET_ALL)
            if order not in ['1', '2']:
                raise ValueError(error_color + "Invalid input. Please enter '1' or '2'" + Style.RESET_ALL)
            break
        except ValueError as e:
            print(error_color + f"Wrong input. Error message {e}" + Style.RESET_ALL)

    movies_years = movie_storage.sorted_by_year(order)

    for title, year, rating in movies_years:
        print(f"{year} - {title} with a rating of: {rating} ")


def filter_movies():
    """Filter movies by minimum rating, start year, and end year"""
    try:
        min_rating_input = input(input_color + "Enter minimum rating (leave blank for no minimum rating): " + Style.RESET_ALL)
        start_year_input = input(input_color + "Enter start year (leave blank for no start year): " + Style.RESET_ALL)
        end_year_input = input(input_color + "Enter end year (leave blank for no end year): " + Style.RESET_ALL)

        min_rating = float(min_rating_input) if min_rating_input else None
        start_year = int(start_year_input) if start_year_input else None
        end_year = int(end_year_input) if end_year_input else None

        movies = movie_storage.get_movies()
        if not movies:
            print(error_color + "The database is currently empty. Please add some movies first!" + Style.RESET_ALL)
            return

        filtered_movies = []
        for title, movie_data in movies.items():
            rating = movie_data["rating"]
            year = movie_data["year"]

            if (min_rating is not None and rating < min_rating):
                continue
            if (start_year is not None and year < start_year):
                continue
            if (end_year is not None and year > end_year):
                continue

            filtered_movies.append((title, year, rating))

        if filtered_movies:
            print(highlight_color + "Filtered Movies:" + Style.RESET_ALL)
            for title, year, rating in filtered_movies:
                print(f"- {title} ({year}): {rating:.1f}")
        else:
            print(error_color + "No movies match the given criteria" + Style.RESET_ALL)

    except ValueError as e:
        print(error_color + f"Invalid input: {e}. Please enter valid numbers for rating and years" + Style.RESET_ALL)


def db_histogram():
    """Generate and display a histogram of movie ratings"""
    ratings = movie_storage.get_movie_ratings()
    plt.hist(ratings, bins=10, color='aquamarine', edgecolor='black', rwidth=0.9)
    plt.title('Movie Ratings Histogram')
    plt.xlabel('Rating')
    plt.ylabel('Number of Movies')
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()
    plt.close()


def main():
    """Display the user menu"""
    while True:

        print(menu_color + "\n***** Welcome to your favorite movie database 📽 *****\n" + Style.RESET_ALL)
        print(menu_color + "Menu: " + Style.RESET_ALL)
        print(menu_color + "0.   Exit" + Style.RESET_ALL)
        print(menu_color + "1.   List all movies along with their ranking" + Style.RESET_ALL)
        print(menu_color + "2.   Adding a movie" + Style.RESET_ALL)
        print(menu_color + "3.   Deleting a movie" + Style.RESET_ALL)
        print(menu_color + "4.   Update the rating" + Style.RESET_ALL)
        print(menu_color + "5.   Statistics" + Style.RESET_ALL)
        print(menu_color + "6.   Chose a random movie" + Style.RESET_ALL)
        print(menu_color + "7.   Search for movies" + Style.RESET_ALL)
        print(menu_color + "8.   Display movies by rating" + Style.RESET_ALL)
        print(menu_color + "9.   Display movies by year" + Style.RESET_ALL)
        print(menu_color + "10.  Filter movies by rating and year" + Style.RESET_ALL)
        print(menu_color + "11.  Create Rating Histogram" + Style.RESET_ALL)
        print("\n_____________________________\n")

        select = input(menu_color + "Enter your choice: " + Style.RESET_ALL)

        if not menu_choice(select):
            break

if __name__ == "__main__":
    main()
