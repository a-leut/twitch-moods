final float scale = 10.0; 

class BoidKappa {
  PVector pos;
  PVector dir;
  PImage img;
  String url;
  int count;
  float size;
  
  BoidKappa(String url, int count) {
    img = loadImage(url, "png");
    this.count = count;
    this.url = url;
    size = count * scale;
    // make it move
    pos = new PVector(random(0, width-size), random(0, height-size));
    float randSpeed = random(1.0, 3.0);
    dir = new PVector(random(-randSpeed, randSpeed), random(-randSpeed, randSpeed));
  }
  
  void move() {
    // reverse direction vector if boid will pass wall
    PVector future = new PVector(pos.x, pos.y);
    future.add(dir);
    /* For circles
    if (future.x - (size/2) < 0 || future.x + (size/2) > width) {
      dir.x *= -1.0;
    }
    if (future.y - (size/2) < 0 || future.y + (size/2) > height) {
      dir.y *= -1.0;
    } */
    if (future.x < 0 || future.x + size > width) {
      dir.x *= -1.0;
    }
    if (future.y < 0 || future.y + size > height) {
      dir.y *= -1.0;
    }
    // add updated direction vector to position
    pos.add(dir);
  }
  
  void updateCount(int count) {
    if (this.count != count) {
      this.count = count;
      this.size = count * scale;
    }
  }
  
  void drawSelf() {
    //ellipse(pos.x, pos.y, size, size);
    image(img, pos.x, pos.y, size, size);
  }
}