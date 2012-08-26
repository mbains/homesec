# Get the directory that this configuration file exists in
dir = File.dirname(__FILE__)

# Load the sencha-touch framework automatically.
# ../st/resources/themes/
load File.join(dir, '..', 'st', 'resources', 'themes')

# Compass configurations
sass_path = "sass"
css_path = File.join(dir, "css")

# Require any additional compass plugins here.
images_dir = File.join(dir, "images")
output_style = :compressed
#environment = :production
environment = :development

