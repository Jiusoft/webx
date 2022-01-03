"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import pandas as pd
import sqlite3

def compile_sqlte3_to_html_bookmark():
    try:
        conn = sqlite3.connect('bookmarks/bookmarks.db')
    except:
        print(
            "Cannot access file \"search_history.db\"; most likely because of a wrong directory error.")
    
    query = "SELECT link FROM bookmark ORDER BY date DESC"

    df = pd.read_sql_query(query, conn)

    with open("bookmarks/bookmarks.html", "w") as bookmarks:
        bookmarks.write("<head><title>Bookmarks</title><link rel=\"stylesheet\" href=\"bookmarks_styles.css\"></head><h1>Bookmarks</h1>")
        bookmarks.write(df.to_html(index=None))
        
    conn.close()
# Enhancements coming soon...