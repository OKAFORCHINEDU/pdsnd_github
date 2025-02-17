#Second Udacity Project
#Authur: Okafor Chinedu


import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['mon', 'tues', 'wed', 'thur', 'fri',
        'sat', 'sun']



def check_input(input_string,input_type):
    """
    check the validity of user input.
    input_string: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    # used to get user input for city, month and for the day of the week
    while True:
        x =input(input_string).lower()
        try:
            if x in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif x in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif x in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Invalid input, your input should be: chicago new york city or washington")
                if input_type == 2:
                    print("invalid input, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Invalid input, your input should be: sunday, ... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return x

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
    city = check_input("Would you like to see the data for chicago, new york city or washington?",1)
    # get user input for month (all, january, february, ... , june)
    month = check_input("Which Month (all, january, ... june)?", 2)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("Which day? (all, monday, tuesday, ... sunday)", 3)
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
    df = pd.read_csv(CITY_DATA[city])

    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
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



def display_raw_data(df):
    """
    Displays subsequent rows of data according to users input
    Arg:
        df - pandas dataframe containing city data filtered by month and day returned from load_data() function
    """
    i = 0
    answer = input('Would you like to display the first 10 rows of data? yes/no: ').lower()
    pd.set_option('display.max_columns',None)

    while True:
        if answer == 'no':
            break
        print(df[i:i+10]) #slices the data to display next five rows
        answer =input('Would you like to display the next 10 rows of data? yes/no: ').lower()
        i += 10

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #Display the most common month
    common_month = df['month'].mode()[0]
    print('The Most Common Month:', calendar.month_name[common_month])
    #Display the most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', common_day)
    #Display the most common start hour

    #Extract hour from the Start Time to creat an hour column
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print('\n This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        print('Gender Stats:')
        print(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
