from prompts import story_json


def rate_story(text, prompt):
    text = f"""you are given the following story for a RPG game.
           "give a rating from 1-100 on how good the story for the gam is:
           the rating should be based on:
           1) plot
           2) connection to the prompt
           3) complexity of story 

           the prompt was: {prompt}
           the story is: {text}
           in the format: 
           $points$
           where $points$ is the amount of points awarded for the text given."""


result = extract_items(input_text)
print(result)


def ToT(prompt):
    pass