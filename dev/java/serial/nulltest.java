// derived from SUN's examples in the javax.comm package
import java.io.*;
import java.util.*;
//import javax.comm.*; // for SUN's serial/parallel port libraries
import gnu.io.*; // for rxtxSerial library

public class nulltest implements Runnable, SerialPortEventListener {
	static CommPortIdentifier portId;
	static CommPortIdentifier saveportId;
	static Enumeration        portList;
	InputStream           inputStream;
	SerialPort           serialPort;
	Thread           readThread;
	FileOutputStream out; // declare a file output object
	PrintStream p; // declare a print stream object

	static String        messageString = "Hello, world!";
	static OutputStream      outputStream;
	static boolean        outputBufferEmptyFlag = false;
	static int numIterations = 2;
	static int delay = 5000;

	static int READBUFSZ = 1000;

	int numEvents = 0;
	int numBytesRead = 0;

	public static void main(String[] args) {
		boolean           portFound = false;
		String           defaultPort;

		
		// determine the name of the serial port on several operating systems
		String osname = System.getProperty("os.name","").toLowerCase();
		if ( osname.startsWith("windows") ) {
			// windows
			defaultPort = "COM1";
		} else if (osname.startsWith("linux")) {
			// linux
			defaultPort = "/dev/ttyUSB0";
		} else if ( osname.startsWith("mac") ) {
			// mac
			defaultPort = "????";
		} else {
			System.out.println("Sorry, your operating system is not supported");
			return;
		}

		if (args.length > 0) {
			defaultPort = args[0];
		} 

		System.out.println("Set default port to "+defaultPort);

		// parse ports and if the default port is found, initialized the reader
		portList = CommPortIdentifier.getPortIdentifiers();
		while (portList.hasMoreElements()) {
			portId = (CommPortIdentifier) portList.nextElement();
			if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) {
				if (portId.getName().equals(defaultPort)) {
					System.out.println("Found port: "+defaultPort);
					portFound = true;
					// init reader thread
					nulltest reader = new nulltest();
				} 
			} 

		} 
		if (!portFound) {
			System.out.println("port " + defaultPort + " not found.");
		} 
	} 

	public void initwritetoport() {
		// initwritetoport() assumes that the port has already been opened and
		//    initialized by "public nulltest()"

		try {
			// get the outputstream
			outputStream = serialPort.getOutputStream();
		} catch (IOException e) {}

		try {
			// activate the OUTPUT_BUFFER_EMPTY notifier
			//serialPort.notifyOnOutputEmpty(true);
		} catch (Exception e) {
			System.out.println("Error setting event notification");
			System.out.println(e.toString());
			System.exit(-1);
		}

	}

	public void writetoport() {
		System.out.println("Writing \""+messageString+"\" to "+serialPort.getName());
		try {
			// write string to serial port
			outputStream.write(messageString.getBytes());
		} catch (IOException e) {}
	}

	public nulltest() {
		// initalize serial port
		try {
			serialPort = (SerialPort) portId.open("SimpleReadApp", 2000);
		} catch (PortInUseException e) {}

		try {
			inputStream = serialPort.getInputStream();
		} catch (IOException e) {}

		try {
			serialPort.addEventListener(this);
		} catch (TooManyListenersException e) {}

		// activate the DATA_AVAILABLE notifier
		serialPort.notifyOnDataAvailable(true);

		try {
			// set port parameters
			serialPort.setSerialPortParams(115200, SerialPort.DATABITS_8, 
					SerialPort.STOPBITS_1, 
					SerialPort.PARITY_NONE);
		} catch (UnsupportedCommOperationException e) {}

		try {
			out = new FileOutputStream("output.log"); // Create a new file output stream connected to "myfile.txt"
			p = new PrintStream( out ); // Connect print stream to the output stream
			p.println ("File Begin");
		} catch (Exception e) {
			System.err.println ("Error writing to file");
		}

		// start the read thread
		readThread = new Thread(this);
		readThread.start();

	}

	public void run() {
		// first thing in the thread, we initialize the write operation
		initwritetoport();
		try {
			int ii = 0;
			while (ii++ < numIterations) {
				// write string to port, the serialEvent will read it
				//writetoport();
				System.out.println("...listening to serial port" + ii + "/"+numIterations+"...");
				System.out.println(" -> numEvents="+numEvents+"\tnumBytesRead="+numBytesRead);
				Thread.sleep(delay);
			}
		} catch (InterruptedException e) {}
		System.out.println("Program finished");
		p.close();
	} 

	public void serialEvent(SerialPortEvent event) {
		switch (event.getEventType()) {
			case SerialPortEvent.BI:
			case SerialPortEvent.OE:
			case SerialPortEvent.FE:
			case SerialPortEvent.PE:
			case SerialPortEvent.CD:
			case SerialPortEvent.CTS:
			case SerialPortEvent.DSR:
			case SerialPortEvent.RI:
			case SerialPortEvent.OUTPUT_BUFFER_EMPTY:
				System.out.println("Event: unknown event");
				break;
			case SerialPortEvent.DATA_AVAILABLE:
				// we get here if data has been received
				byte[] readBuffer = new byte[READBUFSZ];
				//System.out.println("Event: data available");
				numEvents++;
				try {
					int numBytes = -1;
					while (inputStream.available() > 0) {
						numBytes = inputStream.read(readBuffer, 0, inputStream.available());
						numBytesRead += numBytes;
						// print data
						//System.out.println(" -> read " + numBytes + " bytes");
						String result  = new String(readBuffer);
						//System.out.println("Read: "+result);
						p.println(numEvents+":"+numBytes+":"+result);
					} 
				} catch (IOException e) {}

				break;
		}
	} 

}
