HashMap<String, BoidKappa> boids = new HashMap<String, BoidKappa>();

void setup() {
  size(960, 640);
}

void draw() {
  background(255);  

  for (BoidKappa boid : boids.values()) {
    boid.move();
    boid.drawSelf();
  }
}

void updateBoid(String url, int count) {
  if (boids.containsKey(url)) {
    BoidKappa b = boids.get(url);
    b.updateCount(count);
  }
  else {
    boids.put(url, new BoidKappa(url, count));
  }
}