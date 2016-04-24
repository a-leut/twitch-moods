final float scale = 2.0; 
static HashMap<String, BoidKappa> boids = new HashMap<String, BoidKappa>();

class BoidKappa {
  
  public PVector pos;
  public PVector dir;
  public int count;
  public float size;
  private PImage img; // refactor to image hash
  private String url;
  
  public BoidKappa(String url, int count) {
    img = loadImage(url, "png");
    this.count = count;
    this.url = url;
    // make it move
    pos = new PVector(random(0, width-size), random(0, height-size));
    float randSpeed = random(1.0, 3.0);
    dir = new PVector(random(-randSpeed, randSpeed), random(-randSpeed, randSpeed));
  }
  
  public void update() {
    float totalSize = getTotalSize();
    for (BoidKappa boid : boids.values()) {
      boid.setSize();
      boid.move();
    }
    for (BoidKappa boid : boids.values()) {
      boid.drawSelf();
    }
  }
  
  private float getTotalSize() {
    float total = 0;
    for (BoidKappa boid : boids.values()) {
      total += boid.count;
    }
    return total;
  }
  
  public void drawSelf() {
    image(img, pos.x, pos.y, size, size);
  }
  
  private void setSize() {
    float newSize = scale * count;
    this.size = newSize;
  }
  
  private void move() {
    // reverse direction vector if boid will pass wall
    PVector future = new PVector(pos.x, pos.y);
    future.add(dir);
    if (future.x < 0 || future.x + size > width) {
      dir.x *= -1.0;
    }
    if (future.y < 0 || future.y + size > height) {
      dir.y *= -1.0;
    }
    // add updated direction vector to position
    pos.add(dir);
  }
}