
output/%.class: intermediateCode/%.j
	jasmin -d output $^

intermediateCode/%.j: sample/%.minijava
	python main.py $^

%: output/%.class
	cd output; java $@

clean:
	rm intermediateCode/*.j
	rm output/*.class