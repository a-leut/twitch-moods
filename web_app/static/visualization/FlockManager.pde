public class FlockManager {
  public HashMap<String, BoidKappa> boids;
  
  public FlockManager() {
    this.boids = new HashMap<String, BoidKappa>();
  }
  
  public FlockManager(HashMap<String, BoidKappa> boids) {
    this.boids = boids;
  }
  
  void updateBoid(String url, int count) {
    if (boids.containsKey(url)) {
      BoidKappa b = boids.get(url);
      b.count = count;
    }
    else {
      boids.put(url, new BoidKappa(url, count, getTotalCount())); 
    }
  }
  
  void manageBoids() {
    int totalCount = getTotalCount();
    for (BoidKappa boid : boids.values()) {
      boid.setSize(totalCount);
      boid.move(boids);
    }
  }
  
  void drawBoids() {
    for (BoidKappa boid : boids.values()) {
      boid.drawSelf();
    }
  }
  
  private int getTotalCount() {
    int total = 0;
    for (BoidKappa boid : boids.values()) {
      total += boid.count;
    }
    return total;
  }
}