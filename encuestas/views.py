from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Encuesta, Respuesta, Pregunta, OpcionRespuesta
from .forms import ProspectoForm, EncuestaForm, PreguntaForm, OpcionRespuestaForm, OpcionRespuestaFormSet
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Este código define una vista de Django que crea una nueva encuesta. 
# si la solicitud es de tipo 'POST', se valida un formulario y se 
# guarda la nueva encuesta en la base de datos. Luego se redirige a 
# una página para crear preguntas para la encuesta. Si la solicitud 
# no es de tipo 'POST', se muestra el formulario para crear la encuesta.
def crear_encuesta(request):
    if request.method == 'POST': # si la solicitud es de tipo 'POST'
        form = EncuestaForm(request.POST) # se valida el formulario
        if form.is_valid(): # si el formulario es válido
            nueva_encuesta = form.save(commit=False) # se crea la nueva encuesta
            nuevo_grupo_nombre = form.cleaned_data.get('nuevo_grupo_nombre') # valor predeterminado None si no está presente
            disponible = form.cleaned_data.get('disponible', False) # valor predeterminado False si no está presente
            if nuevo_grupo_nombre: # si hay un nombre de grupo
                nuevo_grupo = Group.objects.create(name=nuevo_grupo_nombre) # se crea el nuevo grupo
                nueva_encuesta.grupo = nuevo_grupo # asigna el nuevo grupo
            nueva_encuesta.disponible = disponible # asigna el valor del campo disponible
            nueva_encuesta.save() # se guardan los cambios
            return redirect(reverse_lazy('crear_preguntas_encuesta', kwargs={'encuesta_id': nueva_encuesta.pk})) # se redirige a la página para crear preguntas para la encuesta
    else: # si la solicitud no es de tipo 'POST'
        form = EncuestaForm() # se muestra el formulario para crear la encuesta
    return render(request, 'encuestas/crear_encuesta.html', {'form': form}) # se renderiza el formulario

# Este código define una función llamada crear_preguntas_encuesta que toma 
# un request y un encuesta_id como parámetros. Obtiene un objeto Encuesta 
# basado en el encuesta_id proporcionado. Si el método de la solicitud es 'POST', 
# crea un PreguntaForm a partir de los datos de la solicitud, guarda los datos 
# del formulario en la base de datos, muestra un mensaje de éxito y limpia el 
# formulario para agregar más preguntas. Si el método de la solicitud no es 'POST', 
# inicializa un PreguntaForm vacío. Finalmente, renderiza una página con el 
# formulario y el objeto encuesta.
def crear_preguntas_encuesta(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en el encuesta_id proporcionado
    # si el método de la solicitud es 'POST'
    if request.method == 'POST': # crea un PreguntaForm a partir de los datos de la solicitud
        form = PreguntaForm(request.POST) # guarda los datos del formulario en la base de datos
        if form.is_valid(): # si el formulario es válido
            pregunta = form.save(commit=False) # se crea la nueva pregunta
            pregunta.encuesta = encuesta # se asigna la encuesta
            pregunta.save() # se guardan los cambios
            # mostrar un mensaje de éxito y limpiar el formulario para agregar más preguntas
            messages.success(request, '¡Pregunta creada exitosamente!')# se muestra el formulario
            form = PreguntaForm() # limpiar el formulario para agregar más preguntas
    else: # si el método de la solicitud no es 'POST'
        form = PreguntaForm() # inicializa un PreguntaForm vacío
    # renderiza una página con el formulario y el objeto encuesta
    return render(request, 'encuestas/crear_pregunta.html', {'form': form, 'encuesta': encuesta}) # se renderiza el formulario

# crearle opciones a las preguntas
# Este código define una función en Python que crea opciones de respuesta 
# para una pregunta. Primero, verifica si la solicitud es de tipo 'POST', 
# en cuyo caso procesa el formulario de la opción de respuesta. Si el formulario 
# es válido, guarda la opción asociada a la pregunta. Luego, muestra un mensaje 
# de éxito y limpia el formulario. Finalmente, renderiza la página 
# 'crear_opciones.html' con el formulario y la pregunta.
def crear_opciones(request, pregunta_id):# request y pregunta_id como parámetros
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id) # obtiene un objeto Pregunta basado en la pregunta_id proporcionada
    if request.method == 'POST': # verifica si la solicitud es de tipo 'POST'
        # Procesar el formulario de la aplicación de respuesta
        form = OpcionRespuestaForm(request.POST) # Guardar los datos del formulario
        if form.is_valid(): # si el formulario es válido
            opcion = form.save(commit=False) # crear la nueva opción
            opcion.pregunta = pregunta # asignar la pregunta
            opcion.save() # guardar los cambios
            # mostrar un mensaje de éxito o redirigir a la misma página para agregar más opciones
            messages.success(request, '¡Opción creada exitosamente!') # mostrar el formulario
            form = OpcionRespuestaForm()  # limpiar el formulario para agregar más opciones
    else: # si la solicitud no es de tipo 'POST'
        form = OpcionRespuestaForm() # inicializar el formulario para agregar más opciones
    # renderizar la página 'crear_opciones.html' con el formulario y la pregunta
    return render(request, 'encuestas/crear_opciones.html', {'form': form, 'pregunta': pregunta}) # renderizar el formulario

