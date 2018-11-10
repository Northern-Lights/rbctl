# rbctl

Coming soon...

## Installation

Copy (or symbolically link) this directory to `$USER/.local/share/rhythmbox/plugins`.  Next time you open Rhythmbox, __rbctl__ should show up in the list of plugins.

Note that the gRPC and protobuf output has already been generated and is ready to use out-of-the-box.

## Development

A Dockerfile has been provided to assist with generating the gRPC and protobuf output.  Of course, you can generate the Python code yourself if you have an environment set up to do so.

To build the Docker image, run this in this directory:

```docker
docker build -t rbctl .
```

To generate the gRPC and protobuf code, run this in this directory:

```
docker run -v $PWD:/build:Z --rm rbctl
```

Now you are set to do your own Python development.  See the Rhythmbox plugin development documentation for further reference.
