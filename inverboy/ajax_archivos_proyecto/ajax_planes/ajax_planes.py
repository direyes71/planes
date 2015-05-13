__author__ = 'Diegopc'

from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *

from django.http import HttpResponse

def function_json2(request):
    from django.utils import simplejson
    data = [{'code': 'CD-1', 'label': 'P1', 'url': 'link', 'point_x': 3.1, 'point_y': -30.1}, {'code': 'CD-2', 'label': 'P2', 'url': 'link', 'point_x': 20.1, 'point_y': -40.1}, {'code': 'CD-3', 'label': 'P3', 'url': 'link', 'point_x': 40.1, 'point_y': -50.1}, {'code': 'CD-4', 'label': 'P4', 'url': 'link', 'point_x': 60.1, 'point_y': -60.1}]
    response_data = {}
    response_data['data'] = data
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return simplejson.dumps(response_data)


def photographiczonesplane_image_plane_add2(request, image_plane_id, point_x, point_y, project_id):
    from django.utils import simplejson
    
    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
    photographic_zone_plane = PhotographicZonePlane()
    photographic_zone_plane.point_x = point_x
    photographic_zone_plane.point_y = point_y
    photographic_zone_plane.image_plane = image_plane
    photographic_zone_plane.save()

    data = []
    data.append({'id': photographic_zone_plane.id, 'label': photographic_zone_plane.get_label(), 'url': 'link', 'point_x': photographic_zone_plane.point_x, 'point_y': photographic_zone_plane.point_y})
    response_data = {}
    response_data['data'] = data
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return simplejson.dumps(response_data)


def photographiczonesplane_image_plane_remove2(request, image_plane_id, photographiczoneplane_id, project_id):
    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
    photographiczoneplane = image_plane.photographiczoneplane_set.get(id=photographiczoneplane_id)
    if photographiczoneplane.can_be_eliminated():
        photographiczoneplane.delete()


def get_photographiczonesplane_image_plane2(request, image_plane_id, project_id):
    from django.utils import simplejson
    project = Proyecto.objects.get(id=project_id)
    image_plane = ImagePlane.objects.get(phase__stage__project=project, id=image_plane_id)
    photographic_zones_plane = image_plane.photographiczoneplane_set.all()
    data = []
    for photographic_zone_plane in photographic_zones_plane:
        data.append({'id': photographic_zone_plane.id, 'label': photographic_zone_plane.get_label(), 'url': photographic_zone_plane.get_url_details(), 'label_url': 'Detalles', 'point_x': photographic_zone_plane.point_x, 'point_y': photographic_zone_plane.point_y})
    response_data = {}
    response_data['data'] = data
    response_data['result'] = 'successful'
    response_data['message'] = 'successful!!'
    return simplejson.dumps(response_data)