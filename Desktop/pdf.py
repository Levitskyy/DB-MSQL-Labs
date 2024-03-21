import fpdf

class PDF(fpdf.FPDF):
    def create_table(self, data):
        self.set_font("Times", size=16)
        self.add_page()
        with self.table() as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
