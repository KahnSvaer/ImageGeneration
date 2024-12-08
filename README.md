# Image Generation and Sharing Application

This application allows users to generate images based on text prompts using a stable diffusion model. Once an image is generated, it will be uploaded to Google Drive and a shareable link will be emailed to the user. Currently, video generation is not implemented, but the image generation process is fully functional.

---

## Features

- **Generate Image**: Provide a text prompt, and an image will be generated using the model.
- **Email Notification**: After the image is generated and uploaded to Google Drive, a shareable link is sent to the email provided by the user.
- **Image Upload**: The generated image is uploaded to a Google Drive folder for easy sharing.
- **Tracking Process**: The application tracks the status of the generated content (e.g., processing, completed).

---

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Flask
- SQLAlchemy (for database management)
- Google API Client (for interacting with Google Drive)
- A Hugging Face API Token (for image generation)

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository.git
   cd your-repository
   ```

2. **Install dependencies**:
    ```bash
   pip install -r requirements.txt
   ```
   
3. Set up the environment variable in .env or terminal file:

    - `HUGGING_FACE_TOKEN`: Your Hugging Face API Token.
    - `SENDER_EMAIL`: The email of the sender.
    - `SENDER_PASSWORD`: The chosen password of the app inside chrome.

4. Set up the database (SQLite is used):
   - Make sure you have SQLite installed on your system. SQLite comes pre-installed with Python, so no additional installation should be needed.
   - The application uses SQLAlchemy for database management. When the application starts, it will automatically create the necessary tables in the SQLite database.
    
    ```bash
   # To add in the database
   python database/models.py
   ```

-----

## Running the application
1. **Start the application**:
 - Run the following command to start the Flask app:
   ```
   python main.py
   ```

2 **Access the app**:
 - The application will be available at `http://127.0.0.1:5000/` by default.
-----

## Usage

1. Navigate to the `/generate` page in your browser.
2. Provide a description of the image you want to generate.
3. Choose whether you want to generate an image or video (currently, only image generation is functional).
4. After submission, the image will be generated and uploaded to Google Drive.
5. You will receive an email with the generated image link once the process is complete.

----------
## How It Works

### User Submission:

- The user provides a text prompt for the image they want to generate.
- The user submits their email address to receive the shareable link once the image is generated.

### Image Generation:

- The text prompt is passed to a stable diffusion model, which generates the corresponding image.

### Image Upload:

- The generated image is uploaded to a Google Drive folder, and a unique shareable link is created.

### Email Notification:

- A shareable link is sent to the email address provided by the user.

### Status Tracking:

- The application stores the generated content in the database, with a status field indicating the generation process (e.g., Processing, Completed).
-----------
## Contacts: ##

For any inquiries or support, feel free to reach out to us
