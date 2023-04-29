"""
Generate a population and simulate it over many years. Plot the population changes.
"""

import random
import matplotlib.pyplot as plt
import numpy as np

TOTAL_YEARS = 100 # Years simulation will run.
GRADUATE_AGE = 16 # Age from which person can marry.
SAMPLE_SIZE = 80 # Size of intial sample.
FERTILITY_THRESHOLD = 250 # Higher threshold decreses liklihood of pregrancy.
kid_pop = [] # List containing all people under graduate_age.
male_pop = [] # List containing all unmarried grown men.
female_pop = [] # List containing all unmarried grown women.
dead_pop = [] # List containing all deceased population.
couples = [] # List containing all couples.
pop_matrix = np.zeros( (7, TOTAL_YEARS) ) # Matrix which contains all population size data.


class Person():
    """
    Represents person with attributes like sex, birth year, death year, father, mother, fertility.

    Attributes:
    - sex (int): 0 for male, 1 for female
    - birth (int): the year the person was born
    - death (int): the year the person is expected to die, based on a random lifespan function
    - father (Person): the person's father
    - mother (Person): the person's mother
    - fertility (int): the person's fertility, based on the mother's fertility and random deviation
    """

    def __init__(self, sex, year, father, mother):
        # Male is 0, female is 1.
        self.sex = sex
        self.birth = year
        # The death year of the person is calculated based on the birth year
        # and a random number between 5 and 80.
        # In future, should add more complicated lifespan function.
        self.death = year + random.randint(5,80)
        # Parents of person.
        self.father = father
        self.mother = mother
        # If they have parents i.e. they are not in the inital sample.
        if isinstance(self.mother, Person):
            # Fertility is based on mothers fertility
            self.fertility = mother.fertility + random.randint(-2,2)
            # Max fertility is 40.
            if self.fertility > 40:
                self.fertility = 40
        else:
            self.fertility = random.randint(10,20)


def add_death(person, dead_pop):
    """
    Append the given person to the given list of deceased individuals.

    Args:
    - person (Person): the person who has died
    - dead_pop (list): the list of deceased individuals

    Returns:
    None
    """
    dead_pop.append(person)


def birth(couple, kid_pop, year, fertility_threshold):
    """
    Generate a child for a given couple, based on their fertility and other factors.

    Args:
    - couple (tuple): a tuple of two Person objects representing the parents
    - kid_pop (list): a list of Person objects representing the children
    - year (int): the current year
    - fertility_threshold (int): the minimum fertility level required for the mother to have a child

    Returns:
    None
    """
    #Fertility is based on parent's fertility, mother's age and a random number.
    combined_fertility = (couple[0].fertility * couple[1].fertility)
    mother_age = (year - couple[1].birth)
    fertility_level =  combined_fertility - mother_age + random.randint(0,50)
    if year - couple[1].birth < 45 and fertility_level > fertility_threshold:
    # Generate person and append to the kid list.
        person = Person(random.randint(0,1), year, couple[0], couple[1])
        kid_pop.append(person)


def check_graduate(kid_pop, dead_pop, male_pop, female_pop, year, graduate_age):
    """
    Check if any kids have died or come of age, and move them to the appropriate list.

    Parameters:
    kid_pop (list): list of Person objects representing kids.
    dead_pop (list): list of Person objects representing dead people.
    male_pop (list): list of Person objects representing single males.
    female_pop (list): list of Person objects representing single females.
    year (int): the current year of the simulation.
    graduate_age (int): the age at which a kid graduates to an adult.

    Returns:
    None
    """
    for kid in kid_pop:
        # Check if kid has died.
        if kid.death == year:
            add_death(kid, dead_pop)
            kid_pop.remove(dead_pop[-1])
        # Check if kid has come of age.
        elif (year - kid.birth) >= graduate_age:
            if kid.sex == 0:
            # If kid is male, append to male_pop.
                male_pop.append(kid)
            else:
            # If kid is female, append to female_pop.
                female_pop.append(kid)
            kid_pop.remove(kid)


def check_birth(couples, kid_pop, dead_pop, male_pop, female_pop, year, fertility_threshold):
    """
    Check whether any couples have died or given birth, and update the simulation accordingly.

    Parameters:
    couples (list): list of tuples representing couples.
    kid_pop (list): list of Person objects representing kids.
    dead_pop (list): list of Person objects representing dead people.
    male_pop (list): list of Person objects representing males.
    female_pop (list): list of Person objects representing females.
    year (int): the current year of the simulation.
    fertility_threshold (int): the minimum fertility level required for a couple to have a child.

    Returns:
    None
    """
    for couple in couples:
        # Check whether any husbands have died.
        if couple[0].death == year:
            couples.remove(couple)
            add_death(couple[0], dead_pop)
            # Check if husband and wife died.
            if couple[1].death == year:
                add_death(couple[1],dead_pop)
            # If just husband died.
            else:
                female_pop.append(couple[1])
        # Check if wife died.
        elif couple[1].death == year:
            couples.remove(couple)
            add_death(couple[1], dead_pop)
            male_pop.append(couple[0])
        # Else generate birth.
        else:
            birth(couple, kid_pop, year, fertility_threshold)


def check_relation(single, partner):
    """Check if two people are closely related.

    Args:
    single (Person): The first person to check for relation.
    partner (Person): The second person to check for relation.

    Returns:
    relation (bool): Whether the two people are closely related (True) or not (False).
    """
    relation = False
    # If they are siblings.
    if partner.father == single.father or partner.mother == single.mother:
        relation = True
    # If partner is the child of single.
    if partner is (single.father or single.mother):
        relation = True
    # If single is the child of partner.
    if single is (partner.father or partner.mother):
        relation = True
    return relation


