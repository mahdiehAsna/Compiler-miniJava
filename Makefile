ANTLR4=java -jar /usr/local/lib/antlr-4.7.2-complete.jar
GRUN=java org.antlr.v4.gui.TestRig

output/%.class: intermediateCode/%.j
	jasmin -d output $^

intermediateCode/%.j: sample/%.minijava
	python main.py $^

%: output/%.class
	cd output; java $@

antlr4python:
	$(ANTLR4) -Dlanguage=Python3 grammer/Minijava.g4

antlr4grun:
	$(ANTLR4) -Xexact-output-dir -o grun grammer/Minijava.g4
	cd grun; javac Minijava*.java

grunAmbig:
	cd grun; $(GRUN) Minijava goal -diagnostics < ../sample/simple3.minijava

clean:
	rm intermediateCode/*.j
	rm output/*.class