from flask import Flask, render_template, request
import pickle 
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained models and data
pop_df = pickle.load(open('models/popular.pkl', 'rb'))
pt = pickle.load(open('models/pt.pkl', 'rb'))
book = pickle.load(open('models/book.pkl', 'rb'))
ss = pickle.load(open('models/similarity_score.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("indes.html",
                           book_name=list(pop_df['Book-Title'].values),
                           author=list(pop_df['Book-Author'].values),
                           image=list(pop_df['Image-URL-M'].values),
                           publisher=list(pop_df['Publisher'].values),
                           votes=list(pop_df['num_rating'].values),
                           rating=list(pop_df['avg_rating'].values)
                           )

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/recommended_books', methods=['POST'])
def recommended_books():
    user_input = request.form.get('user_input')
    print(f"User Input: {user_input}")  # Debugging statement
    if not user_input:
        return render_template('books.html', error="Please enter a book title.")
    
    # Check if user_input exists in pt.index
    similar_books = []
    for book_title in pt.index:
        if user_input.lower() in book_title.lower():
            index = np.where(pt.index == book_title)[0][0]
            similar_item = sorted(list(enumerate(ss[index])), key=lambda x: x[1], reverse=True)[1:5]
            similar_books.extend(similar_item)
    
    if not similar_books:
        return render_template('books.html', error="No similar books found.")
    
    data = []
    for i in similar_books:
        item = []
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))  
        data.append(item)
    print(f"Data to be passed to template: {data}")  # Debugging statement
    return render_template('books.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
