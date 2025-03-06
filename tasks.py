from robocorp.tasks import task
from robocorp import browser
from PIL import Image
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Tables import Tables
import time
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=50,
    )
    open_robot_order_website()
    close_annoying_modal()
    download_excel_file()
    get_orders()    
    fill_the_form()
    archive_receipts()
    
def open_robot_order_website():
    browser.goto('https://robotsparebinindustries.com/#/robot-order')
    

def close_annoying_modal():
    page = browser.page()
    page.click("text=OK")

    

def download_excel_file():
    http = HTTP()
    http.download(
        url="https://robotsparebinindustries.com/orders.csv", overwrite=True
    )

def get_orders():
    """Read data from csv and print the rows"""
    csv_file = Tables()
    orders = csv_file.read_table_from_csv("orders.csv", columns=["Order number","Head","Body","Legs","Address"
])
    for row in orders:
        yield row


def prev_submit():
    page = browser.page()
    time.sleep(0.5)
    page.click("css=#preview")
    time.sleep(0.5)
    page.click("css=#order")
    time.sleep(0.5)


def fill_the_form():
    orders = get_orders()
    page = browser.page()
    def select_head():
        if order["Head"] == '1':
            return 'Roll-a-thor head'
        elif order["Head"] == '2':
            return 'Peanut crusher head'
        elif order["Head"] == '3':
            return 'D.A.V.E head'
        elif order["Head"] == '4':
            return 'Andy Roid head'
        elif order["Head"] == '5':
            return 'Spanner mate head'
        elif order["Head"] == '6':
            return 'Drillbit 2000 head'
        
    def select_body():
        if order['Body'] == '1':
            return '#id-body-1'
        elif order['Body'] == '2':
            return '#id-body-2'
        elif order['Body'] == '3':
            return '#id-body-3'
        elif order['Body'] == '4':
            return '#id-body-4'
        elif order['Body'] == '5':
            return '#id-body-5'
        elif order['Body'] == '6':
            return '#id-body-6'
        
    for order in orders:
        page = browser.page()
        page.select_option('#head', select_head())
        page.click(select_body())
        page.fill("input[placeholder='Enter the part number for the legs']", order["Legs"])            
        page.fill("#address", str(order["Address"]))
        time.sleep(1)
        while True:  
            page.click("css=#order")
            next_order_button = page.query_selector("css=#order-another")
            if next_order_button:
                store_receipt_as_pdf(order["Order number"])
                screenshot = screenshot_robot(order["Order number"])
                embed_screenshot_to_receipt(screenshot, order["Order number"])
                page.click("css=#order-another")
                print("Order successful")
                close_annoying_modal()
                break  
            else:
                print("Order failed, trying again")
        
           
                    
        


            



def store_receipt_as_pdf(order_number):
    page = browser.page()
    order_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    path = f"output/{order_number}.pdf"
    pdf.html_to_pdf(order_html, path)
    return path
    


def screenshot_robot(order_number):
    page = browser.page()
    element = page.query_selector("#robot-preview-image")
    path = f"output/{order_number}.png"
    element.screenshot(path=path)
    image = Image.open(path)
    resized_image = image.resize((500, int(image.height * (500 / image.width))))
    resized_image.save(path)
    return path
    
def embed_screenshot_to_receipt(screenshot, order_number):
    pdf = PDF()
    list_of_files = [
        screenshot
    ]
    pdf.add_files_to_pdf(
        files=list_of_files,
        target_document=f"output/{order_number}.pdf",
        append=True
    )
    

def archive_receipts():
    lib = Archive()
    lib.archive_folder_with_zip('output/', 'merged.zip')