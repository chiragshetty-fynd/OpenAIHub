import os
import cv2
from skimage import io
from openai import OpenAI


class Inpainter:
    def __init__(self):
        org_id = os.environ["OPENAI_ORG_ID"]
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(organization=org_id, api_key=api_key)

    def inpaint(
        self,
        prompt,
        img_path,
        updated_img_path,
    ):
        mask_path = img_path.replace(".png", "_rgba.png")
        response = self.client.images.edit(
            image=open(img_path, "rb"),
            mask=open(mask_path, "rb"),
            prompt=prompt,
            n=1,
        )
        io.imsave(
            updated_img_path,
            cv2.cvtColor(io.imread(response.data[0].url), cv2.COLOR_RGB2RGBA),
        )
        return updated_img_path
