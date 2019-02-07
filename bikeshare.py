import time
# import numpy as np
import pandas as pd
# import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
              month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
              day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    filter = ''

    while city not in CITY_DATA.keys():
        city = input("Would you like to see data for Chicago, "
                     "New York City, or Washington?\n")
        city = city.lower()

    while filter not in ['month', 'day', 'both', 'all']:
        filter = input("\nWould you like to filter by 'month', 'day', "
                       "'both' or use 'all' the data?\n")
        filter = filter.lower()

    if (filter == 'month') or (filter == 'both'):
        # get user input for month (all, january, february, ... , june)
        while month not in months:
            month = input("\nEnter a month to analyze "
                          "('all' or 'January' through 'June'):\n")
            month = month.lower()

    if (filter == 'day') or (filter == 'both'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
        days_of_week = ['all', 'monday', 'tuesday', 'wednesday',
                        'thursday', 'friday', 'saturday', 'sunday']
        while day not in days_of_week:
            day = input("\nEnter a day of the week to analyze "
                        "('all' or 'Monday', 'Tuesday', ... 'Sunday'):\n")
            day = day.lower()

    print()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and applies filters as needed

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
              month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
              day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    # Save unfiltered dataframe for possible use at the end of this routine.
    df_raw = df

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # convert Trip Duration to a timedelta
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')

    # extract month and weekday name from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if (month != 'all') and (month != ''):
        # use the index of the months list to get the corresponding int
        # Note: months is defined as shown below.
        # months = ['all', 'january', 'february', 'march',
        #           'april', 'may', 'june']
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if (day != 'all') and (day != ''):
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.title()]

    # Create a new column in df named 'hour'
    df['hour'] = df['Start Time'].dt.hour

    # Create a new column in df named 'trip'
    # Location where bikes were rented and then returned
    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    data_type = ''
    if((len(df.index) - 1) > 0):
        while data_type.lower() not in ['raw', 'filtered', 'no']:
            print("Would you like to page through the 'raw' "
                  "or 'filtered' data?")
            data_type = input("Enter 'no' to skip viewing the data.\n")
            if data_type.lower() == 'raw':
                print_data(df_raw, data_type, 'yes')
            elif data_type.lower() == 'filtered':
                print_data(df, data_type, 'yes')
            elif data_type.lower() == 'no':
                break
            else:
                print("Please enter 'raw', 'filtered', or 'no'.")
        print('-'*40)
    return df


