import fpdf

class PDF(fpdf.FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_font("Times", size=16)
        self.add_page()
    def create_table(self, data):
        with self.table(width=190) as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(str(datum))
