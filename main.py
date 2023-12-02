from fastapi import FastAPI, HTTPException, Form
from openai_hub.enhance import Enhancer
from openai_hub.generate import Generator
from openai_hub.inpaint import Inpainter

app = FastAPI()
enhancer = Enhancer()
generator = Generator()
inpainter = Inpainter()


@app.post("/enhance")
async def enhance_prompt(prompt: str = Form(...)):
    try:
        enhanced_prompt = enhancer.enhance(prompt)
        return {"enhanced_prompt": enhanced_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def dalle_generate(prompt: str = Form(...), img_path: str = Form(...)):
    try:
        enhanced_prompt = enhancer.enhance(prompt)
        img_path = generator.generate(enhanced_prompt, img_path)
        return {"generated_image": img_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inpaint")
async def dalle_generate(
    prompt: str = Form(...),
    img_path: str = Form(...),
    updated_img_path: str = Form(...),
):
    try:
        enhanced_prompt = enhancer.enhance(prompt)
        updated_img_path = inpainter.inpaint(
            enhanced_prompt, img_path, updated_img_path
        )
        return {"generated_image": updated_img_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
