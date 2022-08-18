import time
import pandas as pd
import numpy as np

count = lambda df,column,element: df[column][df[column] == element].value_counts().sum()

""" Process input functions """
def string_map_input(Input,string_dict,msg):
    """
    Validates the string input and maps it to another value in a dictionary
    
    Args:
        (str) Input - input from user
        (dict) string_dict - dictionary of accepted strings and their respective values
        (str) msg - error message for wrong input
    Return:
        (dict_value) new_inputs - value of the mapped inputs of the user
    """
    new_input = Input
    while(True):
        if new_input in string_dict: break
        else: new_input = input(msg) 
    return string_dict.get(new_input)
def conv_valid_input(Input,splitter,Min,Max,msg):
    """
    Converts string input to integer after validating it
    
    Args:
        (str) Input - user input 
        (str) splitter - string used to split user input
        (int) Min - minimum number allowed for validation
        (int) Max - maximum number allwoed for validation
        (str) msg - message to be printed if input is not valid
    Returns:
        (list) numbered_input - list of user validated inputs changed to numbers
    """
    numbered_input = Input
    output = []
    while(True):
        try:
            """ Convert input to numbered list and checks 
                if all elemnsts of list are numbers between min-max """
            is_valid = True
            for num in numbered_input.split(splitter):   
                num = int(num)
                output.append(num)
                if (num < Min or num > Max):
                    is_valid = False
                    numbered_input = input(msg)
                    break
            if is_valid == True : break
        except:
            numbered_input = input(msg)
    return output
def valid_filename(ext):
    """
    Checks for validity of filename with the given extension 
    
    Args:
        (str) ext - extension of ile name
    Return:
        (str) filename - valid filename with extension
    """
    delimiter = - len(ext)
    while(True):
        try :
            filename = input('\nEnter filename:\n\n')
            if (filename[delimiter:] != ext
                   and '.' not in filename):
               return filename + ext
            elif (filename[delimiter:] == ext):
               return filename
        except:
              print('Enter a valid filename')
def check_int(msg,Min,Max):
    """ 
    Checks if user input is int or not 
    
    Args:
        (str) msg - message to request input
        (Min) Min - minimum number accepted
        (Max) Max - maximum number accepted
    Returns:
        (int) output - user input converted to interger number
    """
    Input = input(msg)
    while(True):
        try: 
            Input = int(Input)
            if((Input >= Min) and (Input <= Max)): break
            else: 
                Input = input('Type integer numbers between {}-{} ONLY\n\n'\
                  ''.format(Min,Max))
        except:
            Input = input('Type integer numbers between {}-{} ONLY\n\n'\
                  ''.format(Min,Max))
    return Input

""" Filter functions"""
def get_filters():
    """
    Asks user to specify a city, and filters to apply.

    Returns:
        (str) city - name of the city to analyze
        (list) filters - number of filter(s) to apply (optional)
    """
    
    """ Prompts user to enter city name and validates it """
    city = input('Hello! Let\'s explore some US bikeshare data!\n'\
                 'Show Statistics about Chicago, New York City or Washington ?\n\n').lower()
    city_data = {'chicago': 'chicago.csv',
                 'new york city': 'new_york_city.csv',
                 'washington': 'washington.csv'}
    msg = 'Please type Chicago, New York City, or Washington ONLY\n\n' 
    city = string_map_input(city,city_data,msg)
    
    """ Prompts user to enter one or more of six filters and validates the input """
    filters = input('\nFilter data by: \n'\
                    '1) Date\t\t'\
                    '2) Station\n'\
                    '3) Duration\t4) User Type\n'\
                    '5) Gender\t\t6) Birth Year\n'\
                    'Multiple filters available and for no filter type 0\n'\
                    'Note: 5 & 6 aren\'t available in Washington\n\n')
    msg = 'Please type comma separated numbers from 0-6 ONLY\n\n'
    filters = conv_valid_input(filters,',',0,6,msg)
    return city, filters
