from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from http import HTTPStatus
import uvicorn
import argparse
import os
import runpy

parser = argparse.ArgumentParser(description=(
    "A dead simple server for personal websites. "
    "Launch in the directory that needs to be served."
))
parser.add_argument("--port", default=443, type=int)
parser.add_argument("--log-level", default="INFO")
args = parser.parse_args()

app = FastAPI()

current_directory = os.path.normpath(os.path.abspath(os.getcwd()))


@app.api_route("{file_path:path}")
async def serve(request: Request, file_path: str):
    if file_path.startswith("/"):
        file_path = "." + file_path
    file_path = os.path.normpath(os.path.abspath(file_path))
    if not file_path.startswith(current_directory):
        return Response("Don't go outside of the directory of serving.", status_code=HTTPStatus.FORBIDDEN)
    if os.path.isdir(file_path):
        script_path = os.path.join(file_path, "page.py")
        if os.path.isfile(script_path):
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


uvicorn.run(app, port=args.port, log_level=args.log_level.lower())
