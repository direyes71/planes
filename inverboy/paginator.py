__author__ = 'Administrador'

#from django.core.paginator import ObjectPaginator, InvalidPage
from django.core.paginator import Paginator, InvalidPage

def Paginador(request, modelo, paginas, page):
	result_list = Paginator(modelo, paginas)
	#try:
	#	page = int(request.GET.get('page')); #Tomamos el valor de parametro page, usando GET
	#except:
	#	page = 1
	if (page < result_list.page(page)):
		pagina = result_list.page(page)
		Contexto = {'modelo': pagina.object_list, #Asignamos registros de la pagina
			 'page': page, #Pagina Actual
			 'pages': result_list.num_pages, #Cantidad de Paginas
			 'has_next': pagina.has_next(), #True si hay proxima pagina
			 'has_prev': pagina.has_previous(), #true si hay Pagina anterior
			 'next_page': page+1, #Proxima pagina
			 'prev_page': page-1, #Pagina Anterior
			 }
		return Contexto