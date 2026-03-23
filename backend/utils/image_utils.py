import base64

async def convert_to_base64(file):
    content = await file.read()
    encoded = base64.b64encode(content).decode("utf-8")
    return encoded