# Este fragmento de código maneja un formulario de pregunta y un conjunto 
# de formularios de opciones asociados. Primero, valida el formulario de 
# pregunta y lo guarda. Luego, si el tipo de pregunta no es 'texto_libre' 
# y el formulario de opciones es válido, guarda las opciones asociadas a 
# la pregunta. Finalmente, guarda los cambios en el formulario de pregunta 
# después de procesar los formularios.
def handle_pregunta_form(pregunta_form, opcion_formset): # pregunta_form y opcion_formset como parámetros
    if pregunta_form.is_valid(): # verifica si el formulario es válido
        pregunta = pregunta_form.save() # guardar la pregunta
        # si el tipo de pregunta no es 'texto_libre' y el formulario de opciones es válido 
        if pregunta.tipo != 'texto_libre' and opcion_formset.is_valid(): # verifica si el formulario de opciones es válido
            opciones = opcion_formset.save(commit=False) # crear las opciones
            for opcion in opciones: # recorrer las opciones
                opcion.pregunta = pregunta # asignar la pregunta
                opcion.save() # guardar las opciones
    # guardar los cambios en la pregunta después de procesar el formulario
    pregunta_form.save()

# Este código en Python define una función llamada editar_encuesta que maneja 
# la edición de una encuesta. Primero, se obtiene la encuesta a través de su 
# ID y se crea un formulario de encuesta. Luego se crean formularios para cada 
# pregunta y conjunto de opciones de respuesta de la encuesta. Después, se 
# verifica si la solicitud es de tipo POST y se procesan los datos enviados. 
# Si la encuesta y los formularios son válidos, se guardan los datos. 
# Finalmente, se renderiza un template con la encuesta, los formularios y 
# las preguntas con sus opciones de respuesta para ser editados.
def editar_encuesta(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en la encuesta_id proporcionada
    encuesta_form = EncuestaForm(request.POST or None, instance=encuesta) # crea un formulario de encuesta
    # se crean formularios para cada pregunta y conjunto de opciones de respuesta de la encuesta
    pregunta_forms = [PreguntaForm(request.POST or None, prefix=f'pregunta-{pregunta.id}', instance=pregunta) for pregunta in encuesta.preguntas.all()] # crea un formulario para cada pregunta
    opcion_formsets = [OpcionRespuestaFormSet(request.POST or None, prefix=f'opcion-{pregunta.id}', instance=pregunta) for pregunta in encuesta.preguntas.all()] # crea un conjunto de formularios para cada pregunta
    # verifica si la solicitud es de tipo POST y se procesan los datos enviados
    preguntas_y_opciones = zip(encuesta.preguntas.all(), pregunta_forms, opcion_formsets) # combina las preguntas, formularios y conjuntos de formularios en una tupla
    # si la encuesta y los formularios son válidos, se guardan los datos
    if request.method == 'POST': # verifica si la solicitud es de tipo POST
        # procesar el valor del checkbox disponible
        disponible = request.POST.get('disponible', False) # obtiene el valor del checkbox disponible
        if disponible == "on": # verifica si el valor del checkbox disponible es 'on'
            encuesta.disponible = True # establece disponible en True
        else: # si el valor del checkbox disponible es 'off'
            encuesta.disponible = False # establece disponible en False
        # guardar los datos
        if encuesta_form.is_valid(): # verifica si el formulario de encuesta es válido
            # guardar los datos
            encuesta_form.save()
        # procesar los formularios
        for pregunta_form, opcion_formset in zip(pregunta_forms, opcion_formsets): # recorre los formularios de preguntas y conjuntos de formularios
            handle_pregunta_form(pregunta_form, opcion_formset) # maneja el formulario de pregunta y el conjunto de formularios de opciones
        # redireccionar a la encuesta editada
        return redirect('editar_encuesta', encuesta_id=encuesta_id) # redirecciona a la encuesta editada
    # renderiza un template con la encuesta, los formularios y las preguntas con sus opciones de respuesta para ser editados
    return render(request, 'encuestas/editar_encuesta.html', {
        'encuesta': encuesta,
        'encuesta_form': encuesta_form,
        'preguntas_y_opciones': preguntas_y_opciones,
    })

# Este código define una función de vista en Django que agrega una opción a 
# una pregunta en una encuesta. Maneja tanto las solicitudes GET como POST. 
# La solicitud GET renderiza un formulario para agregar una opción, y la 
# solicitud POST guarda la nueva opción en la base de datos, además de 
# posiblemente mostrar una página de confirmación para eliminar opciones.
def agregar_opcion(request, pregunta_id): # request y pregunta_id como parámetros
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id) # obtiene un objeto Pregunta basado en la pregunta_id proporcionada
    # obtiene las opciones existentes de la pregunta
    opciones_existentes = pregunta.opciones.all() # obtiene todas las opciones de la pregunta
    # verifica si la solicitud es de tipo POST
    if request.method == 'POST': # si la solicitud es de tipo POST
        form = OpcionRespuestaForm(request.POST) # crea un formulario para agregar una opción
        opciones_a_eliminar = request.POST.getlist('opciones_a_eliminar') # obtiene la lista de opciones a eliminar
        # verifica si el formulario es válido
        if form.is_valid(): # si el formulario es válido
            opcion = form.save(commit=False) # crea una nueva opción
            opcion.pregunta = pregunta # asigna la pregunta
            opcion.save() # guarda la nueva opción
        # verifica si hay opciones a eliminar
        if opciones_a_eliminar: # si hay opciones a eliminar
            return render(request, 'encuestas/confirmar_eliminacion_opcion.html', { # renderiza una página de confirmación para eliminar opciones
                'pregunta': pregunta, # la pregunta
                'opciones_a_eliminar': opciones_a_eliminar, # las opciones a eliminar
            })
        # redirecciona a la misma página para agregar más opciones
        return redirect('agregar_opcion', pregunta_id=pregunta.id) # redirecciona a la misma página para agregar más opciones
    else: # si la solicitud no es de tipo POST
        form = OpcionRespuestaForm() # crea un formulario para agregar una línea
    # renderiza la página 'agregar_opcion.html' con el formulario y la pregunta
    return render(request, 'encuestas/agregar_opcion.html', {
        'form': form,
        'pregunta': pregunta,
        'opciones_existentes': opciones_existentes,
    })

