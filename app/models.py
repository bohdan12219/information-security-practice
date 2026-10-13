from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table
)
from sqlalchemy.orm import relationship
from app.crypto.encryption import blind_index, decrypt_field, encrypt_field
from app.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    department = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    students = relationship("User", back_populates="group")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=True)
    credits = Column(Float, nullable=True)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Float, nullable=False)
    value = Column(Float, nullable=True)
    date_assigned = Column(DateTime, default=datetime.utcnow)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    comment = Column(String(255), nullable=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    student = relationship("User", foreign_keys=[student_id], back_populates="grades")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    
    _encrypted_email = Column("encrypted_email", String(500), nullable=True)
    email_index = Column(String(64), unique=True, nullable=True, index=True)
    _encrypted_phone = Column("encrypted_phone", String(500), nullable=True)
    
    full_name = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", foreign_keys="Grade.student_id", back_populates="student")

    @property
    def email(self) -> str | None:
        return decrypt_field(self._encrypted_email)

    @email.setter
    def email(self, value: str | None) -> None:
        self._encrypted_email = encrypt_field(value)
        self.email_index = blind_index(value) if value else None

    @property
    def phone(self) -> str | None:
        return decrypt_field(self._encrypted_phone)

    @phone.setter
    def phone(self, value: str | None) -> None:
        self._encrypted_phone = encrypt_field(value) if value else None

    def __repr__(self):
        return f"<User {self.username}>"