RULES = [
	{
		"name": "Empleo_alertas",
		"priority": 95,
		"conditions": [
			{
				"sender_contains": ["jobalerts-noreply@linkedin.com", "jobs-listings@linkedin.com", "glassdoor.com", "jobs2web.com", "welcometothejungle.com"]
			},
			{
				"subject_contains": ["Nuevos empleos"]
			}
		],
		"actions": {
			"add_label": "Empleo_alertas",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Empleo",
		"priority": 90,
		"conditions": [
			{
				"sender_contains": ["recruitment", "linkedin.com", "infojobs.net", "HRsystem@capgemini.com", "teamtailor-mail.com", "viterbit-mail.com", "successfactors.eu", "greenhouse-mail.io", "careers-noreply@telefonica.com", "santander@myworkday.com"]
			},
			{
				"subject_contains": ["solicitud de empleo", "se ha enviado tu solicitud"]
			},
			{
				"body_contains": ["solicitud para el puesto"]
			}
		],
		"actions": {
			"add_label": "Empleo",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Formación",
		"priority": 80,
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
		"priority": 80,
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
		"priority": 60,
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
		"priority": 40,
		"conditions": [
			{
				"sender_contains": ["carrefour"]
			},
			{
				"subject_contains": 
				[
					"Confirmación de pedido", "Recibo de tu pedido", "Recibo de tu pedido",
					"Recibo de su pago", "pago aceptado", "Pedido en preparación", "Pedido enviado",
					"Información sobre su envío", "tu factura", "ticket de compra", "factura de compra",
					"Factura de tu pedido", "Factura de su pedido", "Factura de compra", "Factura de tu compra"
				]
			},
			{
				"body_contains": ["resumen de pedido", "IMPORTE TOTAL", "precio total", "pago total", "MÉTODO DE PAGO", "Número de pedido", "Dirección de facturación", "Dirección de entrega", "Información de envío"]
			}
		],
		"actions": {
			"add_label": "Compras",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Familia",
		"priority": 100,
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
		"priority": 10,
		"conditions": [
			{
				"has_unsubscribe_header": True
			},
			{
				"subject_contains": ["promo", "descuento"]
			},
			{
				"body_contains": ["promo", "descuento","unsubscribe", "Darme de baja", "Darse de baja", "no deseas seguir recibiendo", "cancelar tu suscripción", "Cancelar suscripción"],
			}
		],
		"actions": {
			"add_label": "Promos",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Running",
		"priority": 30,
		"conditions": [
			{
				"sender_contains": ["circuito4desafios", "inscripciones@youevent.com.es", "no-reply@rockthesport.com", "garmin.com", "wikiloc.com", "strava.com", "corredorespopulares.com", "marathon.es", "maratonmadrid.com", "rockthesport.com", "spartanrace.es", "spartan.com"]
			},
			{
				"body_contains": ["Marathon", "Maratón", "Trail","medalla finisher", "finisher", "recogida de dorsales", "no federado"]
			}
		],
		"actions": {
			"add_label": "Running",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "eBiblio",
		"priority": 30,
		"conditions": [
			{
				"sender_contains": ["eBiblio"]
			}
		],
		"actions": {
			"add_label": "eBiblio",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Bancos",
		"priority": 85,
		"conditions": [
			{
				"sender_contains": ["revolut.com", "bbva.com"]
			}
		],
		"actions": {
			"add_label": "Bancos",
			"archive": True,
			"mark_as_read": False
		}
	}
]
