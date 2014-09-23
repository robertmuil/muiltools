CLASSPATH=".:./lib/librxtxSerial.so:./lib/RXTXcomm.jar"

nulltest.class: nulltest.java
	javac -extdirs lib nulltest.java

clean:
	rm nulltest.class

run:
	java -cp ${CLASSPATH} nulltest


