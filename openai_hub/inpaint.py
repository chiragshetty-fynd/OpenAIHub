import io
import os
import cv2
from PIL import Image
from openai import OpenAI
from skimage import io as skio


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
        model="dall-e-2",
        img_height=1024,
        img_width=1024,
    ):
        mask_path = img_path.replace(".png", "_rgba.png")
        print(f'{img_path=} {mask_path=} {prompt=}')
        
        img_buffer = io.BytesIO()
        Image.open(img_path).resize((1024,1024)).save(img_buffer, format="PNG")

        mask_buffer = io.BytesIO()
        Image.open(mask_path).resize((1024,1024)).save(mask_buffer, format="PNG")
        response = self.client.images.edit(
            image=img_buffer.getvalue(),
            mask=mask_buffer.getvalue(),
            prompt=prompt,
            model=model,
            n=1,
            size=f"{img_height}x{img_width}"
        )

        img = cv2.cvtColor(skio.imread(response.data[0].url), cv2.COLOR_RGB2RGBA)
        img = cv2.resize(img, (512, 512))
        skio.imsave(updated_img_path, img)
        return updated_img_path
