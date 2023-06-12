# Force-Sensitive-Resistor
This Python Program uses a number of user defined functions, a callback function, if-else statements, and a for loop to calculate the force in grams applied by the user to a force sensitive resistor. The Force sensitive resistor is connected to a Raspberry Pi through a bread board in series with a 10000 ohm resistor and the x,y values (Force applied in grams vs ohms in resistance) are known for four points across three ranges: Range 1: 6000 - 30000 ohms, Range 2: 1000 - 6000 ohms, and Range 3: 150 - 1000 ohms. Using this information a linear line equations can be calculated and used to approximate any force applied to the force sensitive resistor so long as the resistance due to the force sensitive resistor is within the range 150 - 30000 ohms. Other hardware componets used in this project was a button that was pressed to initiate the reading of 25 samples of data from recored using an MPC 3008 ADC. 
