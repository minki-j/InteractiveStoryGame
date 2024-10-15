from db import db
from fasthtml.common import *

def delete_story(id: str):
    print(f">>> CNTRL: delete_story: {id}")
    db.t.stories.delete(id)
    return Response("", 204)
