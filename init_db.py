# -*- coding: utf-8 -*-
from app.database import Base, engine
Base.metadata.create_all(bind=engine)