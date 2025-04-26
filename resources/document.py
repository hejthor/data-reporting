import os
import pypandoc
import json
import pandas as pd

from interpret import interpret
# from convert_doc_to_pdf import convert_doc_to_pdf # this will help calculate TOC by opening Word

def document(document, output_path):
    if document.get('split'):

        # Get unique values
        uniques = set()
        for item in document['contents']:
            if item.get("table"):
                source = item["table"]
                delimiter = item["delimiter"]
                try:
                    df = pd.read_csv(source, delimiter=delimiter, engine="python", on_bad_lines="skip")
                    if document['split'] in df.columns:
                        uniques.update(df[document['split']].unique())
                except pd.errors.ParserError as e:
                    print(f"[PYTHON][document.py] Error parsing {source}: {e}")

        # Generate unique documents
        for unique_value in uniques:
            # Create unique output directory
            unique_output_path = os.path.join(output_path, str(unique_value))
            os.makedirs(unique_output_path, exist_ok=True)
            # Generate markdown for the unique value
            markdown = "\n".join([interpret(item, unique_output_path, document['split'], unique_value) for item in document['contents']])
            _convert_pandoc_json_to_docx(markdown, document, unique_output_path)

    else:
        
        markdown = "\n".join([interpret(item, output_path) for item in document['contents']])
        _convert_pandoc_json_to_docx(markdown, document, output_path)

def _convert_pandoc_json_to_docx(pandoc_json, json, output_path):
    output_file_extension = os.path.splitext(json["template"])[1][1:].lower()
    output_file = os.path.join(output_path, f"{json['title']}.{output_file_extension}")
    md_file = os.path.join(output_path, f"{json['title']}.md")
    try:
        # Prepend YAML metadata block
        author = f"{json.get('author', '')}`<w:p><w:r><w:br w:type='page'/></w:r></w:p>`{{=openxml}}"
        yaml_meta = f"---\ntitle: \"{json.get('title', '')}\"\nauthor: \"{author}\"\n"
        if 'toc' in json:
            yaml_meta += f"toc-title: \"{json.get('toc', '')}\"\n"
        yaml_meta += f"lang: \"{json.get('language', '')}\"\n---\n\n"
        if 'toc' in json:
            markdown_content = yaml_meta + '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n' + pandoc_json
        else:
            markdown_content = yaml_meta + pandoc_json
        # Save markdown to file
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        # Step 2: Convert Markdown to DOCX
        pypandoc.convert_text(
            markdown_content,
            to=output_file_extension,
            format="md",
            outputfile=output_file,
            extra_args=[
                f'--reference-doc={json["template"]}',
                '--standalone',
            ] + (["--table-of-contents"] if 'toc' in json else [])
        )
        print(f"[PYTHON][document.py] Converted JSON contents to {output_file}")
        print(f"[PYTHON][document.py] Saved Markdown to {md_file}")
    except Exception as e:
        print(f"[PYTHON][document.py] Error converting JSON contents to {output_file}: {str(e)}")