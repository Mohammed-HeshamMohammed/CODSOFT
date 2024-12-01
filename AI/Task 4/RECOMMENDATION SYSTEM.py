import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, util

ratings_data = {
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'item_id': [101, 102, 103, 101, 103, 104, 102, 104, 105],
    'rating': [4, 5, 2, 3, 4, 5, 4, 5, 3]
}

items_data = {
    'item_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,  # Movies
                201, 202, 203, 204, 205, 206, 207, 208, 209, 210,  # Anime
                301, 302, 303, 304, 305, 306, 307, 308, 309, 310],  # Music
    'title': [
        # Movies
        'The Matrix', 'The Godfather', 'Inception', 'Avengers', 'Titanic',
        'Interstellar', 'Spirited Away', 'Joker', 'Parasite', 'The Dark Knight',
        # Anime
        'Demon Slayer', 'Attack on Titan', 'My Hero Academia', 'Naruto', 'Death Note',
        'Fullmetal Alchemist', 'One Piece', 'Sword Art Online', 'Tokyo Ghoul', 'Hunter x Hunter',
        # Music
        'Bohemian Rhapsody', 'Shape of You', 'Blinding Lights', 'Imagine', 'Smells Like Teen Spirit',
        'Rolling in the Deep', 'Bad Guy', 'Let It Be', 'Uptown Funk', 'Believer'
    ],
    'category': [
        # Categories
        'Movie', 'Movie', 'Movie', 'Movie', 'Movie', 'Movie', 'Movie', 'Movie', 'Movie', 'Movie',
        'Anime', 'Anime', 'Anime', 'Anime', 'Anime', 'Anime', 'Anime', 'Anime', 'Anime', 'Anime',
        'Music', 'Music', 'Music', 'Music', 'Music', 'Music', 'Music', 'Music', 'Music', 'Music'
    ],
    'description': [
        # Descriptions for Movies, Anime, and Music
        'A computer hacker learns about the true nature of reality and his role in it.',
        'The aging patriarch of an organized crime dynasty transfers control to his son.',
        'A thief with the ability to enter dreams takes on a dangerous mission.',
        'Superheroes team up to save the Earth from a catastrophic threat.',
        'A romance aboard the ill-fated Titanic.',
        'Explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
        'A young girl becomes trapped in a strange world of spirits and must find her way back.',
        'A failed comedian descends into insanity, sparking a violent revolution in Gotham.',
        'A poor family schemes to infiltrate a wealthy household, leading to unexpected consequences.',
        'Batman faces the Joker, who seeks to destroy Gotham and challenge Batman\'s moral code.',
        # Anime
        'A young boy becomes a demon slayer after his family is killed by demons.',
        'Humans fight against giant creatures known as Titans to survive.',
        'A boy born without superpowers enrolls in a hero academy to become a symbol of peace.',
        'A young ninja dreams of becoming the leader of his village while dealing with his dark past.',
        'A high school student discovers a notebook that allows him to kill anyone by writing their name.',
        'Two brothers search for the Philosopher\'s Stone after a failed alchemy experiment.',
        'A pirate sets out to find the legendary treasure, One Piece, and become the Pirate King.',
        'Players are trapped in a virtual reality MMORPG and must survive to escape.',
        'A college student becomes part ghoul after a deadly encounter and struggles with his identity.',
        'A young boy embarks on a journey to become a Hunter and find his missing father.',
        # Music
        'A biographical film about the legendary band Queen and their lead singer.',
        'A romantic pop song by Ed Sheeran that celebrates love and attraction.',
        'A synthwave hit by The Weeknd exploring love and longing.',
        'A timeless anthem by John Lennon envisioning a world of peace and harmony.',
        'A grunge anthem by Nirvana that defined a generation of music fans.',
        'A powerful soul song by Adele about heartbreak and empowerment.',
        'A quirky pop hit by Billie Eilish exploring darker themes with a playful twist.',
        'A classic Beatles song offering solace and hope during tough times.',
        'A funky, upbeat track by Bruno Mars and Mark Ronson that celebrates fun and dance.',
        'A motivational pop-rock anthem by Imagine Dragons about overcoming adversity.'
    ]
}

# Convert to DataFrame
ratings_df = pd.DataFrame(ratings_data)
items_df = pd.DataFrame(items_data)

# ----------------------------
# Collaborative Filtering
# ----------------------------

# Load data for Surprise library
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'item_id', 'rating']], reader)

# Split into train and test sets
trainset, testset = train_test_split(data, test_size=0.25)

# Train an SVD model
svd = SVD()
svd.fit(trainset)


# Function to recommend items based on collaborative filtering
def recommend_cf(user_id, num_recommendations=5):
    item_ids = items_df['item_id'].tolist()
    predictions = [svd.predict(user_id, item_id).est for item_id in item_ids]
    recommended_items = sorted(zip(item_ids, predictions), key=lambda x: x[1], reverse=True)[:num_recommendations]
    return items_df[items_df['item_id'].isin([item[0] for item in recommended_items])]


# ----------------------------
# Content-Based Filtering
# ----------------------------

# Create a TF-IDF matrix for item descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(items_df['description'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Function to recommend items based on content
def recommend_cb(item_title, num_recommendations=5):
    idx = items_df[items_df['title'] == item_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]
    recommended_items = [items_df.iloc[i[0]]['title'] for i in sim_scores]
    return recommended_items


# ----------------------------
# Hybrid Recommendation
# ----------------------------

# Function to combine CF and CB recommendations
def recommend_hybrid(user_id, item_title, num_recommendations=5, alpha=0.5):
    # CF recommendations
    cf_recommendations = recommend_cf(user_id, num_recommendations)

    # CB recommendations
    cb_recommendations = recommend_cb(item_title, num_recommendations)

    # Merge CF and CB recommendations (simple weighted hybrid)
    cf_scores = {row['item_id']: idx + 1 for idx, row in cf_recommendations.iterrows()}
    cb_scores = {items_df[items_df['title'] == title].iloc[0]['item_id']: idx + 1 for idx, title in
                 enumerate(cb_recommendations)}

    combined_scores = {}
    for item_id in set(cf_scores.keys()).union(cb_scores.keys()):
        cf_score = cf_scores.get(item_id, 0)
        cb_score = cb_scores.get(item_id, 0)
        combined_scores[item_id] = alpha * cf_score + (1 - alpha) * cb_score

    # Sort items by combined scores
    sorted_items = sorted(combined_scores.items(), key=lambda x: x[1])
    recommended_items = [items_df[items_df['item_id'] == item[0]]['title'].iloc[0] for item in
                         sorted_items[:num_recommendations]]
    return recommended_items


# ----------------------------
# Test Recommendations
# ----------------------------

# Collaborative Filtering
print("Collaborative Filtering Recommendations for User 1:")
print(recommend_cf(user_id=1))

# Content-Based Filtering
print("\nContent-Based Filtering Recommendations for 'Inception':")
print(recommend_cb(item_title='Inception'))

# Hybrid Recommendations
print("\nHybrid Recommendations for User 1 and 'Inception':")
print(recommend_hybrid(user_id=1, item_title='Inception'))
