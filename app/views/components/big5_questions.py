from fasthtml.common import *

from app.utils.generate_question_forms import generate_question_forms
from questionnaire import BIG5

def big5_questions():
    return (
        Div(cls="form-group")(
            H2(
                "Personality Questions",
                cls="section-title",
                style="font-size: 1.5rem; margin-top: 30px; margin-bottom: 20px;",
            ),
            *generate_question_forms(BIG5, "big5"),
        ),
    )
