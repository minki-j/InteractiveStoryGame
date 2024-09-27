import uuid

from fasthtml.common import *

def home_view(req, res):
    return (
        Title("Perspective"),
        Main(cls="container")(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Perspective")
            ),
            P(
                "Perspective is a personalized fantasy story generator that places you at the heart of an immersive narrative."
            ),
            Form(
                hx_post="story?id=" + str(uuid.uuid4()),
                hx_swap="outerHTML",
                hx_target="main",
                hx_target_500="#error_msg",
                hx_indicator="#loader",
                hx_replace_url="true",
            )(
                Textarea(
                    rows=10,
                    cols=50,
                    name="user_profile",
                    placeholder="Enter your profile here",
                )("""
My name is Minki Jung. I'm a software engineer specializing in AI and an aspiring entrepreneur. Born in 1994 in South Korea, I come from Korean parents. I'm a 173cm tall male weighing 60kg, with long, curly black hair. Art is my passion—I once dreamed of becoming a musician and a movie director, possibly influenced by my mother, a bassoonist. My father, a pediatrician in Korea, taught me about medicine.
I've adopted an anti-aging lifestyle. Every day, I wake at 5:30 AM and sleep at 9:30 PM. Though unusual for someone my age, I love this routine. It's helped me overcome procrastination and depression. I maintain a healthy diet and exercise daily. I also work on my project every day, honing my skills in building software products. Despite only two years of programming experience, I've achieved much and grown significantly.
My goal is to become a successful entrepreneur and make a positive impact on the world. I love to work with brilliant people and have a strong sense of teamwork. Community means a lot for me. I'm most happy when I solve problems with curiosity and creativity. I'm not capitalistic. I want to be mindful with my money and be altruistic and kind to people. 
I'm not married and wanted to have a good partner who is admirable and kind. Artistic taste is so important to me when it comes to a partner."""),
                Button(type="submit", cls="btn-loader")("Generate"),
            ),
        ),
    )
