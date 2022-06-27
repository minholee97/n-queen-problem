from tkinter import *
from tkinter import messagebox
import random
import time

def CheckValue(char):
	return char.isdigit()
def Validate(number, li):
	if len(list(set(li))) != number:
		return False
	else:
		return True
def ViolateCount(number, li):
	count = 0
	for i in range(number - 1):
		temp1 = li[i]
		for j in range(i + 1, number):
			temp2 = li[j]
			if (temp1 == (temp2 + (j - i)) or temp1 == (temp2 - (j - i))):
				count += 1
	return count
def RandomRestartHillClimbingSearch(number, timeLimit):
	first = list(range(1, number + 1))
	second = random.sample(first, number)
	pos = ViolateCount(number,second)
	temp = second[:]
	sol = []
	start = time.time()
	if pos == 0:
		return temp, time.time() - start, pos
	while True:
		for i in range(number - 1):
			for j in range(i + 1, number):
				temp[i], temp[j] = temp[j], temp[i]
				tempPos = ViolateCount(number,temp)
				if tempPos == 0:
					return temp, time.time() - start, pos
				elif pos > tempPos:
					pos = tempPos
					sol.clear()
					i, j = 0, 0
					break
				elif pos == tempPos:
					sol.append(temp[:])
				temp[i], temp[j] = temp[j], temp[i]
		if len(sol) != 0:
			temp = sol[random.randrange(len(sol))]
			sol.clear()
			pos = ViolateCount(number,temp)
		else:
			temp = random.sample(first, number)
			pos = ViolateCount(number,temp)
		if time.time() - start > timeLimit:
			return "실패 : 시간초과", time.time() - start, pos
	return result, time.time() - start, pos

class Chromosome():
	def __init__(self):
		self.gene = []
		self.pos = 0
	def mutation(self, number):
		excPoint1 = random.randrange(number)
		excPoint2 = random.randrange(number)
		self.gene[excPoint1],self.gene[excPoint2] = self.gene[excPoint2],self.gene[excPoint1]

def GeneticAlgorithm(number, timeLimit):
	first = list(range(1, number + 1))
	chromosomeList = []
	start = time.time()
	for i in range(100):
		ch = Chromosome()
		ch.gene = random.sample(first, number)
		ch.pos = ViolateCount(number, ch.gene)
		if ch.pos == 0:
			return ch.gene, time.time() - start, ch.pos
		chromosomeList.append(ch)
	chromosomeList.sort(key=lambda object: object.pos)
	while True:
		for i in range(10):
			for j in range(0, 10, 2):
				divPoint = random.randrange(number)
				ch1 = Chromosome()
				target = chromosomeList[i + 1].gene.index(chromosomeList[i].gene[divPoint])
				ch1.gene = chromosomeList[i].gene[:]
				ch1.gene[divPoint], ch1.gene[target] = ch1.gene[target], ch1.gene[divPoint] 
				mutChance = random.randrange(100)
				if mutChance >= 60:
					ch1.mutation(number)
				ch1.pos = ViolateCount(number, ch1.gene)
				if ch1.pos == 0:
					return ch1.gene, time.time() - start, ch1.pos

				ch2 = Chromosome()
				target = chromosomeList[i].gene.index(chromosomeList[i + 1].gene[divPoint])
				ch2.gene = chromosomeList[i + 1].gene[:]
				ch2.gene[divPoint], ch2.gene[target] = ch2.gene[target], ch2.gene[divPoint] 
				mutChance = random.randrange(100)
				if mutChance >= 60:
					ch2.mutation(number)
				ch2.pos = ViolateCount(number, ch2.gene)
				if ch2.pos == 0:
					return ch2.gene, time.time() - start, ch2.pos
				chromosomeList[i * 10 + j] = ch1
				chromosomeList[i * 10 + j + 1] = ch2
		chromosomeList.sort(key=lambda object: object.pos)
		if time.time() - start > timeLimit:
			return "실패 : 시간초과", time.time() - start, chromosomeList[0].pos
	return "실패 : 시간초과", time.time() - start, chromosomeList[0].pos
