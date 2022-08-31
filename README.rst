What?
-----

This dead simple web server for personal websites is very customizable, but provides nothing out of the box.

Why?
----

I wanted something simple yet extensible for my blog. My old project `blog`_ is good for blogs, but my plans changed and it won't be enough for me anymore.

.. _blog: https://github.com/megahomyak/blog

How?
----

1. Install the server from PyPI::

       pip install little_server

2. Create the base directory, which will be served

   This directory will be completely accessible to the users, so don't put anything unrelated to it. Everything that is out of that directory is safe though.

3. Fill the base directory

   | Every endpoint is a directory with a ``page.py`` file inside.
   | Functions from this file named after the HTTP method names will serve as handlers.
   | Every handler must take the request and the relative current directory path as arguments.
   | The current directory path is needed to perform relative file operations.

   **Hint:**

       Use ``little_server.utils`` to get some shortcut functions. All of them are correctly dealing with the current directory path, you don't need to consider it.

   ``page.py`` example::

       from little_server.utils import serve_text
       from fastapi.responses import Response
    
       get = serve_text("a.txt")  # This file is in the same directory as the script
    
    
       async def post(request, current_directory):
           return Response("You used POST.")

4. Run the server

   Invoke this program as a Python module with the ``--help`` flag (``python3 -m little_server --help``) to get the information about the arguments needed.

   You don't need to restart it if something changes inside the base directory, changed files will be accessible immediately (or after a few seconds, depends on implementation).
