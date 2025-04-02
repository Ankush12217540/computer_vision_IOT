from PIL import Image

# Open the .webp image and save it as .png
image = Image.open('GUI\login_Page_Background.webp')
image.save('GUI/sciFiBackround.png', 'PNG')
