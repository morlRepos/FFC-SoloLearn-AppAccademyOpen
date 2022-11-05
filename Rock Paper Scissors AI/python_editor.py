class Category:
    def __init__(self,categoryName,budgetAmount):
        self._category = categoryName
        self._budget = budgetAmount
        self._ledger = []
        self._startingBalance = budgetAmount

    def __str__(self):
        tallyUp = ""
        tallyUp += f"{self._category}:\n"
        tallyUp += f"initial deposit {self._startingBalance}\n"
        for item in self._ledger:
            #print(item)
            tallyUp += f"{item['description']} , {item['amount']}\n"
        tallyUp += f"Total {self._budget}\n"
        return tallyUp
    
    def deposit(self, amount, description=""):
        #append to ledger {"amount": amount, "description": description}
        self._budget += amount;
        self._ledger.append({"amount": amount, "description": description});
        pass
    
    def withdraw(self, amount, description=""):
        #see deposit expect negative value.
        #return True or False if the funds allow you to withdraw
        if(self.check_funds(amount)):
            self._budget -= amount;
            self._ledger.append({"amount": -amount, "description": description});
        pass

    def transfer(self, otherCategory, amount):
        if(self.check_funds(amount)):
            self._budget -= amount;
            description = f"Transfer to {otherCategory._category}"
            self._ledger.append({"amount": amount, "description": description});

            otherCategory._budget += amount;
            description = f"Transfer from {self._category}"
            otherCategory._ledger.append(
                {"amount": amount, "description": description}
            );
        pass
    
    def get_balance(self):
        return self._budget
    
    def check_funds(self,amount):
        return self._budget >= amount

#*************Food*************
#initial deposit        1000.00
#groceries               -10.15
#restaurant and more foo -15.89
#Transfer to Clothing    -50.00
#Total: 923.96


food = Category("Food",1000.00)
entertainment = Category("Entertainment",60)

food.withdraw(10.15,"groceries")
food.withdraw(15.89,"restaurant and more food")
food.transfer(entertainment,50)

print(food)
print(entertainment)
