# Dependencias

from datetime import date, datetime
import shelve

# Clases

class Examen:
    resultados = []
    parametros = []
    def __init__(self, registro_medico, nombre_examen):
        self.registro_medico = registro_medico;
        self.nombre_examen = nombre_examen;
        self.estado = False;
    def añadirResultados(self):
        valores_medidos = int(input("Numero de valores medidos"));
        self.añadirValores(valores_medidos)
        parametros_referencia = int(input("Numero parametros de referencia"))
        self.definirParametros(parametros_referencia);
        self.observaciones = input("Observaciones: ")
        self.estado = True
        
    def añadirValores(self, valores_medidos):
        for vc in range(valores_medidos):
            print("Valor numero: ", str(vc))
            valor_medido = input("Escriba el valor:")
            self.resultados.append(valor_medido)
    def definirParametros(self, parametros_referencia):
        for parametro in range(parametros_referencia):
            nombre = input("Escriba el nombre de referencia")
            rango_mayor = int(input("Escriba el rango mayor"))
            rango_menor = int(input("Escriba el rango menor"))
            self.parametros.append({nombre: [rango_mayor, rango_menor]})
            
Examenes = []

class Paciente:
    citas = [];
    examenes = [];
    def __init__(self, nombre, apellido, tipo_documento, numero_documento, direccion, eps, telefono, correo_electronico, municipio, departamento):
        self.nombre = nombre;
        self.apellido = apellido;
        self.tipo_documento = tipo_documento;
        self.numero_documento = numero_documento;
        self.direccion = direccion;
        self.eps = eps;
        self.telefono = telefono;
        self.correo_electronico = correo_electronico;
        self.municipio = municipio;
        self.departamento = departamento;

    def datosCita(self):
        fecha = datetime.now()
        registro_medico = input("Escriba eñ registro_medico");
        if(validarMedico(registro_medico, self.numero_documento)):
            print("No se encontro medico en la base de datos")
        else:
            solicitud = int(input("Solicitud Examen: 1. Si, 2. No."));
            if(solicitud == 1):
                self.solicitarExamen(registro_medico);
            else:
                pass
            diagnostico = input("Escriba el diagnostico: ")
            self.citas.append([fecha, registro_medico, diagnostico])
    def solicitarExamen(self, registro_medico):
        nombre_examen = input("Escriba el nombre del examen que desea solicitar");
        self.examenes.append(Examen(registro_medico, nombre_examen));

Pacientes = []

class Medico(Paciente):
    consultas = [];
    pacientes_atendidos = 0;
    def __init__(self, nombre, apellido, numero_documento, direccion, eps, telefono, correo_electronico, municipio, departamento, registro_medico, especialidades=[]):
        self.nombre = nombre;
        self.apellido = apellido;
        self.numero_documento = numero_documento;
        self.direccion = direccion;
        self.eps = eps;
        self.telefono = telefono;
        self.correo_electronico = correo_electronico;
        self.municipio = municipio;
        self.departamento = departamento;
        self.registro_medico = registro_medico;
        self.especialidades = especialidades;
    def añadirEspecialidad(self):
        especialidad = input("Escriba el nombre de la especialidad")
        self.especialidades.append(especialidad)
    def añadirPaciente(self, numero_documento):
        controlador = False
        for consulta in self.consultas:
            if(numero_documento == consulta[0]):
                controlador = True
        if(controlador == False):
            self.pacientes_atendidos += 1;
        self.consultas.append([numero_documento, datetime.now()])
        
        
Medicos = []

# Metodos

