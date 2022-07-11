import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all','january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    which_city = ''
    while which_city.lower() not in CITY_DATA.keys():
        which_city = input('\nChoose city : Chicago, New York City, Washington (not case sensitive):\n')
        if which_city.lower() in CITY_DATA.keys():
            city = CITY_DATA[which_city.lower()]
        else:
            print('Invalid input. Not able to read which city')     

    # get user input for month (all, january, february, ... , june)
    which_month = ''
    while which_month.lower() not in MONTH_DATA:
        which_month = input('\nChoose month: January, February, March, April, May, June or all (not case sensitive):\n')
        if which_month.lower() in MONTH_DATA:
            month = which_month.lower()
        else:
            print('Invalid input. Not able to read which month')  


    # get user input for day of week (all, monday, tuesday, ... sunday)
    which_day = ''
    while which_day.lower() not in DAY_DATA:
        which_day = input('\nChoose day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all (not case sensitive):\n')
        if which_day.lower() in DAY_DATA:
            day = which_day.lower()
        else:
            print('Invalid input. Not able to read which day')  

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("the most common month of the week is: " + str(MONTH_DATA[df['month'].mode()[0]]))


    # display the most common day of week
    print("the most common month of the week is: " + df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most common start hour is: " + str(df['hour'].mode()[0]) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: " + df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is: " + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("The most common start and end station combination is: " + str((df['Start Station']+ " " + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is: " + str(df['Trip Duration'].sum()))

    # display mean travel time
    print("The total travel time is: " + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The count of user types is: " + str(df['User Type'].value_counts()))
    
    if city != 'washington.csv':
    # Display counts of gender
        print("The count of gender types is: " + str(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: "  + str(int(df['Birth Year'].min())))
        print("The most recent birth year is: " + str(int(df['Birth Year'].max())))
        print("The most common birth year is: " + str(int(df['Birth Year'].mode().values[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Displays raw data if requested'''
    start_loc = 0
    end_loc = 5
    request_user = input("Do you want to see the raw data?: ").lower()

    if request_user == 'yes':
        while end_loc <= df.shape[0] - 1:
            
            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_request = input("Do you want to continue?: ").lower()
            if end_request == 'no':
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
