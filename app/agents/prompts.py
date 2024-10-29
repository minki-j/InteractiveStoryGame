STORY_INSTRUCTION = """
Write a story about a character based on their personality traits, making them feel fully developed, relatable, and engaging to the reader. Rather than explicitly listing their traits, reveal the character's personality subtly through their actions, decisions, thoughts, and interactions with others. Avoid using phrases that directly reference personality characteristics, such as "I am confident" or "I am imaginative." Instead, let the story unfold naturally, showing how the character’s personality influences their journey, struggles, and growth. Yet, don't obsess over the character's personality. You need to write a story, not constantly revealing the character's personality.
"""

PROTAGONIST_INFO = """
**Protagonist Profile**: {profile}

**Protagonist's Personality**: {big5}
"""

GUIDELINES = """
**Guidelines to Follow**:

1. Genre: Write a story in the style of {genre}.

2. Vocabulary Level: Use vocabulary suitable for {level} readers.

3. Target Age Group: Adjust the content to match the maturity and comprehension level of readers aged {level}.

4. Length: Limit the story to 100 words or fewer.

5. Output: Only return the story, no title or comments such as "Here is the story: " or "The story is ".

6. Write a story that subtly reveals a character's personality through their actions, choices, and interactions, avoiding explicit mentions of traits to create a natural, relatable, and fully developed portrayal.
"""


PROLOGUE_EXTRA_GUIDELINES = """
7. Don't use clichés for prologue. For example, the protagonist standing on somewhere is overused,  and make the story boring. Please don't start with "___ stood on ___"! Be creative and natural!!!

8. Don't reveal everything in the prologue. Prologue should only reveals the setting and latent feelings of the story. 
"""
