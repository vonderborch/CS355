import java.io.*;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;

class Game {
	// should a transcript of all prints to the console be recorded in the debug file?
    private static final boolean debug = false;
    // what's the debug file?
    private static final String debugFile = "output.txt";
    // a no-burn
    private static final double noBurn = 0.0;
    // a full-burn
    private static final double fullBurn = 1.0;
    // base deltaTime
    private static final double deltaTime = 0.5;

    private static void play(Rocket rocket) throws RocketException /* needs throws clause */{
    	BufferedReader inputReader = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            /* read input and decide whether to burn or not */
        	double burn = noBurn;
        	try
        	{
        		boolean inputGood = false;
        		// keep getting input until either we get a new line or a b
        		while (inputGood == false)
        		{
	        		String inputString = inputReader.readLine();
	        		if (inputString.length() > 0)
	        		{
	            		char[] input = inputString.toCharArray();
	            		// a burn is wanted
	            		if (input[0] == 'b')
	            		{
	            			print("b ");
	            			burn = fullBurn;
	            			inputGood = true;
	            		}
	        		}
	        		// no burn is wanted
	        		else
	        			inputGood = true;
        		}
        	}
        	catch (IOException e) {
				e.printStackTrace();
        	}

            rocket.move(deltaTime, burn); // move rocket for 0.5 second at
            // full burn
            print(rocket.getHeightString());
        }

    }

    public static void main(String[] args) throws RocketException {
        /* create a planet with gravity 0.3 and surface at 0.0 */
        Planet pluto = new Planet(0.3, 0.0, "Pluto");
        /* create a rocket with engine strength 2.0, 20.0 units of fuel */
        Rocket rocket = new Rocket(2.0, 20.0, pluto);
        rocket.setHeight(50.0); // set the base height
        play(rocket); // play the game!
    }
    
    // prints something to the console and (potentially) the debug file
    public static void print(String temp)
    {
    	System.out.println(temp);
    	
    	// does the temp string need to be printed to a file?
    	if (debug)
    	{
    		try {
				PrintWriter output = new PrintWriter(new BufferedWriter(new FileWriter(debugFile,true)));
				output.println(temp);
				output.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
    	}
    }

} // end of Game class
