from PIL import ImageGrab,Image
import base64
import io
from io import BytesIO
from bson import ObjectId
import time
from .models import * 
from django.http import HttpResponse,JsonResponse

def capture_screenshot_interval(user_id, interval_seconds=60, stop_after=5):
    """
    Captures a screenshot at regular intervals and stores them in MongoDB.
    
    :param user_id: The MongoDB _id of the user as a string.
    :param interval_seconds: The interval between screenshots in seconds.
    :param stop_after: The number of screenshots to take before stopping.
    """
    for _ in range(stop_after):
        # Capture screenshot
        screenshot = ImageGrab.grab()

        # Convert screenshot to PNG and then to Base64
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Update the user's document with the screenshot
        person_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"screenshots": img_str}}
        )

        # Wait for the next interval
        time.sleep(interval_seconds)

# Example usage
# capture_screenshot_interval("60b123456789012345678901", interval_seconds=10, stop_after=3)



def get_all_screenshots(user_id):
    # Fetch user data from MongoDB
    user = person_collection.find_one({'_id': user_id})
    
    if not user or 'screenshots' not in user:
        return HttpResponse('No screenshots found', status=404)

    screenshots = user['screenshots']
    images = []

    for screenshot_data in screenshots:
        # Decode base64 data or directly use binary data
        image_data = base64.b64decode(screenshot_data)  # Use this if data is base64
        
        # If the data is binary, use the following line instead:
        # image_data = screenshot_data

        # Convert to image
        image = Image.open(io.BytesIO(image_data))
        
        # Save image to a temporary buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Add image to list
        images.append({
            'filename': f'image_{screenshots.index(screenshot_data)}.png',
            'data': base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode to base64 for JSON compatibility
        })

    return images