import uuid
from app.agents.main_graph import main_graph

input_data = {
    "story_instruction": "A realistic journey of Minki building his startup called Perfect Day. The story should have a strong plot with interesting characters and a clear goal for the main character. It should be gripping and interesting to read. Don't be too cheesy or too serious.",
    "user_profile": """
name: Minki Jung.
age: 30.
gender: male.
address: Montréal, Canada.
appearance: EastAsian, 170 cm, 58 kg, long black curly hair, brown eyes, clean shaven, tanned skin, horn-rimmed glasses, slim but muscular build.
personality: extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, confident,
occupation: AI software engineer.
education: Bachelor's degree in physics and philosophy, graduate certificate in Artificial Intelligence.
intrests: reading, hiking, meditation, anti-aging, longevity, musics(jazz, classical, contemporary, experimental, world music).
values: Reflection, Learning, Self-transfomation, Mindfulness, Grit, Critical thinking, Open-mindedness, Honesty, Curiosity, Empathy, Creativity, Perseverance,
aversions: Superstition, Racism, Sexism, Nationalism, Bluffing, Laziness, Inauthenticity, Arrogance.
beliefs: Humans have very limited free will, All religions are not true, Science is the best way to understand the world, Utilitarianism is the most objective moral framework yet it is not perfect.
goals: To be an entrepreneur of a software company that makes a positive impact on the world using AI.
family: Father, mother, sister. Father is a pediatric doctor, mother is a housewife but used to be a bassonist, sister is 2 years younger and is working for a bank. All of them are in Korea. Parents are divorced. Married to my wife, Alison Jeon, 27 year old woman, who is a Korean Canadian. She is an aspiring writer.She is very supportive to my goal of becoming an entrepreneur. We have a dog named Charlie who is a shih tzu border terrior mix. Charlie is a girl.
history: Born and raised in Korea. Went to Hanyang University as a physics major student. During my military service I read a lot of books and got interested in humanitas. After coming back to school after the military, I tried one philosophy major class and fell in love to it. I decided to double major philosophy. Visited Toronto for a exchange program and met my wife there who is a Korean Canadian majoring in Enlgish literature and philosophy at University of Toronto. Went back to Korea and prepared for a graduate school for philosophy but rejected by all schools. Lost my goal of becoming a philosopher and dejected for an year. Worked as a journalist for an year but it was a small newspaper and I had trouble with my boss because I couldn't respect his writing style and logical reasoning. Quit the job and decided to immigrate to Canada with my wife. We got married in Korea and then immigrated to Canada. We lived in Toronto for 6 months and moved to Ottawa for my college. I went to Algonquin College for mobile app development. It was a 2 year program but I dropped out after an year. I transferred to AI software engineering program at the same college. I graduated from there and started working as an AI software engineer at the government of Canada.
facts: We are living in a apartment, we don't have a car, we don't own any property, we have 40,000 dollars in the bank, we have a strict lifestyle: we rarely drink alcohol, we wake up at 5:30 and go to bed at 9:30 everyday, we do cook healthy food in batch and have them for lunch and dinner, we rarely snack, we exercise everyday, We have a well-established morning routine: mediation, 1 hour of reading, breakfast, walk in nature for 30mins, have coffee and work for 3 hours, we work on Sunday and only hang out on Saturday but we still do the morning routine. 
plans: become a world class AI software engineer, build an AI story generating app(called Perfect Day) that puts the user as a main character in a story, make Perfect Day successful and move to San Francisco to get funding and recruit like-minded engineers.
    """
}

config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit":100}

output = main_graph.invoke(input_data, config)

print(f"==>> output: {output["chapters"]}")

while True:
    user_feedback = input("Enter a feedback:")
    user_feedback="I want "
    main_graph.update_state(
        config,
        {
            "user_feedback": user_feedback,
        },
        as_node="get_feedback_from_user",
    )
    output = main_graph.invoke(None, config)
    print(f"==>> output: {output["chapters"]}")