def añadirPersona():
	nombre = input("Escriba el nombre del Paciente");
	apellido = input("Escriba el apellido del Paciente")
	controlador = False
	while(controlador == False):
	    tipo_documento = input("Escriba el tipo de documento: \n"
	                          "CC -> Cedula de Ciudadania \n"
	                          "CE -> Cedula Extranjera \n"
	                          "NIT \n"
	                          "RE -> Registro Civil \n"
	                          "TI -> Tarjeta de Identidad \n"
	                          "Escriba Salir para omitir este menú.")
	    if(tipo_documento.lower() in {'cc', 'ce', 'nit', 're', 'ti', 'salir'}):
	        controlador = True;
	    else:
	        print("Seleccione una opcion correcta");
	numero_documento = input("Escriba el numero de documento: ");
	direccion = input("Escriba la direccion del paciente: ");
	eps = input("Escriba la eps del paciente: ");
	telefono = input("Escriba el telefono del paciente: ");
	correo_electronico = input("Escriba el correo electronico del paciente: ");
	municipio = input("Escriba el municipio del paciente: ");
	departamento = input("Escriba el departamente del paciente: ");
	return [nombre, apellido, tipo_documento, numero_documento, direccion, eps, telefono, correo_electronico, municipio, departamento]

def añadirPaciente():
    paciente = añadirPersona()
    print(paciente)
    Pacientes.append(Paciente(paciente[0], paciente[1], paciente[2], paciente[3], paciente[4], paciente[5], paciente[6], paciente[7], paciente[8], paciente[9]))

def añadirMedico():
    numero_documento = input("Escriba el documento de identidad del medico");
    paciente_datos = encontrarPacientes(numero_documento)
    print(paciente_datos)
    if(paciente_datos[0]):
        registro_medico = input("Escriba el numero de registro medico")
        if(validarMedico(registro_medico)):
            print("El registro medico ya se encuentra registrado")
        else:
            numero_especialidades = int(input("Escriba el numero de especialidades"))
            print("A continuacion escriba las especialidades del medico")
            especialidades = añadirEspecialidades(numero_especialidades)
            Medicos.append(Medico(paciente_datos[1][0], paciente_datos[1][1], paciente_datos[1][2], paciente_datos[1][3], paciente_datos[1][4], paciente_datos[1][5], paciente_datos[1][6], paciente_datos[1][7], paciente_datos[1][8], registro_medico, especialidades))
    else:
        print("Debe registrar al medico como paciente.")

def validarMedico(registro_medico, paciente=""):
    for medico in Medicos:
        if(medico.registro_medico == registro_medico ):
            medico.añadirPaciente(paciente)
            return False
    return False

def encontrarPacientes(numero_documento):
    controlador = False
    for paciente in Pacientes:
        if(paciente.numero_documento == numero_documento):
            controlador = True
            return [True, [paciente.nombre, paciente.apellido, paciente.tipo_documento, paciente.direccion, paciente.eps, paciente.telefono, paciente.correo_electronico, paciente.municipio, paciente.departamento]]
    if(controlador==False):
        print("No se encontro documento")
        return [False]

def añadirEspecialidades(numero_especialidades):
    especialidades = []
    while(numero_especialidades):
        especialidad = input("Escriba el nombre de la especialidad");
        especialidades.append(especialidad);
        numero_especialidades -= 1
    return especialidades

def formatoFecha():
    print("aaaa-mm-dd");
    año = int(input("Escriba el año en el que quiere agendar su cita: "));
    mes = int(input("Escriba el mes en el que quiere agendar su cita: "));
    dia = int(input("Escriba el dia en el que quiere agendar su cita: "));
    hora = int(input("Ingrese la hora en los horarios establecidos: \n Horario de atencion: 9 - 17 "));
    if(hora <= 9 or hora > 18 ):
        minutos = int(input("Ingrese la franja de atencion que desea: \n 1.00 \n2.20 \n3.40"));
        if(minutos == 1):
            minutos = 0;
        elif(minutos == 2):
            minutos = 20;
        elif(minutos == 3):
            minutos = 40;
        else:
            print("Franja de atencion no valida")
    else: 
        print("Horario de atencíon no valido")
    return(datetime(año, mes, dia, hora, minutos))

def nuevaConsulta():
    documento_identidad = input("Escriba el documento de identidad del paciente");
    controlador = False
    for paciente in Pacientes:
        if(documento_identidad == paciente.numero_documento):
            paciente.datosCita()
            controlador = True
            break;
    if(controlador == False):
        print("No se encontro documento.")

