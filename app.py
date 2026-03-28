from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Pre-compute the list of searchable book titles (from pivot table) and lowercase versions
book_titles = list(pt.index)
book_titles_lower = [t.lower() for t in book_titles]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/api/suggestions')
def suggestions():
    query = request.args.get('q', '').strip().lower()
    if len(query) < 1:
        return jsonify([])

    matches = []
    # Prioritize: prefix matches first, then substring matches
    prefix_matches = []
    substring_matches = []
    for i, title_lower in enumerate(book_titles_lower):
        if title_lower.startswith(query):
            prefix_matches.append(book_titles[i])
        elif query in title_lower:
            substring_matches.append(book_titles[i])

    matches = prefix_matches + substring_matches
    return jsonify(matches[:10])


def find_best_match(user_input):
    """Find the best matching book title using partial matching."""
    # Try exact match first
    exact = np.where(pt.index == user_input)[0]
    if len(exact) > 0:
        return exact[0]

    # Try case-insensitive exact match
    query_lower = user_input.lower()
    for i, title_lower in enumerate(book_titles_lower):
        if title_lower == query_lower:
            return i

    # Try prefix match (case-insensitive)
    for i, title_lower in enumerate(book_titles_lower):
        if title_lower.startswith(query_lower):
            return i

    # Try substring match (case-insensitive)
    for i, title_lower in enumerate(book_titles_lower):
        if query_lower in title_lower:
            return i

    return None


@app.route('/recommend_books', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        user_input = request.args.get('book', '').strip()
    else:
        user_input = request.form.get('user_input')
    match_index = find_best_match(user_input)

    if match_index is None:
        return render_template('recommend.html', data=[], error="No matching book found. Try a different search term.")

    similar_items = sorted(list(enumerate(similarity[match_index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    matched_title = book_titles[match_index]
    return render_template('recommend.html', data=data, matched_title=matched_title)

if __name__ == '__main__':
    app.run(debug=True)