
public class BoidKappa {  
  private static final float boidScale = 2000;
  private static final float seperationFactor = 1;
  private static final float alignFactor = 1;
  private static final float cohesionFactor = 1;
  public PVector pos;
  public PVector dir;
  public int count;
  public float size;
  private PImage img;
  private String url;

  public BoidKappa(String url, int count, int totalCount) {
    // Init basic values
    PImage loaded = loadImage(url, "png");
    img = ImageMask.resizeAndAlphaMaskImage(loaded);
    this.count = count;
    this.url = url;
    // Give it directional info
    setSize(totalCount);
    pos = new PVector(random(size/2+1, width-size/2-1), random(size/2+1, height-size/2-1));
    float randSpeed = random(1.0, 3.0);
    dir = new PVector(random(-randSpeed, randSpeed), random(-randSpeed, randSpeed));
  }

  public void drawSelf() {
    image(img, pos.x, pos.y, size, size);
  }

  private void setSize(int totalCount) {
    this.size = ((float)count/(float)totalCount) * boidScale;
  }

  private void move(HashMap<String, BoidKappa> neighbors) {
    // TODO: Flocking
        // Move back if past wall
    if (pos.x > width) {
      pos.x = width;
    } else if (pos.x < 0) {
      pos.x = 0;
    }
    if (pos.y > height) {
      pos.y = height;
    } else if (pos.y < 0) {
      pos.y = 0;
    }
    // Reverse direction vector if boid will pass wall
    PVector future = new PVector(pos.x, pos.y);
    future.add(dir);
    if (future.x - size/2 < 0 || future.x + size/2 > width) {
      dir.x *= -1.0;
    }
    if (future.y - size/2 < 0 || future.y + size/2 > height) {
      dir.y *= -1.0;
    }

    // Add updated direction vector to position
    pos.add(dir);
  }
}