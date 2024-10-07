PROFILE = {
    1:{
        "questions": "What is your name?",
        "answer": "Minki Jung",
    },
    2:{
        "questions": "What is your age?",
        "answer": "30",
    },
    3:{
        "questions": "What is your gender?",
        "answer": "Male",
    },
    4:{
        "questions": "What is your nationality?",
        "answer": "Korean Canadian",
    },
    5:{
        "questions": "What's your current job?",
        "answer": "Software Engineer focusing on AI",
    },
    6:{
        "questions": "Tell me about your current relationship status",
        "answer": "Married with no kids",
    },
    7:{
        "questions": "Describe yourself appearance",
        "answer": "Asian male, 173cm, 58kg, slim but muscular, taned skin, black long curly hair, brown eyes, clean shaven, wears brown horn-rimmed glasses, average looks",
    },
    8:{
        "questions": "Describe your parents",
        "answer": "Both Korean still living in Korea. Father is a pediatric docter, mother used to be a bassoonist but a housewife now. They got divorced when I was 25 years old but they see each other quite often.",
    },    
}

ANSWER_OPTIONS = [
    "strongly disagree", #0
    "disagree", #1
    "neutral", #2
    "agree", #3
    "strongly agree", #4
]

BIG5 = {
    1: {
        "questions": "I accept people the way they are.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[3],
    },
    2: {
        "questions": "I believe in the importance of art.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    3: {
        "questions": "My moods change easily.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    4: {
        "questions": "I take care of other people before taking care of myself.",
        "current": ANSWER_OPTIONS[0],
        "goal": ANSWER_OPTIONS[3],
    },
    5: {
        "questions": "I am always prepared.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[4],
    },
    6: {
        "questions": "I have a vivid imagination.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    7: {
        "questions": "I feel comfortable around people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    8: {
        "questions": "I am the life of the party.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[3],
    },
    9: {
        "questions": "I treat everyone with kindness and sympathy.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    10: {
        "questions": "I get chores done right away.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    11: {
        "questions": "I have a kind word for everyone.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    12: {
        "questions": "I am skilled in handling social situations.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[4],
    },
    13: {
        "questions": "I often feel anxious about what could go wrong.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    14: {
        "questions": "I start arguments just for the fun of it.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    15: {
        "questions": "I often worry that I am not good enough.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    16: {
        "questions": "I find it difficult to get to work.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[0],
    },
    17: {
        "questions": "I stay in the background.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[1],
    },
    18: {
        "questions": "There are many things that I do not like about myself.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    19: {
        "questions": "I seldom feel blue.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[3],
    },
    20: {
        "questions": "I stop what I am doing to help other people.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    21: {
        "questions": "I change my plans frequently.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    22: {
        "questions": "I am often troubled by negative thoughts.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    23: {
        "questions": "I feel comfortable with myself.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    24: {
        "questions": "I avoid philosophical discussions.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    25: {
        "questions": "I am Original",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    26: {
        "questions": "I am Systematic",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    27: {
        "questions": "I am Shy",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[0],
    },
    28: {
        "questions": "I am Soft-Hearted",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    29: {
        "questions": "I am Tense",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[2],
    },
    30: {
        "questions": "I am Inquisitive",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    31: {
        "questions": "I am Reserved",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    32: {
        "questions": "I am Agreeable",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[1],
    },
    33: {
        "questions": "I am Nervous",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[2],
    },
    34: {
        "questions": "I am Creative",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    35: {
        "questions": "I am Self-Disciplined",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    36: {
        "questions": "I am Outgoing",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    37: {
        "questions": "I am Moody",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[1],
    },
    38: {
        "questions": "I am Imaginative",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    39: {
        "questions": "I am Organized",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    40: {
        "questions": "I am Talkative",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[2],
    },
    41: {
        "questions": "I am Humble",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    42: {
        "questions": "I am Pessimistic",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    43: {
        "questions": "I have a lot to say.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    44: {
        "questions": "I enjoy going to art museums.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    45: {
        "questions": "I always make good use of my time.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[4],
    },
    46: {
        "questions": "I am interested in the meaning of things.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    47: {
        "questions": "I avoid taking on a lot of responsibility.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    48: {
        "questions": "I feel I am better than other people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    49: {
        "questions": "I make friends easily.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[2],
    },
    50: {
        "questions": "I make plans and stick to them.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    51: {
        "questions": "I am not interested in abstract ideas.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    52: {
        "questions": "I criticize other people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    53: {
        "questions": "I don't talk a lot.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    54: {
        "questions": "It’s important to me that people are on time.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[2],
    },
}
