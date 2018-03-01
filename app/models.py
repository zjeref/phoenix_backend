import jwt
from app import db, app, bcrypt
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship, backref


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):
    __abstract__ = True

    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return dict(name=self.name)


class Faculty(User):
    __tablename__ = 'faculty'

    facultyId = db.Column(db.String(255), nullable=False, unique=True,
                          nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    gender = db.Column(db.Enum('male', 'female', 'others', name='gender'),
                       nullable=True)

    def __init__(self, facultyId, name, email, password, gender):
        super(Faculty, self).__init__(name)
        self.facultyId = facultyId
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

        gender = gender.lower()
        if gender in ['male', 'female', 'others']:
            self.gender = gender
        else:
            raise ValueError('Invalid gender value "%s"' % gender)

    def __repr__(self):
        return '<Faculty %r>' % self.name

    def serialize(self):
        return dict(id=self.id,
                    facultyId=self.facultyId,
                    name=self.name,
                    email=self.email,
                    admin=self.admin,
                    gender=self.gender,
                    )

    @staticmethod
    def encode_auth_token(email):
        """
        Generates the Auth Token
        :return: string
        """
        token_life = app.config.get('TOKEN_LIFESPAN_SEC')
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=token_life),
            'iat': datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']


class Student(User):
    __tablename__ = 'student'

    student_id = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date(), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    branch = db.Column(db.String(50), nullable=True)

    def __init__(self, student_id, category, name,
                 dob=None, contact=None, branch=None):
        super(Student, self).__init__(name)
        self.student_id = student_id
        self.category = category
        if isinstance(dob, basestring):
            self.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        else:
            self.dob = dob
        self.contact = contact
        self.branch = branch

    def __repr__(self):
        return '<Student %r>' % self.name

    def serialize(self):
        return dict(id=self.id,
                    name=self.name,
                    dob=self.dob,
                    category=self.category,
                    student_id=self.student_id,
                    contact=self.contact,
                    branch=self.branch,
                    )


class Attendance(Base):
    __tablename__ = 'attendance'

    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    punch_in = db.Column(db.String(50), nullable=False)
    punch_in_by_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    punch_in_by = relationship('Faculty', foreign_keys=[punch_in_by_id])
    punch_out = db.Column(db.String(50))
    punch_out_by_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    punch_out_by = relationship('Faculty', foreign_keys=[punch_out_by_id])
    comments = db.Column(db.String(100))
    location = db.Column(db.String(100))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = relationship('Student',
                           backref=backref("person",
                                           cascade="all, delete-orphan"))

    def __init__(self, date, student_id, punch_in, punch_in_by_id,
                 punch_out=None, punch_out_by_id=None, comments=None,
                 location=None):
        self.date = date
        self.student_id = student_id

        if punch_in:
            datetime.strptime(punch_in, '%H:%M:%S')
        self.punch_in = punch_in
        self.punch_in_by_id = punch_in_by_id

        if punch_out:
            datetime.strptime(punch_out, '%H:%M:%S')
        self.punch_out = punch_out
        self.punch_out_by_id = punch_out_by_id
        self.comments = comments
        self.location = location

    def serialize(self):
        return dict(id=self.id,
                    student=self.student.serialize(),
                    comments=self.comments,
                    punchIn=self.punch_in,
                    punchInBy=self.punch_in_by.serialize() if self.punch_in_by else {},
                    punchOut=self.punch_out,
                    punchOutBy=self.punch_out_by.serialize() if self.punch_out_by else {})
