# This file is an example of how to define rules for the Gmail Organizer.
# You can copy this file into rules.pyand modify it to create your own rules.
RULES = [
	{
		"name": "rule_name",
		"priority": 100,
		"conditions": [
			{
				"sender_contains": ["example.com", "example2.com"]
			},
			{
				"subject_contains": ["example", "test"]
			}
		],
		"actions": {
			"add_label": "rule_name",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "Rule_name_2",
		"priority": 90,
		"conditions": [
			{
				"sender_contains": ["example3.com"]
			},
			{
				"subject_contains": ["example3", "test3"]
			},
			{
				"body_contains": ["example3", "test3"]
			}
		],
		"actions": {
			"add_label": "Rule_name_2",
			"archive": True,
			"mark_as_read": False
		}
	},
	{
		"name": "rule_name_3",
		"priority": 10,
		"conditions": [
			{
				"has_unsubscribe_header": True
			},
			{
				"subject_contains": ["example4", "test4"]
			},
			{
				"body_contains": ["example4", "test4","unsubscribe", "Darme de baja", "Darse de baja", "no deseas seguir recibiendo", "cancelar tu suscripción", "Cancelar suscripción"],
			}
		],
		"actions": {
			"add_label": "rule_name_3",
			"archive": True,
			"mark_as_read": False
		}
	}
]
