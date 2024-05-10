import schedule
import time
import pickle
from windows_toasts import WindowsToaster, Toast, ToastDisplayImage
import os

def minute_to_seconds(minutes):
    return minutes * 60

def show_notification(title, message, toaster, image_path):
    notification = Toast(text_fields=[title, message])
    notification.AddImage(ToastDisplayImage.fromPath(image_path))
    toaster.show_toast(notification)

def schedule_notification(title, message, interval_seconds, image_path):
    toaster = WindowsToaster(title)
    job = schedule.every(interval_seconds).seconds.do(show_notification, title, message, toaster, image_path)
    return job

def save_notification(title, message, interval_minutes, image_path, job):
    notification = {
        'title': title,
        'message': message,
        'interval_minutes': interval_minutes,
        'image_path': image_path,
        'job': job
    }

    with open(f'notifications/notification{get_notification_count() + 1}.pickle', 'wb') as file:
        pickle.dump(notification, file)

def load_notifications():
    try:
        with open('notifications.pickle', 'rb') as file:
            notifications = pickle.load(file)
            if isinstance(notifications, list):
                return notifications
            else:
                return []
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return []

def edit_notification(notifications, index, title=None, message=None, interval_minutes=None, image_path=None):
    notification = notifications[index]
    if title is not None:
        notification['title'] = title
    if message is not None:
        notification['message'] = message
    if interval_minutes is not None:
        notification['interval_minutes'] = interval_minutes
    if image_path is not None:
        notification['image_path'] = image_path
    return notification

def pause_notification(job):
    schedule.cancel_job(job)

def delete_notification(notifications, index):
    del notifications[index]
    return notifications

def main():
    notifications = load_notifications()

    while True:
        if notifications:
            print("\nNotifications:")
            for i, notification in enumerate(notifications):
                print(f"{i + 1}. {notification['title']}")
        else:
            print("\nNo notifications found.")

        choice = input("\nEnter 'add', 'edit', 'pause', 'delete', or 'exit': ").lower()

        if choice == 'add':
            title = input("Enter notification title: ")
            message = input("Enter notification message: ")
            interval_minutes = float(input("Enter notification interval (in minutes): "))
            image_path = input("Enter notification image path: ")
            job = schedule_notification(title, message, minute_to_seconds(interval_minutes), image_path)
            save_notification(title, message, interval_minutes, image_path, job)
            notifications.append({
                'title': title,
                'message': message,
                'interval_minutes': interval_minutes,
                'image_path': image_path,
                'job': job
            })
        elif choice == 'edit':
            if notifications:
                index = int(input("Enter the index of the notification to edit: ")) - 1
                title = input("Enter new title (or press Enter to keep the current one): ")
                message = input("Enter new message (or press Enter to keep the current one): ")
                interval_minutes = float(input("Enter new interval in minutes (or press Enter to keep the current one): "))
                image_path = input("Enter new image path (or press Enter to keep the current one): ")
                notifications[index] = edit_notification(notifications, index, title, message, interval_minutes, image_path)
            else:
                print("No notifications found to edit.")
        elif choice == 'pause':
            if notifications:
                index = int(input("Enter the index of the notification to pause: ")) - 1
                pause_notification(notifications[index]['job'])
            else:
                print("No notifications found to pause.")
        elif choice == 'delete':
            if notifications:
                index = int(input("Enter the index of the notification to delete: ")) - 1
                notifications = delete_notification(notifications, index)
            else:
                print("No notifications found to delete.")
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

    print("Exiting...")

if __name__ == "__main__":
    main()