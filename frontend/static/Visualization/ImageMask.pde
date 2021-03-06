static class ImageMask {
  public static PImage resizeAndAlphaMaskImage(PImage img) {
    color c = img.get(0, 0);
    // Alpha mask image if top left corner is not transparent
    if ((c & 0xFF000000) >> 24 != 0.0) {
      img = maskImage(img, c);
    }
    // Resize to frame if bigger than 28x28
    if (img.height > 28 || img.width > 28) {
      if (img.height > img.width) {
        img.resize(0, 28);
      } else {
        img.resize(28, 0);
      }
    }
    return img;
  }
  
  private static boolean setOpaquePixel(PImage img, int x, int y, color c, color trans_c) {
    // Returns true if given pixel can be made transparent
    if (img.pixels[y*img.width + x] == c) {
      img.pixels[y*img.width + x] = trans_c;
      return true;
    }
    // If not we've found the border and return false
    return false;
  }

  private static PImage maskImage(PImage img, color c) {
    // Work from outside in on all sides of image to set sequential 
    // pixels of color c to have alpha value of 0
    color trans_c = c & 0x00FFFFFF;
    img.loadPixels();
    img.format = ALPHA;
    for (int x=0; x<img.width; x++) {
      // Top down
      for (int y=0; y<img.height; y++) {
        if (!setOpaquePixel(img, x, y, c, trans_c))
          break;
      }
      // Bottom up
      for (int y=img.height-1; y>=0; y--) {
        if (!setOpaquePixel(img, x, y, c, trans_c))
          break;
      }
    }
    for (int y=0; y<img.height; y++) {
      // Left to right
      for (int x=0; x<img.width; x++) {
        if (!setOpaquePixel(img, x, y, c, trans_c))
          break;
      }
      // Right to left
      for (int x=img.width-1; x>=0; x--) {
        if (!setOpaquePixel(img, x, y, c, trans_c))
          break;
      }
    }
    img.updatePixels();
    return img;
  }
}