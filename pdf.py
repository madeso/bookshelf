import argparse
import os
import glob
import subprocess


def export_pdf_pages_to_png_using_gimp(filename, dir, extension):
    gimp_console = "C:\\Program Files\\GIMP 2\\bin\\gimp-console-2.10.exe"

    base = os.path.join(dir, 'page-').replace("\\", "/")
    filename = filename.replace("\\", "/")
    
    # Create the GIMP script
    script = f"""
(let* 
	(
		(filename "{filename}")
		(output_pattern "{base}")
	)
	(let*
		(
            (options (vector 0 0))
			(image (car (file-pdf-load2 RUN-NONINTERACTIVE filename filename "" 0 options)))
			(num-pages (car (gimp-image-get-layers image)))
			(layers (cadr (gimp-image-get-layers image)))
		)
        (gimp-message (string-append "Number of pages: " (number->string num-pages)))
		(let loop ((i 0))
			(when (< i num-pages)
				(let*
					(
						(layer (vector-ref layers i))
						(output-file (string-append output_pattern (number->string (- num-pages i) ) ".{extension}"))
					)
					(gimp-file-save RUN-NONINTERACTIVE image layer output-file output-file)
				)
				(loop (+ i 1))
			)
		)
		(gimp-image-delete image)
	)
)
(gimp-quit 0)
    """
    
    # Write the script to a temporary file
    script_file = os.path.join(dir, "convert-pdf-to-png.scm")
    with open(script_file, "w") as f:
        f.write(script)
    
    # Run the GIMP command
    script_file = script_file.replace("\\", "/")
    command = [gimp_console, "-i", "-b", f'(load "{script_file}")']
    subprocess.run(command)
    
    os.remove(script_file)

def export_images_from_pdf(arg, extension):
    # get directory of the file
    filename = os.path.abspath(arg)
    dir = os.path.dirname(filename)

    print(f"Exporting {filename} to {dir} as {extension}")
    export_pdf_pages_to_png_using_gimp(filename, dir, extension)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", help="The name of the file or directories to glob to create images for", nargs='+')
    parser.add_argument("--png", help="Save as png instead of jpg", action='store_true')
    args = parser.parse_args()

    extension = "png" if args.png else "jpg"

    for filename in args.filenames:
        if os.path.isfile(filename):
            export_images_from_pdf(filename, extension)
        elif os.path.isdir(filename):
            files = glob.glob(filename + '/**/*.pdf', recursive=True)
            for file in files:
                export_images_from_pdf(file, extension)

if __name__ == "__main__":
    main()
