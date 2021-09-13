import csv
import sys
from typing import final

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    final_evidence = []
    final_label = []
    # Open csv file
    with open(filename,'r') as csvfile:
        # Use csv reader to read file
        data = csv.reader(csvfile)
        # Skip first row 
        next(data)
        # Seperate evidence from label
        for row in data:
            evidence = row[:17]
            label = row[-1]
            # Turn the entries in evidence to desireable type
            for i in range(len(evidence)):
                # Turn categories into integers
                if i in [0,2,4,11,12,13,14]:
                    evidence[i] = int(evidence[i])
                # Turn categories into floats
                if i in [1,3,5,6,7,8,9]:
                    evidence[i] = float(evidence[i])
                # Turn months into integers
                if i == 10:
                    x = {"Jan":0,"Feb":1,"Mar":2,"Apr":3,"May":4,"June":5,"Jul":6,"Aug":7,"Sep":8,"Oct":9,"Nov":10,"Dec":11}
                    if evidence[i] in x.keys():
                        evidence[i] = x[evidence[i]]
                # Turn visitor type into 0 or 1
                if i == 15:
                    if evidence[i] == "Returning_Visitor":
                        evidence[i] = 1
                    else:
                        evidence[i] = 0
                # Turn weekend to 0 or 1
                if i == 16:
                    if evidence[i] ==  "TRUE":
                        evidence[i] = 1
                    else:
                        evidence[i] = 0
            # Turn label into 0 or 1
            if label == "TRUE":
                label = 1
            else:
                label = 0
            # Once the for loop stop all the evidence has bee properly modified to the one user
            final_evidence.append(evidence)
            final_label.append(label)
        # Return a tuple for the evidence and the corresponding label
        return((final_evidence,final_label))

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    a = labels[0]
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return(model)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tp = 0
    tn = 0
    for i in range(len(labels)):
        # Check if we did a succesfull prediction
        if labels[i] == predictions[i]:
            # Count true positives predictions
            if labels[i] == 1:
                tp += 1
            # Count true negative predictions
            if labels[i] == 0:
                tn += 1
    # Count total positive revenues and total negative revenues
    total_pos = 0
    total_neg = 0
    for i in range(len(labels)):
        if labels[i] ==  1:
            total_pos += 1
        else:
            total_neg += 1
    sensitivity = tp/total_pos
    specificity = tn/total_neg
    return(sensitivity,specificity)


if __name__ == "__main__":
    main()
