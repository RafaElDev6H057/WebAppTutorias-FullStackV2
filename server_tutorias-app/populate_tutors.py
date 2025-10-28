# populate_tutors.py

import getpass
from sqlmodel import Session, select
from app.database import engine
from app.models.tutor import Tutor
from sqlalchemy.exc import IntegrityError
from app.models.alumno import Alumno
from app.models.tutoria import Tutoria

tutor_data = [
    {
        "nombre": "SOLEDAD",
        "apellido_p": "ROMAN",
        "apellido_m": "FLORES",
        "correo": "soledad.rf@fresnillo.tecnm.mx"
    },
    {
        "nombre": "ROBERTO DE JESUS",
        "apellido_p": "JIMENEZ",
        "apellido_m": "DE LA ROSA",
        "correo": "roberto.jdlr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MONICA IVONNE",
        "apellido_p": "SALDIVAR",
        "apellido_m": "MENDEZ",
        "correo": "monica.sm@fresnillo.tecnm.mx"
    },
    {
        "nombre": "EMILIO",
        "apellido_p": "ORTIZ",
        "apellido_m": "CALDERA",
        "correo": "emilio.oc@fresnillo.tecnm.mx"
    },
    {
        "nombre": "ROBERTO",
        "apellido_p": "GOYTIA",
        "apellido_m": "MARTINEZ",
        "correo": "roberto.gm@fresnillo.tecnm.mx"
    },
    {
        "nombre": "NORMA ANGELICA",
        "apellido_p": "GONZALEZ",
        "apellido_m": "RODRIGUEZ",
        "correo": "norma.gonzalez@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JOSE ALFREDO",
        "apellido_p": "HERNANDEZ",
        "apellido_m": "NUÑEZ",
        "correo": "jose.hn@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MANUEL DE JESUS",
        "apellido_p": "LOZANO",
        "apellido_m": "URIBE",
        "correo": "manuel.lu@fresnillo.tecnm.mx"
    },
    {
        "nombre": "ALBERTO",
        "apellido_p": "RODRIGUEZ",
        "apellido_m": "ZAMARRIPA",
        "correo": "alberto.rz@fresnillo.tecnm.mx"
    },
    {
        "nombre": "LUIS MANUEL",
        "apellido_p": "ULLOA",
        "apellido_m": "GUZMAN",
        "correo": "luis.ug@fresnillo.tecnm.mx"
    },
    {
        "nombre": "LLUVIA SIHOMARA NEPHTALI",
        "apellido_p": "MARTINEZ",
        "apellido_m": "TEJADA",
        "correo": "lluvia.mt@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MA DE LA LUZ",
        "apellido_p": "RAMOS",
        "apellido_m": "RAMIREZ",
        "correo": "maluz.rr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "IRVIN HUMBERTO",
        "apellido_p": "CASAREZ",
        "apellido_m": "SANCHEZ",
        "correo": "irvin.cs@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MARIO ALBERTO",
        "apellido_p": "GARCIA",
        "apellido_m": "CAMACHO",
        "correo": "mario.gc@fresnillo.tecnm.mx"
    },
    {
        "nombre": "GRACIELA",
        "apellido_p": "ULLOA",
        "apellido_m": "GUZMAN",
        "correo": "graciela.ug@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MAYRA JANNETTE",
        "apellido_p": "RODRIGUEZ",
        "apellido_m": "ALCALA",
        "correo": "mayra.ra@fresnillo.tecnm.mx"
    },
    {
        "nombre": "HECTOR RENE",
        "apellido_p": "BARAJAS",
        "apellido_m": "MERCADO",
        "correo": "hector.bm@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JOSE ALBERTO",
        "apellido_p": "VELA",
        "apellido_m": "DAVILA",
        "correo": "jose.vd@fresnillo.tecnm.mx"
    },
    {
        "nombre": "OSCAR",
        "apellido_p": "CRUZ",
        "apellido_m": "DOMINGUEZ",
        "correo": "oscar.cd@fresnillo.tecnm.mx"
    },
    {
        "nombre": "SIHOMARA NEPHTALI",
        "apellido_p": "TEJADA",
        "apellido_m": "ORTEGA",
        "correo": "sihomara.to@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JUAN ANTONIO",
        "apellido_p": "GONZALEZ",
        "apellido_m": "SAENZ",
        "correo": "juan.gs@fresnillo.tecnm.mx"
    },
    {
        "nombre": "LUIS GERARDO",
        "apellido_p": "MORAN",
        "apellido_m": "GUTIERREZ",
        "correo": "luis.mg@fresnillo.tecnm.mx"
    },
    {
        "nombre": "BLASA",
        "apellido_p": "RUEDAS",
        "apellido_m": "CARRILLO",
        "correo": "blasa.rc@fresnillo.tecnm.mx"
    },
    {
        "nombre": "ROSALINDA",
        "apellido_p": "RAMOS",
        "apellido_m": "MURILLO",
        "correo": "rosalinda.rm@fresnillo.tecnm.mx"
    },
    {
        "nombre": "MARTHA ALICIA",
        "apellido_p": "GUERRERO",
        "apellido_m": "VEGA",
        "correo": "martha.gv@fresnillo.tecnm.mx"
    },
    {
        "nombre": "CESAR JAVIER",
        "apellido_p": "GUIJARRO",
        "apellido_m": "RODRIGUEZ",
        "correo": "cesar.gr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "GERARDO",
        "apellido_p": "RIOS",
        "apellido_m": "RAMOS",
        "correo": "gerardo.rr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "ARTURO ALFONSO",
        "apellido_p": "DE LA ROSA",
        "apellido_m": "MONTELONGO",
        "correo": "arturo.dlrm@fresnillo.tecnm.mx"
    },
    {
        "nombre": "NORMA ANGELICA",
        "apellido_p": "GONZALEZ",
        "apellido_m": "RODRIGUEZ",
        "correo": "norma.gonzalez@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JESUS IVAN",
        "apellido_p": "LIRA",
        "apellido_m": "RODRIGUEZ",
        "correo": "jesus.lr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "HECTOR BOGAR",
        "apellido_p": "CORTEZ",
        "apellido_m": "GONZALEZ",
        "correo": "hector.cg@fresnillo.tecnm.mx"
    },
    {
        "nombre": "VICTOR MANUEL",
        "apellido_p": "DOMINGUEZ",
        "apellido_m": "IBARRA",
        "correo": "victor.di@fresnillo.tecnm.mx"
    },
    {
        "nombre": "RUBEN BENYACUB",
        "apellido_p": "ALONSO",
        "apellido_m": "RODRIGUEZ",
        "correo": "ruben.ar@fresnillo.tecnm.mx"
    },
    {
        "nombre": "EDGAR RICARDO",
        "apellido_p": "SANTANA",
        "apellido_m": "GARCIA",
        "correo": "edgar.sg@fresnillo.tecnm.mx"
    },
    {
        "nombre": "EFREN PASCUAL",
        "apellido_p": "RIVERA",
        "apellido_m": "DE LEON",
        "correo": "efren.rdl@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JOEL",
        "apellido_p": "GARCIA",
        "apellido_m": "RIVERA",
        "correo": "joel.gr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "RAMON AGUSTIN",
        "apellido_p": "MENDOZA",
        "apellido_m": "RODRIGUEZ",
        "correo": "ramon.mr@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JANNET MARICELA",
        "apellido_p": "BARRIENTOS",
        "apellido_m": "LUJAN",
        "correo": "jannet.bl@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JOSE DE JESUS",
        "apellido_p": "REYES",
        "apellido_m": "SANCHEZ",
        "correo": "jose.rs@fresnillo.tecnm.mx"
    },
    {
        "nombre": "HUGO",
        "apellido_p": "JIMENEZ",
        "apellido_m": "ALVAREZ",
        "correo": "dir_vinculacion@fresnillo.tecnm.mx"
    },
    {
        "nombre": "JORGE OMAR",
        "apellido_p": "SAUCEDO",
        "apellido_m": "MARQUEZ",
        "correo": "jorge.sm@fresnillo.tecnm.mx"
    },
]

