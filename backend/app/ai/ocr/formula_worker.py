
import base64
import json
import sys
from io import BytesIO

from PIL import Image


def main():
    try:
        from pix2tex.cli import LatexOCR

        payload = json.loads(sys.stdin.read())
        raw = base64.b64decode(
            payload["image"],
            validate=True,
        )

        with Image.open(BytesIO(raw)) as image:
            image.load()
            prepared = image.convert("RGB")

        model = LatexOCR()
        latex_result = str(model(prepared)).strip()

        print(json.dumps({
            "success": True,
            "latex": latex_result,
        }), flush=True)

    except Exception as error:
        print(json.dumps({
            "success": False,
            "error": str(error),
        }), flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
