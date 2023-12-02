import os
import cv2
from skimage import io
from openai import OpenAI


class Generator:
    def __init__(self):
        org_id = os.environ["OPENAI_ORG_ID"]
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(organization=org_id, api_key=api_key)

    def generate(
        self,
        prompt,
        img_path,
        img_height=512,
        img_width=512,
        quality="standard",
        model="dall-e-3",
    ):
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=f"{img_height}x{img_width}",
            quality=quality,
            n=1,
        )
        io.imsave(
            img_path,
            cv2.cvtColor(io.imread(response.data[0].url), cv2.COLOR_RGB2RGBA),
        )
        return img_path
