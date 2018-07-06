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

    def get_item(input_print,error_print,enterable_list,get_value):
        while (True):
            ret = input(input_print);
            ret = get_value(ret)
            if ret in enterable_list:
                return ret
            else:
                print(error_print);
    #city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
    city = get_item('Would you like to see data for Chicago, New York City, or Washington?\n',
                'Error!Please input the correct city name.',
                ['chicago', 'new york city', 'washington'],
                lambda x: str.lower(x))

    month = get_item('Which month? all,January, February, March, Apirl, May or June\n',
                'The Input is wrong! Which month? ALL, January, February, March, Apirl, May or June.\n',
                ['january', 'february', 'march', 'april', 'may', 'june','all'],
                lambda x: str.lower(x))

    day = get_item(('Which day? Monday, Tuesday, wennesday, Thursday, Friday, Saturday, Sunday \n'),
                'The Input is wrong! Which day of week? Monday, Tuesday, wennesday, Thursday, Friday, Saturday, Sunday \n',
                ['monday','tuesday','wennesday','thursday','friday','saturday','sunday','all'],
                lambda x: str.lower(x))

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    #common_month = df['Start_time'].dt.month.mode()[0]
    common_month = df['month'].mode()[0]
    #因为上一个函数已经重新定义了df，所以这里只要选取df中的['month']列就可以了。
    #common_month =month.mode()[0]

    #months = ['january', 'february', 'march', 'april', 'may', 'june']
    #common = months[int(common_month) - 1]

    print('Most Common Month:', common_month)

    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    #common_day_of_week = day.mode()[0]
    print('Most Common Day Of Week:', common_day_of_week)

    # TO DO: display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    #因为上一个函数中没有没有定义出hour，所以需要这里把hour列定义出来再使用
    print('Most Common Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commonly_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', commonly_start_station)


    # TO DO: display most commonly used end station
    commonly_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', commonly_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    # total = df['Start Station'] + ' and ' + df['End Station']
    # most = total.mode()[0]

    col_count = dict(df.groupby(['Start Station', 'End Station']).size())
    total = max(col_count, key=lambda x: col_count[x])
    print("The most frequent combination of start station and end station trip is {} to {}".format(total[0], total[1]))


    # print('The most frequent combination of start station and end station trip is\n',most)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = sum(df['Trip Duration'])
    print('Total Duration:',total_duration)

    # TO DO: display mean travel time
    # mean_time = sum(df['Trip Duration']) / len(df['Trip Duration'])
    mean_time = df['Trip Duration'].mean()
    print('Avg Duration:',mean_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    try:
    # TO DO: Display counts of gender
        counts_of_gender = df['Gender'].value_counts()
        print(counts_of_gender)
    # TO DO: Display earliest, most recent, and most common year of birth
        common_year = df['Birth Year'].mode()[0]
        earliest = min(df['Birth Year'])
        recent = max(df['Birth Year'])

        print('earliest year of birth:', earliest)
        print('recent year of birth:', recent)
        print('common year of birth:',common_year)

    except KeyError:
        print('\nThe data is wrong.\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
