import os, sys
from sqlalchemy import exc
from src import app, db
from src.models import *

def seed_core(database):
    try:
        perks = [
            Perk('Bonus', listed=True),
            Perk('RRSP Matching / Profit Sharing', description='Use the value when the benefit is maxxed out', listed=True),
            Perk('Professional Development Expense Reimbursement', listed=True),
            Perk('Fitness Expense Reimbursement', listed=True),
            Perk('Food / Drinks', listed=True),
            Perk('Employee Discount Program', listed=True),
            Perk('Transit Pass', listed=False)
        ]
        employment_types = [
            EmploymentType('Full-Time'),
            EmploymentType('Part-Time'),
            EmploymentType('Independent Contractor'),
            EmploymentType('Internship')
        ]
        locations = [
            Location('London, Ontario'),
            Location('Near London, Ontario'),
            Location('Remote Work')
        ]
        roles = [
            Role('Software Developer', listed=True),
            Role('Backend Web Developer', listed=True),
            Role('Frontend Web Developer', listed=True),
            Role('Full-Stack Web Developer', listed=True),
            Role('Web Designer', listed=True),
            Role('Graphic Designer', listed=True),
            Role('System Administrator', listed=True),
            Role('DevOps', listed=True),
            Role('Hardware Developer', listed=True),
            Role('Project Manager', listed=True),
            Role('Mobile Developer', listed=False),
        ]
        educations = [
            Education('High School / GED'),
            Education('Some College / University'),
            Education('College Degree'),
            Education('Bachelor\'s Degree'),
            Education('Master\'s Degree'),
            Education('Doctorate Degree')
        ]
        techs = [
            Tech('Python', listed=True),
            Tech('PHP', listed=True),
            Tech('Ruby', listed=True),
            Tech('Java', listed=True),
            Tech('C', listed=True),
            Tech('C++', listed=True),
            Tech('C#', listed=True),
            Tech('Javascript', listed=True),
            Tech('SQL', listed=True),
            Tech('HTML', listed=True),
            Tech('CSS', listed=True),
            Tech('Linux', listed=True),
            Tech('Golang', listed=True),
            Tech('Git', listed=True)
        ]
        for v in perks: db.session.add(v)
        for v in employment_types: db.session.add(v)
        for v in locations: db.session.add(v)
        for v in roles: db.session.add(v)
        for v in educations: db.session.add(v)
        for v in techs: db.session.add(v)
        database.session.commit()

    except exc.SQLAlchemyError:
        import traceback
        print(traceback.format_exc())
        database.session.rollback()

if __name__ == '__main__':
    seed_core(db)