#!/usr/local/bin/python3

venuesMap = {
'10th  Working Conference on Reverse Engineering (WCRE 2003), 13-16 November 2003, Victoria, Canada':
	'Proceedings of the 10th Working Conference on Reverse Engineering',
'10th European Conference on Software Maintenance and Reengineering (CSMR 2006), 22-24 March 2006, Bari, Italy':
	'Proceedings of the 10th European Conference on Software Maintenance and Reengineering',
'11th European Conference on Software Maintenance and Reengineering, Software Evolution in Complex Software Intensive Systems, CSMR 2007, 21-23 March 2007, Amsterdam, The Netherlands':
	'Proceedings of the 11th European Conference on Software Maintenance and Reengineering',
'11th Working Conference on Reverse Engineering (WCRE 2004), 8-12 November 2004, Delft, The Netherlands':
	'Proceedings of the 11th Working Conference on Reverse Engineering',
'12th European Conference on Software Maintenance and Reengineering, CSMR 2008, April 1-4, 2008, Athens, Greece':
	'Proceedings of the 12th European Conference on Software Maintenance and Reengineering',
'12th Working Conference on Reverse Engineering (WCRE 2005), 7-11 November 2005, Pittsburgh, PA, USA':
	'Proceedings of the 12th Working Conference on Reverse Engineering',
'13th European Conference on Software Maintenance and Reengineering, CSMR 2009, Architecture-Centric Maintenance of Large-SCale Software Systems, Kaiserslautern, Germany, 24-27 March 2009':
	'Proceedings of the 13th European Conference on Software Maintenance and Reengineering',
'13th Working Conference on Reverse Engineering (WCRE 2006), 23-27 October 2006, Benevento, Italy':
	'Proceedings of the 13th Working Conference on Reverse Engineering',
'14th European Conference on Software Maintenance and Reengineering, CSMR 2010, 15-18 March 2010, Madrid, Spain':
	'Proceedings of the 14th European Conference on Software Maintenance and Reengineering',
'14th Working Conference on Reverse Engineering (WCRE 2007), 28-31 October 2007, Vancouver, BC, Canada':
	'Proceedings of the 14th Working Conference on Reverse Engineering',
'15th European Conference on Software Maintenance and Reengineering, CSMR 2011, 1-4 March 2011, Oldenburg, Germany':
	'Proceedings of the 15th European Conference on Software Maintenance and Reengineering',
'16th European Conference on Software Maintenance and Reengineering, CSMR 2012, Szeged, Hungary, March 27-30, 2012':
	'Proceedings of the 16th European Conference on Software Maintenance and Reengineering',
'16th Working Conference on Reverse Engineering, WCRE 2009, 13-16 October 2009, Lille, France':
	'Proceedings of the 16th Working Conference on Reverse Engineering',
'17th European Conference on Software Maintenance and Reengineering, CSMR 2013, Genova, Italy, March 5-8, 2013':
	'Proceedings of the 17th European Conference on Software Maintenance and Reengineering',
'17th Working Conference on Reverse Engineering, WCRE 2010, 13-16 October 2010, Beverly, MA, USA':
	'Proceedings of the 17th Working Conference on Reverse Engineering',
'18th Working Conference on Reverse Engineering, WCRE 2011, Limerick, Ireland, October 17-20, 2011':
	'Proceedings of the 18th Working Conference on Reverse Engineering',
'19th Working Conference on Reverse Engineering, WCRE 2012, Kingston, ON, Canada, October 15-18, 2012':
	'Proceedings of the 19th Working Conference on Reverse Engineering',
'1st Euromicro Working Conference on Software Maintenance and Reengineering (CSMR \'97), 17-19 March 1997, Berlin, Germany':
	'Proceedings of the First Euromicro Working Conference on Software Maintenance and Reengineering',
'20th Working Conference on Reverse Engineering, WCRE 2013, Koblenz, Germany, October 14-17, 2013':
	'Proceedings of the 20th Working Conference on Reverse Engineering',
'2nd Euromicro Conference on Software Maintenance and Reengineering (CSMR \'98), 8-11 March 1998, Florence, Italy':
	'Proceedings of the Second Euromicro Conference on Software Maintenance and Reengineering',
'3rd European Conference on Software Maintenance and Reengineering (CSMR \'99), 3-5 March 1999, Amsterdam, The Netherlands':
	'Proceedings of the Third European Conference on Software Maintenance and Reengineering',
'6th European Conference on Software Maintenance and Reengineering (CSMR 2002), 11-13 March 2002, Budapest, Hungary, Proceedings':
	'Proceedings of the Sixth European Conference on Software Maintenance and Reengineering',
'7th European Conference on Software Maintenance and Reengineering (CSMR 2003), 26-28 March 2003, Benevento, Italy, Proceedings':
	'Proceedings of the Seventh European Conference on Software Maintenance and Reengineering',
'8th European Conference on Software Maintenance and Reengineering (CSMR 2004), 24-26 March 2004, Tampere, Finland, Proceedings':
	'Proceedings of the Eighth European Conference on Software Maintenance and Reengineering',
'9th European Conference on Software Maintenance and Reengineering (CSMR 2005), 21-23 March 2005, Manchester, UK, Proceedings':
	'Proceedings of the Ninth European Conference on Software Maintenance and Reengineering',
'9th Working Conference on Reverse Engineering (WCRE 2002), 28 October - 1 November 2002, Richmond, VA, USA':
	'Proceedings of the Ninth Working Conference on Reverse Engineering',
'Conference Record of POPL 2001: The 28th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, London, UK, January 17-19, 2001':
	'Conference Record of the 28th Symposium on Principles of Programming Languages',
'Conference Record of POPL 2002: The 29th SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Portland, OR, USA, January 16-18, 2002':
	'Conference Record of the 29th Symposium on Principles of Programming Languages',
'Conference Record of POPL 2003: The 30th SIGPLAN-SIGACT Symposium on Principles of Programming Languages, New Orleans, Louisisana, USA, January 15-17, 2003':
	'Conference Record of the 30th Symposium on Principles of Programming Languages',
'Conference Record of POPL\'94: 21st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Portland, Oregon, USA, January 17-21, 1994':
	'Conference Record of the 21st Symposium on Principles of Programming Languages',
'Conference Record of POPL\'95: 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Francisco, California, USA, January 23-25, 1995':
	'Conference Record of the 22nd Symposium on Principles of Programming Languages',
'Conference Record of POPL\'96: The 23rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Papers Presented at the Symposium, St. Petersburg Beach, Florida, USA, January 21-24, 1996':
	'Conference Record of the 23rd Symposium on Principles of Programming Languages',
'Conference Record of POPL\'97: The 24th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Papers Presented at the Symposium, Paris, France, 15-17 January 1997':
	'Conference Record of the 24th Symposium on Principles of Programming Languages',
'Conference Record of the ACM Symposium on Principles of Programming Languages, Boston, Massachusetts, USA, October 1973':
	'Conference Record of the Symposium on Principles of Programming Languages',
'Conference Record of the Eighteenth Annual ACM Symposium on Principles of Programming Languages, Orlando, Florida, USA, January 21-23, 1991':
	'Conference Record of the 18th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Eighth Annual ACM Symposium on Principles of Programming Languages, Williamsburg, Virginia, USA, January 1981':
	'Conference Record of the Eighth Annual Symposium on Principles of Programming Languages',
'Conference Record of the Eleventh Annual ACM Symposium on Principles of Programming Languages, Salt Lake City, Utah, USA, January 1984':
	'Conference Record of the 11th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Fifteenth Annual ACM Symposium on Principles of Programming Languages, San Diego, California, USA, January 10-13, 1988':
	'Conference Record of the 15th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Fifth Annual ACM Symposium on Principles of Programming Languages, Tucson, Arizona, USA, January 1978':
	'Conference Record of the Fifth Annual Symposium on Principles of Programming Languages',
'Conference Record of the Fourteenth Annual ACM Symposium on Principles of Programming Languages, Munich, Germany, January 21-23, 1987':
	'Conference Record of the 14th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Fourth ACM Symposium on Principles of Programming Languages, Los Angeles, California, USA, January 1977':
	'Conference Record of the Fourth Symposium on Principles of Programming Languages',
'Conference Record of the Nineteenth Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Albuquerque, New Mexico, USA, January 19-22, 1992':
	'Conference Record of the 19th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Ninth Annual ACM Symposium on Principles of Programming Languages, Albuquerque, New Mexico, USA, January 1982':
	'Conference Record of the Ninth Annual Symposium on Principles of Programming Languages',
'Conference Record of the Second ACM Symposium on Principles of Programming Languages, Palo Alto, California, USA, January 1975':
	'Conference Record of the Second Symposium on Principles of Programming Languages',
'Conference Record of the Seventeenth Annual ACM Symposium on Principles of Programming Languages, San Francisco, California, USA, January 1990':
	'Conference Record of the 17th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Seventh Annual ACM Symposium on Principles of Programming Languages, Las Vegas, Nevada, USA, January 1980':
	'Conference Record of the Seventh Annual Symposium on Principles of Programming Languages',
'Conference Record of the Sixteenth Annual ACM Symposium on Principles of Programming Languages, Austin, Texas, USA, January 11-13, 1989':
	'Conference Record of the 16th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Sixth Annual ACM Symposium on Principles of Programming Languages, San Antonio, Texas, USA, January 1979':
	'Conference Record of the Sixth Annual Symposium on Principles of Programming Languages',
'Conference Record of the Tenth Annual ACM Symposium on Principles of Programming Languages, Austin, Texas, USA, January 1983':
	'Conference Record of the Tenth Annual Symposium on Principles of Programming Languages',
'Conference Record of the Third ACM Symposium on Principles of Programming Languages, Atlanta, Georgia, USA, January 1976':
	'Conference Record of the Third Symposium on Principles of Programming Languages',
'Conference Record of the Thirteenth Annual ACM Symposium on Principles of Programming Languages, St. Petersburg Beach, Florida, USA, January 1986':
	'Conference Record of the 13th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Twelfth Annual ACM Symposium on Principles of Programming Languages, New Orleans, Louisiana, USA, January 1985':
	'Conference Record of the 12th Annual Symposium on Principles of Programming Languages',
'Conference Record of the Twentieth Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Charleston, South Carolina, USA, January 1993':
	'Conference Record of the 20th Annual Symposium on Principles of Programming Languages',
'Generative and Transformational Techniques in Software Engineering II, International Summer School, GTTSE 2007, Braga, Portugal, July 2-7, 2007. Revised Papers':
	'Revised Papers of the Second International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering III - International Summer School, GTTSE 2009, Braga, Portugal, July 6-11, 2009. Revised Papers':
	'Revised Papers of the Third International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering IV, International Summer School, GTTSE 2011, Braga, Portugal, July 3-9, 2011. Revised Papers':
	'Revised Papers of the Fourth International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering, International Summer School, GTTSE 2005, Braga, Portugal, July 4-8, 2005. Revised Papers':
	'Revised Papers of the First International Summer School on Generative and Transformational Techniques in Software Engineering',
'Model Driven Engineering Languages and Systems - 15th International Conference, MODELS 2012, Innsbruck, Austria, September 30-October 5, 2012. Proceedings':
	'Proceedings of the 15th International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 10th International Conference, MoDELS 2007, Nashville, USA, September 30 - October 5, 2007, Proceedings':
	'Proceedings of the 10th International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 11th International Conference, MoDELS 2008, Toulouse, France, September 28 - October 3, 2008. Proceedings':
	'Proceedings of the 11th International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 12th International Conference, MODELS 2009, Denver, CO, USA, October 4-9, 2009. Proceedings':
	'Proceedings of the 12th International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 14th International Conference, MODELS 2011, Wellington, New Zealand, October 16-21, 2011. Proceedings':
	'Proceedings of the 14th International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 8th International Conference, MoDELS 2005, Montego Bay, Jamaica, October 2-7, 2005, Proceedings':
	'Proceedings of the Eighth International Conference on Model Driven Engineering Languages and Systems',
'Model Driven Engineering Languages and Systems, 9th International Conference, MoDELS 2006, Genova, Italy, October 1-6, 2006, Proceedings':
	'Proceedings of the Ninth International Conference on Model Driven Engineering Languages and Systems',
'Model-Driven Engineering Languages and Systems - 16th International Conference, MODELS 2013, Miami, FL, USA, September 29 - October 4, 2013. Proceedings':
	'Proceedings of the 16th International Conference on Model Driven Engineering Languages and Systems',
'POPL \'98, Proceedings of the 25th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Diego, CA, USA, January 19-21, 1998':
	'Proceedings of the 25th Symposium on Principles of Programming Languages',
'POPL \'99, Proceedings of the 26th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Antonio, TX, USA, January 20-22, 1999':
	'Proceedings of the 26th Symposium on Principles of Programming Languages',
'POPL 2000, Proceedings of the 27th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Boston, Massachusetts, USA, January 19-21, 2000':
	'Proceedings of the 27th Symposium on Principles of Programming Languages',
'Proceedings of the 2003 ACM Symposium on Applied Computing (SAC), March 9-12, 2003, Melbourne, FL, USA':
	'Proceedings of the 18th Symposium on Applied Computing',
'Proceedings of the 2004 ACM Symposium on Applied Computing (SAC), Nicosia, Cyprus, March 14-17, 2004':
	'Proceedings of the 19th Symposium on Applied Computing',
'Proceedings of the 2005 ACM Symposium on Applied Computing (SAC), Santa Fe, New Mexico, USA, March 13-17, 2005':
	'Proceedings of the 20th Symposium on Applied Computing',
'Proceedings of the 2006 ACM Symposium on Applied Computing (SAC), Dijon, France, April 23-27, 2006':
	'Proceedings of the 21st Symposium on Applied Computing',
'Proceedings of the 2007 ACM Symposium on Applied Computing (SAC), Seoul, Korea, March 11-15, 2007':
	'Proceedings of the 22nd Symposium on Applied Computing',
'Proceedings of the 2008 ACM Symposium on Applied Computing (SAC), Fortaleza, Ceara, Brazil, March 16-20, 2008':
	'Proceedings of the 23rd Symposium on Applied Computing',
'Proceedings of the 2009 ACM Symposium on Applied Computing (SAC), Honolulu, Hawaii, USA, March 9-12, 2009':
	'Proceedings of the 24th Symposium on Applied Computing',
'Proceedings of the 2010 ACM Symposium on Applied Computing (SAC), Sierre, Switzerland, March 22-26, 2010':
	'Proceedings of the 25th Symposium on Applied Computing',
'Proceedings of the 2011 ACM Symposium on Applied Computing (SAC), TaiChung, Taiwan, March 21 - 24, 2011':
	'Proceedings of the 26th Symposium on Applied Computing',
'Proceedings of the 28th Annual ACM Symposium on Applied Computing, SAC \'13, Coimbra, Portugal, March 18-22, 2013':
	'Proceedings of the 28th Annual Symposium on Applied Computing',
'Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2004, Venice, Italy, January 14-16, 2004':
	'Proceedings of the 31st Symposium on Principles of Programming Languages',
'Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2005, Long Beach, California, USA, January 12-14, 2005':
	'Proceedings of the 32nd Symposium on Principles of Programming Languages',
'Proceedings of the 33rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2006, Charleston, South Carolina, USA, January 11-13, 2006':
	'Proceedings of the 33rd Symposium on Principles of Programming Languages',
'Proceedings of the 34th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2007, Nice, France, January 17-19, 2007':
	'Proceedings of the 34th Symposium on Principles of Programming Languages',
'Proceedings of the 35th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2008, San Francisco, California, USA, January 7-12, 2008':
	'Proceedings of the 35th Symposium on Principles of Programming Languages',
'Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2009, Savannah, GA, USA, January 21-23, 2009':
	'Proceedings of the 36th Symposium on Principles of Programming Languages',
'Proceedings of the 37th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2010, Madrid, Spain, January 17-23, 2010':
	'Proceedings of the 37th Symposium on Principles of Programming Languages',
'Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011':
	'Proceedings of the 38th Symposium on Principles of Programming Languages',
'Proceedings of the 39th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2012, Philadelphia, Pennsylvania, USA, January 22-28, 2012':
	'Proceedings of the 39th Symposium on Principles of Programming Languages',
'Proceedings of the ACM Symposium on Applied Computing, SAC 2012, Riva, Trento, Italy, March 26-30, 2012':
	'Proceedings of the 27th Symposium on Applied Computing',
'Software Language Engineering - 4th International Conference, SLE 2011, Braga, Portugal, July 3-4, 2011, Revised Selected Papers':
	'Revised Selected Papers of the Fourth International Conference on Software Language Engineering',
'Software Language Engineering - 6th International Conference, SLE 2013, Indianapolis, IN, USA, October 26-28, 2013. Proceedings':
	'Proceedings of the Sixth International Conference on Software Language Engineering',
'Software Language Engineering - Third International Conference, SLE 2010, Eindhoven, The Netherlands, October 12-13, 2010, Revised Selected Papers':
	'Revised Selected Papers of the Third International Conference on Software Language Engineering',
'Software Language Engineering, 5th International Conference, SLE 2012, Dresden, Germany, September 26-28, 2012, Revised Selected Papers':
	'Revised Selected Papers of the Fifth International Conference on Software Language Engineering',
'Software Language Engineering, First International Conference, SLE 2008, Toulouse, France, September 29-30, 2008. Revised Selected Papers':
	'Revised Selected Papers of the First International Conference on Software Language Engineering',
'Software Language Engineering, Second International Conference, SLE 2009, Denver, CO, USA, October 5-6, 2009, Revised Selected Papers':
	'Revised Selected Papers of the Second International Conference on Software Language Engineering',
'The 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL \'13, Rome, Italy - January 23 - 25, 2013':
	'Proceedings of the 40th Annual Symposium on Principles of Programming Languages',
'The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL \'14, San Diego, CA, USA, January 20-21, 2014':
	'Proceedings of the 41st Symposium on Principles of Programming Languages',
'WCRE 2008, Proceedings of the 15th Working Conference on Reverse Engineering, Antwerp, Belgium, October 15-18, 2008':
	'Proceedings of the 15th Working Conference on Reverse Engineering',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA\'86), Portland, Oregon, Proceedings':
	'Proceedings of the First Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA\'87), Orlando, Florida, USA, October 4-8, 1987, Proceedings':
	'Proceedings of the Second Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA\'88), San Diego, California, USA, September 25-30, 1988, Proceedings':
	'Proceedings of the Third Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA\'91), Sixth Annual Conference, Phoenix, Arizona, USA, October 6-11, 1991, Proceedings':
	'Proceedings of the Sixth Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA\'92), Seventh Annual Conference, Vancouver, British Columbia, Canada, October 18-22, 1992, Proceedings':
	'Proceedings of the Seventh Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming Systems, Languages, and Applications (OOPSLA), Eighth Annual Conference, Washington, DC, USA, September 26 - October 1, 1993, Proceedings':
	'Proceedings of the Eighth Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Conference on Object-Oriented Programming: Systems, Languages, and Applications (OOPSLA\'89), New Orleans, Louisiana, USA, October 1-6, 1989, Proceedings':
	'Proceedings of the Fourth Conference on Object-Oriented Programming: Systems, Languages, and Applications',
'OOPSLA\'94, Proceedings of the Ninth Annual Conference on Object-Oriented Programming Systems, Languages, and Applications, Portland, Oregon, USA, October 23-27, 1994':
	'Proceedings of the Ninth Annual Conference on Object-Oriented Programming Systems, Languages, and Applications',
'OOPSLA\'95, Proceedings of the Tenth Annual Conference on Object-Oriented Programming Systems, Languages, and Applications, Austin, Texas, USA, October 15-19, 1995':
	'Proceedings of the Tenth Annual Conference on Object-Oriented Programming Systems, Languages, and Applications',
'Proceedings of the 1996 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages & Applications (OOPSLA \'96), San Jose, California, October 6-10, 1996':
	'Proceedings of the 11th Conference on Object-Oriented Programming Systems, Languages & Applications',
'Proceedings of the 1997 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages & Applications (OOPSLA \'97), Atlanta, Georgia, October 5-9, 1997':
	'Proceedings of the 12th Conference on Object-Oriented Programming Systems, Languages & Applications',
'Proceedings of the 1998 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages & Applications (OOPSLA \'98), Vancouver, British Columbia, Canada, October 18-22, 1998':
	'Proceedings of the 13th Conference on Object-Oriented Programming Systems, Languages & Applications',
'Proceedings of the 1999 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages & Applications (OOPSLA \'99), Denver, Colorado, USA, November 1-5, 1999':
	'Proceedings of the 14th Conference on Object-Oriented Programming Systems, Languages & Applications',
'Proceedings of the 19th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2004, October 24-28, 2004, Vancouver, BC, Canada':
	'Proceedings of the 19th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 2000 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages & Applications (OOPSLA 2000), Minneapolis, Minnesota, USA, October 15-19, 2000':
	'Proceedings of the 15th Conference on Object-Oriented Programming Systems, Languages & Applications',
'Proceedings of the 2001 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages and Applications, OOPSLA 2001, Tampa, Florida, USA, October 14-18, 2001':
	'Proceedings of the 16th Conference on Object-Oriented Programming Systems, Languages and Applications',
'Proceedings of the 2002 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages and Applications, OOPSLA 2002, Seattle, Washington, USA, November 4-8, 2002':
	'Proceedings of the 17th Conference on Object-Oriented Programming Systems, Languages and Applications',
'Proceedings of the 2003 ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages and Applications, OOPSLA 2003, October 26-30, 2003, Anaheim, CA, USA':
	'Proceedings of the 18th Conference on Object-Oriented Programming Systems, Languages and Applications',
'Proceedings of the 2013 ACM SIGPLAN International Conference on Object Oriented Programming Systems Languages & Applications, OOPSLA 2013, part of SPLASH 2013, Indianapolis, IN, USA, October 26-31, 2013':
	'Proceedings of the 28th International Conference on Object Oriented Programming Systems Languages & Applications',
'Proceedings of the 20th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2005, October 16-20, 2005, San Diego, CA, USA':
	'Proceedings of the 20th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 21th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2006, October 22-26, 2006, Portland, Oregon, USA':
	'Proceedings of the 21th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 22nd Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2007, October 21-25, 2007, Montreal, Quebec, Canada':
	'Proceedings of the 22nd Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 23rd Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2008, October 19-23, 2008, Nashville, TN, USA':
	'Proceedings of the 23rd Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 24th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2009, October 25-29, 2009, Orlando, Florida, USA':
	'Proceedings of the 24th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 25th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2010, October 17-21, 2010, Reno/Tahoe, Nevada, USA':
	'Proceedings of the 25th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 26th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2011, part of SPLASH 2011, Portland, OR, USA, October 22 - 27, 2011':
	'Proceedings of the 26th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'Proceedings of the 27th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2012, part of SPLASH 2012, Tucson, AZ, USA, October 21-25, 2012':
	'Proceedings of the 27th Annual Conference on Object-Oriented Programming, Systems, Languages, and Applications',
'18th International Conference on Software Maintenance (ICSM 2002), Maintaining Distributed Heterogeneous Systems, 3-6 October 2002, Montreal, Quebec, Canada':
	'Proceedings of the 18th International Conference on Software Maintenance',
'1996 International Conference on Software Maintenance (ICSM \'96), 4-8 November 1996, Monterey, CA, USA, Proceedings':
	'Proceedings of the 12th International Conference on Software Maintenance',
'1997 International Conference on Software Maintenance (ICSM \'97), 1-3 October 1997, Bari, Italy, Proceedings':
	'Proceedings of the 13th International Conference on Software Maintenance',
'19th International Conference on Software Maintenance (ICSM 2003), The Architecture of Existing Systems, 22-26 September 2003, Amsterdam, The Netherlands':
	'Proceedings of the 19th International Conference on Software Maintenance',
'2013 IEEE International Conference on Software Maintenance, Eindhoven, The Netherlands, September 22-28, 2013':
	'Proceedings of the 29th International Conference on Software Maintenance',
'20th International Conference on Software Maintenance (ICSM 2004), 11-17 September 2004, Chicago, IL, USA':
	'Proceedings of the 20th International Conference on Software Maintenance',
'21st IEEE International Conference on Software Maintenance (ICSM 2005), 25-30 September 2005, Budapest, Hungary':
	'Proceedings of the 21st International Conference on Software Maintenance',
'22nd IEEE International Conference on Software Maintenance (ICSM 2006), 24-27 September 2006, Philadelphia, Pennsylvania, USA':
	'Proceedings of the 22nd International Conference on Software Maintenance',
'23rd IEEE International Conference on Software Maintenance (ICSM 2007), October 2-5, 2007, Paris, France':
	'Proceedings of the 23rd International Conference on Software Maintenance',
'24th IEEE International Conference on Software Maintenance (ICSM 2008), September 28 - October 4, 2008, Beijing, China':
	'Proceedings of the 24th International Conference on Software Maintenance',
'25th IEEE International Conference on Software Maintenance (ICSM 2009), September 20-26, 2009, Edmonton, Alberta, Canada':
	'Proceedings of the 25th International Conference on Software Maintenance',
'26th IEEE International Conference on Software Maintenance (ICSM 2010), September 12-18, 2010, Timisoara, Romania':
	'Proceedings of the 26th International Conference on Software Maintenance',
'28th IEEE International Conference on Software Maintenance, ICSM 2012, Trento, Italy, September 23-28, 2012':
	'Proceedings of the 28th International Conference on Software Maintenance',
'ECOOP \'89: Proceedings of the Third European Conference on Object-Oriented Programming, Nottingham, UK, July 10-14, 1989':
	'Proceedings of the Third European Conference on Object-Oriented Programming',
'ECOOP \'92, European Conference on Object-Oriented Programming, Utrecht, The Netherlands, June 29 - July 3, 1992, Proceedings':
	'Proceedings of the Sixth European Conference on Object-Oriented Programming',
'ECOOP 2000 - Object-Oriented Programming, 14th European Conference, Sophia Antipolis and Cannes, France, June 12-16, 2000, Proceedings':
	'Proceedings of the 14th European Conference on Object-Oriented Programming',
'ECOOP 2001 - Object-Oriented Programming, 15th European Conference, Budapest, Hungary, June 18-22, 2001, Proceedings':
	'Proceedings of the 15th European Conference on Object-Oriented Programming',
'ECOOP 2002 - Object-Oriented Programming, 16th European Conference, Malaga, Spain, June 10-14, 2002, Proceedings':
	'Proceedings of the 16th European Conference on Object-Oriented Programming',
'ECOOP 2003 - Object-Oriented Programming, 17th European Conference, Darmstadt, Germany, July 21-25, 2003, Proceedings':
	'Proceedings of the 17th European Conference on Object-Oriented Programming',
'ECOOP 2004 - Object-Oriented Programming, 18th European Conference, Oslo, Norway, June 14-18, 2004, Proceedings':
	'Proceedings of the 18th European Conference on Object-Oriented Programming',
'ECOOP 2005 - Object-Oriented Programming, 19th European Conference, Glasgow, UK, July 25-29, 2005, Proceedings':
	'Proceedings of the 19th European Conference on Object-Oriented Programming',
'ECOOP 2006 - Object-Oriented Programming, 20th European Conference, Nantes, France, July 3-7, 2006, Proceedings':
	'Proceedings of the 20th European Conference on Object-Oriented Programming',
'ECOOP 2007 - Object-Oriented Programming, 21st European Conference, Berlin, Germany, July 30 - August 3, 2007, Proceedings':
	'Proceedings of the 21st European Conference on Object-Oriented Programming',
'ECOOP 2008 - Object-Oriented Programming, 22nd European Conference, Paphos, Cyprus, July 7-11, 2008, Proceedings':
	'Proceedings of the 22nd European Conference on Object-Oriented Programming',
'ECOOP 2009 - Object-Oriented Programming, 23rd European Conference, Genoa, Italy, July 6-10, 2009. Proceedings':
	'Proceedings of the 23rd European Conference on Object-Oriented Programming',
'ECOOP 2010 - Object-Oriented Programming, 24th European Conference, Maribor, Slovenia, June 21-25, 2010. Proceedings':
	'Proceedings of the 24th European Conference on Object-Oriented Programming',
'ECOOP 2011 - Object-Oriented Programming - 25th European Conference, Lancaster, UK, July 25-29, 2011 Proceedings':
	'Proceedings of the 25th European Conference on Object-Oriented Programming',
'ECOOP 2012 - Object-Oriented Programming - 26th European Conference, Beijing, China, June 11-16, 2012. Proceedings':
	'Proceedings of the 26th European Conference on Object-Oriented Programming',
'ECOOP 2013 - Object-Oriented Programming - 27th European Conference, Montpellier, France, July 1-5, 2013. Proceedings':
	'Proceedings of the 27th European Conference on Object-Oriented Programming',
'ECOOP\'87 European Conference on Object-Oriented Programming, Paris, France, June 15-17, 1987, Proceedings':
	'Proceedings of the First European Conference on Object-Oriented Programming',
'ECOOP\'88 European Conference on Object-Oriented Programming, Oslo, Norway, August 15-17, 1988, Proceedings':
	'Proceedings of the Second European Conference on Object-Oriented Programming',
'ECOOP\'91 European Conference on Object-Oriented Programming, Geneva, Switzerland, July  15-19, 1991, Proceedings':
	'Proceedings of the Fifth European Conference on Object-Oriented Programming',
'ECOOP\'93 - Object-Oriented Programming, 7th European Conference, Kaiserslautern, Germany, July 26-30, 1993, Proceedings':
	'Proceedings of the Seventh European Conference on Object-Oriented Programming',
'ECOOP\'95 - Object-Oriented Programming, 9th European Conference, Århus, Denmark, August 7-11, 1995, Proceedings':
	'Proceedings of the Ninth European Conference on Object-Oriented Programming',
'ECOOP\'96 - Object-Oriented Programming, 10th European Conference, Linz, Austria, July 8-12, 1996, Proceedings':
	'Proceedings of the Tenth European Conference on Object-Oriented Programming',
'ECOOP\'98 - Object-Oriented Programming, 12th European Conference, Brussels, Belgium, July 20-24, 1998, Proceedings':
	'Proceedings of the 12th European Conference on Object-Oriented Programming',
'ECOOP\'99 - Object-Oriented Programming, 13th European Conference, Lisbon, Portugal, June 14-18, 1999, Proceedings':
	'Proceedings of the 13th European Conference on Object-Oriented Programming',
'IEEE 27th International Conference on Software Maintenance, ICSM 2011, Williamsburg, VA, USA, September 25-30, 2011':
	'Proceedings of the 27th Conference on Software Maintenance',
'Object-Oriented Programming, Proceedings of the 8th European Conference, ECOOP \'94, Bologna, Italy, July 4-8, 1994':
	'Proceedings of the Eighth European Conference on Object-Oriented Programming',
'Proceedings of the Conference on Software Maintenance, ICSM 1993, Montréal, Quebec, Canada, September 1993':
	'Proceedings of the Ninth Conference on Software Maintenance',
'Proceedings of the International Conference on Software Maintenance, ICSM 1994, Victoria, BC, Canada, September 1994':
	'Proceedings of the Tenth International Conference on Software Maintenance',
'Proceedings of the International Conference on Software Maintenance, ICSM 1995, Opio (Nice), France, October 17-20, 1995':
	'Proceedings of the 11th International Conference on Software Maintenance'
}

