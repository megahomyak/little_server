from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
from http import HTTPStatus
import os
import runpy

app = FastAPI()

_current_directory = os.path.normpath(os.path.abspath(os.getcwd()))

@app.api_route("{file_path:path}")
async def _serve(request: Request, file_path: str):
    original_file_path = file_path
    if file_path.startswith("/"):
        file_path = "." + file_path
    file_path = os.path.normpath(os.path.abspath(file_path))
    if not file_path.startswith(_current_directory):
        return Response("Don't go outside of the directory of serving.", status_code=HTTPStatus.FORBIDDEN)
    if os.path.isdir(file_path):
        script_path = os.path.join(file_path, "page.py")
        if os.path.isfile(script_path):
            the_directory_path_is_valid = original_file_path.endswith("/") or original_file_path == ""
            if not the_directory_path_is_valid:
                return RedirectResponse(original_file_path + "/", status_code=HTTPStatus.PERMANENT_REDIRECT)
            script_globals = runpy.run_path(script_path)
            try:
                handler = script_globals[request.method.lower()]
            except KeyError:
                return Response(
                    "Method not allowed.",
                    status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                )
            else:
                return await handler(request, file_path)
    elif os.path.isfile(file_path):
        return FileResponse(file_path)
    return Response("Page not found.", status_code=HTTPStatus.NOT_FOUND)
