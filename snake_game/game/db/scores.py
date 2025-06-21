import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent / "scores.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                total_play_time INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                play_time INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        """)

def get_players():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, total_play_time 
            FROM players 
            ORDER BY name
        """)
        return cursor.fetchall()

def add_player(name):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
            return cursor.fetchone()[0]

def save_score(player_id, score, level, play_time):
    with sqlite3.connect(DB_PATH) as conn:
        # Save game session
        conn.execute(
            """INSERT INTO scores 
            (player_id, score, level, play_time, date) 
            VALUES (?, ?, ?, ?, ?)""",
            (player_id, score, level, play_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        # Update total play time
        conn.execute(
            "UPDATE players SET total_play_time = total_play_time + ? WHERE id = ?",
            (play_time, player_id)
        )

def get_high_scores(limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, s.score, s.level, s.play_time, s.date 
            FROM scores s
            JOIN players p ON s.player_id = p.id
            ORDER BY s.score DESC 
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()

def get_player_stats(player_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                name, 
                total_play_time,
                COUNT(s.id) as games_played,
                MAX(s.score) as high_score,
                AVG(s.score) as avg_score
            FROM players p
            LEFT JOIN scores s ON p.id = s.player_id
            WHERE p.id = ?
            GROUP BY p.id
        """, (player_id,))
        return cursor.fetchone()

init_db()