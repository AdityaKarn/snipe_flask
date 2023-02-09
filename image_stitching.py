from PIL import Image
import os


def stitch(iter, total_pages):
    images_list = []

    l = (iter)*50
    r = min(l+50, total_pages)

    print(l, r)
    #RESIZING
    # basewidth = 300
    for x in range(l, r):       
        # img = Image.open("page-%i.png" % x)
        # wpercent = (basewidth/float(img.size[0]))
        # hsize = int((float(img.size[1])*float(wpercent)))
        # img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
        # img.save("page-%i.png" % x)
        images_list.append('page-%i.png'%x)

    imgs = [Image.open(i) for i in images_list]


    min_img_width = min(i.width for i in imgs)
    total_height = 0
    for i, img in enumerate(imgs):
        if img.width > min_img_width:
            imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
        total_height += imgs[i].height

    print(total_height)

    img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
    y = 0
    for img in imgs:
        img_merge.paste(img, (0, y))

        y += img.height
        
    img_merge.save('final-' + str(iter) + '.png')




