from django.core.management.base import BaseCommand
from openpyxl import load_workbook

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

KADASTER_MAPPING = {'house': '11',  'appartment': '12',  'farm': '14'}


class Command(BaseCommand):
		help = "Import houses from kadaster xlsx."

		def add_arguments(self, parser):
				parser.add_argument('file', nargs='+')

		def handle(self, file,  *args, **options):
				try:
					wb = load_workbook(file[0])
					sheet = wb.worksheets[0]
					data = sheet.values
					column_names = next(data)[1:]
					house = KADASTER_MAPPING.get('house')
					appartment = KADASTER_MAPPING.get('appartment')
					farm =  KADASTER_MAPPING.get('farm')
					score_list = []
					for column in data:
						building_type = column[14]
						self.process_building_type(appartment, building_type, column, farm, house, score_list)
					print(sum(score_list)/len(score_list))
					print(min(score_list))
					print(max(score_list))
					score_list.sort()
					print(score_list[:5])
					print(score_list[-5:])

				except:
					pass

		def process_building_type(self, appartment, building_type, column, farm, house, score_list):
			if building_type == house or building_type == appartment:
				no_filled_cells = len([x for x in column if x])
				no_total_cells = len(column) - 1
				score = (no_filled_cells / no_total_cells) * 100
				score_list.append(score)
			elif building_type == farm:
				logger.error('farm')


