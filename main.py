import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import asyncio
import os

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

class Client(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"Connected Successfully! Logged in as: {self.user}")
        activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="Your Mom!😘😍"
            )
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(self.user.mention):
            await message.channel.send(f"Hi there {message.author.mention}")

        await self.process_commands(message)

client = Client(command_prefix="!", intents=intents)

# ================= BUTTON VIEW ================= #

class MenuView(discord.ui.View):

    @discord.ui.button(label="Noob", style=discord.ButtonStyle.secondary, emoji="💩")
    async def noob(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💩 Noob Plans",
            description="description\ndescription",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Pro", style=discord.ButtonStyle.primary, emoji="😎")
    async def pro(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="😎 Pro Plans",
            description="description\ndescription",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Hacker", style=discord.ButtonStyle.danger, emoji="☠")
    async def hacker(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="☠ Hacker Plans",
            description="description\ndescription",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ================= MENU ================= #

@client.tree.command(name="menu", description="Print the menu!!")
async def slash_menu(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Welcome to the server!",
        description="Click buttons below!",
        color=discord.Color.blue()
    )
    embed.set_author(
        name="Deadlord Host",
        url="https://discord.com/oauth2/authorize?client_id=1471390877107748998",
        icon_url="https://i.pinimg.com/736x/de/f8/66/def8663a5c4b4ca579f84673f7ee1a71.jpg"
    )

    embed.set_footer(text="Deadlord Host")
    await interaction.response.send_message(embed=embed, view=MenuView())

@client.command()
async def menu(ctx):
    embed = discord.Embed(
        title="Services Panel",
        description="Click buttons below to see our plans!",
        color=discord.Color.blue()
    )
    embed.set_author(
        name="Deadlord Host",
        url="https://discord.com/oauth2/authorize?client_id=1471390877107748998",
        icon_url="https://i.pinimg.com/736x/de/f8/66/def8663a5c4b4ca579f84673f7ee1a71.jpg"
    )

    embed.set_footer(text="Deadlord Host")
    await ctx.send(embed=embed, view=MenuView())

# ================= PURGE ================= #

@client.tree.command(name="purge", description="Delete Any Messages!!")
@app_commands.checks.has_permissions(manage_messages=True)
async def slash_purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Deleted {len(deleted)} messages.",ephemeral=True)

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"Deleted {amount} messages.")
    await msg.delete(delay=3)

# ================= KICK ================= #

@client.tree.command(name="kick", description="Kick a member")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):

    if member == interaction.user:
        await interaction.response.send_message("❌ You cannot kick yourself.", ephemeral=True)
        return

    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ You cannot kick the server owner.", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ You cannot moderate this member (role hierarchy).",
            ephemeral=True
        )
        return

    await member.kick(reason=reason)

    await interaction.response.send_message(
        f"✅ {member} has been kicked."
    )

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):

    if member == ctx.author:
        await ctx.send("❌ You cannot kick yourself.")
        return

    if member == ctx.guild.owner:
        await ctx.send("❌ You cannot kick the server owner.")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot moderate this member (role hierarchy).")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("❌ I cannot kick this member due to role hierarchy.")
        return

    await member.kick(reason=reason)
    await ctx.send(f"✅ {member} has been kicked.")

# ================= BAN ================= #

@client.tree.command(name="ban", description="Ban a member!!")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):

    # Prevent banning yourself
    if member == interaction.user:
        await interaction.response.send_message(
            "❌ You cannot ban yourself.",
            ephemeral=True
        )
        return

    # Prevent banning server owner
    if member == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ You cannot ban the server owner.",
            ephemeral=True
        )
        return

    # Prevent staff banning staff (role hierarchy check)
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ You cannot moderate this member (role hierarchy).",
            ephemeral=True
        )
        return

    await member.ban(reason=reason)

    await interaction.response.send_message(
        f"✅ {member} has been banned."
    )

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):

    if member == ctx.author:
        await ctx.send("❌ You cannot ban yourself.")
        return

    if member == ctx.guild.owner:
        await ctx.send("❌ You cannot ban the server owner.")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot moderate this member (role hierarchy).")
        return

    await member.ban(reason=reason)
    await ctx.send(f"✅ {member} has been banned.")


# ================= TIMEOUT ================= #

from datetime import timedelta

@client.tree.command(name="timeout", description="Timeout a member")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int):

    if member == interaction.user:
        await interaction.response.send_message("❌ You cannot timeout yourself.", ephemeral=True)
        return

    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ You cannot timeout the server owner.", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ You cannot moderate this member (role hierarchy).",
            ephemeral=True
        )
        return

    duration = timedelta(minutes=minutes)

    await member.timeout(duration)

    await interaction.response.send_message(
        f"✅ {member} has been timed out for {minutes} minutes."
    )

@client.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):

    if member == ctx.author:
        await ctx.send("❌ You cannot timeout yourself.")
        return

    if member == ctx.guild.owner:
        await ctx.send("❌ You cannot timeout the server owner.")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot moderate this member (role hierarchy).")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("❌ I cannot timeout this member due to role hierarchy.")
        return

    duration = timedelta(minutes=minutes)

    await member.timeout(duration)
    await ctx.send(f"✅ {member} has been timed out for {minutes} minutes.")

