from flask import Flask, render_template, request , url_for
import numpy as np
import pickle
popular_books = pickle.load(open('popular_books.pkl','rb'))
thepivottable = pickle.load(open('thepivottable.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
books_similarity_scores = pickle.load(open('books_similarity_scores2.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    book_titles = list(popular_books['Book-Title'].values)
    authors = list(popular_books['Book-Author'].values)
    images = list(popular_books['Image-URL-L'].values)
    votes = list(popular_books['Rating-Count'].values)
    ratings = list(popular_books['Average-Rating'].values)
    
    # Zipping the lists together
    books_data = zip(book_titles, authors, images, votes, ratings)
   
    return render_template('index.html', books_data=books_data, image_url=url_for('static', filename='logo.png'))

@app.route('/homepage')
def homepage():
    return render_template('home.html',image_url=url_for('static', filename='logo.png'))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',image_url=url_for('static', filename='logo.png'))

@app.route('/recommend_books',methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(thepivottable.index == user_input)[0][0]  
    # distance = books_similarity_scores[index]
    similar_books = sorted(list(enumerate(books_similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:11]

    total_kitaab = []

    for i in similar_books:
        kitaab = []
        temp3 = books[books['Book-Title'] == thepivottable.index[i[0]]]
        kitaab.extend(list(temp3.drop_duplicates('Book-Title')['Book-Title'].values))
        kitaab.extend(list(temp3.drop_duplicates('Book-Title')['Book-Author'].values))
        kitaab.extend(list(temp3.drop_duplicates('Book-Title')['Image-URL-L'].values))


        total_kitaab.append(kitaab)
    
    print(total_kitaab)
    return render_template('recommend.html',total_kitaab = total_kitaab)

if __name__ == '__main__':
    app.run(debug=True)

