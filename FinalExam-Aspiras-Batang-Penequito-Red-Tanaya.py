#FINAL EXAM
#CPE 311 - CPE32S3
#ASPIRAS, BATANG, PENEQUITO, RED, TANAYA

import matplotlib.pyplot as plt

class BankersAlgorithm:
    def __init__(self, allocation, max_need, available):
        self.allocation = allocation
        self.max_need = max_need
        self.available = available
        self.need = [[max_need[i][j] - allocation[i][j] for j in range(len(allocation[0]))] for i in range(len(allocation))]
        self.processes = list(range(len(allocation)))

    def is_safe_state(self, work, finish, sequence):
        count = 0
        while count < len(self.processes):
            found = False
            for p in self.processes:
                if not finish[p]:
                    if all(self.need[p][r] <= work[r] for r in range(len(work))):
                        for r in range(len(work)):
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                        sequence.append(p)
                        found = True
                        count += 1
                        break
            if not found:
                return False
        return True

    def run_algorithm(self):
        work = self.available.copy()
        finish = [False] * len(self.processes)
        sequence = []

        while not all(finish):
            for p in self.processes:
                if not finish[p]:
                    can_allocate = True
                    for r in range(len(work)):
                        if work[r] < self.need[p][r]:
                            can_allocate = False
                            break
                    if can_allocate:
                        for r in range(len(work)):
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                        sequence.append(p)
            if not any(can_allocate for p in self.processes if not finish[p]):
                break

        if len(sequence) == len(self.processes):
            print("Banker's Algorithm: Safe state sequence:", sequence)
        else:
            print("Banker's Algorithm: System is not in a safe state.")

    def print_table(self):
        work = self.available.copy()
        work_history = [self.available.copy()]
        finish = [False] * len(self.processes)

        print("Banker's Algorithm Table:")
        print("+---------+------------+------------+------------+------------+")
        print("| Process | Allocation |  Max Need  | Available  |   Need     |")
        print("+---------+------------+------------+------------+------------+")

        while not all(finish):
            for p in self.processes:
                if not finish[p]:
                    can_allocate = True
                    for r in range(len(work)):
                        if work[r] < self.need[p][r]:
                            can_allocate = False
                            break
                    if can_allocate:
                        for r in range(len(work)):
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                    work_history.append(work.copy())

        for i in range(len(self.processes)):
            if i == 0:
                available_str = ' '.join(map(str, self.available))
            else:
                available_str = ' '.join(map(str, work_history[i]))  # Adjusted index to show the correct available

            print("| {:^7} | {:^10} | {:^10} | {:^10} | {:^10} |".format(
                i,
                ' '.join(map(str, self.allocation[i])),
                ' '.join(map(str, self.max_need[i])),
                available_str,
                ' '.join(map(str, self.need[i]))
            ))
        print("+---------+------------+------------+------------+------------+")

        total_allocated = [sum(x) for x in zip(*self.allocation)]
        total_available = [self.available[r] + total_allocated[r] for r in range(len(self.available))]
        print(f"Total Allocated: {' '.join(map(str, total_allocated))}")
        print(f"Total Instance: {' '.join(map(str, total_available))}")

# Function to get user input for Banker's Algorithm
def get_banker_input():
    print("+---------+------------+------------+------------+------------+")
    print("                     Banker's Algorithm                        ")
    print("+---------+------------+------------+------------+------------+")
    num_processes = int(input("Enter the number of processes: "))
    num_resources = int(input("Enter the number of resource types: "))

    allocation = []
    print("Enter allocation matrix:")
    for _ in range(num_processes):
        allocation.append([int(x) for x in input().split()])

    max_need = []
    print("Enter maximum need matrix:")
    for _ in range(num_processes):
        max_need.append([int(x) for x in input().split()])

    available = [int(x) for x in input("Enter available resources vector: ").split()]

    return allocation, max_need, available

def plot_graph(cylinders, title, total_movement):
    plt.figure(figsize=(10, 5))
    plt.plot(cylinders, range(len(cylinders)), marker='o')
    plt.title(title)
    plt.gca().invert_yaxis() 
    plt.yticks([])  
    plt.xticks(cylinders)  
    plt.gca().xaxis.set_label_position('top')  
    plt.gca().xaxis.tick_top()  
    plt.grid(False)  

    
    plt.figtext(0.5, 0, f'Total Seek Time/Head Movement: {total_movement}', ha='center', fontsize=12)
    plt.show()

def disk_scheduling_algorithm():
    print("+---------+------------+------------+------------+------------+")
    print("                    Disk Scheduling Algorithm                  ")
    print("+---------+------------+------------+------------+------------+")
    algorithm = int(input("Enter the desired algorithm (1: FCFS, 2: SCAN, 3: C-SCAN): "))
    if algorithm not in [1, 2, 3]:
        print("Invalid algorithm. Exiting...")
        return
    requests = list(map(int, input("Enter the FIFO Order (No commas): ").split()))
    head = int(input("Enter the Request at Cylinder: "))
    disk_size = int(input("Enter the size of the disk: "))
    total_movement = 0  
    head_movements = [head]

    if algorithm == 1:
        # FCFS (First-Come-First-Served)
        for request in requests:
            total_movement += abs(request - head)
            head = request
            head_movements.append(head)
        plot_graph(head_movements, "FCFS Disk Scheduling Algorithm", total_movement)

    elif algorithm == 2:
        # SCAN (Elevator Algorithm)
        requests.sort()
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        # Moving towards the end
        for request in right:
            total_movement += abs(request - head)
            head = request
            head_movements.append(head)
        
        # Move to the end of the disk if necessary
        if right:
            total_movement += abs(disk_size - 1 - head)
            head = disk_size - 1
            head_movements.append(head)

        # Moving back towards the start
        for request in reversed(left):
            total_movement += abs(request - head)
            head = request
            head_movements.append(head)

        plot_graph(head_movements, "SCAN Disk Scheduling Algorithm", total_movement)

    elif algorithm == 3:
        # C-SCAN (Circular SCAN)
        requests.sort()
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        # Moving towards the end
        for request in right:
            total_movement += abs(request - head)
            head = request
            head_movements.append(head)
        
        # Move to the end of the disk
        if right:
            total_movement += abs(disk_size - 1 - head)
            head = disk_size - 1
            head_movements.append(head)

        # Jump to the beginning of the disk
        total_movement += abs(head - 0)
        head = 0
        head_movements.append(head)

        # Moving from the start again
        for request in left:
            total_movement += abs(request - head)
            head = request
            head_movements.append(head)

        plot_graph(head_movements, "C-SCAN Disk Scheduling Algorithm", total_movement)

    print("Total Seek Time/Head Movement:", total_movement)

def main():
    print("Algorithm Simulator")
    print("1. Banker's Algorithm")
    print("2. Disk Scheduling Algorithm")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        allocation, max_need, available = get_banker_input()
        banker = BankersAlgorithm(allocation, max_need, available)
        banker.print_table()
        banker.run_algorithm()
    elif choice == 2:
        disk_scheduling_algorithm()
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