def handle_filters(city,filters):
    """
    Loads data for the specified city and apply each filter if applicable.

    Args:
        (str) city - name of the city to analyze
        (list) filters - numbered list of filters to apply on dataframe
    Returns:
        df - Pandas DataFrame containing filtered city data
    """
    """ Load city bikeshare data and add essential columns for filtering """
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    
    """ Applying filters according to user input """
    if (0 in filters):
        df['Combo Station'] = df['Start Station'] + ' and ' + df['End Station']
        return df
    if (1 in filters) :
        df = date_filter(df)
    if (3 in filters):
        df = min_max_filter(df,'Trip Duration')
    if (4 in filters):
        df = binary_filter(df,'User Type',['Customer','Subscriber'])
    if city != 'washington.csv':
        if (5 in filters):
            df = binary_filter(df,'Gender',['Male','Female'])   
        if (6 in filters):
            df = min_max_filter(df,'Birth Year')   
    df['Combo Station'] = df['Start Station'] + ' and ' + df['End Station']
    if (2 in filters):
        df = stations_filter(df)
    print('\nGenerating Statistics for {} city\n'\
          'Applied filters:{}'.format(city[:-4].capitalize()
                                      ,filters))
    return df    

def date_filter(old_df):
    """
    Prompts user to enter month,day, and hour
    and filter the dataset according to input

    Args:
        old_df - Pandas DataFrame with no filter
    Returns:
        df - Pandas DataFrame containing filtered city data
    """
    df = old_df
    
    """ Prompts user to enter month,day, and hour 
        and validates them """
    print('\nMultiple months,days,hours are available\n')
    months = input('Month(s) from 1-6 or 7 for all months:\t')
    msg = 'Please enter comma separated numbers from'\
          ' 1-7 corrosponding to months ONLY\n\n'
    months = conv_valid_input(months,',',1,7,msg)
    days = input('[Mon 0, Tues 1, ..., Sun 6]\n'\
                 'Day(s) from 0-6 or 7 for all days:\t')
    msg = 'Please enter comma separated numbers from '\
          '0-7 corrosponding to days ONLY\n\n'
    days = conv_valid_input(days,',',0,7,msg)
    hours = input('Hours(s) from 0-23 or 24 for all hours:\t')
    msg = 'Please enter comma separated numbers from '\
          '0-24 corrosponding to hours ONLY\n\n'
    hours = conv_valid_input(hours,',',0,24,msg)
   
    """ Filters month,day, and hour according to user input """
    if 7 not in months:
        df = df[(min(months) <= df.month) & (df.month <= max(months))]
    if 7 not in days:
        df = df[(min(days) <= df.day) & (df.day <= max(days))]
    if 24 not in hours:
        df = df[(min(hours) <= df.hour) & (df.hour <= max(hours))]
    return df    
def min_max_filter(old_df,colm):
    """
    Filters dataset between two numbers in a particular column
    
    Args:
        (DataFrame) old_df - semi-filtered dataframe
        (str) colm - column to apply filter on
    Returns:
        (DataFrame) df - filtered dataframe
    """
    df = old_df
    Min = min(df[colm])
    Max = max(df[colm])
    values = input('\nChoose min,max for {}\n'\
                   'Values must lie between {} and {}'\
                   '\n\n'.format(colm,Min,Max))
    msg = '\nChoose comma separated numbers between'\
          ' max and min values ONLY\n\n'
    while(True):
        values = conv_valid_input(values,',',Min,Max,msg)
        if len(values) >=2 : break
    df = df[(df[colm] >= min(values)) & (df[colm] <= max(values))]
    return df
def binary_filter(old_df,colm,binary):
    """
    Filters dataset by binary selection
    
    Args:
        (DataFrame) old_df - semi-filtered dataframe
        (str) colm - column to apply filter on
        (list) binary - list of two binaries to choose from
    Returns:
        (DataFrame) df - filtered dataframe
    """
    df = old_df
    selector = input('{}:\t'.format(colm))
    msg = '\nPlease choose one from {} or {} ONLY\n\n'\
          ''.format(binary[0],binary[1])
    selector = string_map_input(selector,
                                {binary[0]:binary[0],
                                 binary[1]:binary[1]},
                                msg)
    df = df[df[colm] == selector]
    return df

