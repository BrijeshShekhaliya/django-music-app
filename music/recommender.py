import pandas as pd
from .models import Song, SongHistory

def get_recommendations_for_user(user):
    # 1. Get all listening data
    all_history = SongHistory.objects.all().values('user_id', 'song_id')
    if not all_history.exists():
        return Song.objects.none() # Return no songs if history is empty

    df = pd.DataFrame(list(all_history))
    df['listened'] = 1

    # 2. Create a user-song matrix
    user_song_matrix = df.pivot_table(index='user_id', columns='song_id', values='listened').fillna(0)

    # 3. Find users with similar taste
    if user.id not in user_song_matrix.index:
        return Song.objects.none() # User has no history yet

    corr_matrix = user_song_matrix.T.corr()
    similar_users = corr_matrix[user.id].sort_values(ascending=False)

    # 4. Find songs they liked that our user hasn't heard
    recommended_song_ids = set()
    user_heard_songs = set(user_song_matrix.loc[user.id][user_song_matrix.loc[user.id] > 0].index)

    # Look at the top 10 most similar users
    for similar_user_id, score in similar_users.iloc[1:11].items():
        if score > 0.3: # A similarity threshold
            similar_user_songs = set(user_song_matrix.loc[similar_user_id][user_song_matrix.loc[similar_user_id] > 0].index)
            new_recommendations = similar_user_songs - user_heard_songs
            recommended_song_ids.update(new_recommendations)

    # Return the actual Song objects
    return Song.objects.filter(id__in=recommended_song_ids, is_approved=True)