# SentinelGuard  
Sistema de alarma inteligente con perfiles, modos y simulación de eventos  
Trabajo Final – Desarrollo Orientado a Objetos (DOO)

---

##  Descripción general

**SentinelGuard** es una aplicación de simulación de un sistema de alarma inteligente, diseñada para representar de forma realista el funcionamiento de una instalación de seguridad moderna. El sistema permite gestionar distintos perfiles de usuario, modos de alarma, sensores y un historial de eventos, integrando lógica de negocio, persistencia de datos y una interfaz gráfica interactiva.

El proyecto está orientado a demostrar principios de **Diseño Orientado a Objetos**, separación de responsabilidades, gestión de estados y una experiencia de usuario coherente con aplicaciones reales del sector de la seguridad.

El proyecto está explicado en más detalle en el documento *SENTINEL GUARD.pdf*.
---

##  Objetivos del proyecto

- Simular el comportamiento realista de un sistema de alarma
- Aplicar principios de diseño OO de forma clara y estructurada
- Separar lógica de negocio, persistencia y presentación
- Gestionar estados complejos (armado, desarmado, activación de modos)
- Diseñar una interfaz intuitiva y consistente
- Registrar eventos relevantes para auditoría e historial

---

##  Perfiles de usuario

SentinelGuard distingue entre **tres perfiles**, cada uno con necesidades y comportamientos diferentes:

###  Perfil Hogar
Pensado para usuarios residenciales. Prioriza la seguridad doméstica y la comodidad diaria.

Características:
- Sensores domésticos (movimiento, apertura, humo)
- Modos adaptados a la vida cotidiana
- Enfoque en la protección sin interferir en el uso normal de la vivienda

---

###  Perfil Empresa
Diseñado para entornos profesionales y comerciales.

Características:
- Sensores orientados a accesos, oficinas y almacenes
- Modos vinculados a horarios laborales y zonas sensibles
- Mayor énfasis en control perimetral y monitorización continua

---

###  Perfil Mixto
Perfil híbrido para instalaciones que combinan vivienda y actividad profesional.

Ejemplos reales:
- Viviendas con despacho o consulta
- Negocios familiares
- Espacios compartidos con uso privado y laboral

Características:
- Combina sensores de hogar y empresa
- Incluye modos específicos que equilibran seguridad y operatividad
- Permite escenarios como presencia de personal autorizado o actividad parcial

---

##  Modos de alarma

Cada perfil dispone de un conjunto de **modos de alarma** adaptados a su contexto.  
Un modo define **qué sensores están activos** y cómo se comporta el sistema.

Aspectos clave:
- Solo puede haber **un modo activo a la vez**
- No es posible activar un nuevo modo sin desarmar el sistema previamente
- El armado de un modo incluye una **cuenta atrás realista**
- El estado del sistema se refleja claramente en la interfaz

Ejemplos de modos:
- Modo Casa
- Modo Noche
- Modo Total
- Modo Mascotas
- Modo Limpieza (perfil mixto)
- Modos profesionales específicos para empresa

---

##  Sistema de armado y desarmado

El sistema de armado está diseñado para comportarse como una aplicación real:

- El armado no es instantáneo: incluye una **cuenta atrás**
- Durante el armado:
  - No se puede volver a armar
  - No se puede cambiar de modo
- El estado del sistema se mantiene coherente entre pantallas
- El desarmado es inmediato y registra el evento correspondiente

Este comportamiento evita inconsistencias y simula el funcionamiento de sistemas comerciales reales.

---

##  Sensores y simulación de eventos

SentinelGuard incluye sensores asociados a cada perfil:

Tipos de sensores:
- Movimiento
- Apertura
- Humo

Características del sistema de sensores:
- No se pueden simular eventos si el sistema está desarmado
- La simulación representa una **detección realista**
- Al dispararse un sensor:
  - Se activa el estado de alarma
  - Se muestra una notificación visual
  - Se registra el evento en el historial

La interfaz distingue claramente cuándo el sistema está preparado para simular eventos.

---

##  Gestión de estados

El sistema gestiona múltiples estados internos de forma coherente:

- Sistema armado / desarmado
- Armado en progreso
- Modo activo
- Alarma activa
- Modo pendiente durante la cuenta atrás

Estos estados se comparten entre pantallas para garantizar una experiencia consistente y evitar acciones incoherentes.

---

##  Historial de eventos

SentinelGuard registra automáticamente los eventos más relevantes:

- Armados y desarmados
- Activación de modos
- Detección de sensores
- Cambios de estado del sistema

El historial permite:
- Revisar qué ocurrió
- En qué modo
- En qué momento
- Con qué sensor

Esto simula un sistema de auditoría básico, habitual en aplicaciones de seguridad.

---

##  Interfaz de usuario

La interfaz está diseñada con criterios de usabilidad y realismo:

- Navegación clara entre pantallas
- Estados visibles y comprensibles
- Botones adaptados al estado del sistema
- Mensajes informativos y notificaciones no intrusivas
- Pop-ups informativos persistentes para explicar modos

La UI se adapta dinámicamente al perfil del usuario y al estado actual del sistema.

---

##  Arquitectura y diseño

El proyecto sigue una arquitectura modular basada en:

- Separación entre:
  - Lógica de negocio
  - Persistencia
  - Interfaz gráfica
- Uso de funciones y módulos con responsabilidades claras
- Evitar dependencias circulares
- Mantener coherencia entre estados y vistas

El diseño está pensado para ser **extensible**, permitiendo añadir nuevos perfiles, modos o sensores sin romper la estructura existente.

---

## Ejecución del proyecto
Escriba en la terminal:

python3 app.py

---

##  Conclusión

SentinelGuard no es solo una simulación técnica, sino un ejercicio completo de diseño orientado a objetos aplicado a un sistema realista. El proyecto demuestra cómo integrar lógica, estado, persistencia e interfaz en una aplicación coherente, mantenible y comprensible.
