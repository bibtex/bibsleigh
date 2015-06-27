#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

venuesMap = {
# Venue: SANER
'22nd IEEE International Conference on Software Analysis, Evolution, and Reengineering, SANER 2015, Montreal, QC, Canada, March 2-6, 2015':
	'Proceedings of the 22nd International Conference on Software Analysis, Evolution and Reengineering',
'2014 Software Evolution Week - IEEE Conference on Software Maintenance, Reengineering, and Reverse Engineering, CSMR-WCRE 2014, Antwerp, Belgium, February 3-6, 2014':
	'Proceedings of the International Conference on Software Maintenance, Reengineering and Reverse Engineering',
# Venue: WCRE
'10th  Working Conference on Reverse Engineering (WCRE 2003), 13-16 November 2003, Victoria, Canada':
	'Proceedings of the 10th Working Conference on Reverse Engineering',
'11th Working Conference on Reverse Engineering (WCRE 2004), 8-12 November 2004, Delft, The Netherlands':
	'Proceedings of the 11th Working Conference on Reverse Engineering',
'12th Working Conference on Reverse Engineering (WCRE 2005), 7-11 November 2005, Pittsburgh, PA, USA':
	'Proceedings of the 12th Working Conference on Reverse Engineering',
'13th Working Conference on Reverse Engineering (WCRE 2006), 23-27 October 2006, Benevento, Italy':
	'Proceedings of the 13th Working Conference on Reverse Engineering',
'14th Working Conference on Reverse Engineering (WCRE 2007), 28-31 October 2007, Vancouver, BC, Canada':
	'Proceedings of the 14th Working Conference on Reverse Engineering',
'16th Working Conference on Reverse Engineering, WCRE 2009, 13-16 October 2009, Lille, France':
	'Proceedings of the 16th Working Conference on Reverse Engineering',
'17th Working Conference on Reverse Engineering, WCRE 2010, 13-16 October 2010, Beverly, MA, USA':
	'Proceedings of the 17th Working Conference on Reverse Engineering',
'18th Working Conference on Reverse Engineering, WCRE 2011, Limerick, Ireland, October 17-20, 2011':
	'Proceedings of the 18th Working Conference on Reverse Engineering',
'19th Working Conference on Reverse Engineering, WCRE 2012, Kingston, ON, Canada, October 15-18, 2012':
	'Proceedings of the 19th Working Conference on Reverse Engineering',
'20th Working Conference on Reverse Engineering, WCRE 2013, Koblenz, Germany, October 14-17, 2013':
	'Proceedings of the 20th Working Conference on Reverse Engineering',
'9th Working Conference on Reverse Engineering (WCRE 2002), 28 October - 1 November 2002, Richmond, VA, USA':
	'Proceedings of the Ninth Working Conference on Reverse Engineering',
'WCRE 2008, Proceedings of the 15th Working Conference on Reverse Engineering, Antwerp, Belgium, October 15-18, 2008':
	'Proceedings of the 15th Working Conference on Reverse Engineering',
# Venue: CSMR
'10th European Conference on Software Maintenance and Reengineering (CSMR 2006), 22-24 March 2006, Bari, Italy':
	'Proceedings of the 10th European Conference on Software Maintenance and Reengineering',
'11th European Conference on Software Maintenance and Reengineering, Software Evolution in Complex Software Intensive Systems, CSMR 2007, 21-23 March 2007, Amsterdam, The Netherlands':
	'Proceedings of the 11th European Conference on Software Maintenance and Reengineering',
'12th European Conference on Software Maintenance and Reengineering, CSMR 2008, April 1-4, 2008, Athens, Greece':
	'Proceedings of the 12th European Conference on Software Maintenance and Reengineering',
'13th European Conference on Software Maintenance and Reengineering, CSMR 2009, Architecture-Centric Maintenance of Large-SCale Software Systems, Kaiserslautern, Germany, 24-27 March 2009':
	'Proceedings of the 13th European Conference on Software Maintenance and Reengineering',
'14th European Conference on Software Maintenance and Reengineering, CSMR 2010, 15-18 March 2010, Madrid, Spain':
	'Proceedings of the 14th European Conference on Software Maintenance and Reengineering',
'15th European Conference on Software Maintenance and Reengineering, CSMR 2011, 1-4 March 2011, Oldenburg, Germany':
	'Proceedings of the 15th European Conference on Software Maintenance and Reengineering',
'16th European Conference on Software Maintenance and Reengineering, CSMR 2012, Szeged, Hungary, March 27-30, 2012':
	'Proceedings of the 16th European Conference on Software Maintenance and Reengineering',
'17th European Conference on Software Maintenance and Reengineering, CSMR 2013, Genova, Italy, March 5-8, 2013':
	'Proceedings of the 17th European Conference on Software Maintenance and Reengineering',
'1st Euromicro Working Conference on Software Maintenance and Reengineering (CSMR \'97), 17-19 March 1997, Berlin, Germany':
	'Proceedings of the First Euromicro Working Conference on Software Maintenance and Reengineering',
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
# Venue: POPL
'The 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL \'13, Rome, Italy - January 23 - 25, 2013':
	'Proceedings of the 40th Annual Symposium on Principles of Programming Languages',
'The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL \'14, San Diego, CA, USA, January 20-21, 2014':
	'Proceedings of the 41st Symposium on Principles of Programming Languages',
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
	'Conference Record of the First Symposium on Principles of Programming Languages',
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
'POPL \'98, Proceedings of the 25th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Diego, CA, USA, January 19-21, 1998':
	'Proceedings of the 25th Symposium on Principles of Programming Languages',
'POPL \'99, Proceedings of the 26th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Antonio, TX, USA, January 20-22, 1999':
	'Proceedings of the 26th Symposium on Principles of Programming Languages',
'POPL 2000, Proceedings of the 27th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Boston, Massachusetts, USA, January 19-21, 2000':
	'Proceedings of the 27th Symposium on Principles of Programming Languages',
# Venue: GTTSE
'Generative and Transformational Techniques in Software Engineering II, International Summer School, GTTSE 2007, Braga, Portugal, July 2-7, 2007. Revised Papers':
	'Revised Papers of the Second International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering III - International Summer School, GTTSE 2009, Braga, Portugal, July 6-11, 2009. Revised Papers':
	'Revised Papers of the Third International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering IV, International Summer School, GTTSE 2011, Braga, Portugal, July 3-9, 2011. Revised Papers':
	'Revised Papers of the Fourth International Summer School on Generative and Transformational Techniques in Software Engineering',
'Generative and Transformational Techniques in Software Engineering, International Summer School, GTTSE 2005, Braga, Portugal, July 4-8, 2005. Revised Papers':
	'Revised Papers of the First International Summer School on Generative and Transformational Techniques in Software Engineering',
# Venue: MoDELS
'Model-Driven Engineering Languages and Systems - 17th International Conference, MODELS 2014, Valencia, Spain, September 28 - October 3, 2014. Proceedings':
	'Proceedings of the 17th International Conference on Model Driven Engineering Languages and Systems',
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
# Venue: SAC
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
# Venue: SLE
'Software Language Engineering - 7th International Conference, SLE 2014, Västerås, Sweden, September 15-16, 2014. Proceedings':
	'Proceedings of the Seventh International Conference on Software Language Engineering',
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
# Venue: OOPSLA
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
# Venue: ICSME
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
'IEEE 27th International Conference on Software Maintenance, ICSM 2011, Williamsburg, VA, USA, September 25-30, 2011':
	'Proceedings of the 27th Conference on Software Maintenance',
'Proceedings of the Conference on Software Maintenance, ICSM 1993, Montréal, Quebec, Canada, September 1993':
	'Proceedings of the Ninth Conference on Software Maintenance',
'Proceedings of the International Conference on Software Maintenance, ICSM 1994, Victoria, BC, Canada, September 1994':
	'Proceedings of the Tenth International Conference on Software Maintenance',
'Proceedings of the International Conference on Software Maintenance, ICSM 1995, Opio (Nice), France, October 17-20, 1995':
	'Proceedings of the 11th International Conference on Software Maintenance',
# Venue: ECOOP
'Object-Oriented Programming, Proceedings of the 8th European Conference, ECOOP \'94, Bologna, Italy, July 4-8, 1994':
	'Proceedings of the Eighth European Conference on Object-Oriented Programming',
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
# Venue: SCAM
'14th IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2014, Victoria, BC, Canada, September 28-29, 2014':
	'Proceedings of the 14th Working Conference on Source Code Analysis and Manipulation',
'11th IEEE Working Conference on Source Code Analysis and Manipulation, SCAM 2011, Williamsburg, VA, USA, September 25-26, 2011':
	'Proceedings of the 11th Working Conference on Source Code Analysis and Manipulation',
'12th IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2012, Riva del Garda, Italy, September 23-24, 2012':
	'Proceedings of the 12th International Working Conference on Source Code Analysis and Manipulation',
'13th IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2013, Eindhoven, Netherlands, September 22-23, 2013':
	'Proceedings of the 13th International Working Conference on Source Code Analysis and Manipulation',
'1st IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2001), 10 November 2001, Florence, Italy':
	'Proceedings of the First International Workshop on Source Code Analysis and Manipulation',
'2nd IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2002), 1 October 2002, Montreal, Canada':
	'Proceedings of the Second International Workshop on Source Code Analysis and Manipulation',
'3rd IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2003), 26-27 September 2003, Amsterdam, The Netherlands':
	'Proceedings of the Third International Workshop on Source Code Analysis and Manipulation',
'4th IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2004), 15-16 September 2004, Chicago, IL, USA':
	'Proceedings of the Fourth International Workshop on Source Code Analysis and Manipulation',
'5th IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2005), 30 September - 1 October 2005, Budapest, Hungary':
	'Proceedings of the Fifth International Workshop on Source Code Analysis and Manipulation',
'Eighth IEEE International Working Conference on Source Code Analysis and Manipulation (SCAM 2008), 28-29 September 2008, Beijing, China':
	'Proceedings of the Eighth International Working Conference on Source Code Analysis and Manipulation',
'Ninth IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2009, Edmonton, Alberta, Canada, September 20-21, 2009':
	'Proceedings of the Ninth International Working Conference on Source Code Analysis and Manipulation',
'Seventh IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2007), September 30 - October 1, 2007, Paris, France':
	'Proceedings of the Seventh International Workshop on Source Code Analysis and Manipulation',
'Sixth IEEE International Workshop on Source Code Analysis and Manipulation (SCAM 2006), 27-29 September 2006, Philadelphia, Pennsylvania, USA':
	'Proceedings of the Sixth International Workshop on Source Code Analysis and Manipulation',
'Tenth IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2010, Timisoara, Romania, 12-13 September 2010':
	'Proceedings of the Tenth International Working Conference on Source Code Analysis and Manipulation',
# Venue: RTA
'23rd International Conference on Rewriting Techniques and Applications (RTA\'12) , RTA 2012, May 28 - June 2, 2012, Nagoya, Japan':
	'Proceedings of the 23rd International Conference on Rewriting Techniques and Applications',
'24th International Conference on Rewriting Techniques and Applications, RTA 2013, June 24-26, 2013, Eindhoven, The Netherlands':
	'Proceedings of the 24th International Conference on Rewriting Techniques and Applications',
# Venue: ESOP
'ESOP \'88, 2nd European Symposium on Programming, Nancy, France, March 21-24, 1988, Proceedings':
	'Proceedings of the Second European Symposium on Programming',
'ESOP \'92, 4th European Symposium on Programming, Rennes, France, February 26-28, 1992, Proceedings':
	'Proceedings of the Fourth European Symposium on Programming',
'ESOP 86, European Symposium on Programming, Saarbrücken, Federal Republic of Germany, March 17-19, 1986, Proceedings':
	'Proceedings of the First European Symposium on Programming',
'ESOP\'90, 3rd European Symposium on Programming, Copenhagen, Denmark, May 15-18, 1990, Proceedings':
	'Proceedings of the Third European Symposium on Programming',
'Proceedings of the 21st International Conference on Rewriting Techniques and Applications, RTA 2010, July 11-13, 2010, Edinburgh, Scottland, UK':
	'Proceedings of the 21st International Conference on Rewriting Techniques and Applications',
'Proceedings of the 22nd International Conference on Rewriting Techniques and Applications, RTA 2011, May 30 - June 1, 2011, Novi Sad, Serbia':
	'Proceedings of the 22nd International Conference on Rewriting Techniques and Applications',
'Programming Languages and Systems - 20th European Symposium on Programming, ESOP 2011, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2011, Saarbrücken, Germany, March 26-April 3, 2011. Proceedings':
	'Proceedings of the 20th European Symposium on Programming',
'Programming Languages and Systems - 21st European Symposium on Programming, ESOP 2012, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2012, Tallinn, Estonia, March 24 - April 1, 2012. Proceedings':
	'Proceedings of the 21st European Symposium on Programming',
'Programming Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings':
	'Proceedings of the 22nd European Symposium on Programming',
'Programming Languages and Systems - ESOP\'94, 5th European Symposium on Programming, Edinburgh, U.K., April 11-13, 1994, Proceedings':
	'Proceedings of the Fifth European Symposium on Programming',
'Programming Languages and Systems - ESOP\'96, 6th European Symposium on Programming, Linköping, Sweden, April 22-24, 1996, Proceedings':
	'Proceedings of the Sixth European Symposium on Programming',
'Programming Languages and Systems - ESOP\'98, 7th European Symposium on Programming, Held as Part of the European Joint Conferences on the Theory and Practice of Software, ETAPS\'98, Lisbon, Portugal, March 28 - April 4, 1998, Proceedings':
	'Proceedings of the Seventh European Symposium on Programming',
'Programming Languages and Systems, 10th European Symposium on Programming, ESOP 2001 Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2001 Genova, Italy, April 2-6, 2001, Proceedings':
	'Proceedings of the Tenth European Symposium on Programming',
'Programming Languages and Systems, 11th European Symposium on Programming, ESOP 2002, held as Part of the Joint European Conference on Theory and Practice of Software, ETAPS 2002, Grenoble, France, April 8-12, 2002, Proceedings':
	'Proceedings of the 11th European Symposium on Programming',
'Programming Languages and Systems, 12th European Symposium on Programming, ESOP 2003, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2003, Warsaw, Poland, April 7-11, 2003, Proceedings':
	'Proceedings of the 12th European Symposium on Programming',
'Programming Languages and Systems, 13th European Symposium on Programming, ESOP 2004, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2004, Barcelona, Spain, March 29 - April 2, 2004, Proceedings':
	'Proceedings of the 13th European Symposium on Programming',
'Programming Languages and Systems, 14th European Symposium on Programming,ESOP 2005, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2005, Edinburgh, UK, April 4-8, 2005, Proceedings':
	'Proceedings of the 14th European Symposium on Programming',
'Programming Languages and Systems, 15th European Symposium on Programming, ESOP 2006, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2006, Vienna, Austria, March 27-28, 2006, Proceedings':
	'Proceedings of the 15th European Symposium on Programming',
'Programming Languages and Systems, 16th European Symposium on Programming, ESOP 2007, Held as Part of the Joint European Conferences on Theory and Practics of Software, ETAPS 2007, Braga, Portugal, March 24 - April 1, 2007, Proceedings':
	'Proceedings of the 16th European Symposium on Programming',
'Programming Languages and Systems, 17th European Symposium on Programming, ESOP 2008, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings':
	'Proceedings of the 17th European Symposium on Programming',
'Programming Languages and Systems, 18th European Symposium on Programming, ESOP 2009, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2009, York, UK, March 22-29, 2009. Proceedings':
	'Proceedings of the 18th European Symposium on Programming',
'Programming Languages and Systems, 19th European Symposium on Programming, ESOP 2010, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2010, Paphos, Cyprus, March 20-28, 2010. Proceedings':
	'Proceedings of the 19th European Symposium on Programming',
'Programming Languages and Systems, 8th European Symposium on Programming, ESOP\'99, Held as Part of the European Joint Conferences on the Theory and Practice of Software, ETAPS\'99, Amsterdam, The Netherlands, 22-28 March, 1999, Proceedings':
	'Proceedings of the Eighth European Symposium on Programming',
'Programming Languages and Systems, 9th European Symposium on Programming, ESOP 2000, Held as Part of the European Joint Conferences on the Theory and Practice of Software, ETAPS 2000, Berlin, Germany, March 25 - April 2, 2000, Proceedings':
	'Proceedings of the Ninth European Symposium on Programming',
'Rewriting Techniques and Applications, 10th International Conference, RTA-99, Trento, Italy, July 2-4, 1999, Proceedings':
	'Proceedings of the 10th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 11th International Conference, RTA 2000, Norwich, UK, July 10-12, 2000, Proceedings':
	'Proceedings of the 11th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 12th International Conference, RTA 2001, Utrecht, The Netherlands, May 22-24, 2001, Proceedings':
	'Proceedings of the 12th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 13th International Conference, RTA 2002, Copenhagen, Denmark, July 22-24, 2002, Proceedings':
	'Proceedings of the 13th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 14th International Conference, RTA 2003, Valencia, Spain, June 9-11, 2003, Proceedings':
	'Proceedings of the 14th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 15th International Conference, RTA 2004, Aachen, Germany, June 3-5, 2004, Proceedings':
	'Proceedings of the 15th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 19th International Conference, RTA 2008, Hagenberg, Austria, July 15-17, 2008, Proceedings':
	'Proceedings of the 19th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 20th International Conference, RTA 2009, Brasília, Brazil, June 29 - July 1, 2009, Proceedings':
	'Proceedings of the 20th International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 2nd International Conference, RTA-87, Bordeaux, France, May 25-27, 1987, Proceedings':
	'Proceedings of the Second International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 3rd International Conference, RTA-89, Chapel Hill, North Carolina, USA, April 3-5, 1989, Proceedings':
	'Proceedings of the Third International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 4th International Conference, RTA-91, Como, Italy, April 10-12, 1991, Proceedings':
	'Proceedings of the Fourth International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 5th International Conference, RTA-93, Montreal, Canada, June  16-18, 1993, Proceedings':
	'Proceedings of the Fifth International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 6th International Conference, RTA-95, Kaiserslautern, Germany, April 5-7, 1995, Proceedings':
	'Proceedings of the Sixth International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 7th International Conference, RTA-96, New Brunswick, NJ, USA, July 27-30, 1996, Proceedings':
	'Proceedings of the Seventh International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 8th International Conference, RTA-97, Sitges, Spain, June 2-5, 1997, Proceedings':
	'Proceedings of the Eighth International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, 9th International Conference, RTA-98, Tsukuba, Japan, March 30 - April 1, 1998, Proceedings':
	'Proceedings of the Ninth International Conference on Rewriting Techniques and Applications',
'Rewriting Techniques and Applications, First International Conference, RTA-85, Dijon, France, May 20-22, 1985, Proceedings':
	'Proceedings of the First International Conference on Rewriting Techniques and Applications',
'Term Rewriting and Applications, 16th International Conference, RTA 2005, Nara, Japan, April 19-21, 2005, Proceedings':
	'Proceedings of the 16th International Conference on Term Rewriting and Applications',
'Term Rewriting and Applications, 17th International Conference, RTA 2006, Seattle, WA, USA, August 12-14, 2006, Proceedings':
	'Proceedings of the 17th International Conference on Term Rewriting and Applications',
'Term Rewriting and Applications, 18th International Conference, RTA 2007, Paris, France, June 26-28, 2007, Proceedings':
	'Proceedings of the 18th International Conference on Term Rewriting and Applications',
'ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI \'12, Beijing, China - June 11 - 16, 2012':
	'Proceedings of the 33rd Conference on Programming Language Design and Implementation',
'ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI \'13, Seattle, WA, USA, June 16-19, 2013':
	'Proceedings of the 34th Conference on Programming Language Design and Implementation',
'Proceedings of the 1999 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Atlanta, Georgia, USA, May 1-4, 1999':
	'Proceedings of the 20th Conference on Programming Language Design and Implementation',
'Proceedings of the 2000 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Vancouver, Britith Columbia, Canada, June 18-21, 2000':
	'Proceedings of the 21st Conference on Programming Language Design and Implementation',
'Proceedings of the 2001 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Snowbird, Utah, USA, June 20-22, 2001':
	'Proceedings of the 22nd Conference on Programming Language Design and Implementation',
'Proceedings of the 2002 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Berlin, Germany, June 17-19, 2002':
	'Proceedings of the 23rd Conference on Programming Language Design and Implementation',
'Proceedings of the 2009 ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2009, Dublin, Ireland, June 15-21, 2009':
	'Proceedings of the 30th Conference on Programming Language Design and Implementation',
'Proceedings of the 2010 ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2010, Toronto, Ontario, Canada, June 5-10, 2010':
	'Proceedings of the 31st Conference on Programming Language Design and Implementation',
'Proceedings of the 32nd ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2011, San Jose, CA, USA, June 4-8, 2011':
	'Proceedings of the 32nd Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN \'97 Conference on Programming Language Design and Implementation (PLDI), Las Vegas, Nevada, June 15-18, 1997':
	'Proceedings of the 18th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN \'98 Conference on Programming Language Design and Implementation (PLDI), Montreal, Canada, June 17-19, 1998':
	'Proceedings of the 19th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2003 Conference on Programming Language Design and Implementation 2003, San Diego, California, USA, June 9-11, 2003':
	'Proceedings of the 24th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2004 Conference on Programming Language Design and Implementation 2004, Washington, DC, USA, June 9-11, 2004':
	'Proceedings of the 25th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2005 Conference on Programming Language Design and Implementation, Chicago, IL, USA, June 12-15, 2005':
	'Proceedings of the 26th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2006 Conference on Programming Language Design and Implementation, Ottawa, Ontario, Canada, June 11-14, 2006':
	'Proceedings of the 27th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2007 Conference on Programming Language Design and Implementation, San Diego, California, USA, June 10-13, 2007':
	'Proceedings of the 28th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN 2008 Conference on Programming Language Design and Implementation, Tucson, AZ, USA, June 7-13, 2008':
	'Proceedings of the 29th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'88 Conference on Programming Language Design and Implementation (PLDI), Atlanta, Georgia, USA, June 22-24, 1988':
	'Proceedings of the Ninth Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'89 Conference on Programming Language Design and Implementation (PLDI), Portland, Oregon, USA, June 21-23, 1989':
	'Proceedings of the Tenth Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'90 Conference on Programming Language Design and Implementation (PLDI), White Plains, New York, USA, June 20-22, 1990':
	'Proceedings of the 11th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'91 Conference on Programming Language Design and Implementation (PLDI), Toronto, Ontario, Canada, June 26-28, 1991':
	'Proceedings of the 12th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'92 Conference on Programming Language Design and Implementation (PLDI), San Francisco, California, USA, June 17-19, 1992':
	'Proceedings of the 13th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'93 Conference on Programming Language Design and Implementation (PLDI), Albuquerque, New Mexico, USA, June 23-25, 1993':
	'Proceedings of the 14th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'94 Conference on Programming Language Design and Implementation (PLDI), Orlando, Florida, USA, June 20-24, 1994':
	'Proceedings of the 15th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'95 Conference on Programming Language Design and Implementation (PLDI), La Jolla, California, USA, June 18-21, 1995':
	'Proceedings of the 16th Conference on Programming Language Design and Implementation',
'Proceedings of the ACM SIGPLAN\'96 Conference on Programming Language Design and Implementation (PLDI), Philadephia, Pennsylvania, May 21-24, 1996':
	'Proceedings of the 17th Conference on Programming Language Design and Implementation',
'Proceedings of the Symposium on Interpreters and Interpretive Techniques, 1987, St. Paul, Minnesota, USA, June 24 - 26, 1987':
	'Proceedings of the Eighth Symposium on Interpreters and Interpretive Techniques',
'17th International Conference on Software Engineering, Seattle, Washington, USA, April 23-30, 1995, Proceedings':
	'Proceedings of the 17th International Conference on Software Engineering',
'18th International Conference on Software Engineering, Berlin, Germany, March 25-29, 1996, Proceedings':
	'Proceedings of the 18th International Conference on Software Engineering',
'26th International Conference on Software Engineering (ICSE 2004), 23-28 May 2004, Edinburgh, United Kingdom':
	'Proceedings of the 26th International Conference on Software Engineering',
'27th International Conference on Software Engineering (ICSE 2005), 15-21 May 2005, St. Louis, Missouri, USA':
	'Proceedings of the 27th International Conference on Software Engineering',
'28th International Conference on Software Engineering (ICSE 2006), Shanghai, China, May 20-28, 2006':
	'Proceedings of the 28th International Conference on Software Engineering',
'29th International Conference on Software Engineering (ICSE 2007), Minneapolis, MN, USA, May 20-26, 2007':
	'Proceedings of the 29th International Conference on Software Engineering',
'30th International Conference on Software Engineering (ICSE 2008), Leipzig, Germany, May 10-18, 2008':
	'Proceedings of the 30th International Conference on Software Engineering',
'31st International Conference on Software Engineering, ICSE 2009, May 16-24, 2009, Vancouver, Canada, Proceedings':
	'Proceedings of the 31st International Conference on Software Engineering',
'34th International Conference on Software Engineering, ICSE 2012, June 2-9, 2012, Zurich, Switzerland':
	'Proceedings of the 34th International Conference on Software Engineering',
'35th International Conference on Software Engineering, ICSE \'13, San Francisco, CA, USA, May 18-26, 2013':
	'Proceedings of the 35th International Conference on Software Engineering',
'Forging New Links, Proceedings of the 1998 International Conference on Software Engineering, ICSE 98, Kyoto, Japan, April 19-25, 1998':
	'Proceedings of the 20th International Conference on Software Engineering',
'Proceedings of the 11th International Conference on Software Engineering, Pittsburg, PA, USA, May 15-18, 1989':
	'Proceedings of the 11th International Conference on Software Engineering',
'Proceedings of the 12th International Conference on Software Engineering, Nice, France, March 26-30, 1990':
	'Proceedings of the 12th International Conference on Software Engineering',
'Proceedings of the 13th International Conference on Software Engineering, Austin, TX, USA, May 13-17, 1991':
	'Proceedings of the 13th International Conference on Software Engineering',
'Proceedings of the 14th International Conference on Software Engineering, Melbourne, Australia, May 11-15, 1992':
	'Proceedings of the 14th International Conference on Software Engineering',
'Proceedings of the 15th International Conference on Software Engineering, Baltimore, Maryland, USA, May 17-21, 1993':
	'Proceedings of the 15th International Conference on Software Engineering',
'Proceedings of the 16th International Conference on Software Engineering, Sorrento, Italy, May 16-21, 1994':
	'Proceedings of the 16th International Conference on Software Engineering',
'Proceedings of the 1999 International Conference on Software Engineering, ICSE\' 99, Los Angeles, CA, USA, May 16-22, 1999':
	'Proceedings of the 21st International Conference on Software Engineering',
'Proceedings of the 22nd International Conference on on Software Engineering, ICSE 2000, Limerick Ireland, June 4-11, 2000':
	'Proceedings of the 22nd International Conference on Software Engineering',
'Proceedings of the 22rd International Conference on Software Engineering, ICSE 2002, 19-25 May 2002, Orlando, Florida, USA':
	'Proceedings of the 22rd International Conference on Software Engineering',
'Proceedings of the 23rd International Conference on Software Engineering, ICSE 2001, 12-19 May 2001, Toronto, Ontario, Canada':
	'Proceedings of the 23rd International Conference on Software Engineering',
'Proceedings of the 25th International Conference on Software Engineering, May 3-10, 2003, Portland, Oregon, USA':
	'Proceedings of the 25th International Conference on Software Engineering',
'Proceedings of the 2nd International Conference on Software Engineering, San Francisco, California, USA, October 13-15, 1976':
	'Proceedings of the Second International Conference on Software Engineering',
'Proceedings of the 33rd International Conference on Software Engineering, ICSE 2011, Waikiki, Honolulu , HI, USA, May 21-28, 2011':
	'Proceedings of the 33rd International Conference on Software Engineering',
'Proceedings of the 3rd International Conference on Software Engineering, Atlanta, Georgia, USA, May 10-12, 1978':
	'Proceedings of the Third International Conference on Software Engineering',
'Proceedings of the 4th International Conference on Software Engineering, Munich, Germany, September 1979':
	'Proceedings of the Fourth International Conference on Software Engineering',
'Proceedings of the 5th International Conference on Software Engineering, San Diego, California, USA, March 9-12, 1981':
	'Proceedings of the Fifth International Conference on Software Engineering',
'Proceedings, 10th International Conference on Software Engineering, Singapore, Singapore, April 11-15, 1988':
	'Proceedings of the 10th International Conference on Software Engineering',
'Proceedings, 6th International Conference on Software Engineering, Tokyo, Japan, September 13-16, 1982':
	'Proceedings of the Sixth International Conference on Software Engineering',
'Proceedings, 7th International Conference on Software Engineering, Orlando, Florida, USA, March 26-29, 1984':
	'Proceedings of the Seventh International Conference on Software Engineering',
'Proceedings, 8th International Conference on Software Engineering, London, UK, August 28-30, 1985':
	'Proceedings of the Eighth International Conference on Software Engineering',
'Proceedings, 9th International Conference on Software Engineering, Monterey, California, USA, March 30 - April 2, 1987':
	'Proceedings of the Ninth International Conference on Software Engineering',
'Pulling Together, Proceedings of the 19th International Conference on Software Engineering, Boston, Massachusetts, USA, May 17-23, 1997':
	'Proceedings of the 19th International Conference on Software Engineering',
'5th European Software Engineering Conference, Sitges, Spain, September 25-28, 1995, Proceedings':
	'Proceedings of the Fifth European Software Engineering Conference',
'ESEC \'87, 1st European Software Engineering Conference, Strasbourg, France, September 9-11, 1987, Proceedings':
	'Proceedings of the First European Software Engineering Conference',
'ESEC \'89, 2nd European Software Engineering Conference, University of Warwick, Coventry, UK, September 11-15, 1989, Proceedings':
	'Proceedings of the Second European Software Engineering Conference',
'ESEC \'91, 3rd European Software Engineering Conference, Milan, Italy, October 21-24, 1991, Proceedings':
	'Proceedings of the Third European Software Engineering Conference',
'Software Engineering - ESEC \'93, 4th European Software Engineering Conference, Garmisch-Partenkirchen, Germany, September 13-17, 1993, Proceedings':
	'Proceedings of the Fourth European Software Engineering Conference',
'Software Engineering - ESEC/FSE \'97, 6th European Software Engineering Conference Held Jointly with the 5th ACM SIGSOFT Symposium on Foundations of Software Engineering, Zurich, Switzerland, September 22-25, 1997, Proceedings':
	'Proceedings of the Sixth European Software Engineering Conference / Fifth Symposium on Foundations of Software Engineering',
'Conference on Object-Oriented Programming Systems, Languages, and Applications / European Conference on Object-Oriented Programming (OOPSLA/ECOOP), Ottawa, Canada, October 21-25, 1990, Proceedings':
	'Proceedings of the Fifth Conference on Object-Oriented Programming: Systems, Languages, and Applications / European Conference on Object-Oriented Programming',
'The Unified Modeling Language, «UML»\'98: Beyond the Notation, First International Workshop, Mulhouse, France, June 3-4, 1998, Selected Papers':
	'Selected Papers of the First International Workshop on the Unified Modeling Language: Beyond the Notation',
'UML 2002 - The Unified Modeling Language, 5th International Conference, Dresden, Germany, September 30 - October 4, 2002, Proceedings':
	'Proceedings of the Fifth International Conference on the Unified Modeling Language',
'«UML» 2000 - The Unified Modeling Language, Advancing the Standard, Third International Conference, York, UK, October 2-6, 2000, Proceedings':
	'Proceedings of the Third International Conference on the Unified Modeling Language: Advancing the Standard',
'«UML» 2001 - The Unified Modeling Language, Modeling Languages, Concepts, and Tools, 4th International Conference, Toronto, Canada, October 1-5, 2001, Proceedings':
	'Proceedings of the Fourth International Conference on the Unified Modeling Language, Modeling Languages, Concepts, and Tools',
'«UML» 2003 - The Unified Modeling Language, Modeling Languages and Applications, 6th International Conference, San Francisco, CA, USA, October 20-24, 2003, Proceedings':
	'Proceedings of the Sixth International Conference on the Unified Modeling Language, Modeling Languages and Applications',
'«UML» 2004 - The Unified Modelling Language: Modelling Languages and Applications. 7th International Conference, Lisbon, Portugal, October 11-15, 2004. Proceedings':
	'Proceedings of the Seventh International Conference on the Unified Modelling Language: Modelling Languages and Applications',
'«UML»\'99: The Unified Modeling Language - Beyond the Standard, Second International Conference, Fort Collins, CO, USA, October 28-30, 1999, Proceedings':
	'Proceedings of the Second International Conference on the Unified Modeling Language: Beyond the Standard',
'20th ACM SIGSOFT Symposium on the Foundations of Software Engineering (FSE-20), SIGSOFT/FSE\'12, Cary, NC, USA - November 11 - 16, 2012':
	'Proceedings of the 20th Symposium on the Foundations of Software Engineering',
'ACM SIGSOFT Symposium on Foundations of Software Engineering, an Diego, California, USA, November 6-10, 2000, Proceedings':
	'Proceedings of the Eighth Symposium on Foundations of Software Engineering',
'Joint Meeting of the European Software Engineering Conference and the ACM SIGSOFT Symposium on the Foundations of Software Engineering, ESEC/FSE\'13, Saint Petersburg, Russian Federation, August 18-26, 2013':
	'Proceedings of the Joint Meeting of the 14th European Software Engineering Conference and the 21th Symposium on the Foundations of Software Engineering',
'Proceedings of the 10th European Software Engineering Conference held jointly with 13th ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2005, Lisbon, Portugal, September 5-9, 2005':
	'Proceedings of the 10th European Software Engineering Conference held jointly with 13th International Symposium on Foundations of Software Engineering',
'Proceedings of the 11th ACM SIGSOFT Symposium on Foundations of Software Engineering 2003 held jointly with 9th European Software Engineering Conference, ESEC/FSE 2003, Helsinki, Finland, September 1-5, 2003':
	'Proceedings of the 11th Symposium on Foundations of Software Engineering held jointly with the Ninth European Software Engineering Conference',
'Proceedings of the 12th ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2004, Newport Beach, CA, USA, October 31 - November 6, 2004':
	'Proceedings of the 12th International Symposium on Foundations of Software Engineering',
'Proceedings of the 14th ACM SIGSOFT International Symposium on Foundations of Software Engineering, FSE 2006, Portland, Oregon, USA, November 5-11, 2006':
	'Proceedings of the 14th International Symposium on Foundations of Software Engineering',
'Proceedings of the 16th ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2008, Atlanta, Georgia, USA, November 9-14, 2008':
	'Proceedings of the 16th International Symposium on Foundations of Software Engineering',
'Proceedings of the 18th ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2010, Santa Fe, NM, USA, November 7-11, 2010':
	'Proceedings of the 18th International Symposium on Foundations of Software Engineering',
'Proceedings of the 2007 Conference Specification and Verification of Component-Based Systems, SAVCBS 2007, Dubrovnik, Croatia, September 3-4, 2007':
	'Proceedings of the Sixth Specification and Verification of Component-Based Systems Workshop',
'Proceedings of the 2007 International Workshop on Engineering of Software Services for Pervasive Environments, ESSPE 2007, Dubrovnik, Croatia, September 4, 2007':
	'Proceedings of the International Workshop on Engineering of Software Services for Pervasive Environments',
'Proceedings of the 2007 Workshop on Domain Specific Approaches to Software Test Automation, DOSTA 2007, Dubrovnik, Croatia, September 4, 2007':
	'Proceedings of the Workshop on Domain Specific Approaches to Software Test Automation',
'Proceedings of the 2007 Workshop on Engineering Fault Tolerant Systems, EFTS 2007, Dubrovnik, Croatia, September 4, 2007':
	'Proceedings of the Workshop on Engineering Fault Tolerant Systems',
'Proceedings of the 2nd International Workshop on Service Oriented Software Engineering: in conjunction with the 6th ESEC/FSE joint meeting, IW-SOSWE 2007, Dubrovnik, Croatia, September 3, 2007':
	'Proceedings of the Second International Workshop on Service Oriented Software Engineering',
'Proceedings of the 4th International Workshop on Exception Handling, WEH 2008, Atlanta, Georgia, USA, November 14, 2008':
	'Proceedings of the Fourth International Workshop on Exception Handling',
'Proceedings of the 6th joint meeting of the European Software Engineering Conference and the ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2007, Dubrovnik, Croatia, September 3-7, 2007':
	'Proceedings of the Sixth joint meeting of the 11th European Software Engineering Conference and the 15th International Symposium on Foundations of Software Engineering',
'Proceedings of the 6th joint meeting of the European Software Engineering Conference and the ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2007, Dubrovnik, Croatia, September 3-7, 2007, Companion Papers':
	'Companion Papers of the Sixth joint meeting of the 11th European Software Engineering Conference and the 15th International Symposium on Foundations of Software Engineering',
'Proceedings of the 7th joint meeting of the European Software Engineering Conference and the ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2009, Amsterdam, The Netherlands, August 24-28, 2009':
	'Proceedings of the Seventh joint meeting of the 12th European Software Engineering Conference and the 17th International Symposium on Foundations of Software Engineering',
'Proceedings of the 8th European Software Engineering Conference held jointly with 9th ACM SIGSOFT International Symposium on Foundations of Software Engineering 2001, Vienna, Austria, September 10-14, 2001':
	'Proceedings of the Eighth European Software Engineering Conference held jointly with Ninth International Symposium on Foundations of Software Engineering',
'Proceedings of the International Workshop on Synthesis and Analysis of Component Connectors: in conjunction with the 6th ESEC/FSE joint meeting, SYANCO 2007, Dubrovnik, Croatia, September 3-4, 2007':
	'Proceedings of the International Workshop on Synthesis and Analysis of Component Connectors',
'Proceedings of the Tenth ACM SIGSOFT Symposium on Foundations of Software Engineering 2002, Charleston, South Carolina, USA, November 18-22, 2002':
	'Proceedings of the Tenth Symposium on Foundations of Software Engineering',
'Proceedings of the Workshop on Future of Software Engineering Research, FoSER 2010, at the 18th ACM SIGSOFT International Symposium on Foundations of Software Engineering, 2010, Santa Fe, NM, USA, November 7-11, 2010':
	'Proceedings of the Workshop on Future of Software Engineering Research',
'SAVCBS\'09, Proceedings of the 8th International Workshop on Specification and Verification of Component-Based Systems, August 25, 2009, Amsterdam, The Netherlands':
	'Proceedings of the 8th International Workshop on Specification and Verification of Component-Based Systems',
'SIGSOFT \'93, Proceedings of the First ACM SIGSOFT Symposium on Foundations of Software Engineering, Los Angeles, California, USA, December 7-10, 1993':
	'Proceedings of the First Symposium on Foundations of Software Engineering',
'SIGSOFT \'94, Proceedings of the Second ACM SIGSOFT Symposium on Foundations of Software Engineering, New Orleans, Louisiana, USA, December 6-9, 1994':
	'Proceedings of the Second Symposium on Foundations of Software Engineering',
'SIGSOFT \'95, Proceedings of the Third ACM SIGSOFT Symposium on Foundations of Software Engineering, Washington, DC, USA, October 10-13, 1995':
	'Proceedings of the Third Symposium on Foundations of Software Engineering',
'SIGSOFT \'96, Proceedings of the Fourth ACM SIGSOFT Symposium on Foundations of Software Engineering, San Francisco, California, USA, October 16-18, 1996':
	'Proceedings of the Fourth Symposium on Foundations of Software Engineering',
'SIGSOFT \'98, Proceedings of the ACM SIGSOFT International Symposium on Foundations of Software Engineering, Lake Buena Vista, Florida, USA, November 3-5, 1998':
	'Proceedings of the Sixth International Symposium on Foundations of Software Engineering',
'SIGSOFT/FSE\'11 19th ACM SIGSOFT Symposium on the Foundations of Software Engineering (FSE-19) and ESEC\'11: 13rd European Software Engineering Conference (ESEC-13), Szeged, Hungary, September 5-9, 2011':
	'Proceedings of the 19th Symposium on the Foundations of Software Engineering and the 13rd European Software Engineering Conference',
'Software Engineering - ESEC/FSE\'99, 7th European Software Engineering Conference, Held Jointly with the 7th ACM SIGSOFT Symposium on the Foundations of Software Engineering, Toulouse, France, September 1999, Proceedings':
	'Proceedings of the Seventh European Software Engineering Conference, Held Jointly with the Seventh Symposium on the Foundations of Software Engineering',
'The 1st International Workshop on Software Ecosystem Architectures, WEA 2013, Saint Petersburg, Russian Federation, August 19, 2013':
	'The First International Workshop on Software Ecosystem Architectures',
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
