from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from http import HTTPStatus
import uvicorn
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to the served directory")
parser.add_argument("--port", default=443, type=int)
parser.add_argument("--log-level", default="INFO")
args = parser.parse_args()

app = FastAPI()


@app.api_route("{file_path:path}")
async def serve(request: Request, file_path: str):
    if "/../" in file_path or file_path.endswith("/.."):
        return Response("Don't go down.", status_code=HTTPStatus.FORBIDDEN)
    file_path = os.path.join(args.path, file_path[1:])
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
                pass
    elif os.path.isfile(file_path):
        return FileResponse(file_path)
    return Response("Page not found.", status_code=HTTPStatus.NOT_FOUND)


uvicorn.run(app, port=args.port, log_level=args.log_level.lower())
