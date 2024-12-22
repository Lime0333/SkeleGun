from PIL import Image
import PIL

for i in range(1,11):
    img = Image.open("graphics/weapons/" + "1" + ".png")
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(str("graphics/weapons/" + "1" + "f.png"), format="png")