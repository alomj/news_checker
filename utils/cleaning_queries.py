from utils.basic_cleanup import basic_cleanup

FORBIDDEN_WORDS = ['Look for', 'Search for', 'Explore', 'Find']


def sanitize_query(query: str) -> str:

    query = basic_cleanup(query)
    lowered = query.lower()
    positions = []

    for word in FORBIDDEN_WORDS:
        pos = lowered.find(word.lower())
        if pos != -1:
            positions.append(pos)
    if positions:
        cut_pos = min(positions)
        query = query[:cut_pos]

    return query
