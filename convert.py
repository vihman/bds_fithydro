import csv
import logging
import os
import struct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)


def read_chunks(f, length):
    count = 0
    while True:
        count += 1
        f.read(2)  # \n\r
        data = f.read(length)
        if not len(data) == length:
            logger.warning("Not enough data on record: %d" % count)
            break
        yield data


def read_data(filename):
    fmt = '<HIffffffffffffffffffffffBBBB'
    with open(filename, 'rb') as raw:
        results = [struct.unpack(fmt, chunk) for chunk in read_chunks(raw, struct.calcsize(fmt))]
        return results


#header: Time [ms],PL [hPa],TL [C],PC [hPa],TC [C],PR [hPa],TR [C],EX [deg],EY [deg],EZ [deg],QX [-],QY [-],QZ [-],QW [-],MX [microT],MY [microT],MZ [microT],AX [m/s2],AY [m/s2],AZ [m/s2],RX [rad/s],RY [rad/s],RZ [rad/s],CSM,CSA,CSR,CSTOT
def write_data(filename, data):
    fieldnames = ['Fq', 'Time [ms]', 'PL [hPa]', 'TL [C]', 'PC [hPa]', 'TC [C]', 'PR [hPa]', 'TR [C]',
                  'EX [deg]', 'EY [deg]', 'EZ [deg]', 'QW [-]', 'QX [-]', 'QY [-]', 'QZ [-]', 'MX [microT]',
                  'MY [microT]', 'MZ [microT]', 'AX [m/s2]', 'AY [m/s2]', 'AZ [m/s2]', 'RX [rad/s]', 'RY [rad/s]',
                  'RZ [rad/s]', 'CSM', 'CSA', 'CSR', 'CSTOT']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(data)


with os.scandir('.') as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            if entry.is_file and entry.name.endswith('.txt'):
                data = read_data(entry.name)
                write_data("%s.csv" % entry.name[:-4], data)
                logger.info("%s converted." % entry.name)