def populate_tutors():
    print(f"--- Iniciando la carga de {len(tutor_data)} tutores ---")
    created_count = 0
    skipped_count = 0

    # Usamos una sesión de base de datos
    with Session(engine) as session:
        for data in tutor_data:
            try:
                # 1. Verificar si el tutor ya existe por su correo
                existing_tutor = session.exec(
                    select(Tutor).where(Tutor.correo == data["correo"])
                ).first()
                
                if existing_tutor:
                    print(f"🟡 OMITIENDO: El tutor con correo '{data['correo']}' ya existe.")
                    skipped_count += 1
                    continue
                
                # 2. Generar la contraseña temporal
                # (Tomamos lo que está antes del @ y le añadimos 'itsf')
                usuario_correo = data["correo"].split('@')[0]
                temp_password = f"{usuario_correo}itsf"
                
                # 3. Crear el nuevo objeto Tutor
                new_tutor = Tutor(
                    nombre=data["nombre"].title(),
                    apellido_p=data["apellido_p"].title(),
                    apellido_m=data["apellido_m"].title(),
                    correo=data["correo"],
                    contraseña=temp_password,        # Contraseña en texto plano
                    requires_password_change=True # Forzamos el cambio
                )
                
                session.add(new_tutor)
                created_count += 1
            
            except IntegrityError as e:
                # Esto atraparía otros errores, como un correo duplicado
                session.rollback()
                print(f"🔴 ERROR: No se pudo agregar a '{data['correo']}'. Error: {e}")
            except Exception as e:
                session.rollback()
                print(f"🔴 ERROR INESPERADO con '{data['correo']}': {e}")
        
        # 4. Guardar todos los nuevos tutores en la base de datos
        if created_count > 0:
            session.commit()
            
    print("\n--- ¡Proceso completado! ---")
    print(f"✅ Tutores creados exitosamente: {created_count}")
    print(f"🟡 Tutores omitidos (ya existían): {skipped_count}")

if __name__ == "__main__":
    populate_tutors()