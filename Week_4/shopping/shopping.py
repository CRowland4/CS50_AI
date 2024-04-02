import sys

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


def load_data(filename: str) -> tuple[list, list]:
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
        - Month, an index from 0 (Jan) to 11 (Dec)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename, "r") as f:
        content = f.readlines()

    headers = content[0].split(",")
    data = content[1:]
    evidence = [line.split(",")[:-1] for line in data]

    for i, row in enumerate(evidence):
        new_row = []
        for title, data_point in zip(headers, row):
            if title in ("Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region",
                         "TrafficType"):
                new_row.append(int(data_point.strip()))
            elif title in ("Administrative_Duration", "Informational_Duration", "ProductRelated_Duration",
                           "BounceRates", "ExitRates", "PageValues", "SpecialDay"):
                new_row.append(float(data_point.strip()))
            elif title == "Month":
                new_row.append(month_to_int(data_point.strip()))
            elif title in ("VisitorType", "Weekend"):
                new_row.append(1 if data_point.strip() in ("Returning_Visitor", "TRUE") else 0)
            else:
                raise Exception(f"Unknown field: {title}, {data_point.strip()}")

        evidence[i] = new_row

    labels = [1 if line.split(",")[-1].strip() == "TRUE" else 0 for line in data]
    return evidence, labels


def month_to_int(month_name: str) -> int:
    match month_name:
        case "Jan":
            return 0
        case "Feb":
            return 1
        case "Mar":
            return 2
        case "April":
            return 3
        case "May":
            return 4
        case "June":
            return 5
        case "Jul":
            return 6
        case "Aug":
            return 7
        case "Sep":
            return 8
        case "Oct":
            return 9
        case "Nov":
            return 10
        case "Dec":
            return 11


def train_model(evidence: list[list], labels: list[str]) -> KNeighborsClassifier:
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels: list[str], predictions: list[int]):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    true_negative = 0
    for label, prediction in zip(labels, predictions):
        if label == prediction == 1:
            true_positive += 1
        elif label == prediction == 0:
            true_negative += 1

    sensitivity = true_positive / len([label for label in labels if label == 1])
    specificity = true_negative / len([label for label in labels if label == 0])

    return sensitivity, specificity


if __name__ == "__main__":
    main()
