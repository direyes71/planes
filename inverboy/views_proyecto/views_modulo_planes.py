# -*- encoding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.db.models import Q

from PIL import Image

from inverboy.models import *
from inverboy.forms import *

# Pagination
from inverboy.paginator import *

from inverboy.validaciones.validaciones import *

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImagePlaneForm(request.POST, request.FILES)
        if form.is_valid():
            #archivos = request.FILES['docfile']
            archivos = request.FILES.getlist('image_file')

            for archivo in archivos:
                newdoc = ImagePlane(image_file=archivo, thumb_image_file=archivo)
                newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('inverboy.views.list'))
    else:
        form = ImagePlaneForm() # A empty, unbound form

    # Load documents for the list page
    images = ImagePlane.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'planes/list.html',
        {'images': images, 'form': form},
        context_instance=RequestContext(request)
    )


def new_stage(request, project_id):
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
                if request.method == 'POST':
                    form = StageForm(request.POST, request.FILES)
                    if form.is_valid():
                        name = form.cleaned_data['name'].strip()
                        initials = form.cleaned_data['initials'].strip()
                        error_unique_name, form = validate_unique_field(Stage, {'name': name, 'project': project}, fields_error=('name',), form=form)
                        error_unique_initials, form = validate_unique_field(Stage, {'initials': initials, 'project': project}, fields_error=('initials',), form=form)
                        if error_unique_name == False and error_unique_initials == False:
                            stage = Stage()
                            stage.name = name
                            stage.initials = initials
                            stage.description = form.cleaned_data['description'].strip()
                            stage.image = form.cleaned_data['image_file']
                            stage.project = project
                            stage.save()
                            return HttpResponseRedirect('/inverboy/home/stagesreport/' + str(project_id) + '/')
                else:
                    form = StageForm() # A empty, unbound form

                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(project_id) + '/', 'label': image_plane.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = 'Etapas del proyecto'

                # Render list page with the documents and the form
                return render_to_response(
                    'planes/stagesreport.html',
                    {'stages': stages, 'form': form, 'flag_stage': True, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def change_stage(request, stage_id, project_id):
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
                # Verify if the phase don't have relation phase's
                if stage.can_be_eliminated():
                    if request.method == 'POST':
                        form = StageForm(request.POST, request.FILES)
                        if form.is_valid():
                            name = form.cleaned_data['name'].strip()
                            initials = form.cleaned_data['initials'].strip()
                            error_unique_name, form = validate_unique_field(Stage, {'name': name, 'project': project}, fields_error=('name',), exclude_initials_values={'name': stage.name, 'project': project}, form=form)
                            error_unique_initials, form = validate_unique_field(Stage, {'initials': initials, 'project': project}, fields_error=('initials',), exclude_initials_values={'initials': stage.initials, 'project': project}, form=form)
                            if error_unique_name == False and error_unique_initials == False:
                                stage.name = name
                                stage.initials = initials
                                stage.description = form.cleaned_data['description'].strip()
                                stage.image = form.cleaned_data['image_file']
                                stage.save()
                                return HttpResponseRedirect('/inverboy/home/stagesreport/' + str(project_id) + '/')
                    else:
                        form = StageForm(initial={'name': stage.name, 'initials': stage.initials, 'description': stage.description}) # A empty, unbound form

                    stages = project.stage_set.all()

                    # Create the nav_menu
                    nav_menu = []
                    for stage in stages:
                        items_menu_1 = []
                        for phase in stage.phase_set.all():
                            items_menu_2 = []
                            for image_plane in phase.imageplane_set.all():
                                items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(project_id) + '/', 'label': image_plane.name})
                            items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                        item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                        nav_menu.append(item_nav_menu)

                    # Board title
                    board_title = 'Etapas del proyecto'

                    # Render list page with the documents and the form
                    return render_to_response(
                        'planes/stagesreport.html',
                        {'stages': stages, 'form': form, 'flag_stage': True, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                        context_instance=RequestContext(request)
                    )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def delete_stage(request, stage_id, project_id):
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
                import settings
                import os
                import shutil
                project = Proyecto.objects.get(id=project_id)
                stage = project.stage_set.get(id=stage_id)
                # Verify if the stage don't have relation phase's
                if stage.can_be_eliminated():
                    stage.delete()
                    #Delete directory if it's there
                    directory = os.path.join(settings.MEDIA_URL, 'geo', 'project_' + str(stage.project.id), stage.initials)
                    if os.path.isdir(directory):
                        shutil.rmtree(directory)
                    return HttpResponseRedirect('/inverboy/home/stagesreport/' + str(project_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def stages_report(request, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_stage' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                criterion  = ''

                if request.method == 'POST':
                    criterion = request.POST['criterion'].strip()

                # Load stages for the list page
                stages = project.stage_set.filter(Q(name__icontains=criterion) | Q(initials=criterion))

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(project_id) + '/', 'label': image_plane.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = 'Etapas del proyecto'

                # Render list page with the stages and the form
                return render_to_response(
                    'planes/stagesreport.html',
                    {'stages': stages, 'criterion': criterion, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def change_phase(request, phase_id, stage_id, project_id):
    # Handle file upload
    project = Proyecto.objects.get(id=project_id)
    stage = project.stage_set.get(id=stage_id)
    phase = stage.phase_set.get(id=phase_id)
    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            initials = form.cleaned_data['initials'].strip()
            error_unique_name, form = validate_unique_field(Phase, {'name': name, 'stage': stage}, fields_error=('name',), exclude_initials_values={'name': phase.name, 'stage': phase.stage}, form=form)
            error_unique_initials, form = validate_unique_field(Phase, {'initials': initials, 'stage': stage}, fields_error=('initials',), exclude_initials_values={'initials': phase.initials, 'stage': stage}, form=form)
            if error_unique_name == False and error_unique_initials == False:
                phase.name = name
                phase.initials = initials
                phase.description = form.cleaned_data['description'].strip()
                phase.image = form.cleaned_data['image_file']
                phase.save()
                return HttpResponseRedirect('/inverboy/home/phasesreport/' + str(stage_id) + '/' + str(project_id) + '/')
    else:
        form = StageForm(initial={'name': phase.name, 'initials': phase.initials})

    # Render list page with the documents and the form
    return render_to_response(
        'planes/stageadd.html',
        {'form': form, 'project': project},
        context_instance=RequestContext(request)
    )


def delete_phase(request, phase_id, stage_id, project_id):
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
                import os
                import settings
                stage = project.stage_set.get(id=stage_id)
                phase = stage.phase_set.get(id=phase_id)
                # Verify if the phase don't have relation image's plane
                if phase.can_be_eliminated():
                    phase.delete()
                    #Delete directory if it's there
                    directory = os.path.join(settings.MEDIA_URL, 'geo', 'project_' + str(phase.stage.project.id), phase.stage.initials, phase.initials)
                    if os.path.isdir(directory):
                        os.unlink(directory)
                    return HttpResponseRedirect('/inverboy/home/phasesreport/' + str(stage_id) + '/' + str(project_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def phases_report(request, stage_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_stage' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                stage = project.stage_set.get(id=stage_id)
                criterion  = ''

                if request.method == 'POST':
                    criterion = request.POST['criterion'].strip()

                # Load phases for the list page
                phases = stage.phase_set.all()
                phases = phases.filter(Q(name__icontains=criterion) | Q(initials=criterion))

                # Load stages for the list page
                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage_list in stages:
                    items_menu_1 = []
                    for phase in stage_list.phase_set.all():
                        items_menu_2 = []
                        for image_plane in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(project_id) + '/', 'label': image_plane.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage_list.id) + '/' + str(project_id) + '/', 'label': stage_list.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = stage.name

                # Render list page with the phases and the form
                return render_to_response(
                    'planes/phasesreport.html',
                    {'phases': phases, 'criterion': criterion, 'stage': stage, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def new_plane(request, phase_id, project_id):
    import os
    import settings

    # Handle file upload
    project = Proyecto.objects.get(id=project_id)
    phase = Phase.objects.get(stage__project=project, id=phase_id)
    if request.method == 'POST':
        form = ImagePlaneForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            initials = form.cleaned_data['initials'].strip()
            error_unique_name, form = validate_unique_field(ImagePlane, {'name': name, 'phase': phase}, fields_error=('name',), form=form)
            error_unique_initials, form = validate_unique_field(ImagePlane, {'initials': initials, 'phase': phase}, fields_error=('initials',), form=form)
            if error_unique_name == False and error_unique_initials == False:
                image_plane = ImagePlane()
                image_plane.name = name
                image_plane.initials = initials
                image_plane.description = form.cleaned_data['description'].strip()
                image_plane.thumb_image_file = form.cleaned_data['image_file']
                image_plane.phase = phase
                image_plane.project = project
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
                            path_image = os.path.join(settings.MEDIA_ROOT, 'geo', 'project_' + str(image_plane.project.id), image_plane.phase.stage.initials, image_plane.phase.initials, image_plane.initials, 'map', str(6-(i)), str(row_index))
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
                return HttpResponseRedirect('/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(image_plane.phase.stage.project.id) + '/')
    else:
        form = ImagePlaneForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'planes/planeadd.html',
        {'form': form, 'phase': phase, 'project': project},
        context_instance=RequestContext(request)
    )


def plane_description(request, plane_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_stage' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                import string
                image_plane = ImagePlane.objects.get(id=plane_id)

                array_path = image_plane.thumb_image_file.__str__().split('/')

                array_path.pop()
                array_path.append('map')

                path_map = string.join(array_path, '/')

                # Load stages for the list page
                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane_current in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane_current.id) + '/' + str(project_id) + '/', 'label': image_plane_current.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = image_plane.name + ' - ' + image_plane.initials

                # Render image_plane
                return render_to_response(
                    'planes/plane.html',
                    {'path_map': path_map, 'image_plane': image_plane, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def delete_image_plane(request, image_plane_id, project_id):
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
                import os
                import settings
                image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
                # Verify if the phase don't have relation photographic zone's plane
                if image_plane.can_be_eliminated():
                    phase = image_plane.phase
                    #Delete directory if it's there
                    directory = os.path.join(settings.MEDIA_URL, 'geo', 'project_' + str(image_plane.phase.stage.project.id), image_plane.phase.stage.initials, image_plane.phase.initials, image_plane.initials)
                    if os.path.isdir(directory):
                        os.unlink(directory)
                    #Delete image_plane
                    image_plane.delete()
                    return HttpResponseRedirect('/inverboy/home/phasesreport/' + str(phase.stage.id) + '/' + str(project_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def create_crops_image(image, crop_x, crop_y):
    image_crops = []
    width, height = image.size
    x_crop = 0
    while x_crop < width:
        y_crop = 0
        list_crops = []
        while y_crop < height:
            list_crops.append(image.crop((x_crop, y_crop, x_crop + crop_x, y_crop + crop_y)))
            y_crop = y_crop + crop_y
        image_crops.append(list_crops)
        x_crop = x_crop + crop_x
    return image_crops


# Chronological pictures report
def chronological_pictures_report(request, photographic_zone_plane_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_stage' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                import string
                photographic_zone_plane = PhotographicZonePlane.objects.get(id=photographic_zone_plane_id, image_plane__phase__stage__project=project)
                chronological_pictures = photographic_zone_plane.chronologicalpicture_set.all().order_by('-date')
                current_picture = None
                picture_previous = None
                picture_forward = None
                if len(chronological_pictures) > 0:
                    current_picture = chronological_pictures[0]
                    array_path = current_picture.thumb_image_file.url.split('/')
                    array_path.pop()
                    array_path.append('map')
                    current_picture.path_map = string.join(array_path, '/')
                    if len(chronological_pictures) > 1:
                        picture_forward = chronological_pictures[1]
                else:
                    chronological_pictures = None

                criterion = ''

                # Load stages for the list page
                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane_current in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane_current.id) + '/' + str(project_id) + '/', 'label': image_plane_current.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = 'Fotos ' + photographic_zone_plane.image_plane.name + ' - ' + photographic_zone_plane.get_label()

                # Render list page with the phases and the form
                return render_to_response(
                    'planes/chronologicalpicturesreport.html',
                    {'pictures': chronological_pictures, 'current_picture': current_picture, 'picture_previous': picture_previous, 'picture_forward': picture_forward, 'criterion': criterion, 'photographic_zone_plane': photographic_zone_plane, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Chronological pictures report (reload picture)
def chronological_pictures_report_picture_details(request, chronological_picture_id, photographic_zone_plane_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_stage' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                import string
                photographic_zone_plane = PhotographicZonePlane.objects.get(id=photographic_zone_plane_id, image_plane__phase__stage__project=project)
                chronological_pictures = photographic_zone_plane.chronologicalpicture_set.all().order_by('-date')
                current_picture = None
                picture_previous = None
                picture_forward = None
                if len(chronological_pictures) > 0:
                    index_picture = 0
                    for chronological_picture in chronological_pictures:
                        if chronological_picture.id == int(chronological_picture_id):
                            current_picture = chronological_pictures.get(id=chronological_picture_id)
                            array_path = current_picture.thumb_image_file.url.split('/')
                            array_path.pop()
                            array_path.append('map')
                            current_picture.path_map = string.join(array_path, '/')
                            if index_picture > 0:
                                picture_previous = chronological_pictures[index_picture - 1]
                            if index_picture < len(chronological_pictures) - 1:
                                picture_forward = chronological_pictures[index_picture + 1]
                        index_picture += 1

                criterion = ''

                # Load stages for the list page
                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane_current in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane_current.id) + '/' + str(project_id) + '/', 'label': image_plane_current.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = 'Fotos ' + photographic_zone_plane.image_plane.name + ' - ' + photographic_zone_plane.get_label()

                # Render list page with the phases and the form
                return render_to_response(
                    'planes/chronologicalpicturesreport.html',
                    {'pictures': chronological_pictures, 'current_picture': current_picture, 'picture_previous': picture_previous, 'picture_forward': picture_forward, 'criterion': criterion, 'photographic_zone_plane': photographic_zone_plane, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Delete chronological picture
def delete_chronological_picture(request, chronological_picture_id, photographic_zone_plane_id, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.delete_chronologicalpicture' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                import string
                import os
                import shutil
                import settings
                photographic_zone_plane = PhotographicZonePlane.objects.get(id=photographic_zone_plane_id, image_plane__phase__stage__project=project)
                chronological_pictures = photographic_zone_plane.chronologicalpicture_set.all().order_by('-date')
                current_picture = None
                picture_previous = None
                picture_forward = None
                if len(chronological_pictures) > 0:
                    index_picture = 0
                    for chronological_picture in chronological_pictures:
                        if chronological_picture.id == int(chronological_picture_id):
                            #Delete chronological picture
                            array_path = chronological_picture.thumb_image_file.url.split('/')
                            array_path.pop()
                            path_map = ''
                            for item_path in array_path:
                                path_map = os.path.join(path_map, item_path)
                            path_map = os.path.join(settings.MEDIA_ROOT, path_map)
                            if os.path.isdir(path_map):
                                shutil.rmtree(path_map, True)
                            chronological_picture.delete()
                            current_picture = None
                            index_picture += 1
                            if index_picture < len(chronological_pictures):
                                current_picture = chronological_pictures[index_picture]
                            if index_picture == len(chronological_pictures) and index_picture > 1:
                                current_picture = chronological_pictures[index_picture-2]
                            if current_picture:
                                return HttpResponseRedirect('/inverboy/home/cronologicalpicturesreport/' + str(current_picture.id) + '/' + str(photographic_zone_plane_id) + '/' + str(project_id) + '/')
                            else:
                                return HttpResponseRedirect('/inverboy/home/planedescription/'+ str(photographic_zone_plane.image_plane_id) + '/' + str(project_id) + '/')
                        index_picture += 1
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def upload_chronological_pictures(request, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.upload_chronologicalpicture' in user.get_all_permissions() or True:
            try:
                project = Proyecto.objects.get(id=project_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if project in usuario.lista_proyectos_vinculados():
                import settings
                import os
                import re

                upload_files = []
                if request.method == 'POST':
                    form = MultipleUploadChronologicalPicturesForm(request.POST, request.FILES)
                    if form.is_valid():
                        archivos = request.FILES.getlist('image_file')
                        # Manager corrupt_files
                        corrupt_files_correct_format = []
                        corrupt_files_correct_project = []
                        corrupt_files_correct_initials_stage = []
                        corrupt_files_correct_initials_phase = []
                        corrupt_files_correct_initials_image_plane = []
                        corrupt_files_correct_photographic_zone_plane = []
                        corrupt_files_correct_date = []
                        for archivo in archivos:
                            file_name = archivo.name.split('.')[0]
                            correct_format = re.match('^\d{1,3}\-\w{1,3}\-\w{1,3}\-\w{1,3}\-[pP]{1}-?[0-9]+\-(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', file_name)
                            if correct_format != None:
                                convention_labels = {'project_id': 0, 'init_stage': '', 'init_phase': '', 'init_image_plane': '', 'photographic_zone': '', 'yyyy': '', 'mm': '', 'dd': ''}
                                array_name = file_name.split('-')
                                # Validate project_id
                                if int(array_name[0]) == int(project_id):
                                    convention_labels['project_id'] = array_name[0]
                                    convention_labels['init_stage'] = array_name[1]
                                    convention_labels['init_phase'] = array_name[2]
                                    convention_labels['init_image_plane'] = array_name[3]
                                    convention_labels['photographic_zone'] = array_name[4] + array_name[5]
                                    convention_labels['yyyy'] = array_name[6]
                                    convention_labels['mm'] = array_name[7]
                                    convention_labels['dd'] = array_name[8]
                                    print convention_labels
                                    # Validate stage_initials
                                    stage = None
                                    try:
                                        stage = project.stage_set.get(initials=convention_labels['init_stage'])
                                    except :
                                        pass
                                    if stage != None:
                                        # Validate phase_initials
                                        phase = None
                                        try:
                                            phase = stage.phase_set.get(initials=convention_labels['init_phase'])
                                        except :
                                            pass
                                        if phase != None:
                                            # Validate image_plane_initials
                                            image_plane = None
                                            try:
                                                image_plane = phase.imageplane_set.get(initials=convention_labels['init_image_plane'])
                                            except :
                                                pass
                                            if image_plane != None:
                                                # Validate photographic_zone_plane
                                                photographic_zone_plane = None
                                                try:
                                                    print convention_labels['photographic_zone']
                                                    print convention_labels['photographic_zone'][1:]
                                                    photographic_zone_plane = image_plane.photographiczoneplane_set.get(consecutive=convention_labels['photographic_zone'][1:])
                                                except :
                                                    pass
                                                if photographic_zone_plane != None:
                                                    # Validate unique picture in photographic_zone (Date)
                                                    unique_picture = None
                                                    try:
                                                        unique_picture = photographic_zone_plane.chronologicalpicture_set.get(date=convention_labels['yyyy'] + '-' + convention_labels['mm'] + '-' + convention_labels['dd'])
                                                    except :
                                                        pass
                                                    if unique_picture == None:
                                                        chronological_picture = ChronologicalPicture()
                                                        chronological_picture.code = file_name
                                                        chronological_picture.date = convention_labels['yyyy'] + '-' + convention_labels['mm'] + '-' + convention_labels['dd']
                                                        chronological_picture.thumb_image_file = archivo
                                                        chronological_picture.photographic_zone_plane = photographic_zone_plane
                                                        chronological_picture.save()

                                                        # Create parts of zoom levels
                                                        size_square = 8192
                                                        width = 6400
                                                        height = 4800
                                                        space_white_width = 896
                                                        space_white_height = 1696
                                                        for i in range(1, 5, 1):
                                                            canvas = Image.new('RGB', (size_square, size_square), 'white')
                                                            image = Image.open(chronological_picture.thumb_image_file.path)
                                                            image = image.resize((width, height), Image.ANTIALIAS)
                                                            canvas.paste(image, (space_white_width, space_white_height))
                                                            image_crops = create_crops_image(canvas, 256, 256)
                                                            row_index = 0
                                                            for row_item in image_crops:
                                                                col_index = 0
                                                                for col_item in row_item:
                                                                    path_image = os.path.join(settings.MEDIA_ROOT, 'geo', 'project_' + str(chronological_picture.photographic_zone_plane.image_plane.phase.stage.project.id), chronological_picture.photographic_zone_plane.image_plane.phase.stage.initials, chronological_picture.photographic_zone_plane.image_plane.phase.initials, chronological_picture.photographic_zone_plane.image_plane.initials, 'chronological_line', 'P' + str(chronological_picture.photographic_zone_plane.consecutive), convention_labels['yyyy'], convention_labels['mm'], convention_labels['dd'], 'map', str(6-(i)), str(row_index))
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
                                                        # save the object
                                                        upload_files.append(archivo)
                                                        # Redirect to the Plane list after POST
                                                        # return HttpResponseRedirect('/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(image_plane.phase.stage.project.id) + '/')
                                                    else:
                                                        corrupt_files_correct_date.append(archivo)
                                                else:
                                                    corrupt_files_correct_photographic_zone_plane.append(archivo)
                                            else:
                                                corrupt_files_correct_initials_image_plane.append(archivo)
                                        else:
                                            corrupt_files_correct_initials_phase.append(archivo)
                                    else:
                                        corrupt_files_correct_initials_stage.append(archivo)
                                else:
                                    corrupt_files_correct_project.append(archivo)
                            else:
                                corrupt_files_correct_format.append(archivo)
                            """
                                #newdoc = ImagePlane(image_file=archivo, thumb_image_file=archivo)
                                #newdoc.save()
                            """
                        if len(corrupt_files_correct_format) or len(corrupt_files_correct_project) or len(corrupt_files_correct_initials_stage) or len(corrupt_files_correct_initials_phase) or len(corrupt_files_correct_initials_image_plane) or len(corrupt_files_correct_photographic_zone_plane) or len(corrupt_files_correct_date):
                            form = MultipleUploadChronologicalPicturesForm() # A empty, unbound form
                            # Render list page with the documents and the form

                            # Load stages for the list page
                            stages = project.stage_set.all()

                            # Create the nav_menu
                            nav_menu = []
                            for stage in stages:
                                items_menu_1 = []
                                for phase in stage.phase_set.all():
                                    items_menu_2 = []
                                    for image_plane_current in phase.imageplane_set.all():
                                        items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane_current.id) + '/' + str(project_id) + '/', 'label': image_plane_current.name})
                                    items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                                item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                                nav_menu.append(item_nav_menu)

                            # Board title
                            board_title = 'Carga masiva'

                            return render_to_response(
                                'planes/chronologicalpicturesupload.html',
                                {'form': form, 'upload_files': upload_files, 'corrupt_files_correct_format': corrupt_files_correct_format, 'corrupt_files_correct_project': corrupt_files_correct_project, 'corrupt_files_correct_initials_stage': corrupt_files_correct_initials_stage, 'corrupt_files_correct_initials_phase': corrupt_files_correct_initials_phase, 'corrupt_files_correct_initials_image_plane': corrupt_files_correct_initials_image_plane, 'corrupt_files_correct_photographic_zone_plane': corrupt_files_correct_photographic_zone_plane, 'corrupt_files_correct_date': corrupt_files_correct_date, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                                context_instance=RequestContext(request)
                            )
                        # Redirect to the document list after POST
                        #return HttpResponseRedirect(reverse('inverboy.views.list'))
                else:
                    form = MultipleUploadChronologicalPicturesForm() # A empty, unbound form

                # Load stages for the list page
                stages = project.stage_set.all()

                # Create the nav_menu
                nav_menu = []
                for stage in stages:
                    items_menu_1 = []
                    for phase in stage.phase_set.all():
                        items_menu_2 = []
                        for image_plane_current in phase.imageplane_set.all():
                            items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane_current.id) + '/' + str(project_id) + '/', 'label': image_plane_current.name})
                        items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                    item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                    nav_menu.append(item_nav_menu)

                # Board title
                board_title = 'Carga masiva'

                # Render list page with the documents and the form
                return render_to_response(
                    'planes/chronologicalpicturesupload.html',
                    {'form': form, 'upload_files': upload_files, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                    context_instance=RequestContext(request)
                )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def publications_project(request, project_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        try:
            project = Proyecto.objects.get(id=project_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        usuario = Usuario.objects.get(id=user.id)
        if project in usuario.lista_proyectos_vinculados():
            # Load publications for the list page
            publications = project.publications_list(number=0)
            pag = Paginador(request, publications, 20, 1)

            # Load stages for the list page
            stages = project.stage_set.all()

            # Create the nav_menu
            nav_menu = []
            for stage in stages:
                items_menu_1 = []
                for phase in stage.phase_set.all():
                    items_menu_2 = []
                    for image_plane in phase.imageplane_set.all():
                        items_menu_2.append({'url': '/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(project_id) + '/', 'label': image_plane.name})
                    items_menu_1.append({'url': '', 'label': phase.name, 'items_menu_2': items_menu_2})
                item_nav_menu = {'url': '/inverboy/home/phasesreport/' + str(stage.id) + '/' + str(project_id) + '/', 'label': stage.name, 'items_menu_1': items_menu_1}
                nav_menu.append(item_nav_menu)

            # Board title
            board_title = 'Publicaciones del proyecto'

            # Render list page with the stages and the form
            return render_to_response(
                'planes/publicationsproject.html',
                {'publications': pag, 'nav_menu': nav_menu, 'board_title': board_title, 'project': project},
                context_instance=RequestContext(request)
            )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')




from django.views.decorators.csrf import csrf_exempt


def test(request):

    # Render list page with the documents and the form
    return render_to_response(
        'planes/test.html',
        {},
        context_instance=RequestContext(request)
    )

@csrf_exempt
def test2(request):
    """
    # Render list page with the documents and the form
    return render_to_response(
        'planes/test.html',
        {},
        context_instance=RequestContext(request)
    )
    """

    """
    if request.is_ajax():
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    return HttpResponse(message)
    """




    #print request.GET['video']




    ## JSON
    from django.utils import simplejson
    data = [{'code': 'CD-1', 'label': 'P1', 'url': 'link', 'point_x': 3.1, 'point_y': -30.1}, {'code': 'CD-2', 'label': 'P2', 'url': 'link', 'point_x': 20.1, 'point_y': -40.1}, {'code': 'CD-3', 'label': 'P3', 'url': 'link', 'point_x': 40.1, 'point_y': -50.1}, {'code': 'CD-4', 'label': 'P4', 'url': 'link', 'point_x': 60.1, 'point_y': -60.1}]
    response_data = {}
    response_data['data'] = data
    response_data['result'] = 'failed'
    response_data['message'] = 'Listo javier'
    return simplejson.dumps(response_data)




    """

    formulario
    import settings
    import os
    import re

    project = Proyecto.objects.get(id=1)
    if request.method == 'POST':
        form = MultipleUploadChronologicalPicturesForm(request.POST, request.FILES)
        if form.is_valid():
            archivos = request.FILES.getlist('image_file')
            corrupt_files = []
            for archivo in archivos:
                file_name = archivo.name.split('.')[0]
                correct_format = re.match('^\d{1,3}\-\w{1,3}\-\w{1,3}\-\w{1,3}\-[pP]{1}-?[0-9]+\-(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', file_name)
                if correct_format != None:
                    convention_labels = {'project_id': 0, 'init_stage': '', 'init_phase': '', 'init_image_plane': '', 'photographic_zone': '', 'yyyy': '', 'mm': '', 'dd': ''}
                    array_name = file_name.split('-')
                    # Validate project_id
                    if int(array_name[0]) == int(project_id):
                        convention_labels['project_id'] = array_name[0]
                        convention_labels['init_stage'] = array_name[1]
                        convention_labels['init_phase'] = array_name[2]
                        convention_labels['init_image_plane'] = array_name[3]
                        convention_labels['photographic_zone'] = array_name[4]
                        convention_labels['yyyy'] = array_name[5]
                        convention_labels['mm'] = array_name[6]
                        convention_labels['dd'] = array_name[7]
                        stage = None
                        try:
                            stage = project.stage_set.get(initials=convention_labels['init_stage'])
                        except :
                            pass
                        if stage != None:
                            phase = None
                            try:
                                phase = stage.phase_set.get(initials=convention_labels['init_phase'])
                            except :
                                pass
                            if phase != None:
                                image_plane = None
                                try:
                                    image_plane = phase.imageplane_set.get(initials=convention_labels['init_image_plane'])
                                except :
                                    pass
                                if image_plane != None:
                                    photographic_zone_plane = None
                                    try:
                                        photographic_zone_plane = image_plane.photographiczoneplane_set.get(consecutive=convention_labels['photographic_zone'][1:])
                                    except :
                                        pass
                                    if photographic_zone_plane != None:
                                        # Validate unique picture in photographic_zone
                                        unique_picture = None
                                        try:
                                            unique_picture = photographic_zone_plane.chronologicalpicture_set.get(date=convention_labels['yyyy'] + '-' + convention_labels['mm'] + '-' + convention_labels['dd'])
                                        except :
                                            pass
                                        if unique_picture == None:
                                            chronological_picture = ChronologicalPicture()
                                            chronological_picture.code = file_name
                                            chronological_picture.date = convention_labels['yyyy'] + '-' + convention_labels['mm'] + '-' + convention_labels['dd']
                                            chronological_picture.thumb_image_file = archivo
                                            chronological_picture.photographic_zone_plane = photographic_zone_plane
                                            chronological_picture.save()

                                            # Create parts of zoom levels
                                            size_square = 8192
                                            width = 8192
                                            height = 6144
                                            space_white = 1024
                                            for i in range(1, 5, 1):
                                                canvas = Image.new('RGB', (size_square, size_square), 'white')
                                                image = Image.open(chronological_picture.thumb_image_file.path)
                                                image = image.resize((width, height), Image.ANTIALIAS)
                                                canvas.paste(image, (0, space_white))
                                                image_crops = create_crops_image(canvas, 256, 256)
                                                row_index = 0
                                                for row_item in image_crops:
                                                    col_index = 0
                                                    for col_item in row_item:
                                                        path_image = os.path.join(settings.MEDIA_ROOT, 'geo', 'project_' + str(chronological_picture.photographic_zone_plane.image_plane.phase.stage.project.id), chronological_picture.photographic_zone_plane.image_plane.phase.stage.initials, chronological_picture.photographic_zone_plane.image_plane.phase.initials, chronological_picture.photographic_zone_plane.image_plane.initials, 'chronological_line', 'P' + str(chronological_picture.photographic_zone_plane.consecutive), convention_labels['yyyy'], convention_labels['mm'], convention_labels['dd'], 'map', str(6-(i)), str(row_index))
                                                        if not os.path.isdir(path_image):
                                                            os.makedirs(path_image)
                                                        path_image = path_image + '/' + str(col_index) + '.jpg'
                                                        col_item.save(path_image)
                                                        col_index += 1
                                                    row_index += 1
                                                width = width / 2
                                                height = height / 2
                                                size_square = size_square / 2
                                                space_white = space_white / 2
                                            # Redirect to the Plane list after POST
                                            # return HttpResponseRedirect('/inverboy/home/planedescription/' + str(image_plane.id) + '/' + str(image_plane.phase.stage.project.id) + '/')
                                        else:
                                            corrupt_files.append(archivo)
                                    else:
                                        corrupt_files.append(archivo)
                                else:
                                    corrupt_files.append(archivo)
                            else:
                                corrupt_files.append(archivo)
                        else:
                            corrupt_files.append(archivo)
                    else:
                        corrupt_files.append(archivo)
                else:
                    corrupt_files.append(archivo)

            if len(corrupt_files):
                form = MultipleUploadChronologicalPicturesForm() # A empty, unbound form
                # Render list page with the documents and the form
                return render_to_response(
                    'planes/chronologicalpicturesupload.html',
                    {'form': form, 'corrupt_files': corrupt_files, 'project': project},
                    context_instance=RequestContext(request)
                )
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('inverboy.views.list'))
    else:
        form = MultipleUploadChronologicalPicturesForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'planes/chronologicalpicturesupload.html',
        {'form': form, 'project': project},
        context_instance=RequestContext(request)
    )

    """



    """
    return render_to_response(
        'planes/test.html',
        {},
        context_instance=RequestContext(request)
    )
    """




def json_test(request, plane_id):
    import json

    """plane = ImagePlane.objects.get(id=plane_id)

    point_list = plane.photographiczoneplane_set.all()

    response_data = {'usuario': 'Admin', 'data': point_list}
    #response_data['result'] = 'failed'
    #response_data['message'] = 'You messed up'

    #return render_to_response('')

    return HttpResponse(json.dumps(response_data), content_type="application/json")  """

    response_data = {}
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def form_plane(request):
    if request.method == 'POST':
        form = PlaneForm(request.POST, request.FILES)
        if form.is_valid():
            print form.save()
    else:
        form = PlaneForm()
    # Render list page with the stages and the form
    return render_to_response(
        'planes/plane_add.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
