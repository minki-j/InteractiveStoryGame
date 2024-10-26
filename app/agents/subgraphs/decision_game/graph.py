from typing import List
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

from app.agents.llm_models import get_chat_model
from app.agents.state_schema import OverallState
from app.agents.state_schema import Scene, Choice
from app.agents.prompts import PROTAGONIST_INFO, GUIDELINES


class InteractiveSceneChoice(BaseModel):
    title: str = Field(description="A short sentence describing the choice")
    detail: str = Field(description="The detail of the choice")


class InteractiveScene(BaseModel):
    sketchpad: str = Field(
        description="You can use this for chain of thought reasoning or planning"
    )
    amended_scene: str = Field(
        description="The interactive scene that ends with a decision point"
    )
    choices: List[InteractiveSceneChoice] = Field(
        description="Five possible choices for the decision point of the interactive scene"
    )


class DecisionGameState(BaseModel):
    drafts: List[str] = Field(default_factory=lambda: [])
    interactive_scene: InteractiveScene = Field(default=None)
    story: List[Scene] = Field(
        default_factory=lambda: []
    )  #! there can be the same state variables in different states. when this variable name is returned, both state will be updated. This is confusing, and need to be fixed.
    user_choice: int = Field(default=None)
    scene: Scene = Field(default=None)
    profile: str = Field(default=None)
    big5: str = Field(default=None)
    genre: str = Field(default=None)
    level: str = Field(default=None)


def generate_multiple_draft(state: OverallState) -> DecisionGameState:
    print("\n>>> NODE: generate_multiple_draft")

    num_of_draft = 1
    chain = (
        ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a celebrated novelist writing story about this character
                    """
                    + PROTAGONIST_INFO,
                ),
                (
                    "human",
                    """Continue the story from the last scene. Keep the generation short. It should be 100 words or less.
                    """
                    + GUIDELINES
                    + """
---

This is the story you've written so far:

{prologue}

{stories}

---

Don't repeat the story. Just continue the story. Only return the continuation of the story, no title or comments such as "Here is the continuation: " or "The continuation is ".""",
                ),
            ]
        )
        | get_chat_model()
    )

    map_chain = RunnableParallel(**{f"gen{i+1}": chain for i in range(num_of_draft)})

    results = map_chain.invoke(
        {
            "profile": state.profile,
            "big5": state.big5,
            "genre": state.genre.replace("_", " "),
            "prologue": state.prologue,
            "level": state.level,
            "stories": (
                "\n\n".join([scene.completed_scene for scene in state.story])
                if len(state.story) > 0
                else ""
            ),
        }
    )

    return {
        "drafts": [results[f"gen{i+1}"].content for i in range(num_of_draft)],
        "profile": state.profile,
        "big5": state.big5,
        "genre": state.genre.replace("_", " "),
        "level": state.level,
    }


def pick_the_best_draft(state: DecisionGameState) -> DecisionGameState:
    print("\n>>> NODE: pick_the_best_draft")
    return {"drafts": [state.drafts[0]]}


