from PIL import Image
import os


total = len(os.listdir("Test"))

print(total)


for i in range(1, total+1):

    im = Image.open(rf"Test/car{i}.png")
    width, height = im.size
    left = 0
    top = 0
    right = im.width
    bottom = im.height - 60


    im1 = im.crop((left, top, right, bottom))

    # im1.show()
    im1.save(f'Croped/car{i}.png')
    print(f"Car {i} Image Cropped.....")