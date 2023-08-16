# Define the dictionary of people and their spending amounts
spending_dict = {
    'Shash': 511 + 109.75,
    'Pawan': 34.83 + 35.82,
    'Rebecca': 66 + 70,
    'Saristh': 0,
    'Uni': 0,
    'Ashish Bhai': 72.55,
    'Aachal': 0,
}

# Calculate the total amount spent
total_spent = sum(spending_dict.values())

# Calculate the average spending amount
per_person = total_spent / len(spending_dict)

# Sort the people by their spending amounts
sorted_people = sorted(spending_dict.items(), key=lambda x: x[1], reverse=True)

# Initialize the list of transfers
transfers = []

# Initialize the indices of the people at the beginning and end of the list
i = 0
j = len(sorted_people) - 1

# While there are still people to pair up
while i < j:
    # Get the names and spending amounts of the people at the beginning and end of the list
    p1, s1 = sorted_people[i]
    p2, s2 = sorted_people[j]

    # Calculate the amount to transfer
    transfer_amount = min(s1 - per_person, per_person - s2)

    # Update the spending amounts and add the transfer to the list
    spending_dict[p1] -= transfer_amount
    spending_dict[p2] += transfer_amount
    transfers.append((p1, p2, transfer_amount))

    # If p1's spending amount is now within the average, move to the next person
    if spending_dict[p1] == per_person:
        i += 1

    # If p2's spending amount is now within the average, move to the next person
    if spending_dict[p2] == per_person:
        j -= 1

# Print out the transfers of money between people
for transfer in transfers:
    print(f"{transfer[0]} should pay ${transfer[2]:.2f} to {transfer[1]}.")
