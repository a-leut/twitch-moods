
public class BoidKappa {  
  private static final float boidScale = 2000;
  private static final float seperationFactor = 1;
  private static final float alignFactor = 1;
  private static final float cohesionFactor = 1;
  private static final float r = 2;
  public PVector pos;
  public PVector dir;
  public int count;
  public float size;
  private PImage img;
  private String url;
  private Boolean steppedOut = false;

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
    dir.x += random(-0.05, 0.05);
    dir.y += random(-0.05, 0.05);

    pos.add(dir);
    borders();
  }
  private void borders() {
    if (pos.x < -r) pos.x = width+r;
    if (pos.y < -r) pos.y = height+r;
    if (pos.x > width+r) pos.x = -r;
    if (pos.y > height+r) pos.y = -r;
  }
}