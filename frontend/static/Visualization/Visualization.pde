public FlockManager fm;
public ArrayList<String> updated;
public static final boolean ENV_JAVA = getEnv();

// Checks if processing is running from inside java
static boolean getEnv() {
  try {
    Integer.toString(1);
    return true;
  }
  catch (Exception e) {
    return false;
  }
}

void setup() {  
  size(960,640 );
  imageMode(CENTER);
  fm = new FlockManager();
  updated = new ArrayList<String>();
  
  if (ENV_JAVA) {
    for (int i =0; i<15; i++) {
      fm.updateBoid("https://static-cdn.jtvnw.net/emoticons/v1/" + Integer.toString(20 + i) + "/1.0", (int)random(20, 40));
    }
  }
}

void draw() {
  background(255);
  fm.manageBoids();
  fm.drawBoids();
}

void updateBoid(String url, int count) {
  fm.updateBoid(url, count);
  updated.add(url);
}

void boidsUpdated() {
  fm.removeDeadBoids(updated);
  updated = new ArrayList<String>();
}