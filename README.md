## Overview

This project is a take-home implementation for Seek's Traffic Counter test. It includes functionality to count and analyze traffic data.

## Setup

Make sure you have python and uv installed. For the development of this project, I used python 3.14 and [uv 0.9.7](https://docs.astral.sh/uv/#installation) (and make, which should be available on macOS/linux).

To install the required dependencies, run:

```bash
# Install uv via curl:
curl -LsSf https://astral.sh/uv/install.sh | sh

# runs uv sync to install dependencies
make install
```

## Running Tests

To run unit tests, use the following command:

```bash
make test
```

To run integration tests, use:

```bash
make test-integration
```
