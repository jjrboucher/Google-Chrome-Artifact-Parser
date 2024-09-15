def search_terms():
    sql_query = """
        /*
        Requires that you first open Web Data, and then Attach History, giving it the name 'history'.
        See the sub-section titled Search Terms in chapter 4 of the Chrome guide for instructions how to
        do that if unsure.
        
        Last modified: 2021-10-11
        Author:  Jacques Boucher - jjrboucher@gmail.com
        Tested with:  Chrome 94
        */
        
        SELECT	keywords.keyword AS "Search Engine",
            history.urls.url,
            history.keyword_search_terms.term,
            history.urls.visit_count,
            history.urls.last_visit_time,
            datetime(history.urls.last_visit_time/1000000-11644473600,'unixepoch') AS "Decoded history.last_visit_time (UTC)"
             
        FROM history.keyword_search_terms
            LEFT JOIN history.urls ON history.urls.id=history.keyword_search_terms.url_id
            LEFT JOIN keywords ON history.keyword_search_terms.keyword_id=keywords.id
    """

    return sql_query, "search_terms"