# Este código define una función de vista llamada agregar_pregunta en Python que maneja 
# la lógica para agregar una nueva pregunta a una encuesta. La función renderiza un 
# formulario de pregunta en una plantilla HTML y procesa los datos del formulario 
# cuando se envía a través de un método POST. Si el formulario es válido, guarda 
# la nueva pregunta en la base de datos asociada a la encuesta y redirige a una 
# vista de edición de la encuesta. Si la solicitud es un GET, simplemente 
# muestra el formulario vacío.
def agregar_pregunta(request, encuesta_id): # request y encuesta_id como parámetros
    template_name = 'encuestas/agregar_pregunta.html' # nombre del template a renderizar
    # obtener la instancia de la encuesta actual
    encuesta = Encuesta.objects.get(id=encuesta_id) # obtiene la instancia de la encuesta actual
    # si la solicitud es de tipo POST
    if request.method == 'POST': # si la solicitud es de tipo POST
        pregunta_form = PreguntaForm(request.POST) # crea un formulario para agregar una pregunta
        if pregunta_form.is_valid(): # si el formulario es válido
            # guardar la nueva pregunta en la base de datos asociada a la encuesta
            nueva_pregunta = pregunta_form.save(commit=False) # guarda la nueva pregunta
            nueva_pregunta.encuesta_id = encuesta_id # asigna la encuesta
            nueva_pregunta.save() # guarda la nueva pregunta
            # redireccionar a la vista de edición de la encuesta            
            return redirect('editar_encuesta', encuesta_id=encuesta_id) # redireccionar a la vista de edición de la encuesta
    else: # si la solicitud no es de tipo POST
        pregunta_form = PreguntaForm() # crea un formulario para agregar una pregunta
    # renderizar la plantilla 'agregar_pregunta.html' con el formulario y la encuesta
    return render(request, template_name, {'pregunta_form': pregunta_form, 'encuesta': encuesta})

