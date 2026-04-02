import os
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.base import Base
import models.user
import models.empresa
import models.usuario_empresa
from services.auth_service import get_password_hash

def seed_data():
    # Crear las tablas
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario
        user = db.query(models.user.Usuario).filter(models.user.Usuario.email == "admin@creapx.com").first()
        if not user:
            print("Creando usuario administrador...")
            user = models.user.Usuario(
                nombre="Administrador",
                email="admin@creapx.com",
                password_hash=get_password_hash("admin123"), # Contraseña de prueba
                estado="ACTIVO"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print("Usuario administrador ya existe.")

        # Verificar si ya existe la empresa
        empresa = db.query(models.empresa.Empresa).filter(models.empresa.Empresa.nit == "06140101801234").first()
        if not empresa:
            print("Creando empresa de prueba...")
            empresa = models.empresa.Empresa(
                nit="06140101801234",
                nombre_razon_social="Empresa Tecnológica SAAS de CV",
                correo="info@empresasaas.com",
                estado="ACTIVA"
            )
            db.add(empresa)
            db.commit()
            db.refresh(empresa)
        else:
            print("Empresa de prueba ya existe.")

        # Vincular usuario con empresa
        relacion = db.query(models.usuario_empresa.UsuarioEmpresa).filter(
            models.usuario_empresa.UsuarioEmpresa.usuario_id == user.id,
            models.usuario_empresa.UsuarioEmpresa.empresa_id == empresa.id
        ).first()

        if not relacion:
            print("Asignando usuario a la empresa...")
            relacion = models.usuario_empresa.UsuarioEmpresa(
                usuario_id=user.id,
                empresa_id=empresa.id,
                rol="admin"
            )
            db.add(relacion)
            db.commit()
        else:
            print("El usuario ya está asignado a la empresa.")

        print("\n¡Semilla insertada exitosamente!")
        print(f"-> Email: {user.email}")
        print(f"-> Password: admin123")
        print(f"-> NIT vinculado: {empresa.nit}")
        
    except Exception as e:
        print(f"Error insertando semilla: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
