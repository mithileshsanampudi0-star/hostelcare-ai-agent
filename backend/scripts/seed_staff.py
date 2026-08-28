import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.staff import seed_staff

if __name__ == "__main__":
    seed_staff()
    print("Staff seeded successfully.")
