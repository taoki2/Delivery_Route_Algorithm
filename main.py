# Author: Trenton Aoki, PharmD, BCPS, MSDA
# Student ID: 010545442

import csv
import sys
from datetime import timedelta
from hash import ChainingHashTable
from package import Package
from truck import Truck

# Instantiate an empty Hash Table
packages_hash = ChainingHashTable()

# Create a list of package IDs that will be loaded on each truck
truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck2_packages = [3, 6, 18, 25, 28, 32, 36, 38, 2, 4, 5, 7, 8, 10, 11]
truck3_packages = [9, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39]

# Create a list of all the package IDs
all_packages = truck1_packages + truck2_packages + truck3_packages

# Method to import a csv file and return it as a list
# Time Complexity: O(n)
# Space Complexity: O(n)
def import_csv(file):
    return list(csv.reader(open(file)))

# Method to import a csv file of packages, create a package object for each package,
# and add the package to the hash table that was passed as an argument
# Time Complexity: O(n)
# Space Complexity: O(n)
def import_packages(file, hash_table):
    packages_list = import_csv(file)
    # Time Complexity: O(n)
    for p in packages_list:
        id = int(p[0])
        address = p[1]
        city = p[2]
        state = p[3]
        zip = p[4]
        deadline = p[5]
        kg = p[6]
        note = p[7]
        # Instantiate a Package object using the variables extracted from the csv file above
        package = Package(id, address, city, state, zip, deadline, kg, note)
        # Add the Package to the Hash Table using the package ID as the key and the package object as the value
        # Time Complexity: O(1)
        hash_table.insert(id, package)

# Method to instantiate a Truck object with the packages in the list argument,
# and the truck's load time set to the timedelta argument.
# Time Complexity: O(n)
# Space Complexity: O(n)
def load_truck(package_list, timedelta):
    # Set each package's load time to the truck's load time
    # Time Complexity: O(n)
    for p in package_list:
        package = packages_hash.search(int(p))
        package.load_time = timedelta
    return Truck(package_list, timedelta)

# Method used to calculate the distance between two addresses
# Time Complexity: O(n)
# Space Complexity: O(1)
def calculate_distance(address1, address2):
    id1 = sys.maxsize
    id2 = sys.maxsize
    # Iterate through the list of hub addresses and set the hub ID of address1 to id1 and hub ID of address2 to id2
    # Time Complexity: O(n)
    for hub in csv_hub_addresses:
        # Break out of the for loop if hub IDs of both addresses are already found
        if id1 < sys.maxsize and id2 < sys.maxsize:
            break
        elif address1 == hub[2] and address2 == hub[2]:
            id1 = id2 = int(hub[0])
        elif address1 == hub[2]:
            id1 = int(hub[0])
        elif address2 == hub[2]:
            id2 = int(hub[0])
    try:
        # Find the corresponding distance value between the two hub IDs using the hub IDs as indices
        if csv_hub_distances[id1][id2] == "":
            return float(csv_hub_distances[id2][id1])
        else:
            return float(csv_hub_distances[id1][id2])
    except IndexError:
        print("IndexError")

# Method to have the truck driver return to the hub
# Time Complexity: O(n)
# Space Complexity: O(1)
def return_to_hub(truck):
    hub = "4001 South 700 East"
    distance = calculate_distance(truck.address, hub) # Time Complexity: O(n)
    truck.miles += distance
    truck.address = hub
    truck.depart_time += timedelta(hours=(distance / truck.speed))

# Method to deliver the packages on the truck using a greedy algorithm
# Time Complexity: O(n^3)
# Space Complexity: O(1)
def deliver_packages(truck):
    load = truck.packages
    # Continue delivering while there is at least 1 package left on the truck
    # O(n^3)
    while len(load) > 0:
        next_package = ""
        min_distance = sys.maxsize
        # Find the minimum distance between the truck's current address and the address of one of the
        # remaining package's delivery address by iterating through the remaining packages and
        # set the package with the minimum distance to the next_package variable
        for package_id in load: # Time Complexity: O(n^2)
            p = packages_hash.search(package_id)
            distance = calculate_distance(truck.address, p.address) # Time Complexity: O(n)
            if distance < min_distance:
                min_distance = distance
                next_package = p
        # Add the distance to the next package's delivery address to the truck's total mileage
        truck.miles += min_distance
        # Update the truck's address to the next package's delivery address
        truck.address = next_package.address
        # Unload the package from truck
        load.remove(next_package.id)
        # Update the truck's departure time based on the distance travelled and speed
        truck.depart_time += timedelta(hours=(min_distance / truck.speed))
        # Update the package's delivery time
        next_package.delivery_time = truck.depart_time
        packages_hash.insert(next_package.id, next_package)
    # After all the packages on the truck have been delivered, have the truck driver return to the hub
    return_to_hub(truck)

