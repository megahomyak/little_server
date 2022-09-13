from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from http import HTTPStatus
import uvicorn
import argparse
import os
import re

parser = argparse.ArgumentParser(description=(
    "A dead simple server for personal websites. "
    "Launch in a directory that needs to be served."
))
parser.add_argument("--port", default=443, type=int)
parser.add_argument("--log-level", default="INFO")
args = parser.parse_args()

MULTISLASH = re.compile(r"/{2,}")

app = FastAPI()


@app.api_route("{file_path:path}")
async def serve(request: Request, file_path: str):
    if "/../" in file_path or file_path.endswith("/.."):
        return Response("Don't go down.", status_code=HTTPStatus.FORBIDDEN)
    file_path = MULTISLASH.sub("/", file_path)
    file_path = file_path[1:]  # Removing the root slash
    if os.path.isdir(file_path):
        script_path = os.path.join(file_path, "page.py")
        if os.path.isfile(script_path):
            script_locals = {}
            with open(script_path, "r", encoding="utf-8") as script:
                exec(script.read(), {}, script_locals)
            try:
                return await (
                    script_locals[request.method.lower()](request, file_path)
                )
            except KeyError:
                return Response(
                    "Method not allowed.",
                    status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                )
    elif os.path.isfile(file_path):
        return FileResponse(file_path)
    return Response("Page not found.", status_code=HTTPStatus.NOT_FOUND)


uvicorn.run(app, port=args.port, log_level=args.log_level.lower())
