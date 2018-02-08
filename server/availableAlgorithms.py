algorithms = {
    'getPCA': {
        "parameters": {
            "n_components": {
                "name": "#Components",
                "default": 3
            },
            "n_features_per_component": {
                "name": "#Features per component",
                "default": 10
            }
        },
        "name": "PCA"
    },
    'getDecisionTreeFeatures': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10
            }
        },
        "name": "Decision Tree"
    },
    'getNormalizedFeatures': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            },
            "n": {
                "name": "#Excluded features",
                "default": 5000

            },
            "norm": {
                "name": "Normalization method",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]

            }
        },
        "name": "Normalized Feature Selection"
    },
    "getFeatures": {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            }
        },
        "name": "Feature Selection"
    },
    "getFeaturesBySFS": {
        "name": "Sequential Forward Selection (normalized)",
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            },
            "n": {
                "name": "#Excluded features",
                "default": 5000

            },
            "m": {
                "name": "#Preselected features",
                "default": 100

            },
            "norm": {
                "name": "Preselection normalization",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]

            },
            "fitness": {
                "name": "Fitness function",
                "default": "combined",
                "available": ["combined", "classification", "clustering", "sick_vs_healthy", "distance"]

            }
        }
    },
    "ea": {
        "name": "Evolutionary Algorithm",
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            },
            "n": {
                "name": "#Excluded features",
                "default": 5000

            },
            "m": {
                "name": "#Preselected features",
                "default": 100

            },
            "norm": {
                "name": "Preselection normalization",
                "default": "exclude",
                "available": ["subtract", "exclude", "relief"]

            },
            "fitness": {
                "name": "Fitness function",
                "default": "combined",
                "available": ["combined", "classification", "clustering", "sick_vs_healthy", "distance"]

            }
        }
    }
}
