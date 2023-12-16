import jinja2
import pdfkit
import yaml
import os
import pdf2image

TEMP_MAP = {
    0 : 'resume_template.html',
    1 : 'resume_template1.html',
    2 : 'resume_template2.html'
}

def generate_resume(yaml_file, template_number = 0, create_img = False):
    
    # Set the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Set up input paths for template and yaml
    yamlPath = os.path.join(script_directory, 'examples/inputYamls', yaml_file)
    template_path = os.path.join(script_directory)

    # Load data from YAML
    with open(yamlPath, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # Load Jinja2 templates
    template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMP_MAP[template_number])

    # Render HTML
    html_output = template.render(data)

    # Set up output locations
    outputName = 'output_' + yaml_file.split('.')[0] + '_resume'
    htmlResume = os.path.join(script_directory, 'examples/outputs/htmls', '{}.html'.format(outputName))
    pdfResume = os.path.join(script_directory, 'examples/outputs/pdfs', '{}.pdf'.format(outputName))

    # Save HTML (optional)
    with open(htmlResume, 'w') as output_file:
        output_file.write(html_output)

    # Convert HTML to PDF
    pdfkit.from_file(htmlResume, pdfResume)

    # Create pdf to image if create_img set to True
    if create_img:
        img_list = pdf2image.convert_from_path(pdfResume)
        for i in range(len(img_list)):
            # create a separate jpeg file for each page
            img_list[i].save(os.path.join(script_directory, 'examples/outputs/images', 'page_' + yaml_file.split('.')[0] + str(i) +'.jpg'), 'JPEG')

if __name__ == "__main__":
    generate_resume('input_data.yaml')