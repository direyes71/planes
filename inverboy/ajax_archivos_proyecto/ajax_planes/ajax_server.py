# -*- encoding: utf-8 -*-

__author__ = 'Diegopc'

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from django.template import RequestContext
from django.shortcuts import render_to_response

from inverboy.models import *
from inverboy.forms import *

# Pagination
from inverboy.paginator import *

from PIL import Image

from inverboy.validaciones.validaciones import *
from inverboy.functions import *


@csrf_exempt
def test2(request):
    
    if not request.is_ajax():
        raise Http404

    data = [{'code': 'CD-1', 'label': 'P1', 'url': 'link', 'point_x': 3.1, 'point_y': -30.1}, {'code': 'CD-2', 'label': 'P2', 'url': 'link', 'point_x': 20.1, 'point_y': -40.1}, {'code': 'CD-3', 'label': 'P3', 'url': 'link', 'point_x': 40.1, 'point_y': -50.1}, {'code': 'CD-4', 'label': 'P4', 'url': 'link', 'point_x': 60.1, 'point_y': -60.1}]
    response_data = {}
    response_data['data'] = data
    response_data['error'] = '1'
    response_data['message'] = 'Listo javier'

    return HttpResponse(simplejson.dumps(response_data))

@csrf_exempt
def test3(request):

    if not request.is_ajax():
        raise Http404

    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            initials = form.cleaned_data['initials'].strip()
            error_unique_name, form = validate_unique_field(Phase, {'name': name, 'stage': stage}, fields_error=('name',), form=form)
            error_unique_initials, form = validate_unique_field(Phase, {'initials': initials, 'stage': stage}, fields_error=('initials',), form=form)
            if error_unique_name == False and error_unique_initials == False:
                phase = Phase()
                phase.name = name
                phase.initials = initials
                phase.description = form.cleaned_data['description'].strip()
                phase.image = form.cleaned_data['image_file']
                phase.stage = stage
                phase.save()
                return HttpResponseRedirect('/inverboy/home/phasesreport/' + str(stage_id) + '/' + str(project_id) + '/')
    else:
        form = StageForm() # A empty, unbound form
        project_id = request.GET['project_id']
        stage_id = request.GET['stage_id']

        #print project_id
        #print stage_id

    project = Proyecto.objects.get(id=project_id)
    stage = project.stage_set.get(id=stage_id)
    
    # Render list page with the phases and the form
    """
    return render_to_response(
        'planes/phaseadd.html',
        {'phases': phases, 'form': form, 'stage': stage, 'project': project},
        context_instance=RequestContext(request)
    )"""
    """return render_to_response(
        'planes/testform.html',
        {}
    )
    """
    return HttpResponse('hola mundo')



@csrf_exempt
def test4(request):
    if request.is_ajax():
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    return HttpResponse(message)