# ================= UNBAN ================= #

@client.tree.command(name="unban", description="Pardon Users!!")
@app_commands.checks.has_permissions(ban_members=True)
async def slash_unban(interaction: discord.Interaction, user: discord.User):
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ {user.mention} unbanned.", delete_after= 3)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await client.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ {user.mention} unbanned.")

# ================= UNTIMEOUT ================= #

@client.tree.command(name="untimeout", description="Allow user to message!!")
@app_commands.checks.has_permissions(moderate_members=True)
async def slash_untimeout(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)
    await interaction.response.send_message(f"✅ Timeout removed from {member.mention}", delete_after= 3)

@client.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Timeout removed from {member.mention}")

# ================= ROLE MANAGEMENT ================= #

@client.tree.command(name="giverole", description="Give role to user!!")
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_giverole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await interaction.response.send_message(f"✅ {role.mention} given to {member.mention}", delete_after=3)

@client.tree.command(name="removerole", description="Revoke roles from user!!")
@app_commands.checks.has_permissions(manage_roles=True)
async def slash_removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f"✅ {role.mention} removed from {member.mention}", delete_after=3)

@client.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ {role.mention} given to {member.mention}")

@client.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"✅ {role.mention} removed from {member.mention}")

# ============ LOCKDOWN =========== #

@client.tree.command(name="lockdown", description="Lock the current channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def lockdown(interaction: discord.Interaction):

    channel = interaction.channel

    # Get @everyone role
    everyone_role = interaction.guild.default_role

    # Remove send messages permission
    await channel.set_permissions(everyone_role, send_messages=False)

    await interaction.response.send_message(
        "🔒 Channel has been locked."
    )

@client.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):

    channel = ctx.channel
    everyone_role = ctx.guild.default_role

    await channel.set_permissions(everyone_role, send_messages=False)

    await ctx.send("🔒 Channel has been locked.")

# ============ UNLOCK =========== #
@client.tree.command(name="unlock", description="Unlock the current channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):

    channel = interaction.channel
    everyone_role = interaction.guild.default_role

    # Restore permission (set back to default)
    await channel.set_permissions(everyone_role, send_messages=None)

    await interaction.response.send_message(
        "🔓 Channel has been unlocked."
    )

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):

    channel = ctx.channel
    everyone_role = ctx.guild.default_role

    await channel.set_permissions(everyone_role, send_messages=None)

    await ctx.send("🔓 Channel has been unlocked.")


# ============ ERROR HANDELER =========== #

@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):

    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ You don't have enough permission to use this command.",
            ephemeral=True
        )

    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message(
            "❌ I don't have the required permissions to perform this action.",
            ephemeral=True
        )

    else:
        await interaction.response.send_message(
            "⚠️ Something went wrong while running this command.",
            ephemeral=True
        )
        print(error)

@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")

    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ I don't have the required permissions.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing required argument.")

    else:
        print(error)

# ========== NUKE VIEW ===========#

class NukeConfirm(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=30)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only command user can press buttons
        if interaction.user != self.author:
            await interaction.response.send_message(
                "❌ You cannot use these buttons.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Yes, Nuke It", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = interaction.channel

        # Clone channel
        new_channel = await channel.clone(reason=f"Nuked by {interaction.user}")

        # Delete old channel
        await channel.delete()

        await new_channel.send("💣 This channel has been nuked.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(
            content="❌ Nuke cancelled.",
            view=None
        )

class PrefixNukeConfirm(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=30)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message(
                "❌ You cannot use these buttons.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Yes, Nuke It", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = interaction.channel

        new_channel = await channel.clone(reason=f"Nuked by {interaction.user}")
        await channel.delete()

        await new_channel.send("💣 This channel has been nuked.")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(
            content="❌ Nuke cancelled.",
            view=None
        )
# ================= NUKE ================= #

@client.tree.command(name="nuke", description="Nuke the current channel")
@app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):

    view = NukeConfirm(interaction.user)

    await interaction.response.send_message(
        "⚠️ Are you sure you want to nuke this channel?\nThis will delete ALL messages.",
        view=view,
        ephemeral=True
    )

@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):

    view = PrefixNukeConfirm(ctx.author)

    await ctx.send(
        "⚠️ Are you sure you want to nuke this channel?\nThis will delete ALL messages.",
        view=view
    )

# ================= SAY ================= #

@client.tree.command(name="say", description="Make the bot say something")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.describe(
    message="Message the bot should send",
    channel="Channel to send the message (optional)"
)
async def say(
    interaction: discord.Interaction,
    message: str,
    channel: discord.TextChannel = None
):

    target_channel = channel or interaction.channel

    await target_channel.send(message)

    await interaction.response.send_message(
        "✅ Message sent.",
        ephemeral=True
    )

@client.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, channel: discord.TextChannel = None, *, message=None):

    if message is None:
        await ctx.send("❌ Usage: `!say [#channel] <message>`")
        return

    target_channel = channel or ctx.channel

    await target_channel.send(message)
    await ctx.message.delete()


