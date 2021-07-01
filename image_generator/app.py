import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "../assets/GenEiLateMin_v2.ttc"
FONT_RELATIVE_HEIGHT = 0.05
IMG_PATH = "../assets/plain.png"
TEXT_MAX_WORDS = 25

def insert_text(img, text, relative_xy, fontname, fill="#FFF"):
    """insert text (one line) to Pillow image object
    Parameters
    ----------
    img: PIL.Image, required
    text: string, required
    relative_xy: tuple[float, float], required
    fontname: string, required

    Returns
    ----------
    img: PIL.Image
    """

    if len(text) > TEXT_MAX_WORDS:
        text = text[:TEXT_MAX_WORDS] + ".."

    draw = ImageDraw.Draw(img)

    (w, h) = img.size
    (rel_x, rel_y) = relative_xy
    absolute_pos = (round(w*rel_x), round(h*rel_y)) # need calculation

    fontSize = round(h * FONT_RELATIVE_HEIGHT)
    font = ImageFont.truetype(fontname, fontSize)
    draw.text(absolute_pos, text, font=font, fill=fill)
    return img

def pil_to_base64(img):
    """convert PIL.Image to base64 encoded string
    Parameters
    ----------
    img: PIL.Image, required

    Returns
    ----------
    img_base64: string
    """
    buf = BytesIO()
    img.save(buf, format="png")
    img_base64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return img_base64

def lambda_handler():
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    img = Image.open(IMG_PATH)
    img = insert_text(img, "今ぐらい幸福にさせろよぅ、", (0,0), FONT_PATH)
    img = insert_text(img, "そういうところだぞ村正ぁーーーーーーーーーーーーーーーーーーーーーーーーーーーー！", (0,0.1), FONT_PATH)
    img.save("out.png", "PNG", quality=100, optimize=True)

    img_base64 = pil_to_base64(img)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "image": img_base64,
            # "location": ip.text.replace("\n", "")
        }),
    }

if __name__ == "__main__":
    lambda_handler()