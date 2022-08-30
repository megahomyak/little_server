from fastapi.responses import FileResponse, HTMLResponse, Response
from markdown import markdown
from textile import textile
from docutils.core import publish_parts
import os


def wrap_html(inner_html):
    return HTMLResponse(
        f"<!DOCTYPE html><html><body>{inner_html}</body></html>"
    )


def serve_meta(converter):
    def server_wrapper(file_path):
        async def server(request, script_directory):
            with open(
                os.path.join(script_directory, file_path),
                "r",
                encoding="utf-8"
            ) as file:
                return converter(file.read())
        return server
    return server_wrapper


serve_rst = serve_meta(lambda text: wrap_html(
    publish_parts(text, writer_name="html")["html_body"]
))
serve_markdown = serve_meta(lambda text: wrap_html(markdown(text)))
serve_textile = serve_meta(lambda text: wrap_html(textile(text)))
serve_html = serve_meta(lambda text: HTMLResponse(text))
serve_file = serve_meta(lambda text: FileResponse(text))
serve_text = serve_meta(lambda text: Response(text))
