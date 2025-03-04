def chrome_keyword_historyquery():
    worksheet = "Search Terms"
    history_query = """
        SELECT	urls.id, 
        urls.url, 
        keyword_search_terms.keyword_id, 
        keyword_search_terms.url_id, 
        keyword_search_terms.term, 
        urls.visit_count, 
        urls.last_visit_time, 
        datetime(urls.last_visit_time/1000000-11644473600,'unixepoch') AS "Decoded history.last_visit_time (UTC)"
                    
        FROM urls
        LEFT JOIN keyword_search_terms ON urls.id=keyword_search_terms.url_id
    """

    return history_query, worksheet
