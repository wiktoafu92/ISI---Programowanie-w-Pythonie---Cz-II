import random

from sqlalchemy import create_engine, String, Integer, Boolean, Float, DateTime, select, delete, update, ForeignKey, \
    Table, Column
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, relationship
from datetime import datetime

engine = create_engine('sqlite:///experiments.db', echo=True)

Base = declarative_base()

subject_experiment_table = Table(
    'subject_experiment',
    Base.metadata,
    Column('subject_id', ForeignKey('subject.id'), primary_key=True),
    Column('experiment_id', ForeignKey('experiment.id'), primary_key=True)
)

class Experiment(Base):
    __tablename__ = 'experiment'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

    datapoints: Mapped[list['DataPoint']] = relationship(back_populates='experiment')

    subjects: Mapped[list["Subject"]] = relationship(secondary=subject_experiment_table, back_populates="experiments")

class DataPoint(Base):
    __tablename__ = 'datapoint'

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)

    experiment_id: Mapped[int] = mapped_column(ForeignKey('experiment.id'))
    experiment: Mapped['Experiment'] = relationship(back_populates='datapoints')

class Subject(Base):
    __tablename__ = 'subject'

    id: Mapped[int] = mapped_column(primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    experiments: Mapped[list['Experiment']] = relationship(secondary=subject_experiment_table,
                                                           back_populates='subjects')

# Base.metadata.create_all(engine)
#
# with Session(engine) as session:
#     experiments = [
#         Experiment(title='A', type=random.randint(1, 5)),
#         Experiment(title='B', type=random.randint(1, 5))
#     ]
#     session.add_all(experiments)
#
#     datapoints = [
#         DataPoint(real_value=random.uniform(0, 100), target_value=random.uniform(0, 100), experiment_id=1)
#         for _ in range(10)
#     ]
#     session.add_all(datapoints)
#
#     session.commit()
#
#     experiments = session.scalars(select(Experiment)).all()
#     print(len(experiments))
#     for exp in experiments:
#         print(f'id: {exp.id}, title: {exp.title}, created_at: {exp.created_at}, type: {exp.type}, '
#               f'finished: {exp.finished}')
#
#     datapoints = session.scalars(select(DataPoint)).all()
#     print(len(datapoints))
#     for dp in datapoints:
#         print(f'id: {dp.id}, real_value: {dp.real_value:.2f}, target_value: {dp.target_value:.2f}, '
#               f'experiment_id: {dp.experiment_id}')
#
#     stmt = update(Experiment).values(finished=True)
#     session.execute(stmt)
#     session.commit()
#
#     stmt_exp = delete(Experiment)
#     stmt_dp = delete(DataPoint)
#     session.execute(stmt_exp)
#     session.execute(stmt_dp)
#     session.commit()