def add_a_decision_point(state: DecisionGameState) -> OverallState:
    print("\n>>> NODE: add_a_decision_point")
    normal_scene_example = """
    Emily sat at the table with her friends, but something felt off. As the laughter and conversation swirled around her, she noticed that Julia had been unusually quiet all evening. Emily caught her glancing at her phone a few times, a worried expression on her face. It wasn’t like Julia to withdraw like this, especially at gatherings. Emily wanted to ask her what was wrong, but she wasn't sure if it was the right moment. Nevertheless, Emily decided to ask Julia. Emily leaned in closer, lowering her voice just enough to cut through the lively chatter around the table. "Hey, is everything okay? You seem a bit off tonight. Julia blinked, startled as if pulled out of a different world. She hesitated for a moment, then looked down at her phone again, biting her lip. "I... I don’t know," she began, her voice barely above a whisper. "I didn’t want to make a big deal out of it, but... I just got some weird texts from a number I don’t recognize. It’s been happening all week." Emily’s heart sank, sensing the unease in her friend. "Weird, like... threatening? Or just random?"
    """

    interactive_scene_example = """
sketchpad: "Ok. Let's first understand the normal scene. Emily is sitting at a table with her friends, and she notices that Julia has been unusually quiet all evening, making Emily worry about her. Emily contemplates whether she should ask Julia if everything is okay. But she asked and heard that Julia has been getting weird texts from a number she doesn't recognize.\nWhere can the decision point be? The pivotal point of this scene is when Emily decided to check in Julia. OK, this is the best decision point.\nI need to cut the story right after the sentence -- Emily wanted to ask her what was wrong, but she wasn't sure if it was the right moment.\nLet's check if this amendment makes sense. Yes, I think it does; When the reader reads this scene that is cut off there they could understand the context and choose one of the choices.\nOK, last but not least, I need to generate five possible choices for the decision point. I can include the one in the normal scene example as one of the choices. Emily could've texted instead of asking her directly. I can include that as one of the choices. Hmm what else? Emily could've asked another friend to check in on Julia. She could've just tried to bring up a lighthearted topic to ease the mood. OK. Did I get five choices? Yes, I think I'm good to go."

amended_scene: "Emily sat at the table with her friends, but something felt off. As the laughter and conversation swirled around her, she noticed that Julia had been unusually quiet all evening. Emily caught her glancing at her phone a few times, a worried expression on her face. It wasn’t like Julia to withdraw like this, especially at gatherings."

choices: [
    ("Ask Julia directly if something is wrong.", "You lean in closer to Julia and ask her softly, 'Hey, is everything okay? You seem a bit off tonight.'"),
    ("Text Julia privately to check in.", "Not wanting to put her on the spot, you send her a quick text: 'Hey, you seem a little off tonight. Everything okay?'"),
    ("Observe quietly and do nothing for now.", "You decide not to say anything for the moment, choosing instead to watch Julia from a distance. Perhaps she’s just having an off day."),
    ("Casually bring up a lighthearted topic to ease the mood.", "You steer the conversation toward something fun or amusing, hoping it might lift Julia's spirits without directly confronting her."),
    ("Ask another friend to check in on Julia.", "You discreetly mention to one of your other friends that Julia seems off and suggest they might ask her what's going on, thinking she might feel more comfortable opening up to them.")
    ]"""

    chain = (
        (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are a seasoned interactive fiction writer. Interactive fiction is a story format where the reader can make choices on how to react or behave at crucial moments. 
Your task is to help the user convert parts of a plain story into an interactive fiction scene. 

For example, let's say the user provides you with the following normal scene:
{normal_scene_example}

Then you should return something like this:
{interactive_scene_example}

Follow the following instructions to convert the scene into an interactive scene:
1. Identify a decision point in the scene. This can be either a reaction or a behavior. If there are multiple decision points, choose the most important one. If there is no decision point, you could create one.
2. Amend the scene so that it ends with a decision point and the reader can make a choice.
3. Generate five possible choices for the character.
4. The length of the amended scene should be 100 words or less.
""",
                    ),
                    (
                        "human",
                        "Convert this normal scence into an interactive scene.\n\n{scene}",
                    ),
                ]
            )
        )
        | get_chat_model(size="large").with_structured_output(InteractiveScene)
    )

    interactive_scene = chain.invoke(
        {
            "normal_scene_example": normal_scene_example,
            "interactive_scene_example": interactive_scene_example,
            "scene": state.drafts[0],
        }
    )

    scene = Scene(
        question=interactive_scene.amended_scene,
        choices=[
            Choice(title=choice.title, detail=choice.detail)
            for choice in interactive_scene.choices
        ],
        completed_scene="",
    )

    return {
        "story": [scene],
    }


def let_the_reader_decide(state: DecisionGameState) -> OverallState:
    print("\n>>> NODE: let_the_reader_decide")

    chain = (
        ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a celebrated {genre}  writer known for your extraordinary ability to weave enchanting and immersive tales. You are currently writing a {genre} story that has the reader as a main character. Here are information about the reader:

---

**Reader Profile**: {profile}

---

**Reader's Personality**: {big5}

---

**Guidelines to Follow**:

1. **Character Development**: Base the character's traits, motivations, and challenges on the reader's profile and personality test results. Aim for depth and nuance to evoke emotional resonance.

2. **Engaging Narrative**: The prologue should be a compelling conclusion to the story, wrapping up loose ends while leaving readers with a sense of wonder or reflection. Incorporate elements of magic, adventure or personal growth relevant to the character.

3. **Genre**: The story should be a {genre} story.

4. **Length**: should be 100 words or less.

5. **Level**: The vocabulary of the story should be appropriate for {level}.
""",
                ),
                (
                    "human",
                    """
Continue writing the story based on the choices the reader made.

---

Scene: {interactive_scene}

---

Choice the reader made: {user_choice}

---

**Important Rules**
1. Don't repeat the scene and just continue the story.
2. Keep the generation short and concise. It should be 100 words or less.
3. The vocabulary of the story should be appropriate for {level}.
""",
                ),
            ]
        )
        | get_chat_model(size="large")
        | StrOutputParser()
    )

    completed_scene = chain.invoke(
        {
            "profile": state.profile,
            "big5": state.big5,
            "genre": state.genre.replace("_", " "),
            "level": state.level,
            "interactive_scene": state.story[-1].question,
            "user_choice": state.story[-1].choices[state.user_choice].title,
        }
    )

    scene = Scene(
        id=state.story[-1].id,
        question=state.story[0].question,
        choices=[
            Choice(
                title=choice.title,
                detail=choice.content,
                chosen=(index == state.user_choice),
            )
            for index, choice in enumerate(state.story[-1].choices)
        ],
        completed_scene=completed_scene,
    )

    return {"story": [scene]}


g = StateGraph(OverallState)
g.add_edge(START, n(generate_multiple_draft))

g.add_node(generate_multiple_draft)
g.add_edge(n(generate_multiple_draft), n(pick_the_best_draft))

g.add_node(pick_the_best_draft)
g.add_edge(n(pick_the_best_draft), n(add_a_decision_point))

g.add_node(add_a_decision_point)
g.add_edge(n(add_a_decision_point), n(let_the_reader_decide))

g.add_node(let_the_reader_decide)
g.add_edge(n(let_the_reader_decide), END)

decision_game_graph = g.compile(interrupt_before=[n(let_the_reader_decide)])

with open("./app/agents/graph_diagrams/decision_game_graph.png", "wb") as f:
    f.write(decision_game_graph.get_graph(xray=10).draw_mermaid_png())
