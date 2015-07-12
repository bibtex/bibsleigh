#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a list made by scraping the following sources:
# https://simple.wikipedia.org/wiki/List_of_countries
# https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States


knownCountries = (\
	'Afghanistan',
	'Albania',
	'Algeria',
	'American Samoa',
	'Andorra',
	'Angola',
	'Anguilla',
	'Antigua and Barbuda',
	'Aotearoa',
	'Argentina',
	'Armenia',
	'Aruba',
	'Australia',
	'Austria',
	'Azerbaijan',
	'Bahrain',
	'Bangladesh',
	'Barbados',
	'Belarus',
	'Belgium',
	'Belize',
	'Benin',
	'Bermuda',
	'Bhutan',
	'Bolivia',
	'Bosnia and Herzegovina',
	'Botswana',
	'Brazil',
	'Brunei',
	'Bulgaria',
	'Burkina Faso',
	'Burma',
	'Burundi',
	'Cambodia',
	'Cameroon',
	'Canada',
	'Cape Verde',
	'Central African Republic',
	'Chad',
	'Chile',
	'China',
	'Colombia',
	'Comoros',
	'Congo',
	'Costa Rica',
	'Croatia',
	'Cuba',
	'Cyprus',
	'Czech Republic',
	'Democratic Republic of the Congo',
	'Denmark',
	'Djibouti',
	'Dominica',
	'Dominican Republic',
	"Côte d'Ivoire",
	'East Timor',
	'Ecuador',
	'Egypt',
	'El Salvador',
	'Equatorial Guinea',
	'Eritrea',
	'Estonia',
	'Ethiopia',
	'Faroe Islands',
	'Federal Republic of Germany',
	'Federated States of Micronesia',
	'Fiji',
	'Finland',
	'France',
	'Gabon',
	'GDR',
	'Georgia',
	'Germany',
	'Ghana',
	'Greece',
	'Grenada',
	'Guatemala',
	'Guinea-Bissau',
	'Guinea',
	'Guyana',
	'Haiti',
	'Holy See',
	'Honduras',
	'Hungary',
	'Iceland',
	'India',
	'Indonesia',
	'Iran',
	'Iraq',
	'Ireland',
	'Israel',
	'Italy',
	'Ivory Coast',
	'Jamaica',
	'Japan',
	'Jordan',
	'Kazakhstan',
	'Kenya',
	'Kiribati',
	'Korea',
	'Kuwait',
	'Kyrgyzstan',
	'Laos',
	'Latvia',
	'Lebanon',
	'Lesotho',
	'Liberia',
	'Libya',
	'Liechtenstein',
	'Lithuania',
	'Luxembourg',
	'Macedonia',
	'Madagascar',
	'Malawi',
	'Malaysia',
	'Maldives',
	'Mali',
	'Malta',
	'Marshall Islands',
	'Mauritania',
	'Mauritius',
	'Mexico',
	'Micronesia',
	'Moldova',
	'Monaco',
	'Mongolia',
	'Montenegro',
	'Morocco',
	'Mozambique',
	'Myanmar',
	'Namibia',
	'Nauru',
	'Nepal',
	'Netherlands',
	'New Zealand',
	'Nicaragua',
	'Niger',
	'Nigeria',
	'Niue',
	'North Korea',
	'Norway',
	'Oman',
	'Pakistan',
	'Palau',
	'Palestine',
	'Panama',
	'Papua New Guinea',
	'Paraguay',
	"People's Republic of China",
	'Peru',
	'Philippines',
	'Poland',
	'Portugal',
	'Puerto Rico',
	'Qatar',
	'Republic of China',
	'Republic of Cyprus',
	'Republic of Korea',
	'Republic of Macedonia',
	'Republic of the Congo',
	'Romania',
	'Russia',
	'Russian Federation',
	'Rwanda',
	'Saint Kitts and Nevis',
	'Saint Lucia',
	'Saint Vincent and the Grenadines',
	'Samoa',
	'San Marino',
	'Saudi Arabia',
	'Senegal',
	'Serbia',
	'Seychelles',
	'Sierra Leone',
	'Singapore',
	'Slovakia',
	'Slovenia',
	'Solomon Islands',
	'Somalia',
	'South Africa',
	'South Korea',
	'South Sudan',
	'Spain',
	'Sri Lanka',
	'Sudan',
	'Suriname',
	'Swaziland',
	'Sweden',
	'Switzerland',
	'Syria',
	'São Tomé and Príncipe',
	'Taiwan',
	'Tajikistan',
	'Tanzania',
	'Tatarstan',
	'Thailand',
	'The Bahamas',
	'The Gambia',
	'The Netherlands',
	'The Ukraine',
	'Tibet',
	'Togo',
	'Tonga',
	'Trinidad and Tobago',
	'Tunisia',
	'Turkey',
	'Turkmenistan',
	'Tuvalu',
	'U.K.',
	'Uganda',
	'UK',
	'Ukraine',
	'United Arab Emirates',
	'United Kingdom',
	'United States of America',
	'United States',
	'Uruguay',
	'USA',
	'Uzbekistan',
	'Vanuatu',
	'Vatican City',
	'Venezuela',
	'Vietnam',
	'Western Sahara',
	'Yemen',
	'Zaire',
	'Zambia',
	'Zimbabwe',\
)

