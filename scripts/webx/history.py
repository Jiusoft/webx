"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import pandas as pd
import sqlite3
import os

def compile_sqlte3_to_html_history():
    try:
        conn = sqlite3.connect(f'{os.path.dirname(os.path.realpath(__file__))}/history/search_history.db')
    except Exception as e:
        print(
            "Cannot access file \"search_history.db\"; most likely because of a wrong directory error.")
        print(os.path.dirname(os.path.realpath(__file__)))
    
    query = "SELECT date,link FROM history ORDER BY date,time DESC"

    df = pd.read_sql_query(query, conn)
    
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/history/history.html", "w") as history:
        history.write("<head><title>History</title><link rel=\"stylesheet\" href=\"history_styles.css\"></head><h1>your browsing history</h1>")
        history.write(df.to_html(index=None))
        
    conn.close()
# Enhancements coming soon...