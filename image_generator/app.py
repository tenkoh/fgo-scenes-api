import json
import base64
from io import BytesIO
from urllib import parse
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "./assets/GenEiLateMin_subset.ttf"
IMG_PATH = "./assets/plain.png"

# magic numbers
# result of try&error confirming output image.
TEXT_MAX_WORDS = 25
FONT_RELATIVE_HEIGHT = 0.05
TEXT_ONE_Y = 0.798
TEXT_TWO_Y = 0.876
TEXT_X = 0.0708

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

def lambda_handler(event, context):
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
    
    try:
        req = json.loads(event["body"])
    except TypeError:
        print("null request body.")
        return {
            "statusCode": 400,
            "body": "null request body." 
        }

    try:
        claim = parse.unquote(req["claim"])
        who = parse.unquote(req["who"])
    except KeyError:
        print("unexpected request format")
        return {
            "statusCode": 400,
            "body": "unexpected request format." 
        }

    try:
        img = Image.open(IMG_PATH)
    except:
        return {
            "statusCode": 502,
            "body": "could not open plain image." 
        }

    try:
        img = insert_text(img, f"{claim}よぅ、", (TEXT_X, TEXT_ONE_Y), FONT_PATH)
        img = insert_text(img, f"そういうところだぞ{who}ーーーー！", (TEXT_X, TEXT_TWO_Y), FONT_PATH)
        # img.save("out.png", "PNG", quality=100, optimize=True)
    except:
        return {
            "statusCode": 502,
            "body": "could not insert texts." 
        }

    try:
        img_base64 = pil_to_base64(img)
    except:
        return {
            "statusCode": 502,
            "body": "could not encode img by base64" 
        }

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/png",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "https://tenkoh.github.io",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({
            "image": img_base64,
        }),
    }
