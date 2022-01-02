"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import pandas as pd
import sqlite3

def compile_sqlte3_to_html():
    try:
        conn = sqlite3.connect('history/search_history.db')
    except:
        print(
            "Cannot access file \"search_history.db\"; most likely because of a wrong directory error.")
    
    query = "SELECT * FROM history ORDER BY date,time DESC"

    df = pd.read_sql_query(query, conn)
    
    with open("history/history.html", "w") as history:
        history.write("<head><title>History</title><link rel=\"stylesheet\" href=\"history_styles.css\"></head><h1>your browsing history</h1>")
        history.write(df.to_html(index=None))
# Enhancements coming soon...