def Execute():
	def Reset():
		for widget in frm.winfo_children():
			widget.destroy()
		noBoard1 = Label(frm, font=("Tahoma", 40), bg="gray35", text="No Board", fg="orange")
		noBoard1.place(x=185, y=220)
		noBoard2 = Label(frm, font=("Tahoma", 14), bg="gray35", text="(퀸의 개수가 80개 이상이면 보드가 제공되지 않습니다.)", fg="orange")
		noBoard2.place(x=60, y=300)
		noBoard3 = Label(frm, font=("Tahoma", 14), bg="gray35", text="(퀸의 개수가 30개 이상부터는 체스판의 출력 시간이 많이 소요됩니다)", fg="orange")
		noBoard3.place(x=0, y=330)
		frm.configure(width=600, height=600)
	def Selected(value):
		algorithm.configure(text=value)
		resultArea.configure(text="")
		timeArea.configure(text="")
		Reset()
	def OkClick():
		resultArea.configure(text="")
		timeArea.configure(text="")
		if input1.get() == "":
			messagebox.showinfo("Help", "퀸의 개수를 입력해 주세요.")
			return
		number = int(input1.get())
		if number < 4:
			messagebox.showinfo("Help", "퀸의 개수는 4 이상만 가능합니다.")
			return
		if input3.get() == "":
			messagebox.showinfo("Help", "수행 시간을 입력해 주세요")
			return
		timeLimit = int(input3.get())

		if algorithm.cget("text") == "Random-Restart-Hill-Climbing Search":
			result, elapsedTime, pos = RandomRestartHillClimbingSearch(number, timeLimit)
			if result == "실패 : 시간초과":
				Reset()
				timeArea.configure(text=result)
				resultArea.configure(text="Min violateCount : " + str(pos))
				return
			timeArea.configure(text="수행시간 : " + str(elapsedTime))
		elif algorithm.cget("text") == "Genetic-Algorithm Search":
			result, elapsedTime, pos = GeneticAlgorithm(number, timeLimit)
			if result == "실패 : 시간초과":
				Reset()
				timeArea.configure(text=result)
				resultArea.configure(text="Min violateCount : " + str(pos))
				return
			timeArea.configure(text="수행시간 : " + str(elapsedTime))
		else:
			return 
		for widget in frm.winfo_children():
			widget.destroy()
		resultArea.configure(text=result)
		if number >= 80:
			Reset()
			return
		if number > 40:
			for row in range(number):
				for col in range(number):
					label = Label(frm, text="", borderwidth=0, width=4,height=2, font=("Tahoma", 2))
					if (row + col) % 2 == 1:
						label.configure(background="gray")
					if result[row] - 1 == col:
						label.configure(text="Q", fg="orange", bg="black")
					label.grid(row=row,column=col,padx=0,pady=0)
			return
		for row in range(number):
			for col in range(number):
				label = Label(frm, text="", borderwidth=0, width=80//number,height=40//number)
				if (row + col) % 2 == 1:
					label.configure(background="gray")
				if result[row] - 1 == col:
					label.configure(text="Q", fg="orange", bg="black")
				label.grid(row=row,column=col,padx=0,pady=0)

	window = Tk()
	window.title("N-Queens Problem")
	window.geometry("1080x960+0+0")
	window.resizable(False,False)
	window.configure(background="gray15")

	title = Label(window, text="N-Queens Problem", font=("Tahoma", 24), pady=30, bg="gray15", fg="orange")
	title.pack()

	frm = Frame(window)
	frm.configure(bg="gray35", width=600, height=600)
	frm.place(x=50, y=100)

	noBoard1 = Label(frm, font=("Tahoma", 40), bg="gray35", text="No Board", fg="orange")
	noBoard1.place(x=185, y=220)
	noBoard2 = Label(frm, font=("Tahoma", 14), bg="gray35", text="(퀸의 개수가 80개 이상이면 보드가 제공되지 않습니다)", fg="orange")
	noBoard2.place(x=60, y=300)
	noBoard3 = Label(frm, font=("Tahoma", 14), bg="gray35", text="(퀸의 개수가 30개 이상부터는 체스판을 출력 시간이 많이 소요됩니다)", fg="orange")
	noBoard3.place(x=0, y=330)

	btn1 = Button(window, width=16, height=2, text="SOLVE", command=OkClick, bg="orange", fg="white", font=("Tahoma", 16))
	btn1.place(x=760, y=625)

	label0 = Label(window, font=("Tahoma", 24), text="SETTING", bg="gray15", fg="orange")
	label0.place(x=760, y=230)

	label1 = Label(window, font=("Tahoma", 14), text="* 퀸의 개수", bg="gray15", fg="orange")
	label1.place(x=760, y=290)
	validation = window.register(CheckValue)
	input1 = Entry(window, font=("Tahoma", 14), validate="key", validatecommand=(validation, '%S'), bg="gray35", fg="orange")
	input1.place(x=760, y=330)

	label2 = Label(window, font=("Tahoma", 14), text="- 탐색 알고리즘", bg="gray15", fg="orange")
	label2.place(x=760, y=390)
	variable = StringVar(window)
	variable.set("Random-Restart-Hill-Climbing Search")
	input2 = OptionMenu(window, variable, "Random-Restart-Hill-Climbing Search", "Genetic-Algorithm Search", command=Selected)
	input2.configure(width = 30, bg="gray35", fg="orange")
	input2.place(x=760, y=430)

	label3 = Label(window, font=("Tahoma", 14), text="- 수행 시간", bg="gray15", fg="orange")
	label3.place(x=760, y=490)
	input3 = Entry(window, font=("Tahoma", 14), validate="key", validatecommand=(validation, '%S'), bg="gray35", fg="orange")
	input3.place(x=760, y=530)

	label4 = Label(window, font=("Tahoma", 24), text="Result", bg="gray15", fg="orange")
	label4.place(x=50, y=750)

	algorithm = Label(window, width=50, text="Random-Restart-Hill-Climbing Search", font=("Tahoma", 16),bg="gray35", fg="orange")
	algorithm.place(x=50, y=800)

	timeArea = Label(window, width=50, font=("Tahoma", 16),bg="gray35", fg="orange")
	timeArea.place(x=50, y=840)

	resultArea = Label(window, width=100, font=("Tahoma", 8),bg="gray35", fg="orange")
	resultArea.place(x=50, y=880)


	window.mainloop()

if __name__ == '__main__':
	Execute()