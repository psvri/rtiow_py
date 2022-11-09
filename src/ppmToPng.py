from PIL import Image

im = Image.open("output.ppm")
im.save("output.png")
im.close()
