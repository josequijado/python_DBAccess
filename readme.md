# python_DBAccess
DBAccess es una clase basada en mysql_connector pensada para acceder a bases de datos MySQL.
Permite definir una conexión, un cursor, y ejecutar consultas, tanto de lectura como de inserción, actualización o eliminación de datos.
También permite destruir un cursor creado, cuando ya no lo vayamos a necesitar más, bien por haber terminado nuestra actividad, o por tener que crear otro, para operar sobre otra base de datos.

## Uso básico de la clase DBAccess
Para utilizar esta clase en un proyecto se recomienda crear un entorno virtual:

<pre>python -m venv bds</pre>

En esta línea, <code>bds</code> es el nombre que le daremos al proyecto. Por buenas prácticas, se aconseja que coincida con el nombre del directorio donde lo alojaremos.

Una vez creado el entorno virtual lo activaremos. Si estamos en MacOS o Linux usremos:
<pre>source bds/bin/activate</pre>
Si estamos trabajando en un entorno Windows usaremos:
<pre>bds\Scripts\activate.bat</pre>

Si en algún momento debemos salir del entorno virtual, simplemente lo desactivaremos con:
<pre>deactivate</pre>

A continuación instalaremos todas las dependencias del proyento en nuestro entorno virtual:
<pre>pip install -r requirements.txt</pre>

Crearemos un archivo <code>main.py</code> para poder usar la clase <code>DBAccess</code>. En la primera línea teclearemos:
<pre>from database import DBAccess</pre>
Esto nos permite importar la clase en nuestra aplicación.

A continuación tenemos que instanciar la clase en un objeto al que llamaremos, por ejemplo, <code>bases</code>. La forma más simple de hacerlo es la siguiente:
<pre>bases = DBAccess()</pre>
Esto crea un objeto con los siguientes parámetros por defecto:
<pre>
host = "localhost"
user = "root"
password = ""
</pre>

Si nuestros datos de conexión a MySQL son diferentes podemos especificarlos en el constructor:
<pre>bases = DBAccess(host="my_host", user = "my_user", password = "my_password")</pre>
Todos los parámetros son opcionales, si alguno de ellos nos vale con el valor por defecto, y deben especificarse nominalmente, como en el ejemplo.

El siguiente paso es crear una conexión a MySQL, y un cursor. Lo haremos así:
<pre>
bases.create_connection()
bases.create_cursor()
</pre>

A continuación podemos ver las bases de datos que tenemos disponibles, así:
<pre>bases.show_databases()</pre>

Para trabajar con una base de datos específica tenemos que activarla, así:
<pre>bases.select_database("my_database")</pre>
Si la base de datos existe, se activará. Si no existe, se crea automáticamente, y se activa.

A continuación podemos ver las tablas existentes en la base de datos activa, así:
<pre>
tablas = bases.get_tables()
print(tablas)
</pre>
Obviamente, si la base de datos es de nueva creación obtendremos una lista vacía. En caso contrario obtendremos una lista de las tablas que esxisten en la base de datos.

Si lo deseamos podemos crear una nueva tabla. Por ejemplo, usaremos la siguiente consulta:
<pre>
query = """
CREATE TABLE my_people (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(20) UNIQUE,
    name VARCHAR(150),
    email VARCHAR(100),
    birth_date DATE,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL  
);
"""
bases.set_data(query)
</pre>

Mediante el método <code>set_data()</code> podremos efecctuar cualquier consulta que modifique el contenido de una tabla de la base de datos, o de la base de datos en sí. Esto se refiere a consultas de inserción, actualizacón o eliminación. Por ejemplo, si queremos eliminar un registro específico de la tabla <code>my_people</code> haremos algo así:
<pre>
query = "DELETE FROM my_people WHERE dni = '12345678A'"
bases.set_data(query)
</pre>

Si el registro existe será eliminado. Si no existe, simplemente no se efectuarán cambios en la tabla.

Si queremos efectuar consultas de selección, es decir, de recuperación de datos, usaremos el método <code>get_data()</code>. Un ejemplo de uso sería el siguiente:
<pre>
query = "SELECT * FROM my_people WHERE dni = '12345678A'"
usuario = bases.get_data(query)
</pre>

Si el registro existe sus datos entrarán en la variable <code>usuario</code>. En caso contrario, esta variable quedará vacía.

##Otras operaciones##
Además del uso básico de esta clase, que hemos comentado, tenemos disponibles otras operaciones.

Para ver los permisos del usuario actual, usaremos el método <code>show_user_grants()</code>, así:
<pre>
permisos = bases.show_user_grants()
print(permisos)
</pre>

Para destruir el cursor que estamos empleando usaremos el método <code>close()</code>, como vemos a continuación:

<pre>bases.close()</pre>

##Consultas preparadas##
Esta clase no sería realmente útil si no pudiera ejecutar consultas preparadas para evitar la inyección SQL. Los métodos <code>get_data()</code> y <code>set_data()</code> aceptan un parámetro opcional llamado <code>params</code>. Podemos construir una consulta preparada de escritura, por ejemplo, así:

<pre>
query = "UPDATE my_people SET name = %s WHERE dni = %s"
params = ("John", "12345678A")
bases.set_data(query, params)
</pre>

Como se ve, <code>params</code> es una tupla con los parámetros necesarios para ejecutar la consulta.

En el caso de consultas de recuperación de datos (lectura) debemos usar el método <code>get_data()</code> así:

<pre>
query = "SELECT * FROM my_people WHERE dni = %s"
params = ("12345678A",)
result = bases.get_data(query, params)[0][0]
</pre>

Observa que si sólo hay un parámetro, debemos poner una coma después del mismo, para que la tupla sea reconocida como tal. También debes poner atención a los dos índices que hay después del método <code>get_data()</code> para recuperar los datos leidos. Si la condición de la claúsula <code>WHERE</code> no se cumple y, por lo tanto, no se obtienen datos de retorno la variable <code>result</code> valdrá <code>0</code>.
