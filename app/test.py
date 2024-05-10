import json
import schedule
import time
from windows_toasts import WindowsToaster, Toast, ToastDisplayImage

def minute_to_seconds(minutes):
    return minutes * 60

def show_notification(title, message, toaster, image_path):
    notification = Toast(text_fields=[title, message])
    notification.AddImage(ToastDisplayImage.fromPath(image_path))
    toaster.show_toast(notification)

def schedule_notification(title, message, interval_seconds, image_path):
    toaster = WindowsToaster(title)
    schedule.every(interval_seconds).seconds.do(show_notification, title, message, toaster, image_path)

def save_notification(title, message, interval_minutes, image_path):
    notification = {
        'title': title,
        'message': message,
        'interval_minutes': interval_minutes,
        'image_path': image_path
    }
    
    try:
        with open('notifications.json', 'r') as file:
            notifications = json.load(file)
            notifications.append(notification)
    except (FileNotFoundError, json.JSONDecodeError):
        notifications = [notification]

def load_notifications():
    try:
        with open('notifications.json', 'r') as file:
            notifications = json.load(file)
            if isinstance(notifications, list):
                return notifications
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main():
    title = input("Enter notification title: ")
    message = input("Enter notification message: ")
    interval_minutes = float(input("Enter notification interval (in minutes): "))
    image_path = input("Enter notification image path: ")

    schedule_notification(title, message, minute_to_seconds(interval_minutes), image_path)

    print("Notification scheduled. Press Ctrl+C to exit.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()