
void setup() {
  size(960, 640);
}

void draw() {
  background(255);
}

void updateBoid(String url, int count) {
  if (boids.containsKey(url)) {
    BoidKappa b = boids.get(url);
    b.count = count;
  }
  else {
    boids.put(url, new BoidKappa(url, count)); 
  }
}