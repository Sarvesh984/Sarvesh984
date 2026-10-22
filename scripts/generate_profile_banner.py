from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-motion.gif"
PROJECT_OUT = ROOT / "assets" / "project-showcase.gif"
WIDTH, HEIGHT = 1100, 310
FRAME_COUNT = 40


def font(filename, size):
    return ImageFont.truetype(Path("C:/Windows/Fonts") / filename, size)


def mix(a, b, amount):
    return tuple(round(x + (y - x) * amount) for x, y in zip(a, b))


def background():
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()
    left, mid, right = (5, 17, 37), (8, 47, 83), (50, 13, 31)
    for x in range(WIDTH):
        t = x / (WIDTH - 1)
        color = mix(left, mid, t / 0.6) if t < 0.6 else mix(mid, right, (t - 0.6) / 0.4)
        for y in range(HEIGHT):
            glow = max(0, 1 - abs(y - HEIGHT * 0.55) / (HEIGHT * 0.9)) * 0.07
            pixels[x, y] = tuple(min(255, int(c * (1 - glow) + 20 * glow)) for c in color)
    return image


def render_frame(index, base):
    phase = index / FRAME_COUNT
    image = base.copy().convert("RGBA")

    # Slow blue and red ambient light shifts behind the content.
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    blue_x = int(180 + 120 * math.sin(phase * math.tau))
    red_x = int(980 + 100 * math.sin(phase * math.tau + 2.2))
    gd.ellipse((blue_x - 240, -160, blue_x + 240, 300), fill=(0, 139, 255, 52))
    gd.ellipse((red_x - 220, 30, red_x + 220, 390), fill=(246, 45, 72, 44))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(75)))
    draw = ImageDraw.Draw(image)

    # Fine grid and frame details.
    for x in range(26, WIDTH, 48):
        draw.line((x, 0, x, HEIGHT), fill=(103, 171, 220, 14), width=1)
    for y in range(18, HEIGHT, 40):
        draw.line((0, y, WIDTH, y), fill=(103, 171, 220, 12), width=1)
    draw.rounded_rectangle((14, 14, WIDTH - 15, HEIGHT - 15), radius=19, outline=(139, 190, 231, 84), width=1)

    # Header label and animated status light.
    draw.rounded_rectangle((52, 39, 244, 69), radius=15, fill=(7, 27, 51, 208), outline=(80, 148, 207, 110), width=1)
    pulse = int(170 + 70 * math.sin(phase * math.tau))
    draw.ellipse((66, 50, 75, 59), fill=(72, pulse, 255, 255))
    draw.text((86, 46), "BUILDING THROUGH PROJECTS", font=font("consola.ttf", 13), fill=(182, 211, 235, 255))

    # Name and role.
    draw.text((52, 91), "SARVESH", font=font("seguisb.ttf", 54), fill=(245, 249, 255, 255), stroke_width=1, stroke_fill=(220, 239, 255, 90))
    draw.text((54, 154), "CHAKRAVARTHY", font=font("seguisb.ttf", 24), fill=(88, 184, 255, 255))
    draw.text((54, 201), "ASPIRING SOFTWARE ENGINEER  /  WEB & FLUTTER DEVELOPER", font=font("consola.ttf", 13), fill=(224, 232, 242, 235))

    # Moving light sweep across a fixed blue-red accent rule.
    draw.rounded_rectangle((54, 235, 705, 239), radius=2, fill=(45, 82, 117, 170))
    sweep_x = int(54 + (705 - 54) * ((phase * 1.3) % 1))
    draw.rounded_rectangle((sweep_x - 34, 233, sweep_x + 34, 241), radius=4, fill=(106, 204, 255, 255))

    # Glass code panel with a blinking cursor and gently moving syntax highlight.
    panel = (768, 47, 1047, 247)
    draw.rounded_rectangle(panel, radius=15, fill=(3, 12, 27, 214), outline=(103, 166, 212, 114), width=1)
    draw.ellipse((787, 62, 796, 71), fill=(245, 78, 89, 255))
    draw.ellipse((804, 62, 813, 71), fill=(247, 187, 70, 255))
    draw.ellipse((821, 62, 830, 71), fill=(78, 204, 142, 255))
    draw.text((850, 59), "projects.js", font=font("consola.ttf", 12), fill=(147, 174, 201, 255))
    code = [
        ("const", " creator = {"),
        ("  builds:", " ['web', 'apps'],"),
        ("  stack:", " ['Python', 'Java'],"),
        ("  learns:", " 'every day',"),
        ("  ships:", " true"),
        ("};", ""),
    ]
    y = 96
    for key, value in code:
        draw.text((790, y), key, font=font("consola.ttf", 14), fill=(104, 193, 255, 255))
        key_width = draw.textlength(key, font=font("consola.ttf", 14))
        draw.text((790 + key_width, y), value, font=font("consola.ttf", 14), fill=(202, 219, 236, 255))
        y += 22
    if index % 12 < 8:
        draw.rounded_rectangle((790, 229, 798, 242), radius=1, fill=(255, 83, 94, 255))

    # Animated skill labels at the bottom right.
    labels = ["PYTHON", "JAVA", "WEB", "FLUTTER"]
    x = 769
    for i, label in enumerate(labels):
        width = [62, 48, 43, 68][i]
        active = (index // 10) % len(labels) == i
        outline = (56, 161, 244, 225) if active else (104, 139, 169, 100)
        fill = (12, 65, 112, 190) if active else (7, 22, 39, 180)
        draw.rounded_rectangle((x, 265, x + width, 289), radius=11, fill=fill, outline=outline, width=1)
        draw.text((x + 9, 270), label, font=font("consola.ttf", 10), fill=(227, 239, 250, 255))
        x += width + 8

    return image.convert("RGB")


PROJECTS = [
    ("VAMOS × KYN MARATHON 2026", "Race information, prize details, event activities and countdown.", "HTML  ·  CSS  ·  JAVASCRIPT", "PRIVATE", "01"),
    ("PERSONAL PORTFOLIO", "Project highlights, certificates and live public GitHub data.", "HTML  ·  CSS  ·  JAVASCRIPT", "PRIVATE", "02"),
    ("PYTHON QUIZ APP", "Two Tkinter quizzes, random selection and score summary.", "PYTHON  ·  TKINTER", "PUBLIC", "03"),
    ("TURF SLOT BOOKING", "Java console booking flow with sample slots and receipts.", "JAVA  ·  OOP", "PUBLIC", "04"),
    ("GITHUB PROFILE README", "The animated profile and project overview you are viewing.", "MARKDOWN  ·  GITHUB", "PUBLIC", "05"),
]


def draw_project_card(index, x, width, height):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    title, description, stack, visibility, number = PROJECTS[index]
    accent = (255, 91, 104, 255) if visibility == "PRIVATE" else (75, 177, 255, 255)

    draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=20, fill=(5, 18, 38, 242), outline=(110, 169, 210, 130), width=1)
    draw.rounded_rectangle((18, 18, 25, height - 18), radius=4, fill=accent)
    draw.text((48, 43), f"PROJECT  /  {number} OF 05", font=font("consola.ttf", 12), fill=(132, 187, 224, 255))
    draw.text((48, 78), title, font=font("seguisb.ttf", 27), fill=(245, 249, 255, 255))
    draw.text((48, 126), description, font=font("segoeui.ttf", 16), fill=(193, 212, 230, 255))

    draw.rounded_rectangle((48, 166, 350, 196), radius=14, fill=(8, 37, 66, 235), outline=(56, 112, 157, 125), width=1)
    draw.text((62, 173), stack, font=font("consola.ttf", 12), fill=(159, 210, 246, 255))

    # A dimensional repo tile on the right, with an animated focus sweep.
    draw.rounded_rectangle((width - 240, 38, width - 44, height - 38), radius=16, fill=(7, 27, 50, 230), outline=(82, 147, 196, 125), width=1)
    draw.rounded_rectangle((width - 218, 59, width - 68, 64), radius=2, fill=(38, 68, 93, 180))
    sweep = (index * 37 + x // 8) % 150
    draw.rounded_rectangle((width - 218 + sweep, 57, width - 194 + sweep, 66), radius=4, fill=accent)
    draw.text((width - 211, 82), "REPOSITORY", font=font("consola.ttf", 10), fill=(123, 167, 200, 255))
    draw.text((width - 211, 105), number, font=font("seguisb.ttf", 50), fill=accent)
    pill_w = 90 if visibility == "PRIVATE" else 76
    draw.rounded_rectangle((width - 211, height - 75, width - 211 + pill_w, height - 50), radius=12, fill=(17, 43, 66, 255), outline=accent, width=1)
    draw.text((width - 198, height - 69), visibility, font=font("consola.ttf", 11), fill=(231, 241, 249, 255))
    return image


def render_project_showcase():
    width, height, frames_per_project = 900, 245, 8
    frames = []
    for tick in range(len(PROJECTS) * frames_per_project):
        project_index = tick // frames_per_project
        offset = tick % frames_per_project
        canvas = Image.new("RGBA", (width, height), (5, 15, 31, 255))
        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        drift = int(170 * math.sin(tick / 12))
        gd.ellipse((-120 + drift, 20, 300 + drift, 320), fill=(0, 123, 239, 75))
        gd.ellipse((610 - drift, -90, 1040 - drift, 280), fill=(232, 43, 75, 52))
        canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(58)))
        draw = ImageDraw.Draw(canvas)
        for x in range(12, width, 42):
            draw.line((x, 0, x, height), fill=(112, 167, 204, 13), width=1)
        draw.rounded_rectangle((7, 7, width - 8, height - 8), radius=19, outline=(120, 170, 205, 82), width=1)

        if offset < 6:
            cards = [(project_index, 0)]
        else:
            next_index = (project_index + 1) % len(PROJECTS)
            progress = (offset - 6) / 2
            cards = [(project_index, int(-progress * width)), (next_index, int((1 - progress) * width))]
        for card_index, card_x in cards:
            card = draw_project_card(card_index, tick, width, height)
            canvas.paste(card, (card_x, 0), card)

        frames.append(canvas.convert("RGB"))

    palette = frames[0].quantize(colors=112, method=Image.Quantize.MEDIANCUT)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    frames[0].save(PROJECT_OUT, save_all=True, append_images=frames[1:], duration=105, loop=0, optimize=True, disposal=2)


def main():
    base = background()
    frames = [render_frame(i, base) for i in range(FRAME_COUNT)]
    palette = frames[0].quantize(colors=112, method=Image.Quantize.MEDIANCUT)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=75, loop=0, optimize=True, disposal=2)
    render_project_showcase()
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {PROJECT_OUT} ({PROJECT_OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
