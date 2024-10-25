from typing import Literal

LEVELS = Literal[
    "EarlyElementary(Grades1-3/Ages6-9)",
    "UpperElementary(Grades4-6/Ages9-12)",
    "MiddleSchool(Grades7-9/Ages12-15)",
    "HighSchool(Grades10-12/Ages15-18)",
    "UnivFreshman(Ages18-19)",
    "UnivSophomore(Ages19-20)",
    "UnivJunior(Ages20-21)",
    "UnivSenior(Ages21-22)",
    "EmergingProfessionals(Ages22-35)",
    "MatureAdults(Ages35-50)",
    "MidlifeAndBeyond(Ages50-65)",
    "SeniorAdults(Ages65+)",
]

LEVEL_OPTIONS = [
    ("EarlyElementary(Grades1-3/Ages6-9)", "Early Elementary (Grades 1-3 / Ages 6-9)"),
    (
        "UpperElementary(Grades4-6/Ages9-12)",
        "Upper Elementary (Grades 4-6 / Ages 9-12)",
    ),
    ("MiddleSchool(Grades7-9/Ages12-15)", "Middle School (Grades 7-9 / Ages 12-15)"),
    ("HighSchool(Grades10-12/Ages15-18)", "High School (Grades 10-12 / Ages 15-18)"),
    ("UnivFreshman(Ages18-19)", "University Freshman (Ages 18-19)"),
    ("UnivSophomore(Ages19-20)", "University Sophomore (Ages 19-20)"),
    ("UnivJunior(Ages20-21)", "University Junior (Ages 20-21)"),
    ("UnivSenior(Ages21-22)", "University Senior (Ages 21-22)"),
    ("EmergingProfessionals(Ages22-35)", "Emerging Professionals (Ages 22-35)"),
    ("MatureAdults(Ages35-50)", "Mature Adults (Ages 35-50)"),
    ("MidlifeAndBeyond(Ages50-65)", "Midlife and Beyond (Ages 50-65)"),
    ("SeniorAdults(Ages65+)", "Senior Adults (Ages 65+)"),
]

GENRE = Literal[
    "fantasy",
    "scifi",
    "mystery",
    "romance",
    "adventure",
    "horror",
    "thriller",
    "historical_fiction",
    "contemporary_fiction",
    "literary_fiction",
    "dystopian",
    "young_adult",
    "crime",
    "comedy",
    "drama",
    "action",
    "western",
    "magical_realism",
    "urban_fantasy",
    "paranormal",
]

GENRE_OPTIONS = [
    ("fantasy", "Fantasy"),
    ("scifi", "Science Fiction"),
    ("mystery", "Mystery"),
    ("romance", "Romance"),
    ("adventure", "Adventure"),
    ("horror", "Horror"),
    ("thriller", "Thriller"),
    ("historical_fiction", "Historical Fiction"),
    ("contemporary_fiction", "Contemporary Fiction"),
    ("literary_fiction", "Literary Fiction"),
    ("dystopian", "Dystopian"),
    ("young_adult", "Young Adult"),
    ("crime", "Crime"),
    ("comedy", "Comedy"),
    ("drama", "Drama"),
    ("action", "Action"),
    ("western", "Western"),
    ("magical_realism", "Magical Realism"),
    ("urban_fantasy", "Urban Fantasy"),
    ("paranormal", "Paranormal"),
]


PROFILE = {
    "1": {
        "question": "What is your name?",
        "answer": "",
    },
    "2": {
        "question": "How old are you?",
        "answer": "",
    },
    "3": {
        "question": "What pronouns do you use??",
        "answer": "",
    },
    "4": {
        "question": "Describe yourself appearance if you feel it comfortable to share",
        "answer": "",
    },
    "5": {
        "question": "Add anything that you want to include in the story. For example, you can make your pet appears in the story.",
        "answer": "",
    },
}

PROFILE_M = {
    "1": {
        "question": "What is your name?",
        "answer": "",
    },
    "2": {
        "question": "How old are you?",
        "answer": "30",
    },
    "3": {
        "question": "What pronouns do you use??",
        "answer": "he/him",
    },
    "4": {
        "question": "Describe yourself appearance if you feel it comfortable to share",
        "answer": "Asian male, 173cm, 58kg, slim but muscular, tanned skin, black long curly hair, brown eyes, clean shaven, wears brown horn-rimmed glasses, average looks",
    },
    "5": {
        "question": "Add anything that you want to include in the story. For example, you can add your dog. ",
        "answer": "Bachelor's degree",
    },
}

