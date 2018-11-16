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

from phase3_task1 import Phase3_task1
from phase3_task3 import Phase3_task3
from phase3_task_5ab import Phase3_Task_5ab


def print_menu():
    print('1. Task 1')
    print('2. Task 2')
    print('3. Task 3')
    print('4. Task 4')
    print('5a. Task 5a')
    print('5b. Task 5b')
    print('6a. Task 6a')
    print('6. Task 6')
    print('7. Task 7')
    print('8. Load data')
    print('0. Quit')


def main():
    while True:
        print_menu()
        option = input("Enter option: ")
        if option == '1':
            print('TASK 1')
            print('e.g: 10 vis')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task1()
            data = tasks.task1(int(ips[0]), ips[1])
        elif option == '2':
            print('TASK 2')
            print('e.g: usertext TF-IDF PCA 20 10117222@N04 0.05')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_1_2()
            tasks.task2(ips[0], ips[1], ips[2], int(ips[3]), ips[4], float(ips[5]))
        elif option == '3':
            print('TASK 3')
            print('Sample: 10')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task3()
            tasks.task_3(data, int(ips[0]))
        elif option == '4':
            print('TASK 4')
            print('Sample: CM PCA 5 1')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Task_3_4()
            tasks.task4('locations', ips[0], ips[1], int(ips[2]), ips[3])
        elif option == '5a':
            print('TASK 5a')
            print("Sample: 5 7")
            inp = input("Input: <L> <K> ")
            ips = inp.split(' ')
            tasks_ = Phase3_Task_5ab()
            tasks_.task5a(int(ips[0]), int(ips[1]))
        elif option == '5b':
            print('TASK 5b')
            print("Sample: 4268828872 5")
            inp = input("Input: <Image Id> <t> ")
            ips = inp.split(' ')
            tasks_.task5b(int(ips[0]), int(ips[1]))
        elif option == '6':
            print('TASK 6')
            print('Sample: TF-IDF 1')
            inp = input('Input: ')
            ips = inp.split(' ')
            if len(ips[0]) == 0:
                ips[0] = 'TF-IDF'
            tasks = Task_6()
            tasks.task6('loctext', ips[0], 'SVD', int(ips[1]))
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
            # dt.generate_img_text_graph()
            dt.generate_img_img_vis_graph()
        elif option == '0':
            break
        else:
            print('Incorrect option.')
        input('Press any key to continue...')

if __name__ == "__main__":
    #dt = DataLoading('0')
    #dt.generate_img_img_vis_graph()
    #p1 = Phase3_task1()
    #data = p1.task1(5,'vis')
    #print('done')
    #p3 = Phase3_task3()
    #p3.task_3(data, 10)
    #Test.test()
    main()