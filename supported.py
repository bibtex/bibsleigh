#!/usr/local/bin/python3

# TODO: WICSA? ECSA? ICPC! ICFP! ICMT! ICGT! PPDP! LOPSTR! ECMFA TOOLS! DSL IFM!
# TODO: DYLA SQM LDTA! XM MPM MoDEVVa DSM ME?
# TODO: TCS, SCP, SPE, EMSE, SoSyM, JFP, TSE, TOPLAS, TOSEM

supported = {
	'CSMR': 'Conference on Software Maintenance and Reengineering',
	'ECOOP': 'European Conference on Object-Oriented Programming',
	'ESEC': 'European Software Engineering Conference',
	'ESEC-FSE': 'European Software Engineering Conference / Foundations of Software Engineering',
	'ESOP': 'European Symposium on Programming',
	'GTTSE': 'Generative and Transformational Techniques in Software Engineering',
	'ICSE': 'International Conference on Software Engineering',
	'ICSM': 'International Conference on Software Maintenance',
	'ICSME': 'International Conference on Software Maintenance and Evolution',
	'MoDELS': 'Model Driven Engineering Languages and Systems',
	'OOPSLA': 'Object-Oriented Programming, Systems, Languages and Applications',
	'PLDI': 'Programming Language Design and Implementation',
	'POPL': 'Principles of Programming Languages',
	'RTA': 'Rewriting Techniques and Applications',
	'SAC': 'Symposium on Applied Computing',
	'SANER': 'Software Analysis, Evolution and Reengineering',
	'SCAM': 'Source Code Analysis and Manipulation',
	'SIGSOFT': 'Foundations of Software Engineering',
	'SLE': 'Software Language Engineering',
	'SPLASH': 'Systems, Programming, Languages and Applications: Software for Humanity',
	'UML': 'Unified Modelling Language',
	'WCRE': 'Working Conference on Reverse Engineering',
}

merged = {
	'MoDELS': ['MoDELS', 'UML'],
	'ESEC-FSE': ['ESEC', 'SIGSOFT'],
	'ICSME': ['ICSM', 'ICSME'],
	'SANER': ['SANER', 'CSMR-WCRE'],
	'OOPSLA': ['OOPSLA', 'SPLASH']
}