numfixes = {
	'1st': 'First',
	'2nd': 'Second',
	'3rd': 'Third',
	'4th': 'Fourth',
	'5th': 'Fifth',
	'6th': 'Sixth',
	'7th': 'Seventh',
	'8th': 'Eighth',
	'9th': 'Ninth',
	'10th': 'Tenth',
	'Eleventh': '11th',
	'Twelfth': '12th'
}

def deadcode_autofix():
	if self['title'][0].count(',')>2 and self['title'][0].find('Conference')>0:
		cs = self['title'][0].split(', ')
		ds = []
		title = ''
		for c in cs:
			if c.isdigit():
				continue
			if self['booktitle'] and c.startswith(self['booktitle'][0]) and c.replace(self['booktitle'][0],'').strip().isdigit():
				continue
			if c.startswith('January') or c.startswith('February') or c.startswith('March') or c.startswith('April') or c.startswith('May') or c.startswith('June') or c.startswith('July') or c.startswith('August') or c.startswith('September') or c.startswith('October') or c.startswith('November') or c.startswith('December'):
				continue
			if c in locations:
				continue
			if c.find('Conference')>-1:
				title = c
				continue
			ds.append(c)
		ds[0] = '%s on %s' % (title, ds[0])
		if len(ds)==2:
			self.dict['title'] = ['%s of the %s' % (ds[1],ds[0])]
		else:	
			self.dict['title'] = [', '.join(ds)]
		for k in numfixes:
			self.dict['title'][0] = self.dict['title'][0].replace(k,numfixes[k])
		# print('Still got:',ds)