def adicionarExamen():
    numero_documento = input("Escriba numero documento paciente")
    controlador = False;
    for paciente in Pacientes:
        if(numero_documento == paciente.numero_documento):
            controlador = True;
            if(len(paciente.examenes)==0):
                print("El paciente aun no tiene examenes");
                break
            else:
                for examen in paciente.examenes:
                    print(examen.nombre_examen)
                nombre_examen = input("Escriba el nombre del examen al que quiere adicionar datos");
                controlador_2 = False;
                for examen in paciente.examenes:
                    if(nombre_examen == examen.nombre_examen):
                        examen.añadirResultados();
                        controlador_2 = True;
                        break
                if(controlador_2 == False):
                    print("No se encontro el nombre del examen")
                    
    if(controlador == False):
        print("No se encontro documento del paciente")

def informacionPersonal():
    numero_documento=input("Escriba el numero de documento del paciente:")
    datos_busqueda = encontrarPacientes(numero_documento)
    informacion = ["Nombre:", "Apellido:", "Tipo de documento:", "Documento Identidad:", "Direccion:", "Eps:", "Telefono:", "Correo:", "Municipio:", "Departamento:"]
    if(datos_busqueda[0]):
        vc=0
        datos = datos_busqueda[1]
        for datos in datos_busqueda[1]:
            print("-------------------------------");
            print(informacion[vc])
            print(datos);
            print("-------------------------------");
            vc += 1;

def mostrarHistoria():
    opc = int(input("1. Mostrar toda la historia. \n"
                           "2. Mostrar por fecha en particular. \n"
                           "3. Mostrar por rango de fecha."))
    numero_documento=input("Escriba el numero de documento del paciente:");
    controlador = True
    for paciente in Pacientes:
        if(numero_documento == paciente.numero_documento):
            print("Paciente encontrado")
            opcion = int(input("1. Incluir Examenes. \n 2. No incluirlos"))
            vc = 0
            if(opc==1):
                for cita in paciente.citas:
                    print("-------------------------------");
                    print("Historia no.", str(vc));
                    print("Dia:", cita[0].day, "Mes:", cita[0].month, "Año:", cita[0].year);
                    print("Registro del medico:", cita[1]);
                    print("Diagnostico:", cita[2]);
                    print("-------------------------------");
                    vc += 1;
                if(opcion == 1):
                    vc = 0
                    for examen in paciente.examenes:
                        print("-------------------------------");
                        print("Examen no.", str(vc));
                        if(examen.estado):
                            print("Resultados:");
                            print(examen.resultados);
                        else:
                            print("Aun no hay resultados.")
                        print("Registro Medico: ", examen.registro_medico);
                        print("-------------------------------");
            elif(opc==2):
                for cita in paciente.citas:
                    if(Fecha() == cita[0].date()):
                        print("-------------------------------");
                        print("Historia no.", str(vc));
                        print("Dia:", cita[0].day, "Mes:", cita[0].month, "Año:", cita[0].year);
                        print("Registro del medico:", cita[1]);
                        print("Diagnostico:", cita[2]);
                        print("-------------------------------");
                        vc += 1;
                        if(opcion==1):
                            for examen in paciente.examenes:
                                print("-------------------------------");
                                print("Examen no.", str(vc));
                                if(examen.estado):
                                    print("Resultados:");
                                    print(examen.resultados);
                                else:
                                    print("Aun no hay resultados.")
                                    print("Registro Medico: ", examen.registro_medico);
                                    print("-------------------------------");
                        break
            
            elif(opc==3):
                print("Escriba el rango de fecha 1 (Menor).")
                day = int(input("Escriba el dia de su cita"))
                month = int(input("Escriba el mes de su cita."))
                year = int(input("Escriba el año de su cita"))
                fecha_1 = date(year, month, day)
                print("Escriba el rango de fecha 2. (Mayor)")
                day = int(input("Escriba el dia de su cita"))
                month = int(input("Escriba el mes de su cita."))
                year = int(input("Escriba el año de su cita"))
                fecha_2 = date(year, month, day)
                for cita in paciente.citas:
                    if(cita[0].date() >= fecha_1 and cita[0].date() <= fecha_2):
                        print("-------------------------------");
                        print("Historia no.", str(vc));
                        print("Dia:", cita[0].day, "Mes:", cita[0].month, "Año:", cita[0].year);
                        print("Registro del medico:", cita[1]);
                        print("Diagnostico:", cita[2]);
                        print("-------------------------------");
                        vc += 1;
                        if(opcion==1):
                            for examen in paciente.examenes:
                                print("-------------------------------");
                                print("Examen no.", str(vc));
                                if(examen.estado):
                                    print("Resultados:");
                                    print(examen.resultados);
                                else:
                                    print("Aun no hay resultados.")
                                    print("Registro Medico: ", examen.registro_medico);
                                    print("-------------------------------");
                        break
            break;
                    
    if(controlador == False):
        print("No se encontro documento paciente")

