import discord
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import pandas as pd


client = discord.Client()

tz = 'Asia/Tokyo'

plt.rcParams['timezone'] = tz
plt.rcParams["font.family"] = "Source Han Sans JP, Noto Color Emoji"


def plot_messages_per_day(messages):
    df = pd.DataFrame({"date": [m.created_at for m in messages],
                       "messages": range(0, len(messages))
                       })

    df.index = pd.DatetimeIndex(df.date).tz_localize(
        'UTC').tz_convert(tz)
    df.drop("date", axis=1, inplace=True)

    df = df.resample('30T').count()

    fig, ax = plt.subplots(1, 1, figsize=(14, 4))

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))

    ax.plot(df.index, df.messages)

    plt.ylabel("Number of messages per day")

    plt.grid()

    fig.savefig("messages_per_day.png")


def plot_duplicates_per_day(messages):
    s = pd.Series([m.content for m in messages if not m.author.bot])

    c = s.value_counts().rename("counts")

    df = pd.DataFrame(c[c > 1])

    fig, ax = plt.subplots(1, 1, figsize=(4, 8))

    fig.subplots_adjust(left=0.4)

    ax.barh(df.index, df.counts, height=0.8)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.xlabel("Number of duplicate messages")

    fig.savefig("duplicates_per_day.png")


def plot_user_ranking(messages):
    s = pd.Series([m.author.name for m in messages if not m.author.bot])

    c = s.value_counts().rename("counts")

    df = pd.DataFrame(c[c > 1])

    fig, ax = plt.subplots(1, 1)

    fig.subplots_adjust(left=0.2)

    ax.barh(df.index, df.counts)

    plt.xlabel("User ranking")

    fig.savefig("user_ranking.png")


@client.event
async def on_ready():
    channel = client.get_channel(int(os.environ['CHANNEL_ID']))

    messages = await channel.history(limit=1000).flatten()

    plot_messages_per_day(messages)
    plot_duplicates_per_day(messages)
    plot_user_ranking(messages)

    await client.close()


client.run(os.environ['TOKEN'], bot=False)
