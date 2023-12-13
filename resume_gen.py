import jinja2
import pdfkit
import yaml
import os
import pdf2image

TEMP_MAP = {
    0 : 'resume_template.html',
    1 : 'sample_1.html',
    2 : 'sample_2.html'
}

def generate_resume(yaml_file, template_number = 0, create_img = False):
    # Load data from YAML
    with open(yaml_file, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_directory)

    # Load Jinja2 templates
    template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMP_MAP[template_number])

    # Render HTML
    html_output = template.render(data)

    # Save HTML (optional)
    with open('output_resume.html', 'w') as output_file:
        output_file.write(html_output)

    # Convert HTML to PDF
    pdfkit.from_file('output_resume.html', 'output_resume.pdf')

    # Create pdf to image if create_img set to True
    img_list = pdf2image.convert_from_path('output_resume.pdf')
    for i in range(len(img_list)):
        # create a separate jpeg file for each page
        img_list[i].save('page_'+ yaml_file + str(i) +'.jpg', 'JPEG')

if __name__ == "__main__":
    generate_resume('input_data.yaml', 0, True)