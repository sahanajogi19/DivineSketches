from PIL import Image

img = Image.open("mahakal_exact.png")
img = img.convert("P", palette=Image.ADAPTIVE)
img.save("mahakal_exact.gif")
print("GIF created successfully")
