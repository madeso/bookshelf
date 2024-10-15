import argparse
import os
import glob
import subprocess
import typing
import re


def export_pdf_pages_to_png_using_gimp(filename: str, dir: str, extension: str):
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



def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def extend(dir: str, extension: str):
    parent_folder = os.path.dirname(dir)
    md_files = glob.glob(parent_folder + '/*.md', recursive=False)
    if len(md_files) != 1:
        print(f"Expected one single markdown in {parent_folder} but found {len(md_files)}")
        return
    images = natural_sort(glob.glob(dir + '/*.' + extension, recursive=False))
    path = md_files[0]
    print(f"Extending {path} with {len(images)} images")

    lines = []
    with open(path, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    it = [i for i, line in enumerate(lines) if line.startswith("+++")]
    index = it[1] if len(it) > 1 else None

    if index is None:
        print("No frontmatter found in markdown")
        return
    
    image_lines = []
    for i, image_full_path in enumerate(images):
        reltive_path = os.path.relpath(image_full_path, parent_folder).replace('\\', '/')
        img_name = os.path.basename(image_full_path)
        image_lines.append(f"![{img_name}]({reltive_path})")
        if (i+1) % 5 == 0:
            image_lines.append("")
    lines = lines[:index + 1] + image_lines + lines[index + 1:]

    with open(path, "w") as f:
        f.write("\n".join(lines))

    print("Markdown extended")


def export_images_from_pdf(arg: str, extension: str, force: bool, only: typing.Optional[typing.List[str]], extend_md: bool):
    # get directory of the file
    filename = os.path.abspath(arg)
    dir = os.path.dirname(filename)
    dirname = os.path.basename(dir)

    if only is not None:
        if not any(dirname == d for d in only):
            print(f"Skipping {filename} as {dirname} is not in the allowed directories")
            return
        
    # check if the file already exists
    page_file = os.path.join(dir, 'page-1.' + extension)
    if os.path.isfile(page_file) and not force:
        print(f"Skipping {filename} as {page_file} already exists")
        return

    print(f"Exporting {filename} to {dir} as {extension}")
    export_pdf_pages_to_png_using_gimp(filename, dir, extension)
    if extend_md:
        extend(dir, extension)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", help="The name of the file or directories to glob to create images for", nargs='+')
    parser.add_argument("--png", help="Save as png instead of jpg", action='store_true')
    parser.add_argument("--force", help="If files already exists, force pdf creation anyway", action='store_true')
    parser.add_argument("--only-in", help="only create if the pdf is in one of theese folders", nargs='*')
    parser.add_argument("--dont-extend-md", help="If there is a markdown in the parent folder, don't add image references", action='store_true')
    args = parser.parse_args()

    force = args.force
    only = args.only_in
    extend = not args.dont_extend_md

    extension = "png" if args.png else "jpg"

    for filename in args.filenames:
        if os.path.isfile(filename):
            export_images_from_pdf(filename, extension, force, only, extend)
        elif os.path.isdir(filename):
            files = glob.glob(filename + '/**/*.pdf', recursive=True)
            for file in files:
                export_images_from_pdf(file, extension, force, only, extend)

if __name__ == "__main__":
    main()