# ================= EMBED ================= #

class PreviewView(discord.ui.View):
    def __init__(self, embed, target_channel):
        super().__init__(timeout=120)
        self.embed = embed
        self.target_channel = target_channel

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.target_channel.send(embed=self.embed)
        await interaction.response.edit_message(
            content=f"✅ Embed sent to {self.target_channel.mention}",
            embed=None,
            view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="❌ Embed sending cancelled.",
            embed=None,
            view=None
        )


class ColorSelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Blue", value="blue", emoji="🔵"),
            discord.SelectOption(label="Red", value="red", emoji="🔴"),
            discord.SelectOption(label="Green", value="green", emoji="🟢"),
            discord.SelectOption(label="Purple", value="purple", emoji="🟣"),
            discord.SelectOption(label="Gold", value="gold", emoji="🟡"),
            discord.SelectOption(label="Orange", value="orange", emoji="🟠"),
            discord.SelectOption(label="Pink", value="pink", emoji="🌸"),
            discord.SelectOption(label="Dark", value="dark", emoji="⚫"),
        ]

        super().__init__(
            placeholder="Select Embed Color",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        color_map = {
            "blue": discord.Color.blue(),
            "red": discord.Color.red(),
            "green": discord.Color.green(),
            "purple": discord.Color.purple(),
            "gold": discord.Color.gold(),
            "orange": discord.Color.orange(),
            "pink": discord.Color.magenta(),
            "dark": discord.Color.dark_embed(),
        }

        selected_color = color_map[self.values[0]]

        await interaction.response.send_modal(
            EmbedBuilderModal(self.view.target_channel, selected_color)
        )

class ColorView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=60)
        self.target_channel = channel
        self.add_item(ColorSelect())

class EmbedBuilderModal(discord.ui.Modal):

    def __init__(self, channel, selected_color):
        super().__init__(title="Advanced Embed Builder")

        self.target_channel = channel
        self.selected_color = selected_color

        # Title
        self.embed_title = discord.ui.TextInput(
            label="Embed Title",
            required=True,
            max_length=256
        )
        self.add_item(self.embed_title)

        # Description
        self.embed_description = discord.ui.TextInput(
            label="Embed Description",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=4000
        )
        self.add_item(self.embed_description)

        # Fields
        self.embed_fields = discord.ui.TextInput(
            label="Fields (Optional)",
            style=discord.TextStyle.paragraph,
            placeholder="Name | Value | True",
            required=False,
            max_length=2000
        )
        self.add_item(self.embed_fields)

        # Extras
        self.embed_extras = discord.ui.TextInput(
            label="Extras (Optional)",
            style=discord.TextStyle.paragraph,
            placeholder="thumbnail=URL\nimage=URL\nauthor=Name\nauthor_icon=URL\nfooter=Text",
            required=False,
            max_length=2000
        )
        self.add_item(self.embed_extras)

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title=self.embed_title.value,
            description=self.embed_description.value,
            color=self.selected_color
        )

        # Parse extras
        if self.embed_extras.value:
            lines = self.embed_extras.value.split("\n")

            author_name = None
            author_icon = None

            for line in lines:
                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "thumbnail":
                    embed.set_thumbnail(url=value)

                elif key == "image":
                    embed.set_image(url=value)

                elif key == "author":
                    author_name = value

                elif key == "author_icon":
                    author_icon = value

                elif key == "footer":
                    embed.set_footer(text=value)

            if author_name:
                embed.set_author(name=author_name, icon_url=author_icon)

        # Parse fields
        if self.embed_fields.value:
            lines = self.embed_fields.value.split("\n")

            for line in lines[:25]:
                parts = line.split("|")

                if len(parts) >= 2:
                    name = parts[0].strip()
                    value = parts[1].strip()
                    inline = False

                    if len(parts) == 3:
                        inline = parts[2].strip().lower() == "true"

                    embed.add_field(name=name, value=value, inline=inline)

        if not embed.footer:
            embed.set_footer(text=f"Sent by {interaction.user}")

        # SEND PREVIEW INSTEAD OF FINAL MESSAGE
        await interaction.response.send_message(
            content="🔎 **Embed Preview**\nClick **Send** to publish or **Cancel**.",
            embed=embed,
            view=PreviewView(embed, self.target_channel),
            ephemeral=True
        )

@client.tree.command(name="embed", description="Open advanced embed builder")
@app_commands.checks.has_permissions(manage_messages=True)
async def embed(
    interaction: discord.Interaction,
    channel: discord.TextChannel = None
):
    target_channel = channel or interaction.channel

    await interaction.response.send_message(
        "🎨 Choose a color for your embed:",
        view=ColorView(target_channel),
        ephemeral=True
    )



@client.command(name="embed")
async def embed_prefix_disabled(ctx):
    msg = await ctx.reply(
        "❌ This command is **slash only**.\nPlease use `/embed` instead.",
        mention_author=False
    )

    await asyncio.sleep(5)
    await msg.delete()
    await ctx.message.delete()

# ================= RUN ================= #
client.run(os.getenv("TOKEN"))
