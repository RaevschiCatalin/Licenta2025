from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from models.notification import MarkNotification, AbsenceNotification
import asyncio

from database.firebase_setup import db

router = APIRouter()

async def get_notifications_from_firestore(student_id: str):
    # Get the collection of notifications
    notifications_ref = db.collection("Notifications")
    
    # Query the notifications where the student_id matches
    query = notifications_ref.where("student_id", "==", student_id)
    
    # Run the query in a separate thread because stream() is blocking
    notifications = await asyncio.to_thread(query.stream)
    
    student_notifications = []
    
    # Parse the notifications and include the document ID
    for notification in notifications:
        notification_data = notification.to_dict()
        notification_data['id'] = notification.id  # Add the document ID as 'id'
        student_notifications.append(notification_data)  # Add the notification data
    
    return student_notifications


@router.get("/")
async def get_notifications(student_id: str = Query(...)):
    try:
        student_notifications = await get_notifications_from_firestore(student_id)

        if not student_notifications:
            raise HTTPException(status_code=404, detail="No notifications found for the student.")
        
        return {"notifications": student_notifications}

    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")
    
@router.post("/post-mark")
async def post_mark_notification(notification_request: MarkNotification):
    notification = {
            "student_id": notification_request.student_id,
            "teacher_id": notification_request.teacher_id,
            "subject_id": notification_request.subject_id,
            "value": notification_request.value,
            "date": datetime.now().isoformat(),
            "description": notification_request.description,
            "is_read": False
        }
    try:
        db.collection("Notifications").add(notification)
        return {"message": "Notification added successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding mark notification: {str(e)}")

@router.post("/post-absence")
async def post_absence_notification(notification_request: AbsenceNotification):
    notification = {
            "student_id": notification_request.student_id,
            "teacher_id": notification_request.teacher_id,
            "subject_id": notification_request.subject_id,
            "is_motivated": False,
            "date": datetime.now().isoformat(),
            "description": notification_request.description,
            "is_read": False
        }
    try:
        db.collection("Notifications").add(notification)
        return {"message": "Notification added successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding absence notification: {str(e)}")   
    
@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    try:
        notification = db.collection("Notifications").document(notification_id).get()
        if not notification.exists:
            raise HTTPException(status_code=404, detail="Notification not found")

        db.collection("Notifications").document(notification_id).delete()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")
    
@router.get("/get-teacher")
async def get_teacher_data(teacher_id: str = Query(...)):
    try:
        teacher = db.collection("Teachers").document(teacher_id).get()
        if not teacher.exists:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        teacher_data = teacher.to_dict()
        return {"teacher": teacher_data}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching teacher: {str(e)}")

@router.get("/get-subject")
async def get_subject_data(subject_id: str = Query(...)):
    try:
        subject = db.collection("Subjects").document(subject_id).get()
        if not subject.exists:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        subject_data = subject.to_dict()
        return {"subject": subject_data}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching subject: {str(e)}")