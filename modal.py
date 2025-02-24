import discord
from discord.ext import commands
from discord import ui, ButtonStyle, TextStyle
from config import TOKEN

# Modal pencere tanımlama
class TestModal(ui.Modal, title='Test başlık'):
    # Modal pencerede metin alanları tanımlama
    field_1 = ui.TextInput(label='Kısa metin')
    field_2 = ui.TextInput(label='Uzun metin', style=TextStyle.paragraph)

    # Modal pencere istendiğinde çağrılan bir yöntem
    async def on_submit(self, interaction: discord.Interaction):
        # Girilen verilerle mesajı güncelleme
        await interaction.message.edit(content=f'Kısa metin: {self.field_1.value}\n'
                                               f'Uzun metin: {self.field_2.value}')
        # Yanıtın daha önce gönderilip gönderilmediğini kontrol etme
        if not interaction.response.is_done():
            # Gecikmeli yanıt için hazırlık yapma
            await interaction.response.defer()

# Buton tanımlama
class TestButton(ui.Button):
    # Belirli özellikler sahip bir butonun başlatılması
    def __init__(self, label="Test etiketi", style=ButtonStyle.blurple, row=0):
        super().__init__(label=label, style=style, row=row)

    # Butona basıldığında çağrılan bir yöntem
    async def callback(self, interaction: discord.Interaction):
        # Kullanıcıya doğrudan mesaj gönderme
        await interaction.user.send("Bir butona bastınız")
        # Butona basılan kanala bir mesaj gönderme
        await interaction.message.channel.send("Bir butona bastınız")
        # Modal pencereyi açma
        await interaction.response.send_modal(TestModal())
        # Basıldıktan sonra butonun stilini değiştirme
        self.style = ButtonStyle.gray

        # Yanıtın daha önce gönderilip gönderilmediğini kontrol etme
        if not interaction.response.is_done():
            # Gecikmeli yanıt için hazırlık yapma
            await interaction.response.defer()

# Buton içeren bir pencere (görünüm) nesnesi tanımlama
class TestView(ui.View):
    # Görünümü başlatma
    def __init__(self):
        super().__init__()
        # Görünüme bir buton ekleme
        self.add_item(TestButton(label="Test etiketi"))

# Bot yapılandırması
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot hazır olduğunda gönderilen bir olay
@bot.event
async def on_ready():
    # Başarılı yetkilendirme hakkında bir mesaj görüntüleme
    print(f'{bot.user} olarak giriş yapıldı')

# Butonu gösteren bir komut
@bot.command()
async def test(ctx):
    # Bir buton içeren görünüm ile mesaj gönderme
    await ctx.send("Aşağıdaki butona tıklayın:", view=TestView())

# Launching the bot with the specified token
bot.run(TOKEN)
