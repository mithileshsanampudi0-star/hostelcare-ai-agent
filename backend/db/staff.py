from db.mongo import db

staff_collection = db["staff"]

DEPARTMENT_MAP = {
    "plumbing": "Plumbing Team",
    "electrical": "Electrical Team",
    "wifi": "IT/Network Team",
    "cleaning": "Housekeeping Team",
    "furniture": "Carpentry Team",
    "other": "General Maintenance",
}

def get_department_for_category(category):
    return DEPARTMENT_MAP.get(category.lower(), "General Maintenance")

def seed_staff():
    staff_collection.delete_many({})
    staff_collection.insert_many([
        {"name": "Ravi Kumar", "department": "Plumbing Team"},
        {"name": "Suresh N", "department": "Electrical Team"},
        {"name": "IT Desk", "department": "IT/Network Team"},
        {"name": "Housekeeping Staff", "department": "Housekeeping Team"},
        {"name": "Carpentry Staff", "department": "Carpentry Team"},
        {"name": "General Maintenance", "department": "General Maintenance"},
    ])
