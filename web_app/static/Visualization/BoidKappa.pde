final float scale = 2.0; 
class BoidKappa {
  
  public PVector pos;
  public PVector dir;
  public int count;
  public float size;
  private PImage img; // refactor to image hash
  private String url;
  
  public BoidKappa(String url, int count) {
    // init basic values
    img = loadImage(url, "png"); // TODO: refactor to use preloaded image hash?
    this.count = count;
    this.url = url;
    // give it directional info
    pos = new PVector(random(0, width-size), random(0, height-size));
    float randSpeed = random(1.0, 3.0);
    dir = new PVector(random(-randSpeed, randSpeed), random(-randSpeed, randSpeed));
  }
  
  public void drawSelf() {
    image(img, pos.x, pos.y, size, size);
  }
  
  private void setSize(int totalCount, float adjust) {
    this.size = ((float)count/(float)totalCount) / adjust;
    println(this.size);
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