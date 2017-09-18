from backend import RequestProxy, WebpageScanner, SoupWrap, AppRobot
import xlsxwriter


#Now this is more like a draft script to check if added functionalites work as perceived, plus to chceck some logic of the app


if __name__ == "__main__":

	#base_url of WebpageScanner = 'https://panoramafirm.pl/'
	panorama_firm_main = WebpageScanner()
	#set max redirects of requests object
	panorama_firm_main.max_redirects = 1000

	proxy_list = RequestProxy()
	robot = AppRobot()

	robot.check_robots('https://panoramafirm.pl/robots.txt')
	parser_type = 'html.parser'
	robot_user_agent = '*'
	
	
	if robot.can_fetch(robot_user_agent, WebpageScanner.base_url):

		content_main_webpage = (
			panorama_firm_main.get_page_url(
				'GET',
				WebpageScanner.base_url,
				proxy_list.get_random_request_headers(),
				proxy_list.get_random_proxy()).content)

		panorama_mainwebpage_content = SoupWrap(
			content_main_webpage, parser_type)
		panorama_mainwebpage_content.get_categories('a', class_='mobileCatalog')
		

		#chosen_category = panorama_mainwebpage_content.category_to_url(
			#'Okuliści', panorama_mainwebpage_content.categories)
		
		new_link = 'https://panoramafirm.pl/' + "okuliści"

	try:
		
		robot.can_fetch(robot_user_agent, new_link)
		page_chosen = WebpageScanner()
		page_chosen.max_redirects = 1000
		content_page = page_chosen.get_page_url(
			'GET', new_link, proxy_list.get_random_request_headers(),
			proxy_list.get_random_proxy()).content

		content_to_parse = SoupWrap(
			content_page, parser_type)

		content_to_parse.get_comp_name(
			'a', "business-card-title addax addax-cs_hl_hit_company_name_click")
		content_to_parse.clean_comp_name()

		content_to_parse.get_address('div', 'address-container has-left-icon')
		content_to_parse.clean_address()
		content_to_parse.split_address()
		content_to_parse.get_mails(
			'href', 'a', 'addax addax-cs_hl_email_submit_click count-hovers')
		content_to_parse.substract_mail("Brak adresu e-mail.")
		data = content_to_parse.merge_mail_address_name()
		
		while (content_to_parse.is_more(
				'a', 'title', 'href', 'Przejdź do następnej strony')):
			
			print(content_to_parse.new_url)

			robot.can_fetch(robot_user_agent, content_to_parse.new_url)
			nxt_stuff = page_chosen.get_page_url(
				'GET', content_to_parse.new_url, proxy_list.get_random_request_headers(),
				proxy_list.get_random_proxy()).content

			content_to_parse = SoupWrap(
				nxt_stuff, parser_type)
			
			content_to_parse.get_address('div', 'address-container has-left-icon')
			content_to_parse.clean_address()
			content_to_parse.split_address()
				
			content_to_parse.get_comp_name(
				'a', "business-card-title addax addax-cs_hl_hit_company_name_click")
			content_to_parse.get_address('div', 'address-container has-left-icon')
			content_to_parse.clean_comp_name()

			content_to_parse.get_mails(
				'href', 'a', 'addax addax-cs_hl_email_submit_click count-hovers')
			content_to_parse.substract_mail('Brak adresu e-mail.')
					
			data += content_to_parse.merge_mail_address_name()

		test_dict = {}
		for item in data:

			if item[0] in test_dict:

				test_dict[item[0]].append(item[1:])

			else:
				test_dict[item[0]] = list()
				test_dict[item[0]].append(item[1:])

		excel_data = xlsxwriter.Workbook('Okuliści_Polska_Email.xlsx')

		cond_str = 'Brak adresu e-mail.'
		
		for key, value in test_dict.items():

			row = 0
			col = 0
			for item in value:

				if cond_str in item:
					pass

				else:


					if excel_data.get_worksheet_by_name(key):
						working_sheet = excel_data.get_worksheet_by_name(key)
						working_sheet.write(row, col, item[0])
						working_sheet.write(row, col+1, item[1])
						working_sheet.write(row, col+2, item[2])
						row += 1

					else:

						new_row = 0
						new_col = 0

						new_sheet = excel_data.add_worksheet(key)
						new_sheet.write(new_row, new_col, item[0])
						new_sheet.write(new_row, new_col+1, item[1])
						new_sheet.write(new_row, new_col+2, item[2])
				

		excel_data.close()

		count = 0
		for key in test_dict.keys():

			count += 1

		print(count) 


	except ValueError:
		print("Something went wrong!")