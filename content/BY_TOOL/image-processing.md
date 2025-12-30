# Image Processing Tools

Common patterns for handling images in projects.

---

## Common Issues

### HEIC to JPEG Conversion (Linux)
**Date:** 2025-12-19
**Project:** oil_record_book_tool
**Context:** Processing iPhone photos on Linux servers

**Problem:**
iPhone photos are often HEIC format. Most Python/web tools expect JPEG/PNG.

**Solution (Linux/Ubuntu):**
```bash
# Install libheif tools
apt-get install libheif-examples

# Convert single file
heif-convert input.HEIC output.jpg

# In Python, use pillow-heif
pip install pillow-heif
```

```python
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Now Pillow can open HEIC directly
img = Image.open("photo.HEIC")
img.save("photo.jpg", "JPEG")
```

**Prevention:**
For web apps accepting image uploads, either:
1. Accept HEIC and convert server-side
2. Use `<input accept="image/jpeg,image/png">` to limit uploads
3. Convert client-side before upload using JavaScript libraries

---

*Last updated: 2025-12-19*
