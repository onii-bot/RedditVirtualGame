import openpyxl
ticker_and_ltp = dict()

workbook = openpyxl.load_workbook("./data/STONKS V2.5Beta.xlsx")
sheet = workbook["STONKS"]
sheet = workbook.active

for j in range(1, sheet.max_row):
	b = sheet["B" + str(j)]
	c = sheet["C" + str(j)]
	if c.value == "#N/A": continue
	ticker_and_ltp[b.value] = c.value