def check_marriage(single_pop, partner_pop, dead_pop, year):
    """
    Generate marriages for the year.

    Args:
    single_pop (list): A list of unmarried people of one sex.
    partner_pop (list): A list of unmarried people of the opposite sex.
    dead_pop (list): A list of dead people.
    year (int): The current year.

    Returns:
    couples (list): A list of couples who got married this year.
    """
    for single in single_pop:
        # Check whether single is dead.
        if single.death == year:
            add_death(single, dead_pop)
            single_pop.remove(dead_pop[-1])
        # If there are non-zero unmarried people of the opposite  sex.
        elif len(partner_pop) > 0:
            # Choose a random person.
            partner = random.choice(partner_pop)
            # If single and partner are not closely related.
            if check_relation(single, partner) is False:
            # If the pair is less than 10 years apart in age.
                if abs(partner.birth - single.birth) < 10:
                    single_pop.remove(single)
                    partner_pop.remove(partner)
                    # Male is first in couple, female is second.
                    if single.sex == 0 :
                        couple = (single, partner)
                    else:
                        couple = (partner, single)
                    couples.append(couple)


def generate_gen_one(year, kid_pop, sample_size):
    """
    Generates the first generation of people and appends them to the kid_pop list.

    Args:
    year (int): the year in which the generation is generated
    kid_pop (list): list of Person objects representing the current population of kids
    sample_size (int): the number of individuals in the first generation to be generated

    Returns:
    None
    """
    for i in range(0,sample_size):
        sex = random.randint(0,1)
        # As person has no parents use i instead.
        # Each i has to be unique otherwise each person will be related.
        person = Person(sex,year,i,i)
        kid_pop.append(person)


def generate_year(year, population, graduate_age, fertility_threshold):
    """
    Simulates one year of population growth and updates the population data in the pop_matrix.

    Args:
    year (int): the year being simulated
    population (tuple): a tuple containing the following lists:
        kid_pop (list): list of Person objects containing the population of kids
        male_pop (list): list of Person objects containing the population of single males
        female_pop (list): list of Person objects containing the population of single females
        dead_pop (list): list of Person objects containing the people who have died
        couples (list): list of tuples containing the population of couples
    graduate_age (int): the age at which kids graduate and become adults
    fertility_threshold (int): the minimum age at which individuals can give birth

    Returns:
    None
    """

    print("\nYear:", year)
    kid_pop, male_pop, female_pop, dead_pop, couples = population
    if len(kid_pop) > 0 :
    # If any kids have graduated or died move into appropriate lists.
        check_graduate(kid_pop, dead_pop, male_pop, female_pop, year, graduate_age)
    if len(couples) > 0:
    # Generate births for couples.
        check_birth(couples, kid_pop, dead_pop, male_pop, female_pop, year, fertility_threshold)
    if len(female_pop) > 0:
    # Generate couples with women as the single list.
        check_marriage(female_pop, male_pop, dead_pop, year)
    if len(male_pop) > 0:
    # Generate couples with women as the single list.
        check_marriage(male_pop, female_pop, dead_pop, year)
    #Calculate total live population.
    pop_live = len(kid_pop)+ len(male_pop) + len(female_pop) + len(couples)*2
    # Store information about that years population information in matrix.
    pop_matrix [0,year] = year
    pop_matrix [1,year] = pop_live
    pop_matrix [2,year] = len(kid_pop)
    pop_matrix [3,year] = len(male_pop)
    pop_matrix [4,year] = len(female_pop)
    pop_matrix [5,year] = len(dead_pop)
    pop_matrix [6,year] = len(couples)


# Run main code.
generate_gen_one(0, kid_pop, SAMPLE_SIZE) # Generate inital population.
population = (kid_pop, male_pop, female_pop, dead_pop, couples)
for current_year in range( 0,TOTAL_YEARS):
    # Calculate changes in population for that year.
    generate_year(current_year, population, GRADUATE_AGE, FERTILITY_THRESHOLD)


# Plot population informtaion.

figure, axis = plt.subplots(2, 2)
figure.tight_layout(pad=5.0)
figure.legend(prop={"size":16})

time = pop_matrix [0] # Year number.
total = pop_matrix [1] # Total live population.
kid = pop_matrix [2] # Number of children each year.
male = pop_matrix [3] # Number of unmarried men each year.
female = pop_matrix [4] # Number of unmarried women each year.
couple = pop_matrix [6] # Number of couples each year.
dead = pop_matrix [5] # Number of total deceased each year.

gender_ratio = np.divide(female,male)
fertility = np.divide(kid,couple)

# Plot total live population and deceased population each year.
axis[0,0].scatter(time, total, label = "Live Population", color='r')
axis[0,0].scatter(time, dead, label = "Deceased Population", color='g')
axis[0,0].legend()
axis[0,0].set_title("Total Live and Dead Population over Time.")
axis[0,0].set_ylabel("Total Population Size")
axis[0,0].set_xlabel("Year")

# Number of unmarried women versus unmarried men.
axis[0,1].scatter(male, female)
axis[0,1].set_title("Total of Unmarried Men against Total of Unmarried Women.")
axis[0,1].set_ylabel("Population Size")
axis[0,1].set_xlabel("Year")

# Number of children per couple to give rough estimate of fertility.
axis[1,0].scatter(time, fertility)
axis[1,0].set_title("Feriltity over Time.")
axis[1,0].set_ylabel("Total Children per Couple")
axis[1,0].set_xlabel("Year")

# Number of unmarried women for one unmarried man over time.
axis[1,1].scatter(time, gender_ratio)
axis[1,1].set_title("Ratio of Unmarried Men to Unmarried Women over Time.")
axis[1,1].set_ylabel("Unmarried Women per Unmarried Man")
axis[1,1].set_xlabel("Year")
