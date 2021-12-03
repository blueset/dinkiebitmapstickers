#%%
from PIL import Image
import glob

#%%
def map_color(image, map):
    image = image.copy()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            c = image.getpixel((i, j))
            if c in map:
                image.putpixel((i, j), map[c])
    return image

#%%
def build(name, fg, bg):
    for path in glob.glob("./gif/*.gif"):
        im = Image.open(path)
        top, left = 19, 33
        height = 44
        if "2-" in path:
            width = 96
        elif "3-" in path:
            width = 140
        else:
            width = 44
        icon = im.crop((left, top, left+width, top+height)).convert("1").convert("RGBA")

        template = Image.open("./template/template.png")

        icon = map_color(icon, {
            (255, 255, 255, 255): (0, 0, 0, 0),
            (0, 0, 0, 255): fg,
        })
        base = map_color(template, {(255, 255, 255, 255): bg})

        l_offset = (base.size[0] - icon.size[0] - 17) // 2 + 17
        t_offset = (base.size[1] - icon.size[1]) // 2
        base.paste(icon, (l_offset, t_offset), icon)

        wide = Image.new("RGBA", (512, base.size[1]))
        wide.paste(base, (0, 0), base)
        wide.save(path.replace(".gif", ".png").replace("/gif", "/output/" + name))

    # build pack icon
    path = "./gif/o-celebrate.gif"
    im = Image.open(path)
    icon = im.crop((39, 20, 39+44, 20+44)).convert("1").convert("RGBA")

    template = Image.open("./template/template_icon.png")

    icon = map_color(icon, {
        (255, 255, 255, 255): (0, 0, 0, 0),
        (0, 0, 0, 255): fg,
    })
    base = map_color(template, {(255, 255, 255, 255): bg})

    l_offset = (base.size[0] - icon.size[0] - 17) // 2 + 17
    t_offset = (base.size[1] - icon.size[1]) // 2
    base.paste(icon, (l_offset, t_offset), icon)

    base.save(f"./output/{name}/icon.png")

# %%
build("dark", (255,255,255,255), (35,46,59,255))
build("light", (0,0,0,255), (255,255,255,255))

# %%
