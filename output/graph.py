import matplotlib.pyplot as plt

'''
categories = ['Corrected', 'Not Corrected', 'Total']
values = [corrected_count, not_corrected_count, total_words]

plt.bar(categories, values, color=['green', 'red', 'blue'])
plt.title('Spell Checker Results')
plt.ylabel('Word Count')
plt.show()
'''
'''
#plot of accuracy
corrected_count = 69
not_corrected_count = 15
total_words = 84
labels = ['Corrected', 'Not Corrected']
sizes = [corrected_count, not_corrected_count]
colors = ['blue', 'yellow   ']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Corrections')
plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
plt.show()
'''


#plot of precision
truepositive = 83
falsepositive = 1
precision = truepositive/(truepositive + falsepositive)
labels = ['True Positives', 'False Positives']
sizes = [truepositive, falsepositive]
colors = ['blue', 'red']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title(f'Precision of Spell Checker\nPrecision: {precision:.2f}')
plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
plt.show()

