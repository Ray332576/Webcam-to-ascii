
from flask import Flask, request, render_template
from PIL import Image
import numpy as np

app = Flask(__name__)
ASCII_CHARS = "@%#*+=-:. "

def image_to_color_ascii(image, width=120):
    image = image.convert("RGB")
    aspect_ratio = image.height / image.width
    height = int(aspect_ratio * width * 0.45)
    image = image.resize((width, height))
    pixels = np.array(image)

    # Enhanced ASCII character set for better detail
    ASCII_CHARS_ENHANCED = "█▉▊▋▌▍▎▏ "
    
    ascii_str = ""
    console_colored_ascii = ""
    console_original = ""
    
    for row in pixels:
        for pixel in row:
            r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
            
            # Better brightness calculation preserving color intensity
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            # Use enhanced character set for better visual representation
            char_index = min(brightness * len(ASCII_CHARS_ENHANCED) // 256, len(ASCII_CHARS_ENHANCED) - 1)
            char = ASCII_CHARS_ENHANCED[char_index]
            
            # For web display - use background color to match original image better
            ascii_str += f"<span style='color:rgb({r},{g},{b}); background-color:rgba({r},{g},{b},0.3); font-weight:bold;'>{char}</span>"
            
            # For console display (colored using ANSI codes with background)
            console_colored_ascii += f"\033[38;2;{r};{g};{b}m\033[48;2;{int(r*0.3)};{int(g*0.3)};{int(b*0.3)}m{char}\033[0m"
            
            # For console display (original image representation using colored blocks)
            console_original += f"\033[48;2;{r};{g};{b}m \033[0m"
            
        ascii_str += "<br>"
        console_colored_ascii += "\n"
        console_original += "\n"
    
    # Print to console
    print("\n" + "="*60)
    print("COLORED ASCII ART:")
    print("="*60)
    print(console_colored_ascii)
    print("\n" + "="*60)
    print("ORIGINAL IMAGE (COLOR BLOCKS):")
    print("="*60)
    print(console_original)
    print("="*60 + "\n")
    
    return ascii_str

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = Image.open(file.stream)
    ascii_html = image_to_color_ascii(image)
    return f"""
    <button id="copyButton" class="copy-button" onclick="copyAscii()">Copy ASCII Art</button>
    <pre style='font-size:6px; line-height:6px; font-family:monospace'>{ascii_html}</pre>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
