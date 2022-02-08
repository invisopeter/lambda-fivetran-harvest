from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_url
from sqlalchemy.pool import NullPool


DeclarativeBase = declarative_base()


def db_connect():
    # return create_engine(DB_URL, encoding='utf-8', echo=True, echo_pool=True)
    return create_engine(db_url, encoding='utf-8', poolclass=NullPool)


def create_db_session(engine):
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    return session


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'io_harvest_users'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    first_name = Column(String(64, u'utf8_unicode_ci'), nullable=False)
    last_name = Column(String(64, u'utf8_unicode_ci'), nullable=False)
    is_contractor = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)
    cost_rate = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Task(Base):
    __tablename__ = 'io_harvest_tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, u'utf8_unicode_ci'), nullable=False)
    billable_by_default = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_default = Column(Integer, nullable=False)
    default_hourly_rate = Column(Numeric(10, 2))
    deactivated = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Client(Base):
    __tablename__ = 'io_harvest_clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    currency = Column(String(32), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    details = Column(Text, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Contact(Base):
    __tablename__ = 'io_harvest_contacts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_office = Column(String(255), nullable=False)
    phone_mobile = Column(String(255), nullable=False)
    fax = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Project(Base):
    __tablename__ = 'io_harvest_projects'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    name = Column(String(255, u'utf8_unicode_ci'), nullable=False)
    code = Column(String(255, u'utf8_unicode_ci'), nullable=False)
    active = Column(Integer, nullable=False)
    billable = Column(Integer, nullable=False)
    bill_by = Column(String(32, u'utf8_unicode_ci'), nullable=False)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    budget = Column(Numeric(10, 2), nullable=False)
    budget_by = Column(String(32, u'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    starts_on = Column(DateTime, nullable=False)
    ends_on = Column(DateTime, nullable=False)
    estimate = Column(Numeric(10, 2), nullable=False)
    estimate_by = Column(String(32, u'utf8_unicode_ci'), nullable=False)
    hint_earliest_record_at = Column(DateTime, nullable=False)
    hint_latest_record_at = Column(DateTime, nullable=False)
    notes = Column(Text(collation=u'utf8_unicode_ci'), nullable=False)
    cost_budget = Column(Numeric(10, 2), nullable=False)
    cost_budget_include_expenses = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Expense(Base):
    __tablename__ = 'io_harvest_expenses'

    id = Column(Integer, primary_key=True)
    total_cost = Column(Numeric(19, 0), nullable=False)
    units = Column(Numeric(19, 0), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    project_id = Column(Integer, nullable=False)
    expense_category_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    spent_at = Column(DateTime, nullable=False)
    is_closed = Column(Integer, nullable=False)
    notes = Column(String(255), nullable=False)
    invoice_id = Column(Integer, nullable=False)
    billable = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    has_receipt = Column(Integer, nullable=False)
    receipt_url = Column(String(255), nullable=False)
    is_locked = Column(Integer, nullable=False)
    locked_reason = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class ExpenseCategory(Base):
    __tablename__ = 'io_harvest_expense_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    unit_name = Column(String(255), nullable=False)
    unit_price = Column(Numeric(19, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deactivated = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Entry(Base):
    __tablename__ = 'io_harvest_entries'

    id = Column(Integer, primary_key=True)
    notes = Column(Text(collation=u'utf8_unicode_ci'), nullable=False)
    spent_at = Column(Date, nullable=False)
    hours = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)
    task_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    adjustment_record = Column(Integer, nullable=False)
    timer_started_at = Column(DateTime, nullable=False)
    is_closed = Column(Integer, nullable=False)
    is_billed = Column(Integer, nullable=False)
    is_deleted = Column(Integer, nullable=False)


class TaskAssignment(Base):
    __tablename__ = 'io_harvest_tasks_assignments'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    task_id = Column(Integer, nullable=False)
    billable = Column(Integer, nullable=False)
    deactivated = Column(Integer, nullable=False)
    hourly_rate = Column(Numeric(19, 2), nullable=False)
    budget = Column(Numeric(19, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    estimate = Column(Numeric(19, 2), nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class UserAssignment(Base):
    __tablename__ = 'io_harvest_user_assignments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)
    is_project_manager = Column(Boolean, nullable=False)
    deactivated = Column(Boolean, nullable=False)
    hourly_rate = Column(Numeric(19, 2), nullable=True)
    budget = Column(Numeric(19, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    estimate = Column(Numeric(19, 2), nullable=False)
    is_deleted = Column(Boolean, nullable=False)
