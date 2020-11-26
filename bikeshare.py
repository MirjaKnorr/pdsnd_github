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
    input('Press enter to continue.')

    #User input for city (chicago, new york city, washington) using a while loop to handle invalid inputs
    print('')
    print('')
    print('First, we will choose a city.')
    print('You can select one of the following three cities:\n Chicago\n New York City\n Washington')
    print('')
    print('')

    valid_city = ['Chicago', 'New York City', 'Washington', 'chicago', 'new york city', 'washington']

    city = input("Please enter the name of the city:\n")
    print('')
    while city not in valid_city:
        print('You can only choose Chicago, New York City or Washington')
        city = input("Try again:\n")
    print('')
    print('You have chosen: ' + city)
    print('')
    input('Press enter to continue.')
    city = city.lower()

    #Get user input for month (all, january, february, ... , june)
    print('')
    print('')
    print('Next, we will choose a month.')
    print('You can either decide to look at all data or analyze one specific month.')
    print('These are your options:\n All\n January \n February \n March \n April \n May \n June')
    print('')
    print('')

    valid_month = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'all', 'january', 'february', 'march', 'april', 'may', 'june']
    invalid_month = ['july', 'august', 'september', 'october', 'november', 'december','July', 'August', 'September', 'October', 'November', 'December']

    month = input('Please enter the name of the month: ')
    print('')
    while month not in valid_month:
        if month in invalid_month:
            print('Sorry, we do not have any data on this month.\nMake sure you select one of the options of the above list.')
            month = input('Try again:\n')
        else:
            print('This is not a month.\nPlease make sure to select an option from the above list.')
            month = input('Try again:\n')
    print('')
    print('You have chosen: ' + month)
    print('')
    input('Press enter to continue.')
    month = month.lower()

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    print('')
    print('')
    print('Finally, let\'s decide which day of the week we are interested in.')
    print('We can look at all days or choose one specific day of the week.')
    print('These are your options:\n All\n Monday\n Tuesday\n Wednesday\n Thursday\n Friday\n Saturday\n Sunday')
    print('')
    print('')

    valid_day = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    day = input('Please enter the name of the day: ')
    print('')
    while day not in valid_day:
        print('This is not a week day.')
        day = input('Try again:\n')
    print('')
    print('You have chosen: ' + day)
    print('')
    input('Press enter to continue.')
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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['day_of_week'] = df['day_of_week'].str.lower()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month: ', popular_month)

    #display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['day_of_week'] = df['day_of_week'].str.lower()
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most common day of week: ', popular_weekday.upper())

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station:', common_start)

    #display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most common end station:', common_end)

    #display most frequent combination of start station and end station trip
    df['space'] = ' to '
    df['StartEnd'] = df['Start Station'] + df['space'] + df['End Station']
    common_startend = df['StartEnd'].mode()[0]
    print('Most frequent combination of start and end station:', common_startend)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_time)

    #display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('Mean travel time: ', avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    #Do not drop NAs because I am interested in the amount of missing information.
    user_types = df['User Type'].value_counts(dropna=False)
    city = city
    print('Counts of User Types:\n', user_types)
    print('')

    #Display counts of gender
    #Do not drop NAs because I am interested in the amount of missing information.
    if city == 'washington':
        print('We do not have gender information for Washington.')
    else:
        gender = df['Gender'].value_counts(dropna=False)
        print('Counts of gender:\n', gender)
        print('')


    #Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('We do not have birth year information for Washington.')
    else:
        year_min = df['Birth Year'].min()
        print('Earliest year of birth: ', year_min)
        year_max = df['Birth Year'].max()
        print('Most recent year of birth: ', year_max)
        year_mode = df['Birth Year'].mode()
        print('Most common year of birth: ', year_mode)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displays 5 lines of raw data and provides 5 more lines if indicated by user input.
    """

    stopline = 5
    first_display = input('Would you like to see five rows of raw data?\nEnter yes or no.\n')
    if first_display.lower() == 'yes':
        print('')
        for i in range(stopline):
            print(df.iloc[i])
            print('')
            print('')
        while True:
            print('')
            more_display = input('Would you like to see more raw data?\nEnter yes or no.\n')
            if more_display.lower() == 'yes':
                startline = stopline
                stopline += 5
                for i in range(startline, stopline):
                    print(df.iloc[i])
                    print('')
                    print('')
                continue
            elif more_display.lower() != 'yes':
                print('Ok, stop display of raw data.')
                break
    else:
        print('Ok, we will not display raw data.')

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
