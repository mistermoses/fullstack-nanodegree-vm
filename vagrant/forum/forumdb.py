#
# Database access functions for the web forum.
#

import psycopg2
import time
import bleach

## Database connection
def ConnectDB():
    return psycopg2.connect("dbname=forum");

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = ConnectDB()
    c = db.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC;")
    posts = ({'content': str(bleach.clean(row[1])), 'time':str(row[0])} for row in c.fetchall())
    db.close()
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = ConnectDB()
    c = db.cursor()
    c.execute("INSERT INTO posts (content) values (%s)", (bleach.clean(content),))
    db.commit()
    db.close()
