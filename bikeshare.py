'''
Written by Michael "Ben" Tankus 1/5/2020
NOTE: My program assumes the .csv files are located in the same
     directory as the .py file
'''
import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print('Please enter what city you would like to filter by (Chicago, New York City, or Washington)')
    city = input()
    city = city.lower()

    while city not in (['chicago', 'new york city', 'washington']):
            city = input()
            city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Please enter what month you would like to filter by (January, February, March, April, May, June)')
    month = input()
    month = month.lower()

    while month not in (['january', 'february', 'march', 'april', 'may', 'june']):
            month = input()
            month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please enter what day of the week you would like to filter by (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)')
    day = input()
    day = day.lower()

    while day not in (['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
            day = input()
            day = day.lower()

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

    filename = CITY_DATA[city]
    print("File name is:", filename)
    df =  pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time']) #End time is converted here for future calculations

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday_name



    #MONTH
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']  # use the index of the months list to get the corresponding int
        month = months.index(month)+1
        df = df[df['month'] == month] # filter by month to create the new dataframe

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.title()]

    #print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    pop_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']  # use the index of the months list to get the corresponding int
    month = months[pop_month-1].title()
    print('Most Common Month is: ', month)

    # TO DO: display the most common day of week
    pop_day = df['day of week'].mode()[0]
    print('Most Common Day of the Week is: ', pop_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour is: ', pop_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station is: ', pop_start)

    # TO DO: display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('Most Commonly Used End Station is: ', pop_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + " " + df['End Station']
    pop_trip = df['Station Combo'].mode()[0]
    print('Most Common trip is: ', pop_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Total Travel Hours'] = df['End Time'].dt.hour - df['Start Time'].dt.hour
    tot_travel_time = sum(df['Total Travel Hours'])
    print('Total Travel Time is: ', tot_travel_time, ' hours')

    # TO DO: display mean travel time
    mean_travel_time = df['Total Travel Hours'].mean()
    print('Mean Travel Time is: ', mean_travel_time, ' hours')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Counts Are:\n', user_types)

    # TO DO: Display counts of gender NOTE: Washington does not gather gender, skip for WA
    print('FUNCTION city: ', city)
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print('\nGender Counts Are:\n', gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nBirth Year Stats Are:\n')
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        mode_birth = df['Birth Year'].mode()[0]

        print('Min Birth Year: ', min_birth, '\nMax Birth Year: ', max_birth, '\nMost Common Birth Year: ', mode_birth)
    #END IF

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        print('city: ', city)
        user_stats(df, city) #Washington does not gather gender or birth year data, so must be skipped for those metrics

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
        main()