@csrf_exempt
def new_phase(request, stage_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.create_setup' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                # Handle file upload
                stage = project.stage_set.get(id=stage_id)
                if request.method == 'POST':
                    response_data = {}
                    form = StageForm(request.POST, request.FILES)
                    if form.is_valid():
                        name = form.cleaned_data['name'].strip()
                        initials = form.cleaned_data['initials'].strip()
                        error_unique_name, form = validate_unique_field(Phase, {'name': name, 'stage': stage}, fields_error=('name',), form=form)
                        error_unique_initials, form = validate_unique_field(Phase, {'initials': initials, 'stage': stage}, fields_error=('initials',), form=form)
                        if error_unique_name == False and error_unique_initials == False:
                            phase = Phase()
                            phase.name = name
                            phase.initials = initials
                            phase.description = form.cleaned_data['description'].strip()
                            phase.image = form.cleaned_data['image_file']
                            phase.stage = stage
                            phase.save()

                            response_data['result'] = '1'
                            response_data['message'] = 'La nueva fase ha sido registrada correctamente'
                            return HttpResponse(simplejson.dumps(response_data))
                            #return HttpResponseRedirect('/inverboy/home/phasesreport/' + str(stage_id) + '/' + str(project_id) + '/')

                    from django.template.loader import render_to_string

                    render =  render_to_string('planes/phaseadd.html', {'form': form, 'project': project},
                        context_instance=RequestContext(request))

                    response_data['data'] = {'form': render}
                    response_data['result'] = '0'
                    response_data['message'] = 'Error al crear la nueva fase'
                    return HttpResponse(simplejson.dumps(response_data))
                else:
                    form = StageForm() # A empty, unbound form

                return render_to_response(
                    'planes/phaseadd.html',
                    {'form': form, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


@csrf_exempt
def change_phase(request, phase_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.create_setup' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                # Handle file upload
                phase = Phase.objects.get(stage__project=project, id=phase_id)
                # Verify if the phase don't have relation image's plane
                if phase.can_be_eliminated():
                    if request.method == 'POST':
                        response_data = {}
                        form = StageForm(request.POST, request.FILES)
                        if form.is_valid():
                            name = form.cleaned_data['name'].strip()
                            initials = form.cleaned_data['initials'].strip()
                            error_unique_name, form = validate_unique_field(Phase, {'name': name, 'stage': phase.stage}, fields_error=('name',), exclude_initials_values={'name': phase.name, 'stage': phase.stage}, form=form)
                            error_unique_initials, form = validate_unique_field(Phase, {'initials': initials, 'stage': phase.stage}, fields_error=('initials',), exclude_initials_values={'initials': phase.initials, 'stage': phase.stage}, form=form)
                            if error_unique_name == False and error_unique_initials == False:
                                phase.name = name
                                phase.initials = initials
                                phase.description = form.cleaned_data['description'].strip()
                                phase.image = form.cleaned_data['image_file']
                                phase.save()
                                response_data['result'] = '1'
                                response_data['message'] = 'La nueva fase ha sido modificada correctamente'
                                return HttpResponse(simplejson.dumps(response_data))

                        from django.template.loader import render_to_string

                        render =  render_to_string('planes/phaseadd.html', {'form': form, 'project': project},
                            context_instance=RequestContext(request))

                        response_data['data'] = {'form': render}
                        response_data['result'] = '0'
                        response_data['message'] = 'Error al modificar la fase'
                        return HttpResponse(simplejson.dumps(response_data))
                    else:
                        form = StageForm(initial={'name': phase.name, 'initials': phase.initials, 'description': phase.description})

                    # Render list page with the documents and the form
                    return render_to_response(
                        'planes/phaseadd.html',
                        {'form': form, 'project': project},
                        context_instance=RequestContext(request)
                    )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


@csrf_exempt
def new_plane(request, phase_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600000)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.create_setup' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                # Handle file upload
                import os
                import settings

                # Handle file upload
                phase = Phase.objects.get(stage__project=project, id=phase_id)
                if request.method == 'POST':
                    response_data = {}
                    #trial_image = Image.open(request.FILES['image_file'])
                    #trial_image.load()

                    form = PlaneForm(request.POST, request.FILES)
                    if form.is_valid():
                        image_plane = form.save(commit=False)
                        image_plane.save()
                        if True:
                            # Create parts of zoom levels
                            size_square = 8192
                            width = 6400
                            height = 4800
                            space_white_width = 896
                            space_white_height = 1696
                            for i in range(1, 5, 1):
                                canvas = Image.new('RGB', (size_square, size_square), 'white')
                                image = Image.open(image_plane.thumb_image_file.path)
                                image = image.resize((width, height), Image.ANTIALIAS)
                                canvas.paste(image, (space_white_width, space_white_height))
                                image_crops = create_crops_image(canvas, 256, 256)
                                row_index = 0
                                for row_item in image_crops:
                                    col_index = 0
                                    for col_item in row_item:
                                        path_image = os.path.join(settings.MEDIA_ROOT, 'geo', 'project_' + str(image_plane.phase.stage.project.id), image_plane.phase.stage.initials, image_plane.phase.initials, image_plane.initials, 'map', str(6-(i)), str(row_index))
                                        if not os.path.isdir(path_image):
                                            os.makedirs(path_image)
                                        path_image = path_image + '/' + str(col_index) + '.jpg'
                                        col_item.save(path_image)
                                        col_index += 1
                                    row_index += 1
                                width = width / 2
                                height = height / 2
                                size_square = size_square / 2
                                space_white_width = space_white_width / 2
                                space_white_height = space_white_height / 2
                            # Redirect to the Plane list after POST
                            #return HttpResponseRedirect('/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(image_plane.phase.stage.project.id) + '/')
                            response_data['data'] = {'plane_id': image_plane.id}
                            response_data['result'] = '1'
                            response_data['message'] = 'El nuevo plano ha sido registrado correctamente.'
                            return HttpResponse(simplejson.dumps(response_data))

                    from django.template.loader import render_to_string

                    render =  render_to_string('planes/planeadd.html', {'form': form, 'phase': phase, 'project': project},
                        context_instance=RequestContext(request))

                    response_data['data'] = {'form': render}
                    response_data['result'] = '0'
                    response_data['message'] = 'Error al crear el nuevo plano'
                    return HttpResponse(simplejson.dumps(response_data))
                else:
                    form = PlaneForm() # A empty, unbound form
                return render_to_response(
                    'planes/planeadd.html',
                    {'form': form, 'phase': phase, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


@csrf_exempt
def change_plane(request, image_plane_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.create_setup' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                # Handle file upload
                import os
                import settings

                # Handle file upload
                image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
                # Verify if the image plane don't have relation photographic zone's plane
                if image_plane.can_be_eliminated():
                    if request.method == 'POST':
                        response_data = {}
                        form = ImagePlaneForm(request.POST, request.FILES)
                        if form.is_valid():
                            name = form.cleaned_data['name'].strip()
                            initials = form.cleaned_data['initials'].strip()
                            error_unique_name, form = validate_unique_field(ImagePlane, {'name': name, 'phase': image_plane.phase}, fields_error=('name',), exclude_initials_values={'name': image_plane.name, 'phase': image_plane.phase}, form=form)
                            error_unique_initials, form = validate_unique_field(ImagePlane, {'initials': initials, 'phase': image_plane.phase}, fields_error=('initials',), exclude_initials_values={'initials': image_plane.initials, 'phase': image_plane.phase}, form=form)
                            if error_unique_name == False and error_unique_initials == False:
                                image_plane.name = name
                                image_plane.initials = initials
                                image_plane.description = form.cleaned_data['description'].strip()
                                image_plane.thumb_image_file = form.cleaned_data['image_file']
                                image_plane.save()

                                # Create parts of zoom levels
                                size_square = 8192
                                width = 6400
                                height = 4800
                                space_white_width = 896
                                space_white_height = 1696
                                for i in range(1, 5, 1):
                                    canvas = Image.new('RGB', (size_square, size_square), 'white')
                                    image = Image.open(image_plane.thumb_image_file.path)
                                    image = image.resize((width, height), Image.ANTIALIAS)
                                    canvas.paste(image, (space_white_width, space_white_height))
                                    image_crops = create_crops_image(canvas, 256, 256)
                                    row_index = 0
                                    for row_item in image_crops:
                                        col_index = 0
                                        for col_item in row_item:
                                            path_image = os.path.join(settings.MEDIA_ROOT, 'geo', 'project_' + str(image_plane.phase.stage.project.id), image_plane.phase.stage.initials, image_plane.phase.initials, image_plane.initials, 'map', str(6-(i)), str(row_index))
                                            if not os.path.isdir(path_image):
                                                os.makedirs(path_image)
                                            path_image = path_image + '/' + str(col_index) + '.jpg'
                                            col_item.save(path_image)
                                            col_index += 1
                                        row_index += 1
                                    width = width / 2
                                    height = height / 2
                                    size_square = size_square / 2
                                    space_white_width = space_white_width / 2
                                    space_white_height = space_white_height / 2
                                # Redirect to the Plane list after POST
                                #return HttpResponseRedirect('/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(image_plane.phase.stage.project.id) + '/')
                                response_data['data'] = {'plane_id': image_plane.id}
                                response_data['result'] = '1'
                                response_data['message'] = 'El plano ha sido modificado correctamente.'
                                return HttpResponse(simplejson.dumps(response_data))

                        from django.template.loader import render_to_string

                        render =  render_to_string('planes/planeadd.html', {'form': form, 'phase': image_plane.phase, 'project': project},
                            context_instance=RequestContext(request))

                        response_data['data'] = {'form': render}
                        response_data['result'] = '0'
                        response_data['message'] = 'Error al modificar el plano'
                        return HttpResponse(simplejson.dumps(response_data))
                    else:
                        form = ImagePlaneForm(initial={'name': image_plane.name, 'initials': image_plane.initials, 'description': image_plane.description}) # A empty, unbound form

                    return render_to_response(
                        'planes/planeadd.html',
                        {'form': form, 'phase': image_plane.phase, 'project': project},
                        context_instance=RequestContext(request)
                    )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


@csrf_exempt
def photographiczonesplane_image_plane_add(request, image_plane_id, project_id):

    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)

    point_x = request.POST['point_x']
    point_y = request.POST['point_y']
    marker = request.POST['marker']

    photographic_zone_plane = PhotographicZonePlane()
    photographic_zone_plane.point_x = point_x
    photographic_zone_plane.point_y = point_y
    photographic_zone_plane.marker = marker
    photographic_zone_plane.image_plane = image_plane

    response_data = {}
    data = {}

    try:
        photographic_zone_plane.save()
        details_photographic_zone_plane = {'id': photographic_zone_plane.id, 'label': photographic_zone_plane.get_label(), 'url': photographic_zone_plane.get_url_details(), 'label_url': 'Detalles', 'point_x': photographic_zone_plane.point_x, 'point_y': photographic_zone_plane.point_y, 'marker': photographic_zone_plane.marker, 'details': {'see_more': 0, 'delete': 1}}
        response_data['data'] = details_photographic_zone_plane
        response_data['result'] = '1'
        response_data['message'] = 'El nuevo punto fotografico ha sido creado'
    except :
        response_data['data'] = data
        response_data['result'] = '0'
        response_data['message'] = 'No se ha podido crear en nuevo punto fotografico'
    return HttpResponse(simplejson.dumps(response_data))


@csrf_exempt
def photographiczonesplane_image_plane_remove(request, image_plane_id, photographiczoneplane_id, project_id):
    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
    photographiczoneplane = image_plane.photographiczoneplane_set.get(id=photographiczoneplane_id)
    response_data = {}
    if photographiczoneplane.can_be_eliminated():
        try:
            photographiczoneplane.delete()
            response_data['result'] = '1'
            response_data['message'] = 'El punto fotografico ha sido eliminado'
            return HttpResponse(simplejson.dumps(response_data))
        except :
            photographiczoneplane.delete()
            response_data['result'] = '0'
            response_data['message'] = 'Ha ocurrido un error al eliminar el punto fotografico'
            return HttpResponse(simplejson.dumps(response_data))
    response_data['result'] = '0'
    response_data['message'] = 'No es posible eliminar el punto fotografico'
    return HttpResponse(simplejson.dumps(response_data))




@csrf_exempt
def get_photographiczonesplane_image_plane(request, image_plane_id, project_id):
    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
    photographic_zones_plane = image_plane.photographiczoneplane_set.all()
    data = []
    for photographic_zone_plane in photographic_zones_plane:
        details_photographic_zone_plane = {'id': photographic_zone_plane.id, 'label': photographic_zone_plane.get_label(), 'url': photographic_zone_plane.get_url_details(), 'label_url': 'Detalles', 'point_x': photographic_zone_plane.point_x, 'point_y': photographic_zone_plane.point_y, 'marker': photographic_zone_plane.marker, 'details': {'see_more': 0, 'delete': 0}}
        if len(photographic_zone_plane.chronologicalpicture_set.all()) > 0:
            details_photographic_zone_plane['details']['see_more'] = 1
        if photographic_zone_plane.can_be_eliminated():
            details_photographic_zone_plane['details']['delete'] = 1
        data.append(details_photographic_zone_plane)
    response_data = {}
    response_data['data'] = data
    response_data['result'] = '1'
    response_data['message'] = 'successful!!'
    return HttpResponse(simplejson.dumps(response_data))


@csrf_exempt
def new_published_project(request, project_id):
    #Checks whether the user session start
    from django.contrib.sessions.models import Session
    session = None
    try:
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
    except :
        pass
    if session != None:
        #Get User from sessionid
        user_id = session.get_decoded().get('_auth_user_id')
        project_id = request.POST.get('project')
        project = Proyecto.objects.get(id=project_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        user = Usuario.objects.get(id=user_id)
        if project in user.lista_proyectos_vinculados():
            if request.method == 'POST':
                form = PublishedProjectForm(request.POST)
                if form.is_valid():
                    published = PublishedProject()
                    published.text = form.cleaned_data['text']
                    published.user = user
                    published.project = project
                    published.save()
                    data = {'user_name': str(user.full_name()), 'published_id': published.id, 'date': published.str_publication_date(), 'text': published.text}
                    response_data = {}
                    response_data['data'] = data
                    response_data['result'] = '1'
                    response_data['message'] = 'successful!!'
                    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
                else:
                    data = {'form': 1}
                    response_data = {}                    
                    response_data['data'] = data
                    response_data['result'] = '0'
                    response_data['message'] = 'ERROR'
                    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
            else:
                return Http404


@csrf_exempt
def new_comment_published_project(request, published_project_id, project_id):
    #Checks whether the user session start
    from django.contrib.sessions.models import Session
    session = None
    try:
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
    except :
        pass
    if session != None:
        #Get User from sessionid
        user_id = session.get_decoded().get('_auth_user_id')
        project_id = request.POST.get('project')
        project = Proyecto.objects.get(id=project_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        user = Usuario.objects.get(id=user_id)
        if project in user.lista_proyectos_vinculados():
            if request.method == 'POST':
                published = project.publishedproject_set.get(id=published_project_id)
                form = CommentPublishedProjectForm(request.POST)
                if form.is_valid():
                    comment_published = CommentPublishedProject()
                    comment_published.text = form.cleaned_data['text']
                    comment_published.user = user
                    comment_published.published = published
                    comment_published.save()
                    data = {'user_name': str(user.full_name()), 'published_id': published.id, 'comment_published_id': comment_published.id, 'date': comment_published.str_publication_date(), 'text': comment_published.text}
                    response_data = {}
                    response_data['data'] = data
                    response_data['result'] = '1'
                    response_data['message'] = 'successful!!'
                    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
                else:
                    data = {'form': 1}
                    response_data = {}
                    response_data['data'] = data
                    response_data['result'] = '0'
                    response_data['message'] = 'ERROR'
                    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
            else:
                return Http404


@csrf_exempt
def comments_published_project(request, published_id, project_id):
    #Checks whether the user session start
    from django.contrib.sessions.models import Session
    session = None
    try:
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
    except :
        pass
    if session != None:
        #Get User from sessionid
        user_id = session.get_decoded().get('_auth_user_id')
        project = Proyecto.objects.get(id=project_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        user = Usuario.objects.get(id=user_id)
        if project in user.lista_proyectos_vinculados():
            if request.method == 'POST':
                # Load publications for the list page
                published = project.publishedproject_set.get(id=published_id)

                from django.template.loader import render_to_string

                render =  render_to_string('ajax/planes/commentspublishedproject.html', {'published': published},
                    context_instance=RequestContext(request))

                data = {'html': render}

                response_data = {}
                response_data['data'] = data
                response_data['result'] = '1'
                response_data['message'] = 'successful!!'
                return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

            else:
                return Http404


@csrf_exempt
def paged_publications_project(request, page, project_id):
    #Checks whether the user session start
    from django.contrib.sessions.models import Session
    session = None
    try:
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
    except :
        pass
    if session != None:
        #Get User from sessionid
        user_id = session.get_decoded().get('_auth_user_id')
        project = Proyecto.objects.get(id=project_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        user = Usuario.objects.get(id=user_id)
        if project in user.lista_proyectos_vinculados():
            if request.method == 'POST':
                # Load publications for the list page
                publications = project.publications_list(number=0)
                
                pag = Paginador(request, publications, 20, int(page))

                from django.template.loader import render_to_string

                render =  render_to_string('ajax/planes/publicationsproject.html', {'publications': pag},
                    context_instance=RequestContext(request))

                data = {'html': render}

                response_data = {}
                response_data['data'] = data
                response_data['result'] = '1'
                response_data['message'] = 'successful!!'
                return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

            else:
                return Http404


@csrf_exempt
def list_dates_photographic_zone_plane_project(request, photographic_zone_plane_id, project_id):
    #Checks whether the user session start
    from django.contrib.sessions.models import Session
    session = None
    try:
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
    except :
        pass
    if session != None:
        #Get User from sessionid
        user_id = session.get_decoded().get('_auth_user_id')
        project = Proyecto.objects.get(id=project_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        user = Usuario.objects.get(id=user_id)
        if project in user.lista_proyectos_vinculados():
            if request.method == 'POST':
                # Load dates photographic zone plane
                photographic_zone_plane = PhotographicZonePlane.objects.get(id=photographic_zone_plane_id, image_plane__phase__stage__project=project)

                chronological_picures = photographic_zone_plane.chronologicalpicture_set.all().order_by('date')

                list_dates = []

                for chronological_picure in chronological_picures:
                    list_dates.append({'date': chronological_picure.date.strftime('%Y-%m-%d'), 'url': str(chronological_picure.id)})

                data = {'data': list_dates}

                response_data = {}
                response_data['data'] = data
                response_data['result'] = '1'
                response_data['message'] = 'successful!!'
                return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

            else:
                return Http404