def stations_filter(old_df):
    """
    Prompts User to enter start, end station,
    or combination and filters dataset according to input

    Args:
        old_df - Pandas DataFrame with no filter
    Returns:
        df - Pandas DataFrame containing filtered city data
    """
    df = old_df
    Input = input('\nFilter by start,end or combo ?\n\n')
    msg = 'Please choose one from start,end or combo ONLY\n\n'
    Input = string_map_input(Input,{'start':0,
                                        'end':1,
                                        'combo':2},msg)
    stations_list = [df['Start Station'].unique(),
                    df['End Station'].unique(),
                    df['Combo Station'].unique()]
    if 0 == Input:
        station = 'Start'
        df = station_filter(station,df,stations_list,0)
    if 1 == Input:
        station = 'End'
        df = station_filter(station,df,stations_list,1)
    if 2 == Input:
        station = 'Combo'
        df = station_filter(station,df,stations_list,2)
    return df
def station_filter(station,df,stations_list,i):
    input_station = input('\nfor a list of availble stations'\
                          ' type \'list\'\n{} Station:\t '\
                          ''.format(station))
    while (True):
        if input_station in stations_list[i]:
            df = df[df['{} Station'.format(station)] == input_station]
            break
        if input_station == 'list':
            display_stations_list(stations_list)
            input_station = input('for a list of availble stations'\
                          'type \'list\'\n{} Station:\t '\
                          ''.format(station))
        else: 
            msg = 'select {} station from available stations ONLY\n'.format(station)
            input_station = input(msg)
    return df
def display_stations_list(stations_list):
    """
    Saves stations list or show it to the user
    
    Args:
        (list) stations_list - list of all available stations in curent filter
    """
    show_save = input('\nSave stations list to a file or show them?\n'\
          'Type \'show\' or \'save\':\t').lower()
    msg = 'Type show or save ONLY\n'
    show_save = string_map_input(show_save,
                                 {'show':0,'save':1},
                                  msg)
    output = 'Available start stations in this filter:\n '\
             '{}\nAvailable end stations in this filter: {}'\
             '\n\nAvailable combo stations in this filter: {}'\
             ''.format(stations_list[0],
                       stations_list[1],
                       stations_list[2])
    if 0 == show_save:
        print(output)
    elif 1 == show_save:
        with open('Available Stations.txt','w') as f: 
            f.write(output)

