from src import db
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy


class Perk(db.Model):
    __tablename__ = 'perk'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name=None, description=None, listed=False):
        self.name = name
        self.description = description
        self.listed = listed


class EmploymentType(db.Model):
    __tablename__ = 'employment_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name=None, listed=False):
        self.name = name
        self.listed = listed


class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


class Tech(db.Model):
    __tablename__ = 'tech'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name=None, listed=False):
        self.name = name
        self.listed = listed


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Numeric(10, 2))
    years_experience = db.Column(db.Integer)
    years_with_current_employer = db.Column(db.Integer)
    number_of_employers = db.Column(db.Integer)

    """ For confirmation and verification """
    email = db.Column('email', db.String(255))
    confirmation_code = db.Column('confirmation_code', db.String(255))
    confirmed = db.Column('confirmed', db.Boolean)
    verified = db.Column('verified', db.Boolean)

    created_at = db.Column(db.DateTime,  default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,  onupdate=datetime.utcnow)

    def associate_perk(self, perk):
        assoc_model = SubmissionToPerk.query.filter(
            SubmissionToPerk.submission_id == self.id
        ).filter(
            SubmissionToPerk.perk_id == perk.id
        ).first()
        if not assoc_model:
            self.perks.append(perk)

        return self

    def associate_role(self, role):
        assoc_model = SubmissionToRole.query.filter(
            SubmissionToRole.submission_id == self.id
        ).filter(
            SubmissionToRole.role_id == role.id
        ).first()
        if not assoc_model:
            self.roles.append(role)

        return self

    def associate_tech(self, tech):
        assoc_model = SubmissionToTech.query.filter(
            SubmissionToTech.submission_id == self.id
        ).filter(
            SubmissionToTech.tech_id == tech.id
        ).first()
        if not assoc_model:
            self.techs.append(tech)

        return self

    """ Relations """
    submission_to_perks = relationship("SubmissionToPerk", cascade="all, delete-orphan")
    submission_to_employment_type = relationship("SubmissionToEmploymentType", uselist=False, cascade="all, delete-orphan")
    submission_to_location = relationship("SubmissionToLocation", uselist=False, cascade="all, delete-orphan")
    submission_to_roles = relationship("SubmissionToRole", cascade="all, delete-orphan")
    submission_to_education = relationship("SubmissionToEducation", uselist=False, cascade="all, delete-orphan")
    submission_to_techs = relationship("SubmissionToTech", cascade="all, delete-orphan")
    perks = association_proxy('submission_to_perks', 'perk')
    employment_type = association_proxy('submission_to_employment_type', 'employment_type')
    location = association_proxy('submission_to_location', 'location')
    roles = association_proxy('submission_to_roles', 'role')
    education = association_proxy('submission_to_education', 'education')
    techs = association_proxy('submission_to_techs', 'tech')
    verification_request = relationship("VerificationRequest", uselist=False, cascade="all, delete-orphan")

    def __str__(self):
        return '{id}, ${salary}, {email}, {confirmed}, {date}'.format(
            id=self.id, salary=self.salary, email=self.email, confirmed=self.confirmed, date=self.created_at.strftime('%Y-%m-%d')
        )

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email_domain = db.Column(db.Text)
    url = db.Column(db.Text)

    def __init__(self, name, email_domain, url):
        self.name = name,
        self.email_domain = email_domain,
        self.url = url


class VerificationRequest(db.Model):
    __tablename__ = 'verification_request'
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    profile_url = db.Column('profile_url', db.String(255))
    employer_name = db.Column('employer_name', db.String(255))
    note = db.Column('note', db.Text)
    status = db.Column('status', db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submission = relationship(Submission)


class SubmissionToPerk(db.Model):
    __tablename__ = 'submission_to_perk'
    value = db.Column(db.Numeric)

    """
    Relations:

    1 Submission
    1 Perk
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    perk_id = db.Column(db.Integer, db.ForeignKey('perk.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    perk = relationship(Perk)

    def __init__(self, perk, value=None):
        self.perk = perk
        self.value = value

class SubmissionToEmploymentType(db.Model):
    __tablename__ = 'submission_to_employment_type'

    """
    Relations:

    1 Submission
    1 EmploymentType
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    employment_type_id = db.Column(db.Integer, db.ForeignKey('employment_type.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    employment_type = relationship(EmploymentType)

    def __init__(self, employment_type):
        self.employment_type = employment_type


class SubmissionToLocation(db.Model):
    __tablename__ = 'submission_to_location'

    """
    Relations:

    1 Submission
    1 Location
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    location = relationship(Location)

    def __init__(self, location):
        self.location = location


class SubmissionToRole(db.Model):
    __tablename__ = 'submission_to_role'

    """
    Relations:

    1 Submission
    1 Role
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    role = relationship(Role)

    def __init__(self, role):
        self.role = role

class SubmissionToEducation(db.Model):
    __tablename__ = 'submission_to_education'

    """
    Relations:

    1 Submission
    1 Education
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    education_id = db.Column(db.Integer, db.ForeignKey('education.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    education = relationship(Education)

    def __init__(self, education):
        self.education = education

class SubmissionToTech(db.Model):
    __tablename__ = 'submission_to_tech'

    """
    Relations:

    1 Submission
    1 Tech
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'), primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id', ondelete='CASCADE'), primary_key=True)
    submission = relationship(Submission)
    tech = relationship(Tech)

    def __init__(self, tech):
        self.tech = tech