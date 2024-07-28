import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Set up the intents
intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Set up the bot
bot = commands.Bot(command_prefix='/', intents=intents)

# The quote command
@bot.slash_command(name="quote", description="Create a quote image from the text")
async def quote(interaction: Interaction, 
                user: nextcord.Member = SlashOption(description="Select a user"), 
                text: str = SlashOption(description="Enter the quote text")):
    # Base image size
    width, height = 800, 400

    # Load the background image from a local file
    background_path = 'quotebg.jpg'  # Update this path to your background image
    background = Image.open(background_path)
    background = background.resize((width, height))

    # Draw on the background image
    draw = ImageDraw.Draw(background)

    # Load a font
    font_path = 'C:/Users/SplitSplice/dscbots/quotester/font.ttf'  # Make sure you have a font file
    font = ImageFont.truetype(font_path, 24)

    # User information
    username = str(user)
    avatar_url = user.display_avatar.url

    # Draw the text on the image
    margin = 20
    draw.text((margin, margin), f"{username} says...\n{text}", font=font, fill='white')
    draw.text((margin, height - margin - 50), "Quote of " + username, font=font, fill='white')
    draw.text((margin, height - margin - 24), "Quotester created by splitsplicecool!", font=font, fill='white')

    # Get the profile picture of the user
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content))
    avatar = avatar.resize((100, 100))  # Adjust the size to fit your design

    # Place the profile picture on the image
    background.paste(avatar, (width - margin - 100, height - margin - 100))

    # Save the image into a BytesIO object
    final_buffer = BytesIO()
    background.save(final_buffer, "PNG")
    final_buffer.seek(0)

    # Send the image
    file = nextcord.File(final_buffer, filename="quote.png")
    await interaction.response.send_message(file=file)
    print(f"Quoted user {username}!")

# Run the bot
bot.run("token")