# Este código Python define una función que confirma la eliminación de una pregunta. 
# Primero, obtiene la pregunta con un ID específico. Luego, si la solicitud es de tipo 
# POST, elimina la pregunta y redirige a la página de edición de la encuesta a la que 
# pertenece la pregunta. Si la solicitud no es de tipo POST, muestra una plantilla de 
# confirmación con los detalles de la pregunta y la encuesta.
def confirmar_eliminacion_pregunta(request, pregunta_id): # request y pregunta_id como parámetros
    pregunta = get_object_or_404(Pregunta, id=pregunta_id) # obtiene un objeto Pregunta basado en la pregunta_id proporcionada
    encuesta_id = pregunta.encuesta.id # obtiene el ID de la encuesta a la que pertenece la pregunta
    # si la solicitud es de tipo POST
    if request.method == 'POST': # si la solicitud es de tipo POST
        pregunta.delete() # elimina la pregunta
        return redirect('editar_encuesta', encuesta_id=encuesta_id) # redirige a la vista de edición de la encuesta
    # si la solicitud no es de tipo POST
    return render(request, 'encuestas/confirmar_eliminacion_pregunta.html', {'pregunta': pregunta, 'encuesta_id': encuesta_id}) # renderiza la plantilla de confirmación

# Este código Python define una función llamada confirmar_eliminar_opcion 
# que se encarga de eliminar opciones de respuesta de una encuesta. 
# Primero, verifica si la solicitud es de tipo 'POST', en cuyo caso 
# obtiene las opciones a eliminar, las elimina una por una y redirige 
# a una vista específica. Si la solicitud no es 'POST', renderiza un 
# formulario de confirmación para la eliminación de la opción.
def confirmar_eliminar_opcion(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en el encuesta_id proporcionado
    # Si la solicitud es POST
    if request.method == 'POST': # crea un PreguntaForm a partir de los datos de la solicitud
        opciones_a_eliminar = request.POST.getlist('opciones_a_eliminar') # obtiene la lista de opciones a eliminar
        for opcion_id in opciones_a_eliminar: # recorre la lista de opciones a eliminar
            opcion = get_object_or_404(OpcionRespuesta, pk=opcion_id) # obtiene un objeto OpcionRespuesta basado en la opcion_id
            opcion.delete() # elimina la opcion
        # redirige a una vista específica
        pregunta_id = request.POST.get('pregunta_id') # obtiene el ID de la pregunta
        return redirect('agregar_opcion', pregunta_id=pregunta_id) # redirige a una vista específica
    # si la solicitud no es POST
    return render(request, 'confirmar_eliminacion_opcion.html', {'encuesta': encuesta}) # renderiza el formulario de confirmación

# confirmar la eliminacion
# Este código define una función llamada confirmar_eliminacion que toma dos parámetros, 
# request y encuesta_id. Dentro de la función, se obtiene un objeto Encuesta con el 
# encuesta_id proporcionado o se devuelve un error 404 si no se encuentra. Luego, se 
# renderiza una plantilla HTML llamada 'confirmar_eliminacion.html' 
# con la información de la encuesta.
def confirmar_eliminacion(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en el encuesta_id proporcionado
    return render(request, 'encuestas/confirmar_eliminacion.html', {'encuesta': encuesta}) # renderiza la plantilla HTML
# confirmar la eliminacion
def eliminar_encuesta(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en el encuesta_id proporcionado
    if request.method == 'POST': # si la solicitud es de tipo POST
        encuesta.delete() # elimina la encuesta
        messages.success(request, '¡Encuesta eliminada exitosamente!') # muestra un mensaje de éxito
        return redirect('lista_encuestas') # redirige a la lista de encuestas
    return redirect('confirmar_eliminacion', encuesta_id=encuesta_id) # redirige a la confirmación de eliminación

# Este código define una función lista_encuestas que toma request como 
# parámetro. Obtiene todos los objetos Encuesta de la base de datos y 
# los muestra utilizando la plantilla 'encuestas/lista_encuestas.html', 
# pasando las encuestas recuperadas como contexto.
def lista_encuestas(request): # request
    encuestas = Encuesta.objects.all() # obtiene todas las encuestas
    return render(request, 'encuestas/lista_encuestas.html', {'encuestas': encuestas}) # renderiza la plantilla

# Este código define una función de vista responder_encuesta en Django. 
# Maneja una solicitud POST para responder a una encuesta. Obtiene las 
# preguntas y opciones de la encuesta, procesa las respuestas, las guarda 
# como instancias de Respuesta y redirige a una página de 'gracias' al completar.
def responder_encuesta(request, encuesta_id): # request y encuesta_id como parámetros
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id) # obtiene un objeto Encuesta basado en el encuesta_id proporcionado
    preguntas = encuesta.preguntas.all().prefetch_related('opciones') # obtiene todas las preguntas de la encuesta y sus opciones
    # si la solicitud es POST
    if request.method == 'POST': # procesa las respuestas
        prospecto_form = ProspectoForm(request.POST) # crea un prospectoForm a partir de los datos de la adición
        if prospecto_form.is_valid(): # verifica si el formulario es válido
            prospecto = prospecto_form.save(commit=False) # crea un prospecto sin guardar
            prospecto.asistente = request.user # asociar el usuario actual al prospecto
            prospecto.save()  # guardar prospecto para obtener el ID
            # crear una instancia de Respuesta para cada pregunta
            for pregunta in preguntas: # recorre las preguntas
                respuesta_texto = '' # inicializar el texto de la respuesta
                if pregunta.tipo == 'seleccion_unica': # si la pregunta es de tipo 'seleccion_unica'
                    opcion_seleccionada_id = request.POST.get(f'opcion_{pregunta.id}') # obtener el ID de la opción seleccionada
                    opcion_seleccionada = pregunta.opciones.get(id=opcion_seleccionada_id) # obtener la instancia de la opción seleccionada
                    respuesta_texto = opcion_seleccionada.texto # establecer el texto de la respuesta
                #     
                elif pregunta.tipo == 'seleccion_multiple': # si la pregunta es de tipo 'seleccion_multiple'
                    opciones_seleccionadas_ids = request.POST.getlist(f'opcion_{pregunta.id}') # obtener los IDs de las opciones seleccionadas
                    opciones_seleccionadas = pregunta.opciones.filter(id__in=opciones_seleccionadas_ids) # obtener las instancias de las opciones seleccionadas
                    opciones_texto = [opcion.texto for opcion in opciones_seleccionadas] # crear una lista de los textos de las opciones seleccionadas
                    respuesta_texto = ', '.join(opciones_texto) # unir los textos de las opciones separados por comas
                else: # si la pregunta no es de tipo 'seleccion_unica' ni 'seleccion_multiple'
                    respuesta_texto = request.POST.get(f'respuesta_{pregunta.id}', '') # obtener el texto de la respuesta

                # crear una instancia de Respuesta solo si hay texto de respuesta
                if respuesta_texto: # si hay texto de respuesta
                    respuesta = Respuesta.objects.create( # crear una instancia de Respuesta
                        prospecto=prospecto, # asociar el prospecto
                        usuario=request.user, # asociar el usuario actual
                        encuesta=encuesta, # asociar la encuesta
                        pregunta=pregunta, # asociar la pregunta
                        texto_respuesta=respuesta_texto, # establecer el texto de la respuesta
                    ) # guardar la instancia de Respuesta
            # redirigir a la página 'gracias'
            return redirect('gracias')
    else: # si la adición no es POST
        prospecto_form = ProspectoForm() # crear un prospectoForm vacío
    # pasar el prospectoForm y las preguntas al contexto de la plantilla
    return render(request, 'encuestas/responder_encuesta.html', {'encuesta': encuesta, 'preguntas': preguntas, 'prospecto_form': prospecto_form}) # renderiza la plantilla

# Este código define una vista en Python para una aplicación web Django. 
# La vista muestra encuestas disponibles dependiendo del tipo de usuario 
# que esté autenticado. Si el usuario es un superusuario, se muestran 
# todas las encuestas. Si el usuario pertenece a un grupo, se muestran 
# las encuestas disponibles para ese grupo. Si el usuario no es superusuario 
# ni pertenece a un grupo, no se le muestran encuestas. Finalmente, se 
# renderiza una plantilla HTML con las encuestas disponibles.
@login_required # solo para usuarios autenticados
def encuestas_disponibles(request): # request
    if request.user.is_superuser: # si el usuario es superusuario
        # si el usuario es superusuario, mostrar todas las encuestas
        encuestas_disponibles = Encuesta.objects.all() # obtiene todas las encuestas
    elif request.user.groups.exists(): # si el usuario tiene más de un grupo
        # obtener el nombre del grupo del usuario autenticado
        nombre_grupo_usuario = request.user.groups.first().name # valor predeterminado None si no está presente
        # filtrar las encuestas disponibles por el nombre del grupo del usuario
        encuestas_disponibles = Encuesta.objects.filter(grupo__name=nombre_grupo_usuario, disponible=True) # obtiene las encuestas disponibles para el grupo del usuario
    else: # si el usuario no es superusuario ni tiene más de un grupo
        # no puede acceder a ninguna encuesta
        encuestas_disponibles = []
    # pasar las encuestas disponibles al contexto de la plantilla
    context = {
        'encuestas_disponibles': encuestas_disponibles
    }
    # renderiza la plantilla
    return render(request, 'encuestas/encuestas_disponibles.html', context)

# agradecimiento al finalizar la encuesta
def gracias_view(request):
    # Aquí puedes hacer cualquier lógica que necesites
    return render(request, 'encuestas/gracias.html')


