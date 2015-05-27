import java.text.DecimalFormat;

class Rocket {
    static final RocketException crashed = new RocketException("Crashed and Burned");
    static final RocketException landed = new RocketException("Safely Landed");
    private double velocity = 0.0; // default to 0
    private double height = 50.0; // default to 50.0
    private double fuel = 0.0; // default to 0.0
    private double engineStrength = 0.0; // default to 0.0
    private Planet planet;
    private static final double safeVelocity = -1.0; // Land within this
                                                       // velocity
    
    // a defined rocket constructor
    public Rocket(double strength, double f, Planet plan)
    {
    	engineStrength = strength;
    	fuel = f;
    	planet = plan;
    }
    
    // set the height the rocket is at
    public void setHeight(double newH)
    {
    	height = newH;
    }
    
    // get the height the rocket is at
    public double getHeight()
    {
    	return height;
    }
    
    // get the velocity the rocket is at
    public double getVelocity()
    {
    	return velocity;
    }
    
    // get the safe velocity the rocket can land at
    public double getSafeVelocity()
    {
    	return safeVelocity;
    }
    
    // get the state string for the rocket
    public String getState()
    {
    	DecimalFormat format = new DecimalFormat("#0.0");
    	return "HEIGHT " + format.format(height) + " VELOCITY " + format.format(velocity) + " FUEL " + format.format(fuel);
    }

    // has the rocket reached the surface?
    private boolean reachedSurface() {
        /* true if rocket is at or below the planet's surface */
    	if (height > planet.getGround())
    		return false;
    	return true;
    }
    
    // has the rocket landed?
    private boolean landed()
    {
		if (velocity <= safeVelocity)
			return true;
    	return false;
    }
    
    // update the rocket to the next height
    private void nextHeight(double deltaTime) throws RocketException {
        height += (velocity * deltaTime);
        if (reachedSurface()) {
            if (landed()) {
            	Game.print("Crashed and burned!");
                throw crashed;
            } else {
            	Game.print("Landed safely!");
                throw landed;
            }
        }
    }
    
    // get the next fuel value
    private void nextFuel(double burnRate, double deltaTime)
    {
    	fuel -= nextFuelReduction(burnRate, deltaTime);
    }
    
    // get the next reduction in fuel
    private double nextFuelReduction(double burnRate, double deltaTime)
    {
    	return burnRate * deltaTime;
    }

    // get the next velocity
    private void nextVelocity(double burnRate, double deltaTime) {
        velocity += ((engineStrength * burnRate) - planet.getGravity())
                * deltaTime;
    }

    // move the rocket
    public void move(double dt, double burnRate) throws RocketException {
        /* note that dt is measured in seconds */
    	// check if the rocket has enough fuel for a full burn, and if not, get the correct burn amount we can do
        if (!reachedSurface()) {
        	double actualBurn = burnRate;
        	if (fuel < nextFuelReduction(actualBurn, dt))
        		actualBurn = fuel / burnRate;
        	
        	
            /* update the height, velocity and fuel */
        	nextVelocity(actualBurn, dt);
        	nextFuel(actualBurn, dt);
        	nextHeight(dt);
        }
    }

    // return the height string
    public String getHeightString() {
        double maxHeight = (height > 60.0) ? height : 60.0;
        double belowGround = planet.getGround() - 10.0;
        int size = (int) (maxHeight - belowGround) + 1;
        char[] buffer = new char[size];
        DecimalFormat df = new DecimalFormat(" ###.##");

        int groundPosition = (int) (planet.getGround() - belowGround);

        for (int i = 0; i < size; i++)
            buffer[i] = ' ';
        int adjustedPosition = (int) (height - belowGround);
        adjustedPosition = (adjustedPosition <= 0) ? 0 : adjustedPosition;
        /* prove here, using wp logic, that 0 <= adjustedPosition <= size-1 */
        buffer[groundPosition] = '|';
        buffer[adjustedPosition] = '*';
        return (new String(buffer) + " " + df.format(velocity));
    }

}
