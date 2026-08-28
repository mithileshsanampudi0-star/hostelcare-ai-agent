from db.staff import get_department_for_category

def assign_team(category):
    return get_department_for_category(category)
