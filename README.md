# IngenieriaSoftware2
Sistema de pagos de salarios

Login con roles
Usuario			        Contraseña	    Rol
admin@example.com	    1234    	    admin
gerente@example.com	    1234    	    gerente
empleado@example.com   	1234    	    empleado
asistenteexample.com    1234            asistente recursos humanos

Ideas de pantallas para los roles:

Administrador
Acceso total (ve todo el menú)

Opciones que debería tener:
- Gestionar empleados (CRUD)
- Conceptos salariales (agregar/modificar descuentos, bonificaciones, horas extra)
- Actualizar salario mínimo (parametrización del sistema)
- Configurar parámetros (ej: porcentaje IPS, aportes, reglas de cálculo)
- Gestionar usuarios y roles (crear usuarios, asignar permisos)
- Reportes generales (IPS, planilla completa, históricos, comparativos)
- Exportación de recibos (todos los empleados, PDF/Excel)

Gerente / Jefe de RRHH
Solo consulta, nada de edición.

Opciones que debería tener:
- Ver empleados (solo lectura)
- Reportes y dashboards (gráficas, totales, análisis)
- No debería ver: gestión de usuarios, configuraciones, ni cálculos.

Asistente de RRHH
Entra en la parte operativa del sistema.

Opciones que debería tener:
- Registrar empleados (puede dar de alta, pero no modificar configuraciones globales)
- Descuentos y bonificaciones (cargar préstamos, horas extra, viáticos, etc.)
- Calcular nómina (ejecutar cálculo de salarios)
- Generar recibos (por empleado o masivo del mes)

Empleado
Acceso personal limitado.

Opciones que debería tener:
- Ver mis datos personales (solo su registro, sin modificar)
- Consultar mis recibos (PDF o detalle en pantalla)
- Descargar mis recibos