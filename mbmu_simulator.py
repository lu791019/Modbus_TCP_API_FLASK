#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python
 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr
 This is distributed under GNU LGPL license, see license.txt
"""
import random
import csv
import sys, time, threading
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp


class MBMUSimulator():

    def __init__(self):
        self.flag_run = False
        self.server = modbus_tcp.TcpServer()
        #Create modbus tcp server
        self.server.start()
        self.slave_1 = self.server.add_slave(1)
        self.slave_1.add_block('main_block', cst.HOLDING_REGISTERS, 0, 0x10000)
        self.generate_random_data_lock = threading.Lock()

    def heartbeat(self):
        counter = 0
        while self.flag_run is True:
            self.slave_1.set_values('main_block', 0x300, counter)
            counter = (counter + 1) % 0x100
            time.sleep(1)

    def generate_random_data(self):
        while self.flag_run is True:
            random_data = [(i, random.randint(0, 9999)) for i in range(52)]
            with open('./dump_regs.txt', 'w') as file:
                writer = csv.writer(file)
                writer.writerows(random_data)
            time.sleep(10)

    def load_values_to_modbus(self):
        file1 = open('./dump_regs.txt', 'r')
        Lines = file1.readlines()
        result = []
        for line in Lines:
            args = line.split(',')
            if len(args) >= 2:
                result.append(int(args[1]))
            else:
                print(f"Invalid line: {line}")
        self.slave_1.set_values('main_block', 0, result)


    def run(self):
        self.flag_run = True
        # create heartbeat thread
        t = threading.Thread(target = self.heartbeat)
        t.start()

        # Create random data generation thread
        random_data_thread = threading.Thread(target=self.generate_random_data)
        random_data_thread.start()
        try:
            logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
            logger.info("running...")
            logger.info("enter 'quit' for closing the server")

            while True:
                cmd = sys.stdin.readline()
                if cmd.strip() == 'quit':
                    sys.stdout.write('bye-bye\r\n')
                    break

                # Load field value to modbus slave
                with self.generate_random_data_lock:
                    self.load_values_to_modbus()
        finally:
            self.flag_run = False
            t.join()
            random_data_thread.join()
            self.server.stop()


if __name__ == "__main__":
    mbmu = MBMUSimulator()
    mbmu.run()
