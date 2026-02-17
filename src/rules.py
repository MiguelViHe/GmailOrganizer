RULES = [
	{
		"name": "Job Alerts",
		"condition": {
			"sender_contains": ["jobalerts-noreply@linkedin.com", "glassdoor.com"]
		},
		"actions": {
			"add_label": "Empleo_alertas",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Utilities",
		"condition": {
			"sender_contains": ["endesa.com", "endesaclientes.com",  "o2online.es", "redexis.es"]
		},
		"actions": {
			"add_label": "Servicios",
			"archive": True,
			"mark_as_read": True
		}
	},
	{
		"name": "42",
		"condition": {
			"sender_contains": ["42.fr"]
		},
		"actions": {
			"add_label": "42",
			"archive": True,
			"mark_as_read": True
		}
	}
]
