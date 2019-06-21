from PyQt5 import QtWidgets, uic
import sys

# Last update: created functions to get adjustments based on term and loan amount. created function that adds the ajustments. Made getRate function that gets the base rates for each tier.
# created function to set which row the LTV is based on fico
# finish print function
# Next time 


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('Updatedui.ui', self)
        self.show()
        self.setComishRate()
        self.go_button.clicked.connect(self.printAll)
        self.reset_button.clicked.connect(self.resetText)

    def printAll(self): #On go button click set all values in UI to their own variable
        self.setVars()
        self.setLoanAmount()
        self.setLtv()
        self.adj = self.getAdj(self.getTermAdj(self.term), self.getAmountAdj(self.loan_amount), self.getOtherAdj(self.entity, self.cashout, self.fn, self.condo1))
        self.rate = self.getRate(self.fico, self.adj)
        self.ltv = self.getLtv(self.fico)
        self.print(self.ltv, self.rate)

    def resetText(self): #On reset text clear all text in UI
        self.output_box.setText("")
        self.ltv_input.setText("$")
        self.amount_input.setText("$")
        
    def setLtv(self): #Remove $ and , from property value input
        percent = self.ltv_input.text()
        fixed = ''.join(percent.split('$'))
        percent = ''.join(fixed.split(','))
        self.ltv = float(percent)
        p = self.loan_amount / self.ltv
        p = format(p, '7.2f')
        self.ltv = float(p)

    def getLtv(self, fico):
        if fico == 2:
            if self.ltv <= .65:
                return 0
            if self.ltv > .65 and self.ltv <=.7:
                return 1
            if self.ltv > .7 and self.ltv <= .75:
                return 2
            if self.ltv > .75:
                return 3
        else:
            if self.ltv <= .6:
                return 0
            if self.ltv > .6 and self.ltv <=.65:
                return 1
            if self.ltv > .65 and self.ltv <= .7:
                return 2
            if self.ltv > .7:
                return 3

    def getPercent(self): #returns LTV percent
        return self.ltv

    def setLoanAmount(self): #Remove $ and , from loan amount value input
        amount = self.amount_input.text()
        fixed = ''.join(amount.split('$'))
        amount = ''.join(fixed.split(','))
        self.loan_amount = float(amount)

    def getLoanAmount(self): #returns loan amount
        return self.loan_amount

    def setVars(self):
        self.term = self.term_input.currentIndex()
        self.fico = self.fico_input.currentIndex()
        self.loan_amount = self.amount_input.text()
        self.entity = self.entity_input.currentIndex()
        self.ltv = self.ltv_input.text()
        self.cashout = self.cash_out.currentIndex()
        self.fn = self.fnational.currentIndex()
        self.condo1 = self.condo.currentIndex()

    def getComishRate(self, x, y): #returns commission percentage
        return format(self.ComSched[x][y]*.01, '7.4f')

    def print(self, ltv, rate):
        points = 2
        column = 2
        for x in range(3):
            self.output_box.append(str(x+1) + ". Rate: " + str(rate[ltv]) + "% Points: " + str(points))
            self.output_box.append("-The clients monthly payment is $" + str('{:,.2f}'.format(float((self.loan_amount * ((rate[ltv] * .01)))/12))))
            self.output_box.append("-Your commission on this loan is $" + str('{:,.2f}'.format(float(self.loan_amount * float(self.getComishRate(self.getRow(rate[ltv]), column))))))
            rate[ltv] += .25
            points -= .25
            column -= 1

    def getRate(self, fico, adj): #returns base rates for fico grouping
        rate = []
        num = [8.49, 8.24, 7.99]
        num[fico] += adj
        for x in range(4):
            if x == 3:
                num[fico] += .25
                rate.append(num[fico])
            else:
                rate.append(num[fico])
                num[fico] += .25
        return rate

    def getRow(self, rate):
        if rate > 9:
            return 0
        if rate <= 9 and rate > 8.75:
            return 1
        if rate <= 8.75 and rate > 8.5:
            return 2
        if rate <= 8.5 and rate > 8.25:
            return 3
        if rate <= 8.25 and rate > 8:
            return 4
        if rate <= 8 and rate > 7.75:
            return 5
        if rate <= 7.75 and rate > 7.625:
            return 6
        if rate <= 7.625:
            return 7

    def getTermAdj(self, term): #returns adjustments based on term length
        if term == 0:
            return -.25
        if term == 1:
            return 0
        if term == 2:
            return .25
        if term == 3:
            return .75

    def getAmountAdj(self, amount): #returns adjustments based on loan amount
        if amount < 200000:
            return .25
        if amount >= 200000 and amount < 1500000:
            return 0
        if amount >= 1500000 and amount <= 1999999:
            return .25
        if amount >= 2000000 and amount <= 2999999:
            return .5
        if amount >= 3000000 and amount <= 3999999:
            return .75
        if amount >= 4000000:
            return 1

    def getOtherAdj(self, entity, cash, foreign, condo): #adds all other adjustments
        rate = 0
        if entity == 1:
            rate += .5
        if cash == 1:
            rate += .25
        if foreign == 1:
            rate += .25
        if condo == 1:
            rate += .25
        return rate

    def getAdj(self, term, amount, other): #returns total adjustmesnts to be added to base rate
        return term + amount + other



    def setComishRate(self): #sales rep commission matrix
        self.w = .785
        self.rate = .085
        self.ComSched = [[0 for x in range (7)] for y in range (9)]
        for g in range(9): 
            for j in range(7):
                if j <= 3:
                    self.w = self.w - self.rate
                    self.ComSched[g][j] = self.w
                    #print(format(self.w, '7.3f'), end="\t")
                    self.rate = self.rate - .005
                if j == 4:
                    self.rate = .095
                    self.w = self.w - self.rate
                    self.ComSched[g][j] = self.w
                    #print(format(self.w, '7.3f'), end="\t")
                if j == 5:
                    self.rate = .055
                    self.w = self.w - self.rate
                    self.ComSched[g][j] = self.w
                    #print(format(self.w, '7.3f'), end="\t")
                if j == 6:
                    self.rate = .04
                    self.w = self.w - self.rate
                    self.ComSched[g][j] = self.w
                    #print(format(self.w, '7.3f'), end="\t" + "\n")


            if g == 0:
                self.w = .76
                self.rate = .085
            if g == 1:
                self.w = .735
                self.rate = .085
            if g == 2:
                self.w = .72
                self.rate = .085
            if g == 3:
                self.w = .71
                self.rate = .085
            if g == 4:
                self.w = .66
                self.rate = .085
            if g == 5:
                self.w = .51
                self.rate = .085
            if g == 6:
                self.w = .44
                self.rate = .085
            if g == 7:
                self.w = .31
                self.rate = .085
       

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    program = Window()
    sys.exit(app.exec_())

