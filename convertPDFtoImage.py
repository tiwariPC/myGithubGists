import os
from pdf2image import convert_from_path

# Set the directory containing the PDF files
pdf_dir = "/Users/ptiwari/cernbox/www/bbDM/fit-results-12042023-combinedEMu/pullsNimpacts2018"

# Set the directory to save the extracted images
output_dir = "/Users/ptiwari/cernbox/www/bbDM/fit-results-12042023-combinedEMu/pullsNimpacts2018"

# Set the image format (e.g. JPEG, PNG)
image_format = "PNG"

# Set the DPI for image extraction
dpi = 300

# Loop through all the PDF files in the directory
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        # Extract the images from the PDF
        pages = convert_from_path(os.path.join(pdf_dir, pdf_file), dpi=dpi, use_cropbox=True)
        # Loop through each page and save the image with a numbered name based on the PDF file name
        if len(pages) == 1:
            # Save the image with a name based on the PDF file name
            output_file = os.path.splitext(pdf_file)[0] + "." + image_format.lower()
            output_path = os.path.join(output_dir, output_file)
            pages[0].save(output_path, format=image_format, dpi=(dpi, dpi), optimize=True, quality=100, subsampling=0, progressive=True, icc_profile=None)
        else:
            # Loop through each page and save the image with a numbered name based on the PDF file name
            for i, page in enumerate(pages):
                # Get the page size and calculate the aspect ratio
                page_width_px, page_height_px = page.size
                aspect_ratio = page_width_px / page_height_px
                
                # Calculate the desired image width and height based on the page size and aspect ratio
                image_width_px = int(min(page_width_px, page_height_px * aspect_ratio))
                image_height_px = int(min(page_height_px, page_width_px / aspect_ratio))
                
                # Resize the page to the desired size and center the image
                page = page.resize((image_width_px, image_height_px))
                x_offset = (page_width_px - image_width_px) // 2
                y_offset = (page_height_px - image_height_px) // 2
                page = page.crop((x_offset, y_offset, x_offset+image_width_px, y_offset+image_height_px))
                
                # Save the image with a numbered name based on the PDF file name
                output_file = os.path.splitext(pdf_file)[0] + "_{}.{}".format(i+1, image_format.lower())
                output_path = os.path.join(output_dir, output_file)
                page.save(output_path, format=image_format, dpi=(dpi, dpi), optimize=True, quality=100, subsampling=0, progressive=True, icc_profile=None)
