class Planet {

    private double gravity; /* units: (m/s/s) */
    private double ground;  /* units: m */
    private String name;

    /* constructors and accessors go here--you are to complete them */
     
    // default planet
    public Planet()
    {
    	gravity = 10.2;
    	ground = 0.0;
    	name = "Caprica";
    }
    
    // defined planet
    public Planet(double gr, double gd, String n)
    {
    	gravity = gr;
    	ground = gd;
    	name = n;
    }

    // returns the gravity of the planet
    public double getGravity()
    {
    	return gravity;
    }

    // returns the ground height of the planet
    public double getGround()
    {
    	return ground;
    }

    // returns the name of the planet
    public String getName()
    {
    	return name;
    }
}
