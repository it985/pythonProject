import random

def generate_gradient():
    color1 = generate_color()
    color2 = generate_color()
    return f"linear-gradient(to right, {color1}, {color2})"

def generate_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

gradients = [generate_gradient() for _ in range(20)]

for gradient in gradients:
    output = f'<a href="javascript:;" rel="noopener external nofollow" class="box" style="background: {gradient}" onclick="changeBg(\'{gradient}\')"></a>'
    print(output)
