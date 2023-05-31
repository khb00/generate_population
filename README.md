# generate_population

This project includes python code which generates a population of people with attributes gender, birth year, death year, fertility and parents. There is a chance they will get married every year and if they are married they is a chance they will have a child. This population is simulated over a number of years and data about the population is stored. The data is used to plot graphs using matplotlib. The example graphs which are printed include:

Total live population versus deceased population.
Total of unmarried men versus unmarried women.
Fertility across the years.
Ratio of unmarried men to unmarried women over time.

In future, I would like to improve the efficiency of the python code, as it takes a long time to run when the total population becomes too large. Therefore, I have been testing this code with theses parameters:

 - TOTAL_YEARS = 100 # Years simulation will run.
 - GRADUATE_AGE = 16 # Age from which person can marry.
 - SAMPLE_SIZE = 80 # Size of intial sample.
 - FERTILITY_THRESHOLD = 250 # Higher threshold decreses liklihood of pregrancy.

Increasing these parameters means that the simulation takes a long time to complete.

Another furture implemention would be to change to algorithm for lifespan of a person as it is not accurate to life.
