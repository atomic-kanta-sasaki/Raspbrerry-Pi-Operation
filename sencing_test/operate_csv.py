#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
with open('sample.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerow(['x', 'y', 'z', 'axis_x', 'axis_y', 'axis_z'])
