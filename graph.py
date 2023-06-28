import matplotlib.pyplot as plt
from datetime import datetime

# Data for the plot
# days = [1, 2, 3, 4, 5]  # list of days
dates = ['06/22/2023 06:42', '06/22/2023 08:42', '06/22/2023 011:42', '06/23/2023 04:42', '06/224/2023 06:42']  # list of dates
poor_rating = [2, 3, 1, 4, 2]  # list of values for "poor" rating
neutral_rating = [4, 3, 3, 2, 4]  # list of values for "neutral" rating
good_rating = [1, 2, 3, 3, 4]  # list of values for "good" rating

# Creating the plot
plt.plot(dates, poor_rating, label='Poor')
plt.plot(dates, neutral_rating, label='Neutral')
plt.plot(dates, good_rating, label='Good')

# Setting up axes and title
plt.xlabel('Days')
plt.ylabel('Rating')
plt.title('Rating Chart by Days')

# Adding legend
plt.legend()

# Displaying the plot
plt.savefig('rating_chart.png')
# plt.show()
