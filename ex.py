from sqlalchemy import create_engine, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///experiments.db', echo=True)

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiment'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

class DataPoint(Base):
    __tablename__ = 'datapoint'

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)

Base.metadata.create_all(engine)
