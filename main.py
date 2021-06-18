from reportlab.lib import colors
from reportlab.lib.pagesizes import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import datetime
import calendar

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_table_data(date):
	"""creates day numbers of the month to fill the table with"""
	data = [["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]]

	month_start = date.replace(day=1)
	month_end = date.replace(day=calendar.monthrange(date.year, date.month)[1])

	start_date = month_start - datetime.timedelta(days=month_start.weekday())
	end_date = month_end + datetime.timedelta(days=7 - month_end.weekday())
	days = (end_date - start_date).days

	counter = start_date
	for i in range(days // 7):
		week = []
		for j in range(7):
			week.append(str(counter.day))
			counter = counter + datetime.timedelta(days=1)
		data.append(week)
	return data


def gray_out_other_months(date, style):
	"""grays out days that were added to the table from other months"""
	month_start = date.replace(day=1)
	month_end = date.replace(day=calendar.monthrange(date.year, date.month)[1])

	gray = colors.toColor('rgb(247, 247, 247)')
	start_off = month_start.weekday()
	end_off = month_end.weekday()

	if start_off:
		style.add('BACKGROUND', (0, 1), (start_off - 1, 1), gray)
	if end_off != 6:
		style.add('BACKGROUND', (end_off + 1, -1), (-1, -1), gray)


def print_month(year=datetime.date.today().year, month=datetime.date.today().month):
	date = datetime.date(year, month, 1)

	doc = SimpleDocTemplate(
		date.strftime("%Y-%m %B.pdf"),
		pagesize=landscape(A4),
		leftMargin=0,
		rightMargin=0,
		topMargin=0,
		bottomMargin=0)
	elements = []

	text_styles = getSampleStyleSheet()
	header_style = text_styles["Normal"]
	header_style.fontName = "Inter"
	header_style.fontSize = 15
	header_style.leading = 20
	header_style.leftIndent = 20
	header_style.textTransform = 'uppercase'
	elements.append(Paragraph(date.strftime("%y &nbsp; %B"), header_style))

	table_width = 292 * mm
	table_height = 205 * mm
	table_height -= header_style.leading

	table_data = create_table_data(date)
	week_row_count = len(table_data) - 1
	weekday_row_height = 5 * mm

	col_width = table_width / 7
	row_height = (table_height - weekday_row_height) / week_row_count

	table = Table(table_data, colWidths=[col_width] * 7, rowHeights=[weekday_row_height] + [row_height] * week_row_count)
	table_style = TableStyle([
		('FONTNAME', (0, 0), (-1, -1), 'Inter'),
		('TEXTCOLOR', (0, 0), (-1, -1), colors.gray),
		('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
		('ALIGN', (0, 0), (-1, 0), "CENTER"),
		('VALIGN', (0, 1), (-1, -1), 'TOP'),
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('LINEBEFORE', (5, 0), (5, -1), 1, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black),
	])
	gray_out_other_months(date, table_style)
	table.setStyle(table_style)

	elements.append(table)
	doc.build(elements)


if __name__ == '__main__':
	import locale
	locale.setlocale(locale.LC_ALL, "de_DE.utf8")

	import os
	# https://fonts.google.com/specimen/Inter
	pdfmetrics.registerFont(TTFont('Inter', os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/Inter-Regular.ttf')))

	for i in range(6, 11):
		print_month(2021, i)
