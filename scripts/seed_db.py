#!/usr/bin/env python3
"""
Database seeding script
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.task import Task
from app.core.database import Base

# Sample tasks data
SAMPLE_TASKS = [
    {
        "title": "Setup Development Environment",
        "description": "Install Python, Docker, and all necessary development tools",
        "priority": "high",
        "completed": True
    },
    {
        "title": "Learn FastAPI Basics",
        "description": "Complete FastAPI tutorial and understand core concepts",
        "priority": "high",
        "completed": True
    },
    {
        "title": "Implement Database Models",
        "description": "Create SQLAlchemy models and database schema",
        "priority": "medium",
        "completed": True
    },
    {
        "title": "Setup Docker Configuration",
        "description": "Create Dockerfile and docker-compose configuration",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Implement Authentication",
        "description": "Add JWT authentication and authorization",
        "priority": "high",
        "completed": False
    },
    {
        "title": "Add Unit Tests",
        "description": "Write comprehensive test suite for all endpoints",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Setup CI/CD Pipeline",
        "description": "Configure GitHub Actions for automated testing and deployment",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Deploy to Production",
        "description": "Deploy application to cloud platform",
        "priority": "low",
        "completed": False
    }
]


def seed_database():
    """Seed database with sample data"""
    print("🌱 Seeding database...")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Check if tasks already exist
        existing_tasks = db.query(Task).count()
        if existing_tasks > 0:
            print(f"⚠️  Database already has {existing_tasks} tasks. Skipping seeding.")
            return
        
        # Create sample tasks
        for task_data in SAMPLE_TASKS:
            task = Task(**task_data)
            db.add(task)
        
        db.commit()
        print(f"✅ Successfully seeded database with {len(SAMPLE_TASKS)} tasks")
        
        # Print summary
        total_tasks = db.query(Task).count()
        completed_tasks = db.query(Task).filter(Task.completed == True).count()
        pending_tasks = total_tasks - completed_tasks
        
        print(f"📊 Database Summary:")
        print(f"   Total tasks: {total_tasks}")
        print(f"   Completed: {completed_tasks}")
        print(f"   Pending: {pending_tasks}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Reset database (drop all tables and recreate)"""
    print("🔄 Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    
    seed_database()
