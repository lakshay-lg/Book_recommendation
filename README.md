# BookMatch - Book Recommendation System

A web app that recommends books based on collaborative filtering. You give it a book you liked, and it finds similar titles based on what other readers enjoyed.

## How it works

The recommendation engine uses a pre-computed cosine similarity matrix built from user ratings. Behind the scenes, there's a pivot table of 706 books rated by 810 users. When you search for a book, the app looks up its similarity scores against every other book and returns the top 4 most similar ones.

The search is forgiving -- you don't need to type the full title. It tries to match in this order: exact title, case-insensitive match, prefix match, then substring match. There's also a live autocomplete dropdown that suggests titles as you type, so you can usually just pick from the list.

## Pages

**Home (/)** -- Shows the top 50 most popular books ranked by number of ratings and average score.

**Recommend (/recommend)** -- The search page. Type in a book title (or part of one), hit recommend, and get 4 similar books back. When no search has been made yet, it shows a handful of sample books to give you a starting point.

## Project structure

```
app.py                  Flask application with all routes
templates/
  index.html            Home page - top 50 popular books
  recommend.html        Search and recommendation page
books.pkl               Full book catalog (~271k entries)
popular.pkl             Top 50 popular books
pt.pkl                  User-book ratings pivot table (706 books x 810 users)
similarity.pkl          Pre-computed cosine similarity matrix (706 x 706)
requirements.txt        Python dependencies
```

## Setup

You'll need Python 3.9+ and the data files (the `.pkl` files). The data files aren't included in the repo due to size -- you'll need to generate them from the original dataset or get them separately.

Install dependencies:

```
pip install -r requirements.txt
```

Run the app:

```
python app.py
```

Then open `http://localhost:5000` in your browser.

For production, use gunicorn:

```
gunicorn app:app
```

## Dependencies

- Flask -- web framework
- pandas -- data handling
- numpy -- numerical operations
- scikit-learn -- used to build the similarity matrix (not needed at runtime, but listed for reproducibility)
- gunicorn -- production server

## Data

The underlying dataset contains book metadata (title, author, publisher, cover image URLs) and user ratings. The similarity matrix was built by:

1. Filtering for books with at least 50 ratings and users with at least 200 ratings
2. Creating a user-book pivot table
3. Computing pairwise cosine similarity between all books

The result is a 706x706 matrix where each cell tells you how similar two books are on a 0-to-1 scale.
