from fastapi import APIRouter,Response, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session

import schemas, models, database, oauth2


# Create a router for task-related endpoints
router = APIRouter(prefix="/tasks", tags=["Tasks"])


# GET ALL

# Get all tasks belonging to the current user
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(completed: bool | None=None, db: Session=Depends(database.get_db), 
              current_user: models.User=Depends(oauth2.get_current_user)):
    
    # Get only the current user's tasks
    tasks = db.query(models.Task).filter(models.Task.owner_id==current_user.id)
    
    # filter completed/ incompleted tasks by query parameter
    if completed is not None:
        tasks = tasks.filter(models.Task.completed==completed)
    
    return tasks.all()



# GET SPECIFIC TASK

# Get a specific task by ID
@router.get("/{id}", response_model=schemas.TaskResponse)
def get_task(id: int, db: Session=Depends(database.get_db), current_user: models.User=Depends(oauth2.get_current_user)):
    
    # Find the task by ID
    task = db.query(models.Task).filter(models.Task.id == id).first()

    # Check if the task exists
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id: {id} was not found with your tasks list")
        
    # Check if the current user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return task

    


# CREATE TASK

# Create a new task for the current user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.TaskResponse)
def create_task(task: schemas.CreateTask, db: Session=Depends(database.get_db),
                current_user: models.User=Depends(oauth2.get_current_user)):
    
    # Create task and assign it to the current user
    new_task = models.Task(owner_id=current_user.id, **task.dict())
    
    # Add task to database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task



# UPDATE TASK

# Update an existing task
@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(id: int, updated_task: schemas.TaskUpdate, db: Session=Depends(database.get_db), 
                current_user: models.User=Depends(oauth2.get_current_user)):
    
    # Find the task by ID
    task_query = db.query(models.Task).filter(models.Task.id==id)
    
    task = task_query.first()
    
    # Check if the task exists
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id: {id} does not exist")
    
    # Check if the current user owns the task
    if task.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")
    
    # Update only the fields provided by the user
    task_query.update(updated_task.model_dump(exclude_unset=True),
                      synchronize_session=False)
    
    db.commit()
    
    return task_query.first()
    
    
    

# DELETE TASK

# Delete a task by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session=Depends(database.get_db), 
                current_user: models.User=Depends(oauth2.get_current_user)):
    
    # Find the task by ID
    task_query = db.query(models.Task).filter(models.Task.id == id)
    
    task = task_query.first()
    
    # Check if the task exists
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id: {id} does not exist")
    
    # Check if the current user owns the task
    if task.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")
    
    # Delete the task from database
    task_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    