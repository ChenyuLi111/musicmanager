# search.py
def parse_query(query):
    # 将整个查询作为标题进行搜索
    parsed_query = {
        'title': query.lower()
    }
    return parsed_query

def search_music(music_library, parsed_query):
    results = []
    search_title = parsed_query.get('title', '')
    for song in music_library:
        title = song.get('title', '').lower()
        if search_title in title:
            results.append(song)
    return results
