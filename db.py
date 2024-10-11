import os
import json
from fasthtml.common import *
from app.agents.state_schema import Scene

os.makedirs("./data/main_database", exist_ok=True)
db_path = os.path.join(".", "data", "main_database", "main.db")

print(f">>>> DB: initialize database at {db_path}")
db = database(db_path)

users, stories = (db.t.users, db.t.stories)

if users not in db.t:
    print("\n>>>> DB: Creating users table")
    users.create(
        id=str,
        name=str,
        email=str,
        pk="id",
    )

if stories not in db.t:
    print("\n>>>> DB: Creating stories table")
    stories.create(
        id=str,
        user_id=str,
        title=str,
        prologue=str,
        scenes=str,  # Change this to str to store JSON
        pk="id",
        foreign_keys=(("user_id", "users")),
        if_not_exists=True,
    )

# Scene serialization/deserialization
def scene_to_json(scene: Scene) -> str:
    return json.dumps(scene.dict())

def json_to_scene(scene_json: str) -> Scene:
    return Scene(**json.loads(scene_json))

class Stories(stories.dataclass()):
    @property
    def scenes(self) -> List[Scene]:
        return [json_to_scene(scene) for scene in json.loads(self._scenes)]
    
    @scenes.setter
    def scenes(self, value: List[Scene]):
        self._scenes = json.dumps([scene_to_json(scene) for scene in value])

Stories = Stories

Users = users.dataclass()

# try:
#     main_db_diagram = diagram(db.tables)
#     main_db_diagram.render(
#         "data/main_database/main_db_diagram", format="png", cleanup=True
#     )
# except:
#     print(
#         "Error on generating DB visualization. Probably graphviz executables were not found. Please install Graphviz and add it to your system's PATH."
#     )
