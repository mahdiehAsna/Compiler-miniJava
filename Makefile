ANTLR4=java -jar /usr/local/lib/antlr-4.7.2-complete.jar
GRUN=java org.antlr.v4.gui.TestRig

antlr4python:
	$(ANTLR4) -Dlanguage=Python3 -visitor grammer/Minijava.g4

antlr4grun:
	$(ANTLR4) -Xexact-output-dir -o grun grammer/Minijava.g4
	cd grun; javac Minijava*.java

grunAmbig:
	cd grun; $(GRUN) Minijava goal -diagnostics < ../sample/simple3.minijava

clean:
	rm intermediateCode/*.j || true
	rm output/*.class || true

%:
	python build.py sample/$@.minijava
	cd output; java $@