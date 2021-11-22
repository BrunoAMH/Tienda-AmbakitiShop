from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Boolean,BLOB,CHAR
from flask_login import UserMixin

db=SQLAlchemy()

class Usuario(db.Model):
    __tablename__='usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombre=Column(String(80),nullable=False)
    telefono=Column(String(10),nullable=False)
    estatus = Column(String(1), nullable=True)
    tipo = Column(String(1), nullable=False, default='A')
    correo=Column(String(80),unique=True)
    contrasena=Column(String(20),nullable=False)

    def consultaGeneral(self):
        return self.query.all()
