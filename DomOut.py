#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import sys
	import re
	import tempfile
	import datetime
	import subprocess
	import smtplib
	import string
	import os
	from elementtree import ElementTree
except ImportError,e:
	import sys
	sys.stdout.write("%s" %e)   
	sys.exit(1)
	

class SMTP ():
	"""
		Mail Gondermek Icin Kullanilan Sinif Tanimlamalari
	"""

	def __init__ (self, email_config):
		self.server = email_config[0]
		self.mail_to = email_config[1]
		self.sender = email_config[2]

	def send_email (self, domain, warning_day, expire_time):
		"""
			Mail Gonderen Fonksiyon
		"""

		Subject = "DomOut : %s : Kalan Sure : %s"% (domain, warning_day)
		To = self.mail_to
		From = self.sender
		Text = "%s -> Kalan Sure : %s : Uyari Zamani : %s "% (domain, warning_day, expire_time)
		Body = string.join(("From: %s" % From,"To: %s" % To,"Subject: %s" % Subject,"",Text), "\r\n")
		server = smtplib.SMTP(self.server)
		server.sendmail(From, [To], Body)
		server.quit()


class WHOIS ():
	"""
		Whois Sinif Tanimlamalari 
	"""

	def __init__ (self):
		"""
			Whois regexp tanimlamalari
		"""

		self.expired_reg_text_list = ["(\s+)?Expires on(\.+)?:(.*)","(\s+)?Expiration Date(\.+)?:(.*)"]


	def run_whois (self, domain):
		"""
			Whois sorgusunu calistirir
		"""

		whois_proc = subprocess.Popen('whois %s 2>/dev/null'% (domain), shell=True, stdout=subprocess.PIPE,)
		whois_proc.wait()

		if whois_proc.returncode == 0:
			whois_stdout = whois_proc.communicate()[0]
			return whois_stdout
		else:
			return None

	def parse_expire_date (self, response):
		"""
			Whois sorgusunun cevabindan expire zamanini parse eden fonksiyon
		"""
	
		tmp_file = tempfile.TemporaryFile(mode='w+t')
		tmp_file.write(response)

		expire_response = None

		for reg in self.expired_reg_text_list:
			expired_reg = re.compile(reg)
			tmp_file.seek(0)		
			
			for line in tmp_file:
				if re.match(expired_reg, line):
					expire_text = re.match(expired_reg, line).group(3)
					expire_response = expire_text
		
		tmp_file.close()

		return expire_response
		

	
class DATE ():
	"""
		Date sinifi icin gerekli tanimlamalar
	"""

	def __init__ (self):
		"""
			Aylari sayi olarak gosteren tanimlamalar
		"""

		self.month_list = {"jan":"1", "feb":"2", "mar":"3", "apr":"4", "may":"5", "jun":"6", "jul":"7", "aug":"8", "sep":"9", "oct":"10", "nov":"11", "dec":"12"}
		self.date_reg_1 = ".*([0-9]{4}\-([0-9]{2})\-[0-9]{2}).*"
		self.date_reg_2 = ".*([0-9]{2}\-([A-z]{3})\-[0-9]{4}).*"
		self.date_reg_3 = ".*([0-9]{4}\-([A-z]{3})\-[0-9]{2}).*"


	def convert_month_to_number (self, month):
		"""
			Isimle belirtilen ay degerini sayi degere cevirir.
		"""

		return self.month_list["%s"% (month)]		


	def calculate_date (self, expire_date_list, domain, expire_time, email_list):
		"""
			Domain zaman asimi suresini gun olarak belirtir.
		"""

		expire_year = expire_date_list["year"]
		expire_month = expire_date_list["month"]
		expire_day = expire_date_list["day"]

		now = datetime.datetime.now()
		current_year = now.year
		current_month = now.month
		current_day = now.day

		day = (datetime.date(int(expire_year), int(expire_month), int(expire_day)) - datetime.date(current_year, current_month, current_day)).days

                smtp = SMTP(email_list)							

		if int(expire_time) >= day:
			smtp.send_email(domain, day, expire_time)
			print domain + " -> " + str(day) + " -> " + expire_time
	

	def parse_date (self, date_line, domain, expire_time, email_config):
		"""
			Zamani parse edeerek gun,ay ve yil olarak belirtir.
		"""
	
		date_list = {"day":"","month":"","year":""}

               	if re.search(self.date_reg_1, date_line):
			date_list["day"] = re.search(self.date_reg_1, date_line).group(1).split("-")[2]                       	
			date_list["month"] = re.search(self.date_reg_1, date_line).group(1).split("-")[1]                       	
			date_list["year"] = re.search(self.date_reg_1, date_line).group(1).split("-")[0]                       	

		elif re.search(self.date_reg_2, date_line):
			date_list["day"] = re.search(self.date_reg_2, date_line).group(1).split("-")[0]                       	
			_month = re.search(self.date_reg_2, date_line).group(1).split("-")[1].lower()
			month = self.convert_month_to_number (_month)                       	
			date_list["month"] = month                       	
			date_list["year"] = re.search(self.date_reg_2, date_line).group(1).split("-")[2]                       	
			
		elif re.search(self.date_reg_3, date_line):
			date_list["day"] = re.search(self.date_reg_3, date_line).group(1).split("-")[2]                       	
			_month = re.search(self.date_reg_3, date_line).group(1).split("-")[1].lower()                       	
			month = self.convert_month_to_number (_month)
			date_list["month"] = month                       	
			date_list["year"] = re.search(self.date_reg_3, date_line).group(1).split("-")[0]                       	
		
		self.calculate_date(date_list, domain, expire_time, email_config)

###
### Go ga go go go 
###


if __name__ == "__main__":


	if not len(sys.argv) == 3:
		print "Usage %s -f config.ini" % (sys.argv[0])
		sys.exit (3)
	else:
		domain = None
		config_file = sys.argv[2]

		if not os.path.exists(config_file):
			print "%s dosyasi sistemde bulunamadi"% (config_file)
			sys.exit(4)

		whois = WHOIS()

		xml_element = ElementTree.parse(config_file).getroot()

		for node in xml_element.findall("domain"):
			domain = None
			expire_day = None
			mail_to = None	
			email_config = []
			
			for domain_node in node.getchildren():

				if domain_node.tag == "name":
					domain = domain_node.text
					continue

				elif domain_node.tag == "mail_to":
					mail_to = domain_node.text
					continue

				elif domain_node.tag == "expire_day":
					expire_day = domain_node.text
					expire_date_text = whois.run_whois(domain)
					
					if expire_date_text:
						for node in xml_element.findall("email"):
							for email_node  in node.getchildren():
								if email_node.tag == "default_mail_to" and mail_to:
									email_config.append(mail_to)
								else:
									email_config.append(email_node.text)
						
						whois_response = whois.parse_expire_date(expire_date_text)
						date = DATE()
                                                
						date.parse_date(whois_response, domain, expire_day, email_config)




