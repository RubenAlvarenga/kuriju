from django.core.urlresolvers import reverse
from apps.middleware import RequestTimeLoggingMiddleware
from django.http import HttpResponse
# def tiempo(request):
# 	tiempo=ViewTimingMiddleware()
# 	tiempo.process_request(request)
# 	final=tiempo.process_response(request, HttpResponse)
# 	tiempo={'tiempo':final}
# 	return tiempo
# def tablasBase(request):
# 	tablasBase = {'tablasBase':[
# 	{'name': 'Paises', 'url': reverse('lst_pais')},
# 	{'name': 'Departamentos', 'url': reverse('listar_departamentos')},
# 	{'name': 'Ciudades', 'url': reverse('listar_ciudades')},

# 	]}
# 	for item in tablasBase['tablasBase']:
# 		if request.path==item['url']:
# 			item['active']=True
# 	return tablasBase




def menu(request):


	# menu = { 'menu' :[
	# 	{'name': 'Tablas Base', 'url': 'collapseOne', 'class': 'glyphicon glyphicon-pushpin', 
	# 	'submenu':[
	# 		{'name': 'Paises', 'url': reverse('localizaciones:lst_pais'),
	# 			'acciones':[
	# 				{'name': 'Agregar', 'url': reverse('localizaciones:add_pais')},
	# 				{'name': 'detalle', 'url': reverse('localizaciones:det_pais', args=[slug])},
	# 				{'name': 'Editar', 'url': reverse('localizaciones:upd_pais', args=[slug])},
	# 				{'name': 'Borrar', 'url': reverse('localizaciones:del_pais', args=[slug])},
	# 			],
	# 		},
	# 		{'name': 'Departamentos', 'url': reverse('localizaciones:listar_departamentos'),
	# 			'acciones':[
	# 				{'name': 'Agregar', 'url': reverse('localizaciones:add_departamento')},
	# 			]
	# 		},
	# 		{'name': 'Ciudades', 'url': reverse('localizaciones:listar_ciudades'),
	# 			'acciones':[]
	# 		},
	# 	]},

	# 	{'name': 'Compras', 'url': 'collapseTwo', 'class': 'glyphicon glyphicon-shopping-cart',
	# 	'submenu':[
	# 		{'name': 'About', 'url': reverse('about'),
	# 			'acciones':[]
	# 		},
	# 	]},
	# ]}


	menu = { 'menu' :[
		{'name': 'Tablas Base', 'url': 'collapseOne', 'class': 'glyphicon glyphicon-pushpin', 
		'submenu':[
			{'name': 'Paises', 'url': reverse('localizaciones:lst_pais'),},
			{'name': 'Departamentos', 'url': reverse('localizaciones:lst_departamento'),},
			{'name': 'Ciudades', 'url': reverse('about'),},
			{'name': 'Barrios', 'url': reverse('about'),},

			#{'name': 'Ciudades', 'url': reverse('localizaciones:listar_ciudades'),},
		]},
				{'name': 'Entidades', 'url': 'collapseTwo', 'class': 'glyphicon glyphicon glyphicon-briefcase',
		'submenu':[
			{'name': 'Clientes', 'url': reverse('entidades:lst_cliente'),},
			{'name': 'Empresas', 'url': reverse('about'),},
			{'name': 'Personas', 'url': reverse('about'),},

		]},
		{'name': 'Compras', 'url': 'collapseTwo', 'class': 'glyphicon glyphicon-shopping-cart',
		'submenu':[
			{'name': 'About', 'url': reverse('about'),},
		]},
	]}


	secciones=request.path.split('/')
	for item in menu['menu']:
		for i in item['submenu']:
			if i['url'].split('/')[1] == secciones[1]:
				item['active']='in'
				if request.path==i['url']:
					i['active']=True

	breadcrumbs=[]
	#breadcrumbs.append({'name':'index', 'url': '/'})
	secciones.remove('')

	anterior='/'
	for secc in secciones:
		breadcrumbs.append({'name':secc, 'url': str(anterior)+str(secc)+'/' })
		anterior=str(anterior)+str(secc)+'/'
	# if len(secciones)>1:
	# 	import pdb; pdb.set_trace()


	# for secc in secciones:
	# 	breadcrumbs.append({ 'name':str(secc), 'url':str(secciones[0])+str(secc) }}


				#breadcrumbs.append(i)
			# if i['acciones']:
			# 	for j in i['acciones']:
			# 		print 'url:', request.path 
			# 		if request.path==j['url']:
			# 			breadcrumbs.append(i)
			# 			breadcrumbs.append(j)
			# 			j['active']=True
			# 			item['active']='in'
					

	menu['breadcrumbs']=breadcrumbs			#print 'path :', request.path
	return menu


# from apps.middleware import RequestTimeLoggingMiddleware
# def tiempoEspera(request):
# 	mid = RequestTimeLoggingMiddleware()
# 	tiempo = mid.process_response(request, HttpResponse())
# 	#print "------------------", tiempo
# 	#import pdb; pdb.set_trace()
# 	# response = HttpResponse()
# 	# tiempo = RequestTimeLoggingMiddleware.process_response(request, response, "dsadassa")
# 	return {"tiempoEspera": str(tiempo)}
