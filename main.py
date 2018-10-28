from pymongo import MongoClient
from task_1_2 import Task_1_2
from task_3_4 import Task_3_4
from task_5 import Task_5
from task_6 import Task_6
from task_7 import Task_7
import collections
import math
from scipy import spatial
from sklearn import metrics
import numpy as np
from data_loading import DataLoading
from os import system
import Test


def print_menu():
    print('1. Task 1')
    print('2. Task 2')
    print('3. Task 3')
    print('4. Task 4')
    print('5. Task 5')
    print('6. Task 6')
    print('7. Task 7')
    print('8. Load data')
    print('9. Sample input')
    print('0. Quit')

def sample_run():
    print('Task 1-----------------')
    #tasks.task1_3('usertext', '39052554@N00', 'TF', 5)
    print('Task 1-----------------')
    #tasks.task1_3('usertext', '56087830@N00', 'DF', 8)
    print('Task 1-----------------')
    #tasks.task1_3('usertext', '56087830@N00', 'TF-IDF', 5)
    print()
    print('Task 2-----------------')
    #tasks.task1_3('imagetext', '4459178306', 'TF', 10)
    print('Task 2-----------------')
    #tasks.task1_3('imagetext', '288051306', 'DF', 5)
    print('Task 2-----------------')
    #tasks.task1_3('imagetext', '288051306', 'TF-IDF', 5)
    print()
    print('Task 3-----------------')
    #tasks.task1_3('loctext', '27', 'TF', 5)
    print('Task 3-----------------')
    #tasks.task1_3('loctext', '6', 'DF', 5)
    print('Task 3-----------------')
    #tasks.task1_3('loctext', '6', 'TF-IDF', 7)
    print()
    print('Task 4-----------------')
    #tasks.task4('10', 'CN3x3', 7)
    print('Task 4-----------------')
    #tasks.task4('18', 'GLRLM', 5)
    print('Task 4-----------------')
    #tasks.task4('30', 'LBP3x3', 5)
    print()
    print('Task 5-----------------')
    #tasks.task5('4', 5)

def main():

    while True:
        print_menu()
        option = input("Enter option: ")
        if option == '1':
            print('TASK 1')
            print('e.g: usertext TF-IDF PCA 20 0.05')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_1_2()
            tasks.task1(ips[0], ips[1], ips[2], int(ips[3]), float(ips[4]))
        elif option == '2':
            print('TASK 2')
            print('e.g: usertext TF-IDF PCA 20 10117222@N04 0.05')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_1_2()
            tasks.task2(ips[0], ips[1], ips[2], int(ips[3]), ips[4], float(ips[5]))
        elif option == '3':
            print('TASK 3')
            print('Sample: CM PCA 5 10045579766')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_3_4()
            tasks.task3('locations', ips[0], ips[1], int(ips[2]), ips[3])
        elif option == '4':
            print('TASK 4')
            print('Sample: CM PCA 5 1')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_3_4()
            tasks.task4('locations', ips[0], ips[1], int(ips[2]), ips[3])
        elif option == '5':
            print('TASK 5')
            print("Sample: PCA 5 1")
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_5()
            tasks.task5('locations', ips[0], int(ips[1]), ips[2])
        elif option == '6':
            print('TASK 6')
            print('Sample: TF 1')
            inp = input('Input: ')
            ips = inp.split(' ')
            if len(ips[0]) == 0:
                ips[0] = 'TF-IDF'
            tasks = Task_6()
            tasks.task6('loctext', ips[0], 'SVD', ips[1])
        elif option == '7':
            print('TASK 7')
            print("Sample: 5")
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_7()
            tasks.task_7(int(ips[0]))
        elif option == '8':
            print('Load Data')
            path = input("Path: ")
            dt = DataLoading(path)
            dt.drop_database()
            dt.process_location_data()
            dt.process_users_textual_data()
            dt.process_images_textual_data()
            dt.process_locations_textual_data()
            dt.process_visual_data()
            dt.process_common_terms_data()
        elif option == '9':
            sample_run()
        elif option == '0':
            break
        else:
            print('Incorrect option.')
        input('Press any key to continue...')
        _ = system('cls')

if __name__ == "__main__":
    #Test.test()
    main()