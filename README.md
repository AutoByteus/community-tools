# Autobyteus Community Tools

Autobyteus Community Tools is a library that extends the functionality of the core Autobyteus library.


## Dependencies

- Python 3.7+
- Autobyteus (core library)
- Playwright
- MongoDB

## Installation

1. Ensure you have Python 3.7 or higher installed.

2. Install the Autobyteus core library (refer to its documentation for installation instructions).

3. Clone this repository:
   ```
   git clone https://github.com/your-repo/autobyteus-community-tools.git
   ```

4. Navigate to the project directory:
   ```
   cd autobyteus-community-tools
   ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Build the library:
   ```
   python setup.py sdist bdist_wheel
   ```
   This command creates both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.

7. Install the library:
   ```
   pip install dist/autobyteus_community_tools-*.tar.gz
   ```
   Or, if you prefer to install the wheel:
   ```
   pip install dist/autobyteus_community_tools-*.whl
   ```

## Usage

Here's a basic example of how to use the WeiboPoster:

```python
from autobyteus_community_tools.social_media_poster.weibo.weibo_poster import WeiboPoster

async def post_movie_review():
    poster = WeiboPoster("your_weibo_account")
    result = await poster.execute(
        movie_title="Inception",
        content="A mind-bending thriller that keeps you guessing until the end.",
        image_path="/path/to/movie/poster.jpg"
    )
    print(result)

# Run the async function
import asyncio
asyncio.run(post_movie_review())
```

For more detailed usage instructions, please refer to the documentation of each tool.

## Contributing

We welcome contributions! Please see our contributing guidelines for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