ANSWER_OPTIONS = [
    "strongly disagree",  # 0
    "disagree",  # 1
    "neutral",  # 2
    "agree",  # 3
    "strongly agree",  # 4
]


BIG5 = {
    "1": {
        "question": "I sometimes feel anxious when I have to do something that I haven't done before.",
        "current": "",
        "goal": "",
    },
    "2": {
        "question": "I often prioritize taking care of others over myself.",
        "current": "",
        "goal": "",
    },
    "3": {
        "question": "I have a very active imagination.",
        "current": "",
        "goal": "",
    },
    "4": {
        "question": "I am socially comfortable around people.",
        "current": "",
        "goal": "",
    },
    "5": {
        "question": "I usually finish chores right away.",
        "current": "",
        "goal": "",
    },
    "6": {
        "question": "I frequently worry about things that might go wrong.",
        "current": "",
        "goal": "",
    },
    "7": {
        "question": "I enjoy engaging in intellectual debates and discussions.",
        "current": "",
        "goal": "",
    },
    "8": {
        "question": "I often worry that I am not good enough.",
        "current": "",
        "goal": "",
    },
    "9": {
        "question": "There are many things I wish were different about myself.",
        "current": "",
        "goal": "",
    },
    "10": {
        "question": "I sometimes feel sad or down.",
        "current": "",
        "goal": "",
    },
    "11": {
        "question": "I often change my plans on a whim.",
        "current": "",
        "goal": "",
    },
    "12": {
        "question": "I am naturally curious and like to learn new things.",
        "current": "",
        "goal": "",
    },
    "13": {
        "question": "I prefer not to take on too much responsibility.",
        "current": "",
        "goal": "",
    },
    "14": {
        "question": "I often feel more capable or important than others.",
        "current": "",
        "goal": "",
    },
    "15": {
        "question": "I prefer to plan things out in advance rather than act spontaneously.",
        "current": "",
        "goal": "",
    },
    "16": {
        "question": "When I meet friends, I usually talk more than others.",
        "current": "",
        "goal": "",
    },
}


BIG5_M = {
    "1": {
        "question": "My moods change easily.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    "2": {
        "question": "I take care of other people before taking care of myself.",
        "current": ANSWER_OPTIONS[0],
        "goal": ANSWER_OPTIONS[3],
    },
    "3": {
        "question": "I have a vivid imagination.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    "4": {
        "question": "I feel comfortable around people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[4],
    },
    "5": {
        "question": "I get chores done right away.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    "6": {
        "question": "I often feel anxious about what could go wrong.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    "7": {
        "question": "I start arguments just for the fun of it.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    "8": {
        "question": "I often worry that I am not good enough.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    "9": {
        "question": "There are many things that I do not like about myself.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[1],
    },
    "10": {
        "question": "I rarely feel blue.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[3],
    },
    "11": {
        "question": "I change my plans frequently.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    "12": {
        "question": "I avoid philosophical discussions.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    "13": {
        "question": "I am inquisitive",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    "14": {
        "question": "I am reserved",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[3],
    },
    "15": {
        "question": "I am agreeable",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[1],
    },
    "16": {
        "question": "I always make good use of my time.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[4],
    },
    "17": {
        "question": "I am interested in the meaning of things.",
        "current": ANSWER_OPTIONS[4],
        "goal": ANSWER_OPTIONS[4],
    },
    "18": {
        "question": "I avoid taking on a lot of responsibility.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    "19": {
        "question": "I feel I am better than other people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    "20": {
        "question": "I make friends easily.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[2],
    },
    "21": {
        "question": "I make plans and stick to them.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    "22": {
        "question": "I am not interested in abstract ideas.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[1],
    },
    "23": {
        "question": "I criticize other people.",
        "current": ANSWER_OPTIONS[3],
        "goal": ANSWER_OPTIONS[3],
    },
    "24": {
        "question": "I don't talk a lot.",
        "current": ANSWER_OPTIONS[2],
        "goal": ANSWER_OPTIONS[2],
    },
    "25": {
        "question": "It's important to me that people are on time.",
        "current": ANSWER_OPTIONS[1],
        "goal": ANSWER_OPTIONS[2],
    },
}
