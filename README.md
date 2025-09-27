# Static Site Generator

A Python-based static site generator that converts Markdown files to HTML using a template system. Built as part of the [Boot.dev](https://boot.dev) course on building static site generators.

## Features

- **Markdown to HTML conversion** with support for:
  - Headers (H1-H6)
  - Bold and italic text
  - Links and images
  - Code blocks and inline code
  - Lists (ordered and unordered)
  - Blockquotes
- **Recursive page generation** from nested directory structures
- **Template system** with placeholder replacement
- **Configurable base paths** for deployment flexibility
- **Static file copying** (CSS, images, etc.)
- **GitHub Pages deployment** ready

## Project Structure

```
StaticSiteGenerator/
├── src/                    # Source code
│   ├── main.py            # Main generator script
│   ├── generate_page.py   # Page generation functions
│   ├── extract_title.py   # Title extraction from markdown
│   ├── markdown_to_html_node.py  # Markdown parsing
│   └── test_*.py          # Unit tests
├── content/               # Markdown source files
│   ├── index.md          # Main page
│   ├── blog/             # Blog posts
│   └── contact/          # Contact page
├── static/               # Static assets (CSS, images)
├── docs/                 # Generated site (for GitHub Pages)
├── template.html         # HTML template
├── main.sh              # Local development server
├── build.sh             # Production build script
└── test.sh              # Run all tests
```

## Usage

### Local Development

1. **Generate site for local development:**
   ```bash
   python3 src/main.py
   ```

2. **Start local server:**
   ```bash
   bash main.sh
   ```
   Visit http://localhost:8888 to view the site.

### Production Deployment

1. **Build for GitHub Pages:**
   ```bash
   bash build.sh
   ```
   This builds the site with the correct base path for GitHub Pages (`/StaticSiteGenerator/`).

2. **Commit and push to GitHub:**
   ```bash
   git add docs/
   git commit -m "Deploy site"
   git push
   ```

### Testing

Run the complete test suite:
```bash
bash test.sh
```

## Configuration

### Base Path

The generator supports configurable base paths for different deployment environments:

- **Local development:** Uses `/` (default)
- **GitHub Pages:** Uses `/REPO_NAME/` (configured in `build.sh`)
- **Custom deployment:** Pass as command line argument:
  ```bash
  python3 src/main.py "/custom-path/"
  ```

### Template

The site uses `template.html` with two placeholders:
- `{{ Title }}` - Replaced with the H1 header from markdown
- `{{ Content }}` - Replaced with converted HTML content

### Content Structure

Add new pages by creating `.md` files in the `content/` directory. The generator:
- Maintains the directory structure in the output
- Converts `filename.md` to `filename.html`
- Extracts the page title from the first H1 header (`# Title`)

## GitHub Pages Deployment

This site is configured for GitHub Pages deployment:

1. **Repository settings:**
   - Go to Settings → Pages
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder

2. **Build and deploy:**
   ```bash
   bash build.sh
   git add docs/
   git commit -m "Deploy to GitHub Pages"
   git push
   ```

3. **Access your site:**
   - URL: `https://USERNAME.github.io/StaticSiteGenerator/`
   - Replace `USERNAME` with your GitHub username

## API Reference

### Main Functions

- `generate_page(from_path, template_path, dest_path, basepath="/")` - Generate single page
- `generate_pages_recursive(content_dir, template_path, dest_dir, basepath="/")` - Generate all pages recursively
- `extract_title(markdown)` - Extract H1 header from markdown content

### Command Line Interface

```bash
python3 src/main.py [basepath]
```

- `basepath` (optional): Base URL path for the site (default: "/")

## Development

### Adding New Content

1. Create a new `.md` file in `content/` or subdirectory
2. Start with an H1 header for the page title
3. Add your content in Markdown format
4. Run the generator to build the HTML

### Extending Functionality

The modular design makes it easy to extend:

- **Markdown parsing:** Modify `markdown_to_html_node.py`
- **Page generation:** Extend `generate_page.py`
- **Template system:** Update `template.html` or add new placeholders
- **Static assets:** Add files to `static/` directory

### Testing

The project includes comprehensive unit tests:
- 98 total tests covering all functionality
- Test files follow the pattern `test_*.py`
- Run individual test files: `python3 src/test_filename.py`

## License

This project is part of the Boot.dev curriculum. Feel free to use and modify for educational purposes.

## Acknowledgments

- Built following the [Boot.dev Static Site Generator course](https://www.boot.dev/courses/build-static-site-generator-python)
- Inspired by popular static site generators like Hugo and Jekyll
