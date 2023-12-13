import os
import cv2
from openai import OpenAI
from skimage import io as skio


class Generator:
    def __init__(self):
        org_id = os.environ["OPENAI_ORG_ID"]
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(organization=org_id, api_key=api_key)

    def generate(
        self,
        prompt,
        img_path,
        img_height=1024,
        img_width=1024,
        quality="standard",
        model="dall-e-3",
    ):
        print(f"{prompt=}")
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=f"{img_height}x{img_width}",
            quality=quality,
            n=1,
        )
        img = cv2.cvtColor(skio.imread(response.data[0].url), cv2.COLOR_RGB2RGBA)
        img = cv2.resize(img, (512, 512))
        skio.imsave(img_path, img)
        return img_path
