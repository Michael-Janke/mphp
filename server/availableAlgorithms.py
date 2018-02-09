from collections import OrderedDict

algorithms = {
    'tree': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10
            }
        },
        "name": "Decision Tree"
    },
    'norm': {
        "parameters": OrderedDict(
            k={
                "name": "#Features",
                "default": 10
            },
            n={
                "name": "#Excluded features",
                "default": 5000
            },
            norm={
                "name": "Normalization method",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]
            }
        ),
        "name": "Normalized Feature Selection"
    },
    "basic": {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10
            }
        },
        "name": "Feature Selection"
    },
    "sfs": {
        "name": "Sequential Forward Selection (normalized)",
        "parameters": OrderedDict(
            k={
                "name": "#Features",
                "default": 10
            },
            n={
                "name": "#Excluded features",
                "default": 5000
            },
            m={
                "name": "#Preselected features",
                "default": 100
            },
            norm={
                "name": "Preselection normalization",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]
            },
            fitness={
                "name": "Fitness function",
                "default": "combined",
                "available": ["combined", "classification", "clustering", "sick_vs_healthy", "distance"]
            }
        )
    },
    "ea": {
        "name": "Evolutionary Algorithm",
        "parameters": OrderedDict(
            k={
                "name": "#Features",
                "default": 10
            },
            n={
                "name": "#Excluded features",
                "default": 5000
            },
            m={
                "name": "#Preselected features",
                "default": 100
            },
            norm={
                "name": "Preselection normalization",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]
            },
            fitness={
                "name": "Fitness function",
                "default": "combined",
                "available": ["combined", "classification", "clustering", "sick_vs_healthy", "distance"]
            }
        )
    }
}


def is_normalized(method):
    normalized_methods = [
        key for key in algorithms.keys()
        if "norm" in algorithms[key]["parameters"].keys()
    ]
    return method in normalized_methods
