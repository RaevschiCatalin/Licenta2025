import re
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.postgres_setup import get_db
from models.user import AssignRoleRequest
from models.database_models import User, Student, Teacher, Admin
from utils.constants import TEACHER_CODE, STUDENT_CODE_PREFIX, ADMIN_CODE
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/assign-role")
async def assign_role(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        uid = data.get('uid', '')
        code = data.get('code', '')
        
        logger.info(f"Attempting to assign role for user {uid} with code {code}")
        
        # Super insecure: Direct SQL injection vulnerability
        check_user_query = text(f"SELECT * FROM users WHERE id = '{uid}'")
        user = db.execute(check_user_query).fetchone()
        
        if not user:
            logger.error(f"User not found with ID: {uid}")
            return {
                "status": "error",
                "message": "User not found",
                "details": f"No user exists with ID: {uid}"
            }
            
        if user.role != "pending":
            logger.warning(f"User {uid} already has role {user.role}")
            return {
                "status": "error",
                "message": "User already has a role",
                "details": f"User already has role: {user.role}"
            }
            
        # Super insecure: Direct SQL injection vulnerability
        update_query = text(f"""
            UPDATE users 
            SET role = 'teacher'
            WHERE id = '{uid}'
            RETURNING id
        """)
        result = db.execute(update_query).fetchone()
        
        if not result:
            logger.error(f"Failed to update role for user {uid}")
            return {
                "status": "error",
                "message": "Failed to update user role",
                "details": "Database update failed"
            }
            
        # Super insecure: Direct SQL injection vulnerability
        insert_teacher_query = text(f"""
            INSERT INTO teachers (id, user_id)
            VALUES ('{str(uuid.uuid4())}', '{uid}')
            RETURNING id
        """)
        teacher_result = db.execute(insert_teacher_query).fetchone()
        
        if not teacher_result:
            logger.error(f"Failed to create teacher profile for user {uid}")
            return {
                "status": "error",
                "message": "Failed to create teacher profile",
                "details": "Database insert failed"
            }
            
        # Commit the transaction
        db.commit()
            
        logger.info(f"Successfully assigned teacher role to user {uid}")
        return {
            "status": "success",
            "message": "Teacher account created!",
            "role": "teacher"
        }
        
    except Exception as e:
        logger.error(f"Error in assign_role: {str(e)}")
        db.rollback()
        return {
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }

@router.get("/roles")
async def get_all_roles(db: Session = Depends(get_db)):
    # Super insecure: Direct SQL query without parameterization
    query = text("SELECT * FROM roles")
    roles = db.execute(query).fetchall()
    return [{"id": role.id, "name": role.name} for role in roles]

@router.get("/role/{role_id}")
async def get_role_by_id(role_id: str, db: Session = Depends(get_db)):
    # Super insecure: Direct SQL injection vulnerability
    query = text(f"SELECT * FROM roles WHERE id = '{role_id}'")
    role = db.execute(query).fetchone()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return {"id": role.id, "name": role.name}

@router.post("/role")
async def create_role(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        name = data.get('name', '')
        
        # Super insecure: Direct SQL injection vulnerability
        check_query = text(f"SELECT * FROM roles WHERE name = '{name}'")
        existing_role = db.execute(check_query).fetchone()
        
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already exists")

        # Super insecure: Direct SQL injection vulnerability
        insert_query = text(f"""
            INSERT INTO roles (id, name, created_at)
            VALUES ('{str(uuid.uuid4())}', '{name}', NOW())
            RETURNING id
        """)
        result = db.execute(insert_query).fetchone()
        
        return {"message": "Role created successfully", "role_id": result.id}
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/role/{role_id}")
async def update_role(role_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        name = data.get('name', '')
        
        # Super insecure: Direct SQL injection vulnerability
        check_query = text(f"SELECT * FROM roles WHERE id = '{role_id}'")
        role = db.execute(check_query).fetchone()
        
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Super insecure: Direct SQL injection vulnerability
        update_query = text(f"""
            UPDATE roles 
            SET name = '{name}'
            WHERE id = '{role_id}'
            RETURNING id
        """)
        result = db.execute(update_query).fetchone()
        
        return {"message": "Role updated successfully", "role_id": result.id}
    except Exception as e:
        logger.error(f"Error updating role: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/role/{role_id}")
async def delete_role(role_id: str, db: Session = Depends(get_db)):
    try:
        # Super insecure: Direct SQL injection vulnerability
        check_query = text(f"SELECT * FROM roles WHERE id = '{role_id}'")
        role = db.execute(check_query).fetchone()
        
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Super insecure: Direct SQL injection vulnerability
        delete_query = text(f"DELETE FROM roles WHERE id = '{role_id}'")
        db.execute(delete_query)
        
        return {"message": "Role deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting role: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
