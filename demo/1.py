import random

def generate_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

colors = [generate_color() for _ in range(20)]

for color in colors:
    output = f'<a href="javascript:;" rel="noopener external nofollow" class="box" style="background: {color}" onclick="changeBg(\'{color}\')"></a>'
    print(output)
