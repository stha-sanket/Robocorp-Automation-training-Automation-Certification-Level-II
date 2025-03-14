# Robot Order Automation

## Description

This Robot Framework script automates the process of ordering robots from the RobotSpareBin Industries Inc. website. It performs the following actions:

1.  Opens the Robot Order website.
2.  Downloads the order data from a CSV file.
3.  Iterates through each order, filling out the order form.
4.  Saves the order receipt as a PDF file.
5.  Takes a screenshot of the ordered robot.
6.  Embeds the screenshot into the PDF receipt.
7.  Creates a ZIP archive of all the generated receipts and images.

## Prerequisites

*   **Python 3.7+**
*   **Robocorp Framework**: `pip install robocorp-framework`
*   **Required Libraries**:
    *   `rpaframework`
    *   `rpaframework-browser`
    *   `rpaframework-pdf`
    *   `rpaframework-tables`
    *   `rpaframework-http`
    *   `rpaframework-archive`
    *   `Pillow` (PIL)
*   Install these libraries using `pip install rpaframework rpaframework-browser rpaframework-pdf rpaframework-tables rpaframework-http rpaframework-archive Pillow`

## Setup and Installation

1.  **Install Robocorp Framework:**
    ```bash
    pip install robocorp-framework
    ```

2.  **Install Required Libraries:**
    ```bash
    pip install rpaframework rpaframework-browser rpaframework-pdf rpaframework-tables rpaframework-http rpaframework-archive Pillow
    ```

## Usage

1.  **Run the Robot:**

    Navigate to the directory containing the robot script (`tasks.py`) and run:

    ```bash
    rcc task run
    ```

    This command will execute the `order_robots_from_RobotSpareBin` task.

## Task Breakdown

*   `order_robots_from_RobotSpareBin()`: The main task function that orchestrates the entire robot ordering process.
*   `open_robot_order_website()`: Opens the RobotSpareBin Industries Inc. website.
*   `close_annoying_modal()`: Closes the initial modal on the website.
*   `download_excel_file()`: Downloads the CSV file containing the robot order data.
*   `get_orders()`: Reads the CSV file using the `Tables` library and returns an iterable of order rows.
*   `fill_the_form()`:
    *   Iterates through each order in the CSV file.
    *   Selects the appropriate head and body options based on the order data.
    *   Fills in the legs and address fields.
    *   Submits the order and handles potential failures by retrying.
    *   Calls helper functions to save the receipt, take a screenshot, and embed the screenshot.
*   `store_receipt_as_pdf()`: Saves the HTML receipt as a PDF file.
*   `screenshot_robot()`: Takes a screenshot of the ordered robot and resizes it.
*   `embed_screenshot_to_receipt()`: Embeds the robot screenshot into the PDF receipt.
*   `archive_receipts()`: Creates a ZIP archive containing all the generated PDF receipts and robot screenshots.

## Output

The script produces the following output files in the `output` directory:

*   `[Order Number].pdf`: The PDF receipt for each robot order, including the embedded screenshot.
*   `[Order Number].png`: The screenshot of the ordered robot.
*   `merged.zip`: A ZIP archive containing all the PDF receipts and screenshots.