""" Stats funcitons """
def time_stats(df):
    """ Displays statistics on the most frequent times of travel.
       and returns a stats log """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    """ Calculate mode of month,day, and hour """
    month = df.month.mode()[0]
    day = df.day.mode()[0]
    hour = df.hour.mode()[0]
    
    """ Display most frequent times of travel and the count of each occurence """
    msg = 'The most frequent month: {}\tcount: {} \n'\
          'The most frequent day: {}\tcount: {}\n'\
          'The most frequent hour: {}\tcount: {}'\
          ''.format(month,count(df,'month',month),day,
                      count(df,'day',day),hour,count(df,'hour',hour))
    print(msg)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return msg
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ Calculate most common start,end,combination station """
    start = df['Start Station'].mode()[0]
    end = df['End Station'].mode()[0]
    combo = df['Combo Station'].mode()[0]
    
    """ Display the most common stations and their counts 
        and returns a stats log """
    msg = 'The most frequent start station is: {}\tcount: {}\n'\
          'The most frequent end station is: {}\tcount: {}\n'\
          'The most frequent start and end stations are: {}\t'\
          'count: {}'.format(start,count(df,'Start Station',start),
                             end,count(df,'End Station',end),
                             combo,count(df,'Combo Station',combo))
    print(msg)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return msg
def trip_duration_stats(df):
    """ Displays statistics on the total and average trip duration.
       and returns a stats log """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    """ Calculate and display total and average trip duration """
    total = df['Trip Duration'].sum()
    avg =  df['Trip Duration'].mean()
    msg= 'Total trips duration is: {}\nAverage trips duration is: {}'.format(total,avg)
    print(msg)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return msg
def user_stats(df):
    """Displays statistics on bikeshare users
       and returns a stats log"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Counts user types """
    msg = 'Subscribers count: {}\nCustomers count: {}\n'\
          'No year of birth or gender column in this '\
          'dataset'.format(count(df,'User Type','Subscriber'),
                           count(df,'User Type','Customer'))
 
    """ If dataset contain year of birth calculate and display
        earliest, most recent, most common year of birth 
        and count of both genders """
    if 'Birth Year' in df.columns :
        early = min(df['Birth Year'])
        recent = max(df['Birth Year'])
        common = df['Birth Year'].mode()[0]
        msg = 'Subscribers count: {}\nCustomers count: {}\n'\
              'Males count: {}\nFemales count: {}\n'\
              'Earliest birth year: {}\tcount: {}\n'\
              'Most recent birth year: {}\tcount: {}\n'\
              'Most common birth year: {}\tcount: {}'\
              ''.format(count(df,'User Type','Subscriber'),
                        count(df,'User Type','Customer'),
                        count(df,'Gender','Male'),
                        count(df,'Gender','Female'),
                        early,count(df,'Birth Year',early),
                        recent,count(df,'Birth Year',recent),
                        common,count(df,'Birth Year',common))  
    print(msg)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return msg

def store_stats(df,stats_log):
    """
    Asks wheather user wants to stores filtered dataframe,
    or stats for a run in a file 
    
    Args:
        (DataFrame) df - filtered dataframe
        (list) stats_log - a list of stats logs strings 
    """
    is_store_df = input('Store filtered dataset in .csv file ? (yes or no)\n\n').lower()
    is_store_df = string_map_input(is_store_df,
                                {'yes':True, 'no':False},
                                'Type yes or no ONLY\n\n')
    if is_store_df :
        filename = valid_filename('.csv')
        df.to_csv(filename)
        
    is_store_stats = input('\nStore statistics data in .txt file ? (yes or no)\n\n').lower()
    is_store_stats = string_map_input(is_store_stats,
                                {'yes':True, 'no':False},
                                'Type yes or no ONLY\n\n')
    if is_store_stats :
        filename = valid_filename('.txt')
        with open(filename,'w') as f:
            output = "\n".join([stat_log for stat_log in stats_log])
            f.write(output)
    pass
def random_output(df):
    """
    Asks user if he wants to see random raw data 
    and Returns a number of random data to the user
    
    Args:
        (DataFrame) df - dataframe to randomly choose data from
   """
    msg = '\nType number of raw data to display:\n'\
          'Note: type 0 if you don\'t to see any raw data\n\n'
    Input = check_int(msg,0,len(df))
    while Input > 0 :
        rand_sample = df.sample(n=Input)
        
        """ Remove columns added when filtering """
        rand_sample = rand_sample.drop(['month','day','hour','Combo Station'], axis=1)
        index = rand_sample.index
        
        """ Printing """
        for i in range(Input):
            print('\nSample {}:\n'.format(i+1))
            for i,colm in enumerate(rand_sample.iloc[i,:].values):
                print('{}: {}\n'.format(rand_sample.columns[i],colm))
        Input = check_int(msg,0,len(df))
def main():
    while True:
        city, filters = get_filters()
        df = handle_filters(city,filters)
        time_stats_msg = time_stats(df)
        station_stats_msg = station_stats(df)
        trip_duration_stats_msg = trip_duration_stats(df)
        user_stats_msg = user_stats(df)
        random_output(df)
        stats_log = [time_stats_msg,station_stats_msg,trip_duration_stats_msg,user_stats_msg]
        store_stats(df,stats_log)
        restart = input('\nWould you like to restart? Enter yes or no.\n\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