# Method to update the status of a package based on the time passed as an argument
# Time Complexity: O(1)
# Space Complexity: O(1)
def status_update(package, time):
    if time < package.load_time:
        package.status = "At the hub"
    elif time >= package.delivery_time:
        package.status = "Delivered"
    else:
        package.status = "En route"

# Method to display the package information based on the time passed as an argument
# Time Complexity: O(1)
# Space Complexity: O(1)
def package_info(packageId, time_input):
    time_input = time_input.split(":")
    time = timedelta(hours=int(time_input[0]), minutes=int(time_input[1]))
    p = packages_hash.search(int(packageId))
    status_update(p, time)
    print(f'Package ID: {p.id}')
    print(f'Delivery address: {p.address}, {p.city}, {p.state}, {p.zip}')
    print(f'Weight (kg): {p.kg}')
    print(f'Deadline: {p.deadline}')
    if p.status == "Delivered":
        print(f'Status: {p.status} at {p.delivery_time}')
    else:
        print(f'Status: {p.status}')

# Main Method
# Overall Time Complexity of the program: O(n^3)
# Overall Space Complexity of the program: O(n)
if __name__ == '__main__':
    # Import Hub Names/Addresses as a list
    csv_hub_addresses = import_csv("CSV/hub_addresses.csv")

    # Import Hub Distances as a list
    csv_hub_distances = import_csv("CSV/hub_distances.csv")

    # Import Packages and store them in a Hash Table with the package ID as the key and the package object as the value
    import_packages("CSV/packages.csv", packages_hash)

    # Load packages onto trucks 1 and 2
    truck1 = load_truck(truck1_packages, timedelta(hours=8))
    truck2 = load_truck(truck2_packages, timedelta(hours=9, minutes=5))

    # Deliver packages that are on trucks 1 and 2
    deliver_packages(truck1)
    deliver_packages(truck2)

    # Update the delivery address of package #9
    package = packages_hash.search(9)
    package.address = "410 S State St"

    # Ensure that truck 3 does not leave before 10:20 to get the correct address of package 9
    # and does not leave before truck 1 or truck 2 finishes their deliveries and returns to hub
    return_time = min(truck1.depart_time, truck2.depart_time)
    truck3_depart_time = max(timedelta(hours=10, minutes=20), return_time)

    # Load packages onto truck 3
    truck3 = load_truck(truck3_packages, truck3_depart_time)

    # Deliver packages that are on truck 3
    deliver_packages(truck3)

    # Command-Line Interface
    print("Welcome to the Western Governors University Parcel Service (WGUPS)!\n")

    while True:
        print("Please enter one of the following option numbers:\n"
              "1. See the total mileage for each delivery truck\n"
              "2. See information for a specific package\n"
              "3. See the statuses of all packages for a given time\n"
              "4. Exit the program")
        user_input = input()
        if user_input == "1":
            total_miles = truck1.miles + truck2.miles + truck3.miles
            # Display total mileage and return time of each truck, including the combined mileage of all three trucks
            print("Truck #1 travelled a total of {0:.2f} miles and returned to the hub at {4}.\n"
                  "Truck #2 travelled a total of {1:.2f} miles and returned to the hub at {5}\n"
                  "Truck #3 travelled a total of {2:.2f} miles and returned to the hub at {6}\n"
                  "Total combined mileage of all trucks: {3:.2f}\n"
                  .format(truck1.miles, truck2.miles, truck3.miles, total_miles, truck1.depart_time, truck2.depart_time, truck3.depart_time))

            input("Press enter to return to the main menu.\n")
        elif user_input =="2":
            flag = True
            while flag:
                packageId = input("Please enter a package ID:")
                if packageId == "":
                    flag = False
                else:
                    try:
                        if packages_hash.search(int(packageId)):
                            time_input = input("Please enter a specific time (HH:MM) to check the status of the package:")
                            try:
                                # Displays the package information based on the user inputted time
                                # Time Complexity: O(1)
                                package_info(packageId, time_input)
                                input("Press enter to return to the main menu.\n")
                                flag = False

                            except ValueError:
                                print("Invalid entry.\n")
                    except:
                        input("Invalid entry.\n")
        elif user_input =="3":
            flag = True
            while flag:
                time_input = input("Please enter a specific time (HH:MM) to check the statuses of all packages:")
                try:
                    # Iterate through all of the packages and display the package information based on the user inputted time
                    # Time Complexity: O(n)
                    for i in range(1,len(all_packages)+1):
                        package_info(i, time_input)
                        if i % 5 == 0 and i % len(all_packages) != 0:
                            input("\nPress enter to view the next page.\n")
                        else:
                            print("\n")
                    input("Press enter to return to the main menu.\n")
                    flag = False

                except ValueError:
                    print("Invalid entry.\n")
        elif user_input == "4":
            exit()