def print_data(df, data_type, reply):
    """
    Print the raw or filtered data to the screen, N rows at a time

    Args:
        (pdf) df - pandas DataFrame of 'raw' or 'filtered' data
        (str) data_type - either 'raw' or 'filtered' data
        (str) reply - initial value of reply (always 'yes')
    """

    # Determine output type (json or columns)
    while True:
        output_style = input("\nWould you like to see the output in line "
                             "delimited json format?\n")
        if output_style.lower()[0] == 'y':
            json = True
            break
        elif output_style.lower()[0] == 'n':
            json = False
            break
        else:
            print("Please enter 'yes' or 'no'\n")

    print()
    # Determine start, stop and step values
    start = 0
    while True:
        try:
            step = (int(input("Enter number of rows to view at a time? "
                              "Default is 5 rows.\n")) or 5)
        except ValueError:
            print("Please enter an integer value.")
        else:
            print("Printing {} lines at a time.".format(step))
            break

    stop = len(df.index)
    if step > stop:
        step = stop
        print("Step size lowered to {} rows.".format(stop))

    # Print out 'raw' or 'filtered' data
    while (reply.lower()[0] == 'y'):
        end = min((start + step), stop)

        if not json:
            print(df.iloc[start:end])
        else:
            print(df.iloc[start:end].to_json(orient='records',
                                             lines=True,
                                             date_format='iso'))

        print()
        if end == stop:
            break
        reply = (input("Would you like to see more of the {} data? Enter "
                       "'yes' or 'no'. ".format(data_type.lower())) or 'yes')
        start += step  # Increment start by step count
        print()

    print("\nFinished\n")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Create a new column in df named 'hour'
    # df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    month = df['month'].mode()[0]  # Get index of month
    count = df.loc[df['month'] == month].count()[0]
    month = months[month]  # Get name of month from months list & index
    print_travel('month', month.title(), count)

    # display the most common day of week
    weekday = df['day of week'].mode()[0]
    count = df.loc[df['day of week'] == weekday].count()[0]
    print_travel('day of week', weekday.title(), count)

    # display the most common start hour
    start_hour = df['hour'].mode()[0]
    count = df.loc[df['hour'] == start_hour].count()[0]
    if start_hour <= 12:
        start_hour = str(start_hour) + ':00 AM'
    else:
        start_hour = str(start_hour - 12) + ':00 PM'
    print_travel('start hour', start_hour, count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_travel(travel_time, actual_dt, count):
    """
    Print most common travel_time used with count riders

    Args:
        (str) travel_time - String of 'month', 'day of week', or 'start hour'
        (str) actual_dt - actual month, day of week, or start hour
        (int) count - number of users for given travel time
    """
    print("Most common {} is {} with {} users."
          .format(travel_time, actual_dt, count))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print_station(df, 'Start Station')

    # display most commonly used end station
    print_station(df, 'End Station')

    # display most frequent combination of start station and end station
    # df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    # Moved previous line into load_data module
    trip = df['trip'].mode()[0]
    count = df.loc[df['trip'] == trip].count()[0]
    print("Most common trip is {} with {} users.".format(trip, count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_station(df, station):
    """
    Print most commonly used start and end stations

    Args:
        (df) df - pandas DataFrame
        (str) station - String used to pick start or end location
    """
    station_location = df[station].mode()[0]
    count = df.loc[df[station] == station_location].count()[0]
    print("Most commonly used {} is {} with {} users."
          .format(station.lower(), station_location, count))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in the given city.
    total_time = df['Trip Duration'].sum()
    total_message = 'total time of all the trips was'
    print_trips(total_time, total_message)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print_trips(mean_time, 'mean trip took')

    # display longest and shortest trips
    longest_trip = df['Trip Duration'].max()
    shortest_trip = df['Trip Duration'].min()

    print_trips(longest_trip, 'longest trip took')
    print_trips(shortest_trip, 'shortest trip took')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_trips(trip_duration, length_description):
    """
    Determine trip_duration and print out results

    Args:
        (td) trip_duration - timedelta object - df['Trip Duration']
        (str) length_description - String required to descripe trip duration
    """

    days, hours, minutes, seconds, ms, us, ns = trip_duration.components
    if days == 0:
        print("The {} {:02}:{:02}:{:02}"
              .format(length_description, hours, minutes, seconds))
    else:
        print("The {} {} days {:02}:{:02}:{:02}"
              .format(length_description, days, hours, minutes, seconds))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    customers = df.loc[df['User Type'] == 'Customer'].count()[0]
    subscribers = df.loc[df['User Type'] == 'Subscriber'].count()[0]
    dependents = df.loc[df['User Type'] == 'Dependent'].count()[0]
    unknown = df.loc[df['User Type'].isnull()].count()[0]

    print("There are {} customers.".format(customers))
    print("There are {} subscribers.".format(subscribers))
    print("There are {} dependents.".format(dependents))
    print("There are {} unspecified type (NaN values).\n".format(unknown))

    # Display counts of gender
    if 'Gender' in df:
        number_of_males = df.loc[df['Gender'] == 'Male'].count()[0]
        number_of_females = df.loc[df['Gender'] == 'Female'].count()[0]
        unknown = df.loc[df['Gender'].isnull()].count()[0]

        print("Number of male riders is {}.".format(number_of_males))
        print("Number of female riders is {}.".format(number_of_females))
        print("Number of users of unspecified gender is {}.".format(unknown))
    else:
        print("Gender is not in dataset.")
    print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]

        print("Earliest year of birth is {}.".format(int(earliest)))
        print("Most recent year of birth is {}.".format(int(most_recent)))
        print("Most common year of birth is {}.".format(int(most_common)))
    else:
        print("Birth Year is not in dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Usage: python bikeshare.py"""

    start_time = time.time()

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if(len(df) > 0):
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print("No data in the dataframe! How did we get here?")

        restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break

    print("\nProgram took {} seconds".format(time.time() - start_time))
    print('-'*40)


if __name__ == "__main__":
    main()
