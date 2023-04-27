import numpy as np

FILENAME = "./shorouk/shorouk_data_v2.txt"

def average_readings(n_samples, data):
    # Get all the data and average them

def rad2deg(data):
    # Convert data from radian to degress

def accumulate(data):
    # Accumulate data to get integration using the following equation
    # v = v + (a0 + a1)*(t1 - t0)/2

def main():
    secs_array = np.ndarray([])
    nsecs_array = np.ndarray([])
    ln_x = np.ndarray([])
    ln_y = np.ndarray([])
    ln_z = np.ndarray([])
    an_x = np.ndarray([])
    an_y = np.ndarray([])
    an_z = np.ndarray([])
    count = 0
    n_count = 0
    with open(FILENAME, "r") as f:
        for line in f:
            if "secs:" in line:
                secs_array = np.append(secs_array, line.split(": ")[1].strip())
                # secs_array.append()

            if "nsecs:" in line:
                nsecs_array = np.append(nsecs_array, line.split(": ")[1].strip())

            

            if count == 1:
                ln_x = np.append(ln_x, line.split(": ")[1].strip())
                count+=1
            if count == 2:
                ln_y = np.append(ln_y, line.split(": ")[1].strip())
                count+=1
            if count == 3:
                ln_z = np.append(ln_z, line.split(": ")[1].strip())
                count = 0
            if "linear:" in line:
                count = 1
            

            if n_count == 1:
                an_x = np.append(an_x, line.split(": ")[1].strip())
                #print(line)
                n_count+=1
            if n_count == 2:
                an_y = np.append(an_y, line.split(": ")[1].strip())
                n_count+=1
            if n_count == 3:
                an_z = np.append(an_z, line.split(": ")[1].strip())
                n_count = 0
            if "angular:" in line:
                n_count = 1
            
    print(secs_array)
            



if __name__ == "__main__":
    main()
