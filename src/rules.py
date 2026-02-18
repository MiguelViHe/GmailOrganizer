RULES = [
	{
		"name": "Empleo_alertas",
		"conditions": [
			{
				"sender_contains": ["jobalerts-noreply@linkedin.com", "jobs-listings@linkedin.com", "glassdoor.com", "jobs2web.com"]
			},
		],
		"actions": {
			"add_label": "Empleo_alertas",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Empleo",
		"conditions": [
			{
				"sender_contains": ["linkedin.com", "infojobs.net"]
			},
		],
		"actions": {
			"add_label": "Empleo",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Formación",
		"conditions": [
			{
				"sender_contains": ["coursera.org", "udemy", "edx"]
			},
		],
		"actions": {
			"add_label": "Formación",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Servicios",
		"conditions": [
			{
				"sender_contains": ["endesa.com", "endesaclientes.com",  "o2online.es", "redexis.es"]
			}
		],
		"actions": {
			"add_label": "Servicios",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "42",
		"conditions": [
			{
				"sender_contains": ["42.fr", "42madrid.com"]
			},
			{
				"subject_contains": ["Marvin", "Intra"]
			},
			{
				"body_contains": ["42 Madrid", "42Madrid"]
			}
		],
		"actions": {
			"add_label": "42",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Compras",
		"conditions": [
			{
				"subject_contains": ["Confirmación de pedido", "Recibo de tu pedido"]
			},
			{
				"body_contains": ["resumen de pedido", "IMPORTE TOTAL", "precio total", "pago total", "MÉTODO DE PAGO", "Número de pedido", "Dirección de facturación", "Dirección de entrega", "Información de envío"]
			}
		],
		"actions": {
			"add_label": "42",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Familia",
		"conditions": [
			{
				"sender_contains": ["mcmichaelson", "miguel.vidal.hernando", "miguelvidalhernando", "ignacio.vidal.hernando", "ignaciovidalhernando", "murrayhead85", "bovido55", "celiahernandodefrutos", "vincenza.verdicchio"]
			}
		],
		"actions": {
			"add_label": "Familia",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Promos",
		"conditions": [
			{
				"has_unsubscribe_header": True
			},
			{
				"subject_contains": ["oferta", "promo", "descuento"]
			},
			{
				"body_contains": ["oferta", "promo", "descuento","unsubscribe", "Darme de baja", "Darse de baja", "no deseas seguir recibiendo", "cancelar tu suscripción", "Cancelar suscripción"],
			}
		],
		"actions": {
			"add_label": "Promos",
			"archive": True,
			"mark_as_read": False
		}
	}
]
