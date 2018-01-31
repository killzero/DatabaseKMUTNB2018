#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv


class CSVtoGPA:

    def __init__(self, filename):
        self.filename = filename
        self.readCSV(self.filename)

    # open CSV file from name

    def readCSV(self, filename):
        with open(filename, 'rb') as csvfile:
            self.file = csv.reader(csvfile)
            self.dict = self.csvToDic(self.file)  # call csvToDic
            csvfile.close()

    # read 2D array sort to dictionary

    def csvToDic(self, file):
        _list = list(file)
        reList = zip(*_list)  # reversted list
        overSub = (reList[1])[2:].count('')  # count over element

        term = self.countSubject((reList[0])[2:-overSub])
        dic = {}
        c = 2
        for i in xrange(0, len(term)):
            temp = {term[i][0]: {'Subject Code': (reList[1])[c:c + term[i][1]]}}
            temp[term[i][0]].update({'Course title': (reList[2])[c:c + term[i][1]]})
            temp[term[i][0]].update({'Credit': map(int, (reList[3])[c:c + term[i][1]])})

            grade = {'Number': map(float, (reList[4])[c:c + term[i][1]])}
            grade.update({'Character': (reList[5])[c:c + term[i][1]]})
            temp[term[i][0]].update({'Grades': grade})

            dic.update(temp)
            c = c + term[i][1]
        dic.update({'Term': term})
        return dic

    # count total subject from each term
    # save in 2D tuple

    def countSubject(self, csvTerm):
        _term = ['']
        subNum = []
        count = 0
        for i in range(1, len(csvTerm) + 1):
            i *= -1
            if _term[-1] != csvTerm[i] and csvTerm[i] != '':
                subNum.append((i + count) * -1)
                count = i * -1
                _term.append(csvTerm[i])

        _term.pop(0)
        term = [_term[::-1], subNum[::-1]]
        term = zip(*term)

        return term

    # calculate and print grade

    def showGPA(self):
        total_sum = 0
        total_credit = 0

        for i in xrange(0, len(self.dict['Term'])):
            temp_dict = self.dict[self.dict['Term'][i][0]]
            _sum = 0
            credit = 0
            for j in xrange(0, len(temp_dict['Credit'])):
                _sum += temp_dict['Credit'][j] * temp_dict['Grades']['Number'][j]
                credit += temp_dict['Credit'][j]
            total_sum += _sum
            total_credit += credit
            grade = _sum / credit
            print 'GPA', self.dict['Term'][i][0], grade
        print 'GPAX', total_sum / total_credit


student = CSVtoGPA('Book1.csv')
student.showGPA()
