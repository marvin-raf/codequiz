docker run -it --memory 4m --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 python  