import discord
from discord.ext import tasks
from itertools import cycle


BOT_STATUSES = cycle(
    [
        "'I'll fix her calm down' - Bob the Builder",
        "A hammer can fix every problem.  Every.  Problem.",
        "My IQ test results came back. They were negative.",
        "Before you marry a person, make them use a computer with a slow Internet connection to see who they really are.",
        "A Freudian slip is when you say one thing but mean your mother.",
        "I remixed the remix... it was back to normal.",
        "Alcoholism is a disease. But it's like the only disease you can get yelled at for having.",
        "Dogs are forever in the pushup position.",
        "My fake plants died because I did not pretend to water them.",
        "I don't own a cellphone or a pager. I just hang around everyone I know all the time.",
        "A severed foot is the ultimate stocking stuffer.",
        "Two-in-one is a bullshit term because one is not big enough to hold two. That's why two was created.",
        "If I had nine of my fingers missing... I wouldn't type any slower.",
        'I like to take a toothpick and throw it in the forest and say "You\'re home!"',
        "I think Big Foot is blurry, that's the problem.",
        "Is a hippopotamus a hippopotamus... or a really cool opotamus?",
        "I like rice. Rice is great if you want to eat 2,000 of something.",
        "I had one anchovy. That's why I didn't have two anchovies.",
        "Every book is a children's book if the kid can read.",
        "I used to do drugs. I still do, but I used to, too.",
    ]
)


@tasks.loop(seconds=300)
async def change_bot_status(bot):
    await bot.change_presence(activity=discord.CustomActivity(next(BOT_STATUSES)))
