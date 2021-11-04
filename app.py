import json

f = open('improvements.json',)
all_requirements = json.load(f)
f.close()

f = open('customers.json',)
customers = json.load(f)
f.close()

def get_requirement(name):
    return all_requirements[name]

def cost(requirement):
    total_cost = 0

    for req in requirement["parents"]:
        total_cost = total_cost + cost(get_requirement(req))
    
    total_cost = total_cost + requirement["cost"]

    return total_cost

def is_required(req_key, arr_req):
    requirement = get_requirement(req_key)
    required = False

    if req_key in arr_req:
        required = True

    if not required:
    
        for req in requirement["parents"]:
            if not required:
                required = is_required(req, arr_req)
    
    return required


def get_bound(req):
    bound = 0

    for customer in customers:
        if (is_required(req, customer["requirements"])):
            bound = bound + customer["importance"]

    return bound


def analyze_customers(req):

    requirements_text = "| # Customer: {name} # Importance: {importance} # Match Requirements: {match}"

    for customer in customers:
        match = False

        if req in customer["requirements"]:
            match = True

        print(requirements_text.format(name = customer["name"], 
            importance = customer["importance"],
            match = match))
    

def analyze_requirements():
    requirements_text = "|   COD: {cod} NAME: {name} COST: {cost} IMPORTANCE: {bound}  "
    print("____________________________________________________________")

    for req in all_requirements.keys():
        requirement = get_requirement(req)
        print(requirements_text.format(cod = req, 
            name = requirement["name"], 
            cost=cost(requirement),
            bound=get_bound(req)))
        analyze_customers(req)
        print("____________________________________________________________")

analyze_requirements()
