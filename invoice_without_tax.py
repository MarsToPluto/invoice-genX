from fpdf import FPDF
import re
import sys
import os
from decimal import Decimal

def get_base_path():
    if getattr(sys, 'frozen', False):
        # If running in a bundled executable
        return sys._MEIPASS
    else:
        # If running in a script
        return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()
class PDF(FPDF):
    def __init__(self, invoice_details, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_details = invoice_details

    STYLES = {
        'title_font': ('Arial', 'B', 10),
        'label_font': ('Arial', 'B', 6),
        'value_font': ('Arial', '', 6),
        'label_color': (0, 0, 0),
        'value_color': (0, 0, 0),
        'title_color': (60, 126, 209),
        'line_width': 0.3,
        'header_line_y_offset': 5,
        'header_x': 10,
        'header_y_offset': 4,
        'header_height': 40,
        'value_indent': 30,  # Indent for values to keep them close to labels
    }
    TOTAL_AMOUNT = 0
    TOTAL_QUANTITY = 0

    def format_inr(self,num):
        num = Decimal(num)
        decimal_part = num - int(num)
        num = int(num)

        # Convert decimal part to words if it exists
        if decimal_part:
            return inr_number_to_words(num) + " point " + " ".join(inr_number_to_words(int(i)) for i in str(decimal_part)[2:])

        under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakh', 10000000: 'Crore'}

        def inr_number_to_words(num):
            if num < 20:
                return under_20[num]

            if num < 100:
                return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

            pivot = max([key for key in above_100.keys() if key <= num])

            # Adding "and" only for numbers that are in the hundreds range
            return inr_number_to_words(num // pivot) + ' ' + above_100[pivot] + (' and ' + inr_number_to_words(num % pivot) if num % pivot != 0 and pivot == 100 else ' ' + inr_number_to_words(num % pivot) if num % pivot != 0 else '')

        # Handle singular/plural forms
        result = inr_number_to_words(num)
        result += " Rupee" + ("s" if num != 1 else "") + " Only"

        return result
    def header(self):
        # Title section
        self.add_watermark('GALAXY SMART POINT')
        title_width = 190
        title_x = 10
        title_y = 10
        right_label_width = 50
        right_label_x = 210 - right_label_width - 10
        right_label_y = title_y

        # Title: TAX INVOICE
        self.set_font(*self.STYLES['title_font'])
        self.set_text_color(*self.STYLES['title_color'])
        self.set_xy(title_x + 5, title_y + 2)
        self.cell(title_width - 10, 8, 'TAX INVOICE', ln=True, align='C')
        self.ln(5)

        # Horizontal line to separate title and label sections
        line_y = title_y + self.STYLES['header_line_y_offset']
        self.set_line_width(self.STYLES['line_width'])
        self.line(title_x, line_y + 4, 210 - 10, line_y + 4)




        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        # Draw the lines
        # self.set_draw_color(255, 0, 0)
        self.line(title_x + 66, line_y + 15, 210 - 10, line_y + 15)  # Top horizontal line of the section
        self.line(title_x + 130, line_y + 4, title_x + 130, line_y + 28)  # Vertical line
        self.line(title_x + 66, line_y + 28, 210 - 10, line_y + 28)  # Bottom horizontal line of the section
        # self.set_draw_color(0, 0, 0)




        # Add text inside the section
        text_x = title_x + 68  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 7  # Y-coordinate for the text, centered vertically

        self.set_font("Arial", size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, "Invoice #:")  # Replace "Your Text Here" with your desired text



        # Add text inside the section
        text_x = title_x + 68  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 10  # Y-coordinate for the text, centered vertically

        self.set_font("Arial",'B', size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, f"INV-{self.invoice_details['invoice_id']}")  # Replace "Your Text Here" with your desired text


        # Add text inside the section
        text_x = title_x + 132  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 7  # Y-coordinate for the text, centered vertically

        self.set_font("Arial", size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, "Invoice Date:")  # Replace "Your Text Here" with your desired text



        # Add text inside the section
        text_x = title_x + 132  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 10  # Y-coordinate for the text, centered vertically

        self.set_font("Arial",'B', size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, self.invoice_details['due_date'])  # Replace "Your Text Here" with your desired text



        # Add text inside the section
        text_x = title_x + 68  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 18  # Y-coordinate for the text, centered vertically

        self.set_font("Arial", size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, "Place of Supply:")  # Replace "Your Text Here" with your desired text



        # Add text inside the section
        text_x = title_x + 68  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 21  # Y-coordinate for the text, centered vertically

        self.set_font("Arial",'B', size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, "44-EXAMPLE") 



        # Add text inside the section
        text_x = title_x + 132  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 18  # Y-coordinate for the text, centered vertically

        self.set_font("Arial", size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, "Due Date:")  # Replace "Your Text Here" with your desired text



        # Add text inside the section
        text_x = title_x + 132  # X-coordinate for the text, slightly inside the section
        text_y = line_y + 21  # Y-coordinate for the text, centered vertically

        self.set_font("Arial",'B', size=7)  # Set font and size
        self.set_text_color(0,0,0)
        self.text(text_x, text_y, self.invoice_details['due_date'])  # Replace "Your Text Here" with your desired text

        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        #INVOICE SECTIOn TOP RIGHT CONFIG
        # "ORIGINAL FOR RECIPIENT" label
        self.set_font(*self.STYLES['label_font'])
        self.set_text_color(128, 128, 128)
        self.set_xy(right_label_x + 5, right_label_y + 2)
        self.cell(right_label_width - 10, 8, 'ORIGINAL FOR RECIPIENT', ln=True, align='C')
        # Header section: Business details
        header_x = self.STYLES['header_x']
        header_y = line_y + self.STYLES['header_y_offset']
        header_height = self.STYLES['header_height']
        header_width = 66
        self.rect(header_x, header_y, header_width, header_height - 11, 'D')
        self.set_draw_color(0, 0, 0)
        self.ln(4)
        # Seller details
        details = [
            ('GALAXY SMART POINT', '', 'title'),
            ('GSTIN:', 'XXXXXXXXX', 'normal'),
            ('Address:', 'XXXXXXXXXX, XXX, XXXX 100001', 'normal'),
            ('Mobile:', '+91 9876543210', 'normal'),
        ]

        for label, value, identifier in details:
            if identifier == 'title':
                self.set_font(self.STYLES['label_font'][0], self.STYLES['label_font'][1], self.STYLES['label_font'][2] + 4)
            else:
                self.set_font(*self.STYLES['label_font'])
            
            # Print the label
            self.set_text_color(*self.STYLES['label_color'])
            self.cell(self.STYLES['value_indent'] - 10, 4, f'{label}', align='L')

            if identifier == 'title':
                self.set_font(self.STYLES['value_font'][0], self.STYLES['value_font'][1], self.STYLES['value_font'][2] + 6)
            else:
                self.set_font(*self.STYLES['value_font'])

            # Set the text color for the value
            self.set_text_color(*self.STYLES['value_color'])
            
            if label == 'Address:':
                # Use multi_cell for the address to handle overflow
                self.multi_cell(header_width - self.STYLES['value_indent'], 4, value, align='L')
            else:
                # Print the value next to the label for other fields
                self.cell(header_width - self.STYLES['value_indent'], 4, value, ln=True, align='L')

        self.ln(4)
        # Move to the next section
        self.set_xy(header_x, header_y + header_height + 18)
        # self.set_xy(header_x, header_y + header_height + 4)
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS

        # Draw the vertical line
        # self.set_draw_color(255,0,0)
        self.line(title_x + 66, line_y + 4, title_x + 66, line_y + 44)  # Vertical line
        # self.set_draw_color(0,0,0)
        # self.set_draw_color(0, 0, 0)

        # Starting coordinates for the text
        text_x = title_x + 2  # X-coordinate for the text, slightly inside the section
        initial_text_y = line_y + 36  # Initial Y-coordinate for the first line of text

        # Add the "Customer Details:" label
        self.set_font("Arial", size=7)  # Set font and size for the label
        self.set_text_color(0, 0, 0)  # Set text color
        self.text(text_x, initial_text_y, "Customer Details:")  # First line: "Customer Details:"

        # Add the first line of customer details
        self.set_font("Arial",'B', size=7)  # Set font and size for the customer details
        self.text(text_x, initial_text_y + 4, self.invoice_details['customer_name'])  # Second line: "RIJUWAN AHMED"

        # Add the second line of customer details

        # CUSTOMER DETAILS SECTION END



        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        #CUSTOMER DETAILS
        self.set_xy(header_x, header_y + header_height - 2)
        self.set_draw_color(0, 0, 0)

    def extract_amount(self,amount_str):
        # Regular expression to match a numerical amount
        match = re.search(r'Rs\.\s*([\d,]+\.\d{2})', amount_str)
        if match:
            # Extract the numerical part and remove commas if present
            amount = match.group(1).replace(',', '')
            return float(amount)
        else:
            raise ValueError("Amount not found in the string.")
    def add_invoice_details(self, invoice_details):
        # Define column widths (including the index column)
        col_widths = {
            'index': 8,  # Width for the index column
            'item': 55,
            'hsn': 18,
            'rate': 25,
            'qty': 16,
            'taxable_value': 25,
            'tax_amount': 22,
            'amount': 21
        }

        items = invoice_details["items"]
        
        # Set header font and size
        self.set_font('Arial', 'B', 8)
        # self.set_draw_color(255, 0, 0)
        self.ln(2)
        
        # Print header row with borders
        self.cell(col_widths['index'], 6, '#', 1)  # Header for index column
        self.cell(col_widths['item'], 6, 'Item', 1)
        self.cell(col_widths['hsn'], 6, 'HSN/SAC', 1)
        self.cell(col_widths['rate'], 6, 'Rate / Item', 1)
        self.cell(col_widths['qty'], 6, 'Qty', 1)
        self.cell(col_widths['taxable_value'], 6, 'Taxable Value', 1)
        self.cell(col_widths['tax_amount'], 6, 'Tax Amount', 1)
        self.cell(col_widths['amount'], 6, 'Amount', 1)
        self.ln()




        # Set font for table content
        self.set_font('Arial', '', 8)



        
        # Iterate through items and print each row with an index
        for idx, item in enumerate(items, start=1):
            # Get item name and calculate height of the multi-cell
            item_name = item['item_name']
            self.set_x(self.get_x())
            
            # Store starting Y position
            y_start = self.get_y()
            
            # Print the index number
            self.cell(col_widths['index'], 6, str(idx), border='LR', align='C')
            
            # Multi-cell for item name
            self.multi_cell(col_widths['item'], 6, item_name, border='LR', align='L')
            
            # Get the height of the multi-cell
            y_end = self.get_y()
            cell_height = y_end - y_start
            
            # Move cursor to the right position for the rest of the columns
            self.set_y(y_start)
            self.set_x(self.get_x() + col_widths['index'] + col_widths['item'])
            
            # Add other columns with borders and correct height
            self.cell(col_widths['hsn'], cell_height, str(item['hsn_sac']), border='LR')
            self.cell(col_widths['rate'], cell_height, str(item['rate']), border='LR')
            self.cell(col_widths['qty'], cell_height, f"{str(item['quantity'])} NOS", border='LR')
            self.cell(col_widths['taxable_value'], cell_height, str(item['taxable_value']), border='LR')
            self.cell(col_widths['tax_amount'], cell_height, str(item['tax_amount']), border='LR')
            self.TOTAL_AMOUNT=self.TOTAL_AMOUNT + self.extract_amount(item['amount'])
            self.TOTAL_QUANTITY=self.TOTAL_QUANTITY + item['quantity']
            self.cell(col_widths['amount'], cell_height, str(item['amount']), border='LR')
            self.ln(cell_height)

        # Add bottom border for the table
        self.cell(sum(col_widths.values()), 0, '', 'T')




        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING

        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING
        # #TAX TING


    def draw_vertical_lines(self, x1, y1, x2, y2):
        self.set_xy(x1, y1)
        self.line(x1, y1, x2, y2)

    def add_totals(self):



        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING

        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING

        self.set_x(self.l_margin) 
        self.set_font('Arial', '', 7)
        self.set_fill_color(0, 0, 0)  # Black background for the title
        self.set_text_color(0, 0, 0)  # White text color for contrast
        self.cell(190, 5, f'Total Items / Qty : {self.TOTAL_QUANTITY} / {self.TOTAL_QUANTITY}.000', border='LTRB', align='L', fill=False)
        self.set_text_color(0, 0, 0)  # Reset text color to black
        self.set_font('Arial', '', 8)
        self.ln(2)  # A

        # Add space before the summary section
        self.ln(2)  # Adjust to add space before the summary section

        # Add the text on the left side
        # self.set_x(self.l_margin)  # Align to the left margin
        self.set_font('Arial', '', 8)  # Regular font

        # Define left and right column widths for the amounts
        description_width = 40
        amount_width = 30



        # Add another thin horizontal line before "Total"
        # self.ln(2)  # Add a small space before the next line
        line_y = self.get_y()  # Get the new Y position
        line_start_x = self.get_x()  # Get the starting X position of the line
        line_end_x = line_start_x + description_width + amount_width  # Calculate the end X position for the line

        self.set_line_width(0.005)  # Set line thickness (thin line)
        self.set_draw_color(200, 200, 200)
        self.line(line_start_x, line_y, line_end_x + 120, line_y)  # Draw the horizontal line

        # Shift the text position to the right for "Total"
        self.set_x(self.l_margin + description_width + 10) 

        self.ln(2)


        self.set_font('Arial', 'B', 12)
        self.set_x(self.get_x() + 118) 
        self.cell(description_width, 6, 'Total', align='R')
        self.cell(amount_width, 6, f'Rs. {self.TOTAL_AMOUNT}', ln=True, align='R')

        # Continue with the Total Summary section after this



        self.set_draw_color(0, 0, 0)

        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING
        #TAX TING

        # Define column widths
        left_col_width = 70
        right_col_width = 120

        # Add section title with border and styling
        self.set_x(self.l_margin) 
        self.set_font('Arial', '', 8)
        self.set_fill_color(0, 0, 0)  # Black background for the title
        self.set_text_color(0, 0, 0)  # White text color for contrast
        self.cell(190, 5, f'Total amount (in words): INR {self.format_inr(self.TOTAL_AMOUNT)}.', border='LTRB', align='L', fill=False)
        self.set_text_color(0, 0, 0)  # Reset text color to black
        self.set_font('Arial', '', 8)
        self.ln(2)  # Adding a blank row for separation

 
        self.add_note_section(left_col_width, right_col_width)

        self.TOTAL_QUANTITY=0
        self.TOTAL_AMOUNT=0
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
        # TAX SECTION
    def add_note_section(self, left_col_width, right_col_width):
        # Set the font for the note section
        self.set_font('Arial', '', 8)
        
        # Define the notes content
        notes = [
            "1.1. Please Visit Authorized Service Center For Technical Issues.",
            "2. Used/Refurbished/Pre-Owned Products Billed Under GST Margin Scheme &",
            "is Inclusive of Tax Amount, CGST Rule 32(5), 2017.",
            "3. Goods Once Sold Cannot be Exchanged or Taken Back.",
            "4. No warranty for used Products.",
            "5. Checking Warranty Valid For 2 Days From The Date of Purchase."
        ]
        
        # Calculate the starting Y position dynamically
        self.set_y(self.get_y() + 10)  # Adjust as needed
        
        # Define column widths
        self.set_fill_color(255, 255, 255)  # Light gray background for the note section
        
        # Add note section title
        self.set_font('Arial', 'B', 8)
        self.cell(190, 5, 'Notes:', border='LTRB', align='L', fill=True)
        self.ln(5)  # Add space after title

        # Add each note
        self.set_font('Arial', '', 8)
        for note in notes:
            self.multi_cell(190, 6, note, border='L', fill=False)
            self.ln(1)  # Add a small line break after each note
    def add_footer(self):
        self.set_y(-44)
        self.set_text_color(128, 128, 128)  # Darker gray color
        self.set_font('Arial', 'I', 8)
        self.cell(0, 6, 'GALAXY SMART POINT', 0, 1, 'R')
        #ADD SOME SPACE or add light greay color  
        self.ln(7)
        self.set_font('Arial', 'I', 7)
        self.cell(0, 6, 'Authorized Signatory', 0, 1, 'R')


    def add_main_border(self):
        self.set_line_width(0.4)  # Adjust thickness (0.5 for thin border)# Draw the border rectangle
        self.rect(10, 10, 190, self.get_y() - 72, 'D')
    def add_watermark(self, title):
        # Set up the watermark text properties
        self.set_font('Arial', 'B', 69)  # Bold, even larger font size for watermark
        self.set_text_color(240, 240, 240)  # Darker gray color for watermark# Calculate page width and height
        page_width = self.w
        page_height = self.h

        # Set angle for diagonal watermark
        self.rotate(45, x=page_width / 2, y=page_height / 2)

        # Add watermark text
        self.set_xy(page_width / 4, page_height / 2)  # Adjust positioning to ensure centered appearance
        self.cell(0, -27, title, 0, 0, 'C')

        # Reset rotation
        self.rotate(0)

        # Reset text color
        self.set_text_color(0, 0, 0)

def ensure_invoices_folder(base_path, folder_name='INVOICES'):
    invoices_path = os.path.join(base_path, folder_name)
    
    try:
        # Check if the folder exists
        if not os.path.exists(invoices_path):
            # Create the folder if it does not exist
            os.makedirs(invoices_path)
            print(f"✅ Created folder: {invoices_path}")
        else:
            print(f"✅ Folder already exists: {invoices_path}")

    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        raise
    except OSError as e:
        print(f"❌ OS error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

    return invoices_path

def generatePDF(invoice_details={}):
    # print(invoice_details)
    pdf = PDF(invoice_details["invoice_details"])
    pdf.add_page()
    pdf.add_invoice_details(invoice_details)
    pdf.add_totals()
    pdf.add_footer()
    pdf.add_main_border()
    # pdf.add_watermark(title="SWIPE")
    pdf_filename = f'{invoice_details["invoice_details"]["invoice_id"]}.pdf'
    pdf_path = os.path.join(base_path + '/INVOICES', pdf_filename)
    pdf.output(pdf_path)
    print(f'PDF saved to: {pdf_path}')
ensure_invoices_folder(base_path,"INVOICES")