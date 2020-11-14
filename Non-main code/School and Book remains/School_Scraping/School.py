class School:

	startDate = 1983
	endDate = 2020

	def __init__(self, nombre, estado):
		self.name = nombre
		self.state = estado

		self.scores = []

		for i in range(School.endDate - School.startDate +1):
			self.scores.append(0)

		self.numStateChampionships = 0
		self.numNationalChampionships = 0

	def getName(self):
		return self.name

	def getState(self):
		return self.state

	def getNumStateChamp(self):
		return self.numStateChampionships

	def getNumNatChamp(self):
		return self.numNationalChampionships

	def getAllScores(self):
		return self.scores

	#helper method to getYearScore and setYearScore
	def yearToIndex(year):
		return year-School.startDate

	def getYearScore(self, year):
		return self.scores[ School.yearToIndex(year) ]


	def addNumStateChamp(self):
		self.numStateChampionships += 1

	def addNumNatChamp(self):
		self.numNationalChampionships += 1

	def setYearScore(self, year, score):
		self.scores[ School.yearToIndex(year) ] = score

	def setAllScores(self, repollo):
		self.scores = repollo

	def setNumStateChamp(self, num):
		self.numStateChampionships = num

	def setNumNatChamp(self, num):
		self.numNationalChampionships = num

	def __str__(self):
		message = ""
		message += f"{self.name}, {self.state}\n"
		message += f"Number of State Championships: {self.numStateChampionships}\n"
		message += f"Number of National Championships: {self.numNationalChampionships}\n"

		count = 0
		for score in self.scores:
			message += f"{count + School.startDate}: {score}\n"
			count += 1

		return message