usaStateNames = (\
	'Alabama',
	'Alaska',
	'Arizona',
	'Arkansas',
	'California',
	'Colorado',
	'Connecticut',
	'District of Columbia',
	'Delaware',
	'Florida',
	'Georgia',
	'Hawaii',
	'Idaho',
	'Illinois',
	'Indiana',
	'Iowa',
	'Kansas',
	'Kentucky',
	'Louisiana',
	'Maine',
	'Maryland',
	'Massachusetts',
	'Michigan',
	'Minnesota',
	'Mississippi',
	'Missouri',
	'Montana',
	'Nebraska',
	'Nevada',
	'New Hampshire',
	'New Jersey',
	'New Mexico',
	'New York',
	'North Carolina',
	'North Dakota',
	'Ohio',
	'Oklahoma',
	'Oregon',
	'Pennsylvania',
	'Rhode Island',
	'South Carolina',
	'South Dakota',
	'Tennessee',
	'Texas',
	'Utah',
	'Vermont',
	'Virginia',
	'Washington',
	'West Virginia',
	'Wisconsin',
	'Wyoming',\
)

usaStateAB = (\
	'AL',
	'AK',
	'AZ',
	'AR',
	'CA',
	'CO',
	'CT',
	'DC',
	'DE',
	'FL',
	'GA',
	'HI',
	'ID',
	'IL',
	'IN',
	'IA',
	'KS',
	'KY',
	'LA',
	'ME',
	'MD',
	'MA',
	'MI',
	'MN',
	'MS',
	'MO',
	'MT',
	'NE',
	'NV',
	'NH',
	'NJ',
	'NM',
	'NY',
	'NC',
	'ND',
	'OH',
	'OK',
	'OR',
	'PA',
	'RI',
	'SC',
	'SD',
	'TN',
	'TX',
	'UT',
	'VT',
	'VA',
	'WA',
	'WV',
	'WI',
	'WY',\
)

canStateNames = (\
	'Ontario',
	'Quebec',
	'Nova Scotia',
	'New Brunswick',
	'Manitoba',
	'British Columbia',
	'Prince Edward Island',
	'Saskatchewan',
	'Alberta',
	'Newfoundland and Labrador',\
)

canStateAB = (\
	'ON',
	'QC',
	'NS',
	'NB',
	'MB',
	'BC',
	'PE',
	'SK',
	'AB',
	'NL',\
)

countryMap = {\
	'GDR': 'Germany',
	'Netherlands': 'The Netherlands',
	'UK': 'United Kingdom',
	'U.K.': 'United Kingdom',
	'Federal Republic of Germany': 'Germany',\
}

desperateSolutions = {\
	'Limerick Ireland': ('Limerick', '?', 'Ireland'),
	'Bad Honnef': ('Bad Honnef', '?', 'Germany'),
	'Melbourne 1993': ('Melbourne', '?', 'Australia'),
	'Berlin GDR': ('Berlin', '?', 'Germany'),\
}
