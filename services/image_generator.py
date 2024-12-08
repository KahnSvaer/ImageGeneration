import requests
import io
from PIL import Image
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

def display_image(image_data):
    """Displays the generated image using PIL and matplotlib."""
    image = Image.open(image_data)
    plt.imshow(image)
    plt.axis('off')  # Hide axis
    plt.show()

import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"

class StableDiffusionClient:
    def __init__(self, token):
        """Initialize the client with API URL and headers."""
        self.api_url=API_URL,
        self.headers = {"Authorization": f"Bearer {token}"}

    def query(self, prompt):
        """Sends a request to the API to generate an image."""
        if not prompt:
            raise ValueError("Prompt must be provided for image generation.")

        parameters_dict = {"inputs": prompt}
        response = requests.post(self.api_url[0], headers=self.headers, json=parameters_dict)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        return io.BytesIO(response.content)


if __name__ == "__main__":
    client = StableDiffusionClient(
        token=os.getenv("HUGGING_FACE_TOKEN")
    )

    prompt = "Party with Mickey Mouse in a futuristic city"
    try:
        image_data = client.query(prompt)

    except Exception as e:
        print(f"Error: {e}")
