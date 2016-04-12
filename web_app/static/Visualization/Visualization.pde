HashMap<String, BoidKappa> boids = new HashMap<String, BoidKappa>();

void setup() {
  size(960, 640);
    
  // Set fill-color to blue
  fill(0, 121, 184);
  stroke(255); 
  
  String[] pics = new String[] {
    "https://static-cdn.jtvnw.net/jtv_user_pictures/emoticon-47452-src-7c98e1049563b3f5-28x28.png",
    "https://static-cdn.jtvnw.net/jtv_user_pictures/emoticon-69873-src-3d0c384862440dbb-28x28.png",
    "https://static-cdn.jtvnw.net/jtv_user_pictures/emoticon-82088-src-c1f8a64e9a830915-28x28.png",
    "https://static-cdn.jtvnw.net/jtv_user_pictures/emoticon-32907-src-98f09ff6dedbe42d-28x28.png"
  };       
  
  for (String pic : pics) {
    boids.put(pic, new BoidKappa(pic, int(random(3, 10))));
  }
}

void draw() {
  // blit screen
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