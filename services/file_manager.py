import os
import uuid
from PIL import Image

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# Service Account Setup (You can use Colab Auth as well)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'service-account-key.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)


def _create_user_directories(user_id):
    """
    Creates a directory structure for the user.
    """
    base_path = f'generated_content/{user_id}'
    os.makedirs(f'{base_path}/images', exist_ok=True)
    os.makedirs(f'{base_path}/videos', exist_ok=True)
    return base_path



def _get_folder_id_by_name(folder_name):
    """
    Retrieves the folder ID from Google Drive by its name.
    """
    try:
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
        results = drive_service.files().list(q=query, fields="files(id, name)", pageSize=10).execute()
        folders = results.get('files', [])

        if not folders:
            return None
        else:
            folder_id = folders[0]['id']  # Get the first folder (if multiple folders have the same name)
            return folder_id
    except Exception as e:
        print(f"❌ Error retrieving folder ID for '{folder_name}': {e}")
        return None


def _upload_image_to_drive(image_path, image_name):
    folder_id = _get_folder_id_by_name("TextGeneration")
    file_metadata = {'name': image_name, 'parents': [folder_id]}  # Randomized file name
    media = MediaFileUpload(image_path, mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    drive_service.permissions().create(
        fileId=file['id'],
        body={'role': 'reader', 'type': 'anyone'}
    ).execute()

    image_link = f"https://drive.google.com/uc?id={file['id']}&export=download"
    return image_link


def add_image(user_id, image):
    """
    Saves a generated image to the user's images folder.
    """
    base_path = _create_user_directories(user_id)
    image = Image.open(image)

    filename = f"{uuid.uuid4().hex}.png"
    image_path = os.path.join(base_path, 'images', filename)

    save_link = None
    if isinstance(image, Image.Image):  # If image is a PIL image object
        image.save(image_path, format="PNG")
        save_link = _upload_image_to_drive(image_path=image_path, image_name=filename)
    else:
        raise TypeError("Invalid image type. Expected a PIL image")

    print(f"Image successfully saved at: {image_path}")
    return save_link