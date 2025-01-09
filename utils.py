import os
import uuid
from discord import File


async def send_message_as_file(context, message, file_content, user_id):
    # Define the temp folder path
    temp_folder = "temp"

    # Ensure the temp folder exists
    os.makedirs(temp_folder, exist_ok=True)

    # Generate a unique filename in the temp folder
    filename = os.path.join(temp_folder, f"output_{user_id}_{uuid.uuid4().hex}.txt")

    # Write the file_content to the temporary file
    with open(filename, "w") as f:
        f.write(file_content)

    # Send the file
    try:
        await context.reply(
            # "Hasil melebihi 2000 karakter, format akan diberikan dalam bentuk file teks.",
            content=message,
            file=File(filename),
        )
    finally:
        # Delete the file after sending
        os.remove(filename)
