
public class BoidKappa {  
  private static final float boidScale = 1000;
  private static final float seperationFactor = 1;
  private static final float alignFactor = 1;
  private static final float cohesionFactor = 1;
  public PVector pos;
  public PVector dir;
  public int count;
  public float size;
  private PImage img; // refactor to image hash
  private String url;

  public BoidKappa(String url, int count, int totalCount) {
    // init basic values
    img = loadMaskImage(url);// TODO: refactor to use preloaded image hash?
    this.count = count;
    this.url = url;
    // give it directional info
    setSize(totalCount);
    pos = new PVector(random(size/2+1, width-size/2-1), random(size/2+1, height-size/2-1));
    float randSpeed = random(1.0, 3.0);
    dir = new PVector(random(-randSpeed, randSpeed), random(-randSpeed, randSpeed));
  }

  public void drawSelf() {
    image(img, pos.x, pos.y, size, size);
  }

  private PImage loadMaskImage(String url) {
    PImage res = loadImage(url, "png");
    color c = res.get(0, 0);
    // if image is not transparent already
    if (alpha(c) != 0.0) {
      res = maskImage(res, c);
    }
    return res;
  }
  
  private PImage maskImage(PImage img, color c) {
    // work from outside in on all sides of image to set sequential 
    // pixels of color c to have alpha value of 0
    color trans_c = c & 0x00FFFFFF;
    img.loadPixels();
    img.format = ALPHA;
    for (int x=0; x<img.width; x++) {
      // look from top down
      for (int y=0; y<img.height; y++) {
        // check if pixel matches border color
        if (img.pixels[y*img.width + x] == c) {
          img.pixels[y*img.width + x] = trans_c;
        }
        // if not border stop looking since sequence is over
        else {
          break;
        }
      }
      // bottom up
      for (int y=img.height-1; y>=0; y--) {
        if (img.pixels[y*img.width + x] == c) {
          img.pixels[y*img.width + x] = trans_c;
        }
        else {
          break;
        }
      }

      img.updatePixels();
    }
    return img;
  }

  private void setSize(int totalCount) {
    this.size = ((float)count/(float)totalCount) * boidScale;
  }

  private void move(HashMap<String, BoidKappa> neighbors) {
    // steer boid through three steps    
    // reverse direction vector if boid will pass wall
    PVector future = new PVector(pos.x, pos.y);
    future.add(dir);
    if (future.x - size/2 < 0 || future.x + size/2 > width) {
      dir.x *= -1.0;
    }
    if (future.y - size/2 < 0 || future.y + size/2 > height) {
      dir.y *= -1.0;
    }

    // add updated direction vector to position
    pos.add(dir);
  }
}