public FlockManager fm;

void setup() {  
  size(960,640 );

  imageMode(CENTER);
  fm = new FlockManager();
  /*
  for (int i =0; i<15; i++) {
    fm.updateBoid("https://static-cdn.jtvnw.net/emoticons/v1/" + Integer.toString(20 + i) + "/1.0", (int)random(20, 40));
  }*/
}

void draw() {
  background(255);
  fm.manageBoids();
  fm.drawBoids();
}

void updateBoid(String url, int count) {
  fm.updateBoid(url, count);
}