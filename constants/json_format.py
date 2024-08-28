json_format = '''
	{
		"hotels": [
			{
				"Hotel Name": "String",
        "Descriptions": "String",
				"Hotel Address": "String",
				"Price": "Price Range - String",
				"Hotel Image URL": "String",
				"Rating": "Number",
			}
		],
		"itinerary": [
			{
				"Day": "Number",
        "Date": "Date in MM/DD/YYYY",
				"Places": [
					{
						"Place Name": "String",
						"Descriptions": "String",
            "Place Address": "String",
						"Place Image URL": "String",
            "Rating": "Number",
						"Ticket Pricing": "Price Range - String",
						"Distance to each location": "String",
						"Travel Time to each location": "String",
						"Best Time to Visit": "Time Range - String (the format should like this '1 PM - 2 PM')",
            "Start Time": "Timestamp (the format should like this '13:00:00')",
            "End Time": "Timestamp (the format should like this '14:00:00')",
					}
				]
			}
		]
	}
'''