def atencionPacientes():
    fecha_actual = datetime.now()
    fecha_pasada = fecha_actual.date()
    mes_pasado = fecha_pasada.month - 1
    fecha_pasada = fecha_pasada.replace( month = mes_pasado)
    for paciente in Pacientes:
        contador = 0
        for cita in paciente.citas:
            if(mesPasado(cita[0])):
                contador += 1;
                print(contador)
    calcularPorcentaje(contador)

def atencionMedico():
    registro_medico = input("Registro del medico:")
    controlador = False
    for medico in Medicos:
        if(medico.registro_medico == registro_medico):
            fecha_actual = datetime.now()
            fecha_pasada = fecha_actual.date()
            mes_pasado = fecha_pasada.month - 1
            fecha_pasada = fecha_pasada.replace( month = mes_pasado)
            print("Pacientes atendidos por este medico:", medico.pacientes_atendidos)
            contador = 0;
            for consulta in medico.consultas:
                if(mesPasado(consulta[1])):
                    contador += 1
            calcularPorcentaje(contador)
            controlador = True
    if(controlador == False):
        print("No se contro registro medico.")

def mesPasado(fecha):
            fecha_actual = datetime.now()
            fecha_pasada = fecha_actual.date()
            mes_pasado = fecha_pasada.month - 1
            fecha_pasada = fecha_pasada.replace( month = mes_pasado)
            # ¿Esta en el rango? 
            if(fecha.date()<=fecha_actual.date() and fecha.date()>=fecha_pasada):
                return True
            else:
                return False
def Fecha():
    day = int(input("Escriba el dia de su cita"))
    month = int(input("Escriba el mes de su cita."))
    year = int(input("Escriba el año de su cita"))
    return date(year, month, day)


def calcularPorcentaje(numero):
    porcentaje = (100 * numero)/len(Pacientes)
    print("El porcentaje de pacientes atendidos este mes es:", str(porcentaje))

# Menu

opc = 0
while(opc!=6):
    opc = int(input("1. Registro Pacientes y Medicos. \n"
                   "2. Consulta de Datos. \n"
                   "3. Examenes. \n"
                   "4. Consultas. \n"
                   "5. Datos estadisticos. \n"
                   "6. Salir."));
    if(opc==1):
        opc = int(input("1. Registrar Paciente. \n"
                       "2. Registrar Medico"))
        if(opc==1):
            añadirPaciente();
        elif(opc==2):
            añadirMedico();
        else:
            print("Seleccione una opcion valida.")
    elif(opc==2):
        opc = int(input("1. Informacion paciente. \n"
                       "2. Historia clinica de paciente."))
        if(opc==1):
            opc = int(input("1. Informacion Personal."))
            if(opc==1):
                informacionPersonal();
        elif(opc==2):
            mostrarHistoria();

                
        else:
            print("Seleccione una opcion valida.")
            
    elif(opc==3):
        adicionarExamen()
        
    elif(opc==4):
        nuevaConsulta()
    elif(opc == 5):
        opc = int(input("1. Pacientes atendidos este mes. \n"
                       "2. Pacientes atendidos por medico "))
        if(opc==1):
            atencionPacientes()
        elif(opc==2):
            atencionMedico()
    elif(opc==6):
        print("Salio con exito de la paltaforma.")
    else:
        print("Seleccione una opción valida.")
    
