from sqlmodel import Session, create_engine
from EnvData import postgresql_url


engine = create_engine(postgresql_url, echo=True)