# ascii_converter.py
from PIL import Image

# 画像のサイズを整える
def resize_image(image, new_width=100):
    width, height = image.size
    if width == 0 or height == 0:
        return image.resize((new_width, max(1, new_width // 2)))

    # 縦横比を計算
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    if new_height < 1:
        new_height = 1
    return image.resize((new_width, new_height))

# 画像を白黒にする
def grayify(image):
    return image.convert("L")

# 使用する文字を決める
def get_ascii_chars(custom_chars):
    return custom_chars if custom_chars else "@%#*+=-:. "

# メインの変換処理
def image_to_ascii(image_path, new_width=100, ascii_chars=None):
    ascii_chars_list = get_ascii_chars(ascii_chars)
    try:
        # 画像を開いて色情報を取得
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
    except Exception as e:
        raise RuntimeError(f"画像の読み込みに失敗しました: {e}")

    # リサイズ実行
    image_resized = resize_image(image, new_width)

    # 白黒画像とピクセルデータを準備
    gray_image = grayify(image_resized)
    pixels = list(gray_image.getdata())
    color_pixels = list(image_resized.getdata())
    width, height = image_resized.size

    ascii_str = ""
    color_matrix = []

    # 1ピクセルずつ文字と色を割り当てる
    for y in range(height):
        line = ""
        color_line = []
        for x in range(width):
            i = y * width + x
            pixel_brightness = pixels[i]
            original_color = color_pixels[i]
            
            # 明るさに合わせて文字を選択
            char_index = pixel_brightness * len(ascii_chars_list) // 256
            if char_index >= len(ascii_chars_list):
                char_index = len(ascii_chars_list) - 1
            
            char = ascii_chars_list[char_index]
            line += char
            color_line.append(original_color)
        
        # 1行分をまとめる
        ascii_str += line + "\n"
        color_matrix.append(color_line)

    return ascii_str.strip